# -*- coding: utf-8 -*-
"""Pylons middleware initialization"""
from paste.cascade import Cascade
from paste.registry import RegistryManager
from paste.urlparser import StaticURLParser
from paste.deploy.converters import asbool

from pylons import config
from pylons.error import error_template
from pylons.middleware import error_mapper, ErrorDocuments, ErrorHandler, \
    StaticJavascripts, StatusCodeRedirect
from pylons.wsgiapp import PylonsApp

from www.config.environment import load_environment

from webob import Request
from webob.exc import HTTPBadRequest

class LimitUploadSize(object):

    def __init__(self, app, size):
        self.app = app
        self.size = size

    def __call__(self, environ, start_response):
        req = Request(environ)
        if req.method=='POST':
            len = req.headers.get('Content-length')
            if not len:
                return HTTPBadRequest("No content-length header specified, you suck!")(environ, start_response)
            elif int(len) > self.size:
                return HTTPBadRequest("POST body exceeds maximum limits, your bad!")(environ, start_response)
        resp = req.get_response(self.app)
        return resp(environ, start_response)

def make_app(global_conf, full_stack=True, **app_conf):
    """Create a Pylons WSGI application and return it

    ``global_conf``
        The inherited configuration for this application. Normally from
        the [DEFAULT] section of the Paste ini file.

    ``full_stack``
        Whether or not this application provides a full WSGI stack (by
        default, meaning it handles its own exceptions and errors).
        Disable full_stack when this application is "managed" by
        another WSGI middleware.

    ``app_conf``
        The application's local configuration. Normally specified in the
        [app:<name>] section of the Paste ini file (where <name>
        defaults to main).
    """
    # Configure the Pylons environment
    config = load_environment(global_conf, app_conf)

    # The Pylons WSGI app
    app = PylonsApp(config=config)

    # CUSTOM MIDDLEWARE HERE (filtered by error handling middlewares)

    import pylons
    # Routing/Session/Cache Middleware
    from beaker.middleware import SessionMiddleware
    from routes.middleware import RoutesMiddleware
    app = RoutesMiddleware(app, config['routes.map'])
    app = SessionMiddleware(app, config)


    if asbool(full_stack):
        # Handle Python exceptions
        app = ErrorHandler(app, global_conf, **config['pylons.errorware'])

        # Display error documents for 401, 403, 404 status codes (and
        # 500 when debug is disabled)
        if asbool(config['debug']):
            app = StatusCodeRedirect(app)
        else:
            app = StatusCodeRedirect(app, [401, 403, 404, 500])

    # Establish the Registry for this application
    app = RegistryManager(app)

    # Static files
    javascripts_app = StaticJavascripts()
    static_app = StaticURLParser(config['pylons.paths']['static_files'])
    app = Cascade([static_app, javascripts_app, app])
    #app = LimitUploadSize(app, 30 * 1024000) # 20mb, max upload size
    app.config = config
    return app
