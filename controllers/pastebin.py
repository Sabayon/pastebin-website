# -*- coding: utf-8 -*-
import logging, os, sys
from www.lib.base import *
from www.lib.website import *
import www.model.config as config

from pylons.i18n import _

class PastebinController(BaseController,WebsiteController):

    def __init__(self):
        BaseController.__init__(self)
        WebsiteController.__init__(self)

    def syntax_highlight(self, text, syntax_desc, portal):
        mylexer_id = portal.PASTEBIN_SYNTAXES_MAP.get(syntax_desc)
        if mylexer_id == None:
            return False,text,''
        from pygments import highlight
        from pygments.lexers import get_lexer_by_name
        from pygments.formatters import HtmlFormatter
        try:
            lexer = get_lexer_by_name(mylexer_id, stripall=False)
            formatter = HtmlFormatter(linenos=True)#, cssclass="source")
            return True, highlight(text, lexer, formatter),formatter.get_style_defs('.highlight')
        except:
            return False, text,''

    def index(self):
        config.setup_internal(model, c, session, request)
        # create recaptcha html
        if not session.get('skip_captcha'):
            self._new_captcha()
        self._load_metadata()
        return render_mako('/pastebin/index.html')

    def latest(self):
        config.setup_internal(model, c, session, request)
        portal = self.Portal()
        self._load_metadata(portal = portal)
        c.latest_pasties_extended = portal.get_latest_pastebins(count = 50)
        portal.disconnect(); del portal
        return render_mako('/pastebin/index.html')

    def doc(self):
        config.setup_internal(model, c, session, request)
        portal = self.Portal()
        self._load_metadata(portal = portal)
        portal.disconnect(); del portal
        c.show_doc_page = True
        return render_mako('/pastebin/index.html')

    def _delete_pastebin(self, item, portal):
        pastebin_id = int(item['pastebin_id'])
        pastebin_doctypes_id = item['pastebin_doctypes_id']
        portal.delete_pastebin(pastebin_id)
        txt_log = '[%s] %s' % (
            pastebin_id, _("Removed from db"),)
        if pastebin_doctypes_id != portal.PASTEBIN_DOCTYPES['text']:
            filepath = os.path.join(config.PASTEBIN_DIR,unicode(pastebin_id),
                os.path.basename(item['content']))
            if os.path.isfile(filepath):
                os.remove(filepath)
            txt_log += ' | %s: %s' % (
                _("remove file"), os.path.basename(filepath),)
        return txt_log

    def remove_expired_pastebins(self):
        data_removed = []
        portal = self.Portal()
        expired_pastebins = portal.get_expired_pastebins()
        for item in expired_pastebins:
            txt_log = self._delete_pastebin(item, portal)
            data_removed.append(txt_log)
        # delete recent pastebin table
        portal.delete_pastebin_recent()
        portal.disconnect(); del portal
        if data_removed:
            return '%s' % ('<br/>'.join(data_removed))
        return _('Nothing removed')

    def send(self):

        if request.method != "POST":
            return "%s: %s" % (_("Error"), _("invalid method"),)

        portal = self.Portal()
        user_ip = self._get_remote_ip()
        if not user_ip:
            portal.disconnect(); del portal
            return "%s: %s" % (_("Error"), _("cannot get IP"))
        content = request.params.get('pastie_content')
        docfile = request.params.get('docfile')

        pastebin_syntax_id = request.params.get('pastebin_syntax_id')
        pastebin_doctypes_id = request.params.get('pastebin_doctypes_id')
        expiration_days = request.params.get('expiration_days')
        just_url = request.params.get('just_url')
        my_redirect = self._get_redirect()

        valid = True
        text_as_file = False

        try:
            pastebin_doctypes_id = int(pastebin_doctypes_id)
            if pastebin_doctypes_id == -1:
                pastebin_doctypes_id = portal.PASTEBIN_DOCTYPES['text']
            elif pastebin_doctypes_id == -2:
                pastebin_doctypes_id = portal.PASTEBIN_DOCTYPES['text']
                text_as_file = True
        except (ValueError,TypeError,):
            c.error_message = _('Invalid pastebin_doctypes_id')
            valid = False

        if valid:
            try:
                pastebin_syntax_id = int(pastebin_syntax_id)
                if pastebin_syntax_id == -1:
                    # plain text
                    pastebin_syntax_id = 0
            except (ValueError, TypeError,):
                pastebin_syntax_id = 0

        if valid:
            try:
                expiration_days = int(expiration_days)
                if expiration_days not in range(1,366):
                    expiration_days = 30
            except (ValueError,TypeError,):
                expiration_days = 30

        # captcha check and redirect
        if valid and (not just_url):
            if not session.get('skip_captcha'):
                valid = self._validate_captcha_submit()
                if not valid:
                    # invalid captcha answer
                    c.pastebin_edit_content = content
                    c.default_pastebin_doctypes_id = pastebin_doctypes_id
                    c.pastebin_wrong_captcha = True
                    portal.disconnect(); del portal
                    return self.index()
                # XXX: this could lead to spammers happiness
                session['skip_captcha'] = True
                session.save()

        docfile_avail = False
        if valid:
            if (pastebin_doctypes_id == portal.PASTEBIN_DOCTYPES['text']) and (not content):
                c.error_message = _('Empty buffer/content')
                valid = False
            elif (pastebin_doctypes_id == portal.PASTEBIN_DOCTYPES['text']) and (len(content) > config.PASTEBIN_TEXT_LENGTH):
                c.error_message = _('Too much text dude, are you crazy?')
                valid = False
            elif (pastebin_doctypes_id in [portal.PASTEBIN_DOCTYPES['image'], portal.PASTEBIN_DOCTYPES['file']]):
                docfile_avail = True
                if not hasattr(docfile,'filename'):
                    docfile_avail = False
                if not docfile_avail:
                    c.error_message = _('No stream detected')
                    valid = False
                else:
                    orig_filename = os.path.basename(docfile.filename.lstrip(os.sep))
                    content = orig_filename
                    try:
                        content = str(content)
                    except (UnicodeDecodeError,UnicodeEncodeError,):
                        c.error_message = _('Filename cannot contain non-ASCII characters')
                        valid = False

        # support for posting text that should be placed into a file
        if text_as_file and valid:
            docfile_avail = True
            pastebin_doctypes_id = portal.PASTEBIN_DOCTYPES['file']

        import shutil
        temp_filepath = None
        if docfile_avail and valid:
            # tira su file e scan antivirus
            temp_filepath = os.path.join(config.WEBSITE_TMP_DIR,self._get_random_md5())
            while os.path.lexists(temp_filepath):
                temp_filepath = os.path.join(config.WEBSITE_TMP_DIR,self._get_random_md5())
            with open(temp_filepath,"wb") as f:
                if text_as_file:
                    f.write(content.encode('utf-8'))
                    content = "pastie.txt"
                else:
                    shutil.copyfileobj(docfile.file, f)
                f.flush()
            infected = self._scan_file_for_viruses(temp_filepath)
            fsize = self._get_file_size(temp_filepath)
            if infected:
                try:
                    os.remove(temp_filepath)
                except OSError:
                    pass
                c.error_message = _('You tried to upload a virus, error will be reported, you are fucked')
                valid = False
            elif fsize > config.PASTEBIN_MAX_UPLOAD_FILE_SIZE:
                try:
                    os.remove(temp_filepath)
                except OSError:
                    pass
                c.errorm_message = _('File size too big.')
                valid = False
            elif pastebin_doctypes_id == portal.PASTEBIN_DOCTYPES['image']:
                # controlla immagine o file, se validi
                supported = is_supported_image_file(temp_filepath)
                if not supported:
                    c.error_message = _('Not supported image type')
                    valid = False

        if (not valid) and temp_filepath:
            if os.path.lexists(temp_filepath):
                try:
                    os.remove(temp_filepath)
                except OSError:
                    pass

        pastebin_id = None
        if valid:
            # insert
            status, pastebin_id = portal.insert_pastebin(
                user_ip, expiration_days,
                pastebin_syntax_id, pastebin_doctypes_id,
                content)
            if status:
                pastebin_id = int(pastebin_id)
            if not status:
                valid = False
                c.error_message = '%s' % (pastebin_id,)
            elif (pastebin_doctypes_id != portal.PASTEBIN_DOCTYPES['text']) and temp_filepath:
                # if image or file, move the path
                final_filepath = os.path.join(config.PASTEBIN_DIR,unicode(pastebin_id),content)
                os.makedirs(os.path.dirname(final_filepath))
                try:
                    os.rename(temp_filepath, final_filepath) # atomicity ftw
                except OSError:
                    shutil.move(temp_filepath, final_filepath)

                self._set_default_dir_permissions(os.path.dirname(final_filepath))

        c.valid = valid
        c.pastebin_id = pastebin_id
        if my_redirect:
            c.redirect = my_redirect

        config.setup_internal(model, c, session, request)

        # from shell
        if just_url:
            if valid:
                portal.disconnect(); del portal
                return '%s/pastie/%s' % (c.site_uri,pastebin_id,)
            portal.disconnect(); del portal
            return '%s: %s' % (
                _("Error"), c.error_message,)

        if valid:
            portal.disconnect(); del portal
            return redirect(url("/pastie/%s" % (pastebin_id,)))
        else:
            self._load_metadata(portal)
            portal.disconnect(); del portal
            return render_mako('/pastebin/index.html')

    def pasties(self):
        return redirect(url("/"))

    def show_pastie(self, pastebin_id = None):

        try:
            pastebin_id = int(pastebin_id)
        except (ValueError, TypeError,):
            return redirect(url("/"))

        portal = self.Portal()
        self._load_metadata(portal)
        err_code, pastie = portal.get_pastebin(pastebin_id)
        if not pastie:
            return redirect(url("/"))

        c.pastie_highlighted = False
        if self.pygments:
            pastebin_syntaxes = portal.get_pastebin_syntaxes()
            syntax_highlight_desc = pastebin_syntaxes.get(pastie['pastebin_syntax_id'])
            if syntax_highlight_desc != None:
                done, result, extra_css = self.syntax_highlight(pastie['content'], syntax_highlight_desc, portal)
                if done:
                    pastie['content_clean'] = result
                    c.extra_css = extra_css
                    c.pastie_highlighted = True

        c.pastebin = pastie
        c.pastebin_edit_content = pastie['content']
        c.valid = True
        c.pastebin_id = pastebin_id

        config.setup_internal(model, c, session, request)
        # create captcha html
        if not session.get('skip_captcha'):
            self._new_captcha()
        portal.disconnect(); del portal
        return render_mako('/pastebin/index.html')
