import cgi
import os.path

from paste.urlparser import StaticURLParser
from pylons.middleware import error_document_template, media_path
from webhelpers.html.builder import literal

from www.lib.base import *
from www.lib.website import *
import www.model.config as config

class ErrorController(BaseController, WebsiteController):
    """Generates error documents as and when they are required.

    The ErrorDocuments middleware forwards to ErrorController when error
    related status codes are returned from the application.

    This behaviour can be altered by changing the parameters to the
    ErrorDocuments middleware in your config/middleware.py file.

    """

    def __init__(self):
        BaseController.__init__(self)
        WebsiteController.__init__(self)

    def document(self):
        """Render the error document"""
        config.setup_internal(model, c, session, request)
        # create recaptcha html
        if not session.get('skip_captcha'):
            self._new_captcha()
        self._load_metadata()

        resp = request.environ.get('pylons.original_response')
        c.error_message = "Page error dude, have fun"
        if resp is not None:
            c.code = cgi.escape(request.GET.get('code', str(resp.status_int)))
            c.error_message = literal(resp.body) or cgi.escape(request.GET.get('message', ''))
        c.page_error = True
        c.valid = False

        return render_mako('/pastebin/index.html')

    def img(self, id):
        """Serve Pylons' stock images"""
        return self._serve_file(os.path.join(media_path, 'img'), id)

    def style(self, id):
        """Serve Pylons' stock stylesheets"""
        return self._serve_file(os.path.join(media_path, 'style'), id)

    def _serve_file(self, root, path):
        """Call Paste's FileApp (a WSGI application) to serve the file
        at the specified path
        """
        static = StaticURLParser(root)
        request.environ['PATH_INFO'] = '/%s' % path
        return static(request.environ, self.start_response)
