# -*- coding: utf-8 -*-
import logging
from www.lib.base import *
from www.lib.website import *
from pylons.i18n import _
log = logging.getLogger(__name__)

class LoginController(BaseController, WebsiteController):

    def __init__(self):
        BaseController.__init__(self)
        WebsiteController.__init__(self)
        import www.model.Authenticator
        self.Authenticator = www.model.Authenticator.Authenticator
        import www.model.Portal
        self.Portal = www.model.Portal.Portal
        import entropy.exceptions as etp_exceptions
        self.etp_exceptions = etp_exceptions

    def index(self):
        model.config.setup_all(model, c, session, request)
        if session.get('logged_in'):
            return render_mako('/home.html')
        else:
            c.login_redirect = self._get_redirect()
            c.page_title = _('Hello mate, what about logging in? Have a look below')
            return render_mako('/login.html')

    def activate(self):

        model.config.setup_internal(model, c, session, request)
        error, user_id, registration_validation_id, confirmation_code = self._get_generic_activation_parameters()

        valid = False
        if not error:
            portal = self.Portal()
            valid = portal.registration_validation_check(registration_validation_id, user_id, confirmation_code)
            if valid:
                myauth = self.Authenticator()
                myauth.activate_user(user_id)
                del myauth
                portal.clear_registration_validation(user_id)
            portal.disconnect()
            del portal

        c.activation_successful = valid
        c.confirmation_code = confirmation_code
        c.registration_validation_id = registration_validation_id
        c.user_id = user_id
        c.page_title = _('Sabayon Linux Community activation')
        return render_mako('/activation_successful.html')


    def register(self):
        model.config.setup_permission_data(model, c, session)
        model.config.setup_misc_vars(c, request)

        user_id = self._get_logged_user_id()
        if user_id:
            model.config.setup_all(model, c, session, request)
            return render_mako('/home.html')

        # check ip ban
        portal = self.Portal()
        banned = portal.check_ip_ban(request.environ['REMOTE_ADDR'])
        portal.disconnect()
        del portal
        c.page_title = _('Sabayon Linux Community registration')
        if banned:
            c.ip_banned = request.environ['REMOTE_ADDR']
            return render_mako('/register.html')

        self._new_captcha()

        c.login_redirect = self._get_redirect()
        return render_mako('/register.html')

    def register_submit(self):
        model.config.setup_permission_data(model, c, session)
        model.config.setup_misc_vars(c, request)

        username = request.params.get('username')
        password = request.params.get('new_password')
        password_confirm = request.params.get('password_confirm')
        email = request.params.get('email')
        email_confirm = request.params.get('email_confirm')
        errors = []

        def push_back_fields():
            c.username = username
            c.password = password
            c.password_confirm = password_confirm
            c.email = email
            c.email_confirm = email_confirm

        if not username:
            errors.append(_('Invalid Username'))
            push_back_fields()

        if (email != email_confirm) or not email:
            if not errors: push_back_fields()
            errors.append(_('Invalid Email, empty fields or mismatch'))
            del c.email, c.email_confirm

        if (password != password_confirm) or (not password) or (len(password) < 3) or (len(password) > 30):
            if not errors: push_back_fields()
            errors.append(_('Invalid Password, empty fields or mismatch or wrong length'))
            del c.password, c.password_confirm

        # verify captcha answer
        valid = self._validate_captcha_submit()
        if not valid:
            if not errors: push_back_fields()
            errors.append(_('Invalid Captcha Answer'))

        if errors:
            return '<br/>'.join(errors)

        myauth = self.Authenticator()
        status, user_id = myauth.register_user(username, password, email, not model.config.registration_activation_required)
        if not status:
            del myauth
            return "%s: %s" % (_("Invalid"),user_id,)
        del myauth

        # reg success, send e-mail
        c.registration_successful = True
        c.mail_send_error = False

        portal = self.Portal()
        registration_validation_id, confirmation_code = portal.create_new_registration_validation_id(user_id)
        activation_uri = model.config.registration_activation_uri + "?u=%s&r=%s&c=%s" % (user_id,registration_validation_id,confirmation_code)
        mail_text = model.config.registration_mail_text

        # FIXED: username and passwords are unencoded chars and we need utf-8 here
        mail_text = mail_text.replace('--username--',username.decode('utf-8'))
        mail_text = mail_text.replace('--password--',password.decode('utf-8'))

        mail_text = mail_text.replace('--website_url--',model.config.SITE_URI)
        mail_text = mail_text.replace('--activation_url--',activation_uri)

        try:
            self._send_text_email([email], model.config.registration_mail_subject, mail_text)
        except Exception, e:
            c.mail_send_error = True

        portal.disconnect()
        del portal

        c.login_redirect = self._get_redirect()
        return render_mako('/registration_successful.html')


    def submit(self):

        model.config.setup_all(model, c, session, request)
        login_data = {
            'username': request.params.get('username'),
            'password': request.params.get('password')
        }
        if login_data['password']:
            login_data['password'] = login_data['password'].encode('utf-8')

        myauth = self.Authenticator()
        myauth.set_login_data(login_data)
        error = None
        try:
            logged = myauth.login()
        except (self.etp_exceptions.PermissionDenied, UnicodeEncodeError,), e:
            logged = False
            c.login_error = e

        if logged:
            myauth._update_session_table(myauth.login_data['user_id'], request.environ['REMOTE_ADDR'])
            session['entropy'] = {}
            session['entropy']['entropy_user'] = login_data['username']
            session['logged_in'] = True
            session['entropy']['password_hash'] = model.config.hash_string(login_data['password'])
            session['entropy']['entropy_user_id'] = myauth.login_data['user_id']
            model.config.setup_login_data(model, c, session)
            session.save()

        myauth.disconnect()
        del myauth

        login_redirect = self._get_redirect()
        if logged and login_redirect:
            if model.config.get_http_protocol(request) == "https":
                return redirect(url(login_redirect.replace("http://", "https://")))
            else:
                return redirect(url(login_redirect))
        return redirect(url("/", protocol=model.config.get_http_protocol(request)))

    def logout(self):
        if 'entropy' in session:
            del session['entropy']
        if 'logged_in' in session:
            del session['logged_in']
        session.save()

        model.config.setup_all(model, c, session, request)
        return redirect(url('/', protocol=model.config.get_http_protocol(request)))

    def update_email(self):

        if request.method != "POST":
            return "%s: %s" % (_('Error'), _('invalid HTTP method'))
        user_id = self._get_logged_user_id()
        if not user_id:
            return "%s: %s" % (_('Error'), _('not logged in'))

        # get from POST
        old_email = request.params.get('old_email')
        if not isinstance(old_email,basestring):
            return "%s: %s" % (_('Error'), _('wrong POST'))
        try:
            old_email = str(old_email)
        except:
            return "%s: %s" % (_('Error'), _('invalid old e-mail'))

        email = request.params.get('user_email')
        email_repeat = request.params.get('user_email_confirm')
        if old_email == email:
            return "%s: %s" % (_('Error'), _('you changed nothing'))

        if not (email and email_repeat):
            return "%s: %s" % (_('Error'), _('empty fields'))
        elif email != email_repeat:
            return "%s: %s" % (_('Error'), _('e-mails do not match'))
        elif not (isinstance(email,basestring) and isinstance(email_repeat,basestring)):
            return "%s: %s" % (_('Error'), _('invalid parameters'))

        valid = self._validate_email(email)
        if not valid:
            return "%s: %s" % (_('Error'), _('invalid e-mail (1)'))
        valid = self._validate_email(email_repeat)
        if not valid:
            return "%s: %s" % (_('Error'), _('invalid e-mail (2)'))

        email = str(email)
        portal = self.Portal()
        email_update_validation_id, confirmation_code = portal.create_new_email_update_validation_id(user_id, email)
        activation_uri = model.config.email_update_activation_uri + "?u=%s&r=%s&c=%s" % (user_id,email_update_validation_id,confirmation_code)
        mail_text = model.config.email_update_mail_text
        mail_text = mail_text.replace('--old_email--',old_email)
        mail_text = mail_text.replace('--new_email--',email)
        mail_text = mail_text.replace('--website_url--',model.config.SITE_URI)
        mail_text = mail_text.replace('--activation_url--',activation_uri)

        self._send_text_email([email], model.config.email_update_mail_subject, mail_text)

        portal.disconnect()
        del portal
        return '<font style="color: green">%s</font>: %s.' % (
            _("Success"), _("you must activate your change. You have mail"),)

    def email_activate(self):

        model.config.setup_internal(model, c, session, request)

        error, user_id, validation_id, confirmation_code = self._get_generic_activation_parameters()

        valid = False
        if not error:
            portal = self.Portal()
            email = portal.email_update_validation_check(validation_id, user_id, confirmation_code)
            if email:
                valid = portal.update_user_email(user_id, email)
                if valid: portal.clear_email_update_validation(user_id)
            portal.disconnect()
            del portal

        c.activation_successful = valid
        c.confirmation_code = confirmation_code
        c.email_update_validation_id = validation_id
        c.user_id = user_id
        c.page_title = _('Sabayon Linux Community E-mail Update Activation')
        return render_mako('/email_activation_successful.html')

    def update_password(self):

        if request.method != "POST":
            return "%s: %s" % (_('Error'), _('invalid HTTP method'))
        user_id = self._get_logged_user_id()
        username = self._get_logged_username()
        if not user_id:
            return "%s: %s" % (_('Error'), _('not logged in'))
        if not username:
            return "%s: %s" % (_('Error'), _('not logged in (username)'))

        # get from POST
        current_password = request.params.get('current_password')
        if not current_password:
            return "%s: %s" % (_('Error'), _('where is the current password?'))

        new_password = request.params.get('new_password')
        new_password_repeat = request.params.get('new_password_repeat')
        if not (new_password and new_password_repeat):
            return "%s: %s" % (_('Error'), _('missing fields'))
        elif new_password != new_password_repeat:
            return "%s: %s" % (_('Error'), _('new password fields do not match'))
        elif not (isinstance(new_password,basestring) and isinstance(new_password_repeat,basestring)):
            return "%s: %s" % (_('Error'), _('wtf are you trying to do?'))
        elif current_password == new_password:
            return "%s: %s" % (_('Error'), _('old and new password match'))

        if len(new_password) < 6:
            return "%s: %s" % (_('Error'), _('password too short'))
        elif len(new_password) > 30:
            return "%s: %s" % (_('Error'), _('password too long'))

        # check current_password
        portal = self.Portal()
        valid = portal.check_user_credentials(username,current_password)
        if not valid:
            portal.disconnect()
            del portal
            return "%s: %s" % (_('Error'), _('invalid current password'))

        email = portal.get_user_email(user_id)
        if not email:
            portal.disconnect()
            del portal
            return "%s: %s" % (_('Error'), _('you do not have a valid e-mail'))

        # now create a ticket
        password_update_validation_id, confirmation_code = portal.create_new_password_update_validation_id(user_id, new_password)

        activation_uri = model.config.password_update_activation_uri + "?u=%s&r=%s&c=%s" % (user_id,password_update_validation_id,confirmation_code)
        mail_text = model.config.password_update_mail_text
        # FIXED: username and passwords are unencoded chars and we need utf-8 here
        mail_text = mail_text.replace('--new_password--',new_password.decode('utf-8'))
        mail_text = mail_text.replace('--website_url--',model.config.SITE_URI)
        mail_text = mail_text.replace('--activation_url--',activation_uri)

        self._send_text_email([email], model.config.password_update_mail_subject, mail_text)

        portal.disconnect()
        del portal
        return '<font style="color: green">%s</font>: %s.' % (
            _("Success"), _("you must activate your change. You have mail"),)

    def password_activate(self):

        model.config.setup_internal(model, c, session, request)

        error, user_id, validation_id, confirmation_code = self._get_generic_activation_parameters()

        valid = False
        if not error:
            portal = self.Portal()
            password_hash = portal.password_update_validation_check(validation_id, user_id, confirmation_code)
            if password_hash:
                valid = portal.update_user_password_hash(user_id, password_hash)
                if valid: portal.clear_password_update_validation(user_id)
            portal.disconnect()
            del portal

        c.activation_successful = valid
        c.confirmation_code = confirmation_code
        c.password_update_validation_id = validation_id
        c.user_id = user_id
        c.page_title = _('Sabayon Linux Community Password Update Activation')
        return render_mako('/password_activation_successful.html')
