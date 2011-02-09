"""The base Controller API

Provides the BaseController class for subclassing, and other objects
utilized by Controllers.
"""
import os
import sys
from pylons import tmpl_context as c
from pylons import app_globals as g
from pylons import cache, request, response, session, url
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

def get_buffer():
    """
    Return generic buffer object (supporting both Python 2.x and Python 3.x)
    """
    if sys.hexversion >= 0x3000000:
        return memoryview
    else:
        return buffer

def get_int():
    """
    Return generic int object (supporting both Python 2.x and Python 3.x).
    For Python 2.x a (long, int) tuple is returned.
    For Python 3.x a (int,) tuple is returned.
    """
    if sys.hexversion >= 0x3000000:
        return (int,)
    else:
        return (long, int,)

def isunicode(obj):
    """
    Return whether obj is a unicode.

    @param obj: Python object
    @type obj: Python object
    @return: True, if object is unicode
    @rtype: bool
    """
    if sys.hexversion >= 0x3000000:
        return isinstance(obj, str)
    else:
        return isinstance(obj, unicode)

def convert_to_rawstring(obj, from_enctype = 'raw_unicode_escape'):
    """
    Convert generic string to raw string (str for Python 2.x or bytes for
    Python 3.x).

    @param obj: input string
    @type obj: string object
    @keyword from_enctype: encoding which string is using
    @type from_enctype: string
    @return: raw string
    @rtype: bytes
    """
    if isinstance(obj, get_buffer()):
        if sys.hexversion >= 0x3000000:
            return obj.tobytes()
        else:
            return str(obj)
    if not isunicode(obj):
        return obj
    return obj.encode(from_enctype)

def convert_to_unicode(obj, enctype = 'raw_unicode_escape'):
    """
    Convert generic string to unicode format, this function supports both
    Python 2.x and Python 3.x unicode bullshit.

    @param obj: generic string object
    @type obj: string
    @return: unicode string object
    @rtype: unicode object
    """

    # None support
    if obj is None:
        if sys.hexversion >= 0x3000000:
            return "None"
        else:
            return unicode("None")

    # int support
    if isinstance(obj, get_int()):
        if sys.hexversion >= 0x3000000:
            return str(obj)
        else:
            return unicode(obj)

    # buffer support
    if isinstance(obj, get_buffer()):
        if sys.hexversion >= 0x3000000:
            return str(obj.tobytes(), enctype)
        else:
            return unicode(obj, enctype)

    # string/unicode support
    if isunicode(obj):
        return obj
    if hasattr(obj, 'decode'):
        return obj.decode(enctype)
    else:
        if sys.hexversion >= 0x3000000:
            return str(obj, enctype)
        else:
            return unicode(obj, enctype)

def _is_png_file(path):
    with open(path, "rb") as f:
        x = f.read(4)
    if x == convert_to_rawstring('\x89PNG'):
        return True
    return False

def _is_jpeg_file(path):
    with open(path, "rb") as f:
        x = f.read(10)
    if x == convert_to_rawstring('\xff\xd8\xff\xe0\x00\x10JFIF'):
        return True
    return False

def _is_bmp_file(path):
    with open(path, "rb") as f:
        x = f.read(2)
    if x == convert_to_rawstring('BM'):
        return True
    return False

def _is_gif_file(path):
    with open(path, "rb") as f:
        x = f.read(5)
    if x == convert_to_rawstring('GIF89'):
        return True
    return False

def is_supported_image_file(path):
    """
    Return whether passed image file path "path" references a valid image file.
    Currently supported image file types are: PNG, JPEG, BMP, GIF.

    @param path: path pointing to a possibly valid image file
    @type path: string
    @return: True if path references a valid image file 
    @rtype: bool
    """
    calls = [_is_png_file, _is_jpeg_file, _is_bmp_file, _is_gif_file]
    for mycall in calls:
        if mycall(path):
            return True
    return False

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
