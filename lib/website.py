# -*- coding: utf-8 -*-
from pylons import tmpl_context as c
from pylons import app_globals as g
from pylons import cache, config, request, response, session, url
from pylons.controllers import WSGIController
from pylons.controllers.util import abort, etag_cache, redirect
from pylons.decorators import jsonify, validate
from pylons.i18n import _, ungettext, N_
from pylons.templating import render

from paste.request import construct_url

import stat
import os
import time
import urllib2
import www.lib.helpers as h
import www.model.config as config
from htmlentitydefs import name2codepoint

class WebsiteController:

    USER_AGENT_BLACKLIST = []

    def __init__(self):

        try:
            user_agent = request.environ['HTTP_USER_AGENT']
        except (AttributeError, KeyError):
            user_agent = None
        if user_agent in WebsiteController.USER_AGENT_BLACKLIST:
            abort(503)

        self.VIRUS_CHECK_EXEC = config.VIRUS_CHECK_EXEC
        self.VIRUS_CHECK_ARGS = config.VIRUS_CHECK_ARGS
        import www.model.Portal
        self.Portal = www.model.Portal.Portal

    def _store_vote_in_session(self, pages_id, session):
        session['poll_vote_%s' % (pages_id,)] = True
        session.save()

    def _get_remote_ip(self):
        return request.environ.get('REMOTE_ADDR')

    def _get_random(self):
        return abs(hash(os.urandom(2)))

    def _get_file_size(self, file_path):
        mystat = os.lstat(file_path)
        return int(mystat.st_size)

    def _validate_redirect(self, redirect_url):
        """ Validate HTTP redirect request through whitelist """
        if redirect_url.startswith("/"):
            return redirect_url
        return None

    def _get_redirect(self):
        """
        Properly get the redirect URL by reading HTTP request redirect
        element. Validates the value and return it, if validation fails
        return None.
        """
        redirect_url = request.params.get('redirect')
        if redirect_url:
            redirect_url = redirect_url.encode('utf-8')
            redirect_url = self._validate_redirect(redirect_url)
        return redirect_url

    def _set_user_perms(self, user_id, portal):
        c.my_role = _("User")
        c.is_admin = False
        c.is_moderator = False
        if portal.check_admin(user_id):
            c.is_admin = True
            c.my_role = _("Administrator")
        elif portal.check_moderator(user_id):
            c.is_moderator = True
            c.my_role = _("Moderator")

    def _set_default_dir_permissions(self, mydir):
        for currentdir,subdirs,files in os.walk(mydir):
            try:
                cur_gid = os.stat(currentdir)[stat.ST_GID]
                if cur_gid != config.DEFAULT_WEB_GID:
                    os.chown(currentdir, config.DEFAULT_WEB_UID,
                        config.DEFAULT_WEB_GID)
                cur_mod = self._get_chmod(currentdir)
                if cur_mod != oct(config.DEFAULT_CHMOD_DIR):
                    os.chmod(currentdir,config.DEFAULT_CHMOD_DIR)
            except OSError:
                pass
            for item in files:
                item = os.path.join(currentdir,item)
                try:
                    self._setup_file_permissions(
                        item, config.DEFAULT_WEB_UID,
                        config.DEFAULT_WEB_GID, config.DEFAULT_CHMOD_FILE
                    )
                except OSError:
                    pass

    def _setup_file_permissions(self, myfile, uid, gid, chmod):
        cur_gid = os.stat(myfile)[stat.ST_GID]
        if cur_gid != gid:
            os.chown(myfile,uid,gid)
        cur_mod = self._get_chmod(myfile)
        if cur_mod != oct(chmod):
            os.chmod(myfile,chmod)

    # you need to convert to int
    def _get_chmod(self, item):
        st = os.stat(item)[stat.ST_MODE]
        return oct(st & 0777)

    def _remove_dir(self, mydir):
        import shutil
        if os.path.isdir(mydir):
            shutil.rmtree(mydir, True)
        if os.path.isdir(mydir):
            try:
                os.rmdir(mydir)
            except OSError:
                pass

    def _htmldecode(self, text):
        import re
        charrefpat = re.compile(r'&(#(\d+|x[\da-fA-F]+)|[\w.:-]+);?')
        """Decode HTML entities in the given text."""
        if type(text) is unicode:
            uchr = unichr
        else:
            uchr = lambda value: value > 127 and unichr(value) or chr(value)
        def entitydecode(match, uchr=uchr):
            entity = match.group(1)
            if entity.startswith('#x'):
                return uchr(int(entity[2:], 16))
            elif entity.startswith('#'):
                return uchr(int(entity[1:]))
            elif entity in name2codepoint:
                return uchr(name2codepoint[entity])
            else:
                return match.group(0)
        return charrefpat.sub(entitydecode, text)

    def _htmlencode(self, text):
        return config.htmlencode(text)

    def _get_random_md5(self):
        myrnd = os.urandom(2)
        import hashlib
        m = hashlib.md5()
        m.update(myrnd)
        return m.hexdigest()

    def _scan_file_for_viruses(self, filepath):

        if not os.access(filepath,os.R_OK):
            return False

        args = [self.VIRUS_CHECK_EXEC]
        args += self.VIRUS_CHECK_ARGS
        args += [filepath]
        rc = os.system(' '.join(args)+" &> /dev/null")
        if rc == 1:
            return True
        return False

    def _get_recaptcha(self):
        try:
            from recaptcha.client import captcha
            return captcha
        except ImportError:
            return None

    def _new_captcha(self):
        captcha = self._get_recaptcha()
        if captcha == None: return
        myhtml = captcha.displayhtml(config.recaptcha_public_key)
        c.recaptcha_html = myhtml
        return myhtml

    def _validate_captcha_submit(self):
        challenge = request.params.get('recaptcha_challenge_field')
        response = request.params.get('recaptcha_response_field')
        remoteip = request.environ.get('REMOTE_ADDR')
        captcha = self._get_recaptcha()
        if captcha == None: return True
        tries = 10
        valid_response = False
        while tries:
            tries -= 1
            try:
                captcha_response = captcha.submit(challenge, response,
                    config.recaptcha_private_key, remoteip)
            except urllib2.URLError:
                time.sleep(2)
                continue
            valid_response = captcha_response.is_valid
            break
        if valid_response:
            return True
        return False
