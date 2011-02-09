"""The base Controller API

Provides the BaseController class for subclassing, and other objects
utilized by Controllers.
"""
import os
from pylons import tmpl_context as c
from pylons import app_globals as g
from pylons import cache, config, request, response, session, url
from pylons.controllers import WSGIController
from pylons.controllers.util import abort, etag_cache, redirect
from pylons.decorators import jsonify, validate
from pylons.i18n import _, ungettext, N_, set_lang, add_fallback
from pylons.i18n.translation import LanguageError
from pylons.templating import render_mako

import www.lib.helpers as h
import www.model as model

def is_valid_string(mystr):
    lower = xrange(0, 32)
    upper = xrange(128, 256)
    for s in mystr:
        if ord(s) in lower:
            return False
        if ord(s) in upper:
            return False
    return True

class BaseController(WSGIController):

    def __init__(self):

        lang = request.params.get('lang')
        if lang:
            if is_valid_string(lang):
                try:
                    set_lang(os.path.basename(lang))
                except LanguageError:
                    pass
        else:
            for lang in request.languages:
                if is_valid_string(lang):
                    try:
                        set_lang(lang)
                    except LanguageError:
                        continue
        try:
            add_fallback('en')
        except LanguageError:
            pass

    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        # WSGIController.__call__ dispatches to the Controller method
        # the request is routed to. This routing information is
        # available in environ['pylons.routes_dict']
        return WSGIController.__call__(self, environ, start_response)

# Include the '_' function in the public names
__all__ = [__name for __name in locals().keys() if not __name.startswith('_') \
           or __name == '_']
