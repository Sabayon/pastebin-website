# -*- coding: utf-8 -*-
import hashlib
import datetime, random, os, urllib
from pylons.i18n import _, N_
from www.private import *
from paste.request import construct_url

SITE_URI = 'http://pastebin.sabayon.org'
SITE_URI_SSL = 'https://pastebin.sabayon.org'
MAIN_SITE_URI = "http://www.sabayon.org"

VIRUS_CHECK_EXEC = '/usr/bin/clamscan'
VIRUS_CHECK_ARGS = []
DEFAULT_CHMOD_DIR = 0775
DEFAULT_CHMOD_FILE = 0664
DEFAULT_WEB_USER = "www-data"
DEFAULT_WEB_UID = 33
DEFAULT_WEB_GROUP = "www-data"
DEFAULT_WEB_GID = 33
WEBSITE_TMP_DIR = '/home/sabayonlinux/public_html/pastebin.sabayon.org/temp'
PASTEBIN_DIR = '/home/sabayonlinux/public_html/pastebin.sabayon.org/www/www/public/pasties/store'
PHPBB_DBNAME = "phpbb3"
PORTAL_DBNAME = "portal"
PASTEBIN_MAX_UPLOAD_FILE_SIZE = 5 * 1024000 # 5mb
PASTEBIN_TEXT_LENGTH = 512000
PASTEBIN_URI_PART = 'pasties/store'

uri_path = "/"

def is_https(request):
    return "HTTPS" in request.headers

def get_http_protocol(request):
    if is_https(request):
        return "https"
    return "http"

def setup_all(model, c, session, request):
    setup_session(session)
    setup_misc_vars(c, request)
    session.save()

def setup_internal(model, c, session, request):
    setup_session(session)
    setup_misc_vars(c, request)
    session.save()

def setup_session(session):
    session.setdefault('site_messages', {}):
    session.cookie_expires = False
    session.cookie_domain = '.sabayon.org'

def setup_misc_vars(c, request):
    if is_https(request):
        c.site_uri = SITE_URI_SSL
    else:
        c.site_uri = SITE_URI

    c.main_site_uri = MAIN_SITE_URI
    c.pastebin_uri = os.path.join(c.site_uri, PASTEBIN_URI_PART)

    c.www_current_url = construct_url(request.environ)
    try:
        c.browser_user_agent = request.environ['HTTP_USER_AGENT']
    except KeyError:
        pass

    c.this_uri = request.environ.get('PATH_INFO')
    if request.environ.get('QUERY_STRING'):
        c.this_uri += '?' + request.environ['QUERY_STRING']
    c.this_uri_full = SITE_URI + c.this_uri
    c.this_uri_full_quoted = urllib.quote(htmlencode(c.this_uri_full))

def hash_string(s):
    m = hashlib.md5()
    m.update(s)
    return m.hexdigest()

def get_current_date():
    import time
    my = time.gmtime()
    return "%s/%s/%s" % (my[2],my[1],my[0],)

def remove_html_tags(data):
    import re
    p = re.compile(r'<.*?>')
    return p.sub('', data)

def remove_phpbb_tags(data):
    import re
    p = re.compile(r'\[.*?\]')
    return p.sub('', data)

def digitalize_ip(user_ip):
    try:
        myip = int(user_ip.replace(".",""))
    except (ValueError,TypeError,):
        myip = None
    return myip

def htmlencode(text):
    """Use HTML entities to encode special characters in the given text."""
    text = text.replace('&', '&amp;')
    text = text.replace('"', '&quot;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    return text
