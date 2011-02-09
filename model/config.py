# -*- coding: utf-8 -*-
import hashlib
import datetime, random, os, urllib
from pylons.i18n import _, N_
from www.private import *
from paste.request import construct_url

SITE_URI = 'http://pastebin.sabayon.org'
SITE_URI_SSL = 'https://pastebin.sabayon.org'
WIKI_URI = "http://wiki.sabayon.org"
WIKI_URI_SSL = "https://wiki.sabayon.org"
MAIN_SITE_URI = "http://www.sabayon.org"

VIRUS_CHECK_EXEC = '/usr/bin/clamscan'
VIRUS_CHECK_ARGS = []
DEFAULT_CHMOD_DIR = 0775
DEFAULT_CHMOD_FILE = 0664
DEFAULT_WEB_USER = "entropy"
DEFAULT_WEB_UID = 1000
DEFAULT_WEB_GROUP = "entropy"
DEFAULT_WEB_GID = 1000
GLSA_URI = "http://www.gentoo.org/rdf/en/glsa-index.rdf"
MY_ETP_DIR = "/home/sabayonlinux/public_html/rsync.sabayonlinux.org/entropy/"
ETP_PATH = '/home/sabayonlinux/public_html/pastebin.sabayon.org/www/entropy/libraries'
WEBSITE_TMP_DIR = '/home/sabayonlinux/public_html/pastebin.sabayon.org/temp'
COMMUNITY_REPOS_DIR = "/home/sabayonlinux/public_html/community.sabayon.org/repos/"
SCREENSHOTS_DIR = '/home/sabayonlinux/public_html/www.sabayonlinux.org/www/www/public/images/screenshots'
PASTEBIN_DIR = '/home/sabayonlinux/public_html/pastebin.sabayon.org/www/www/public/pasties/store'
PHPBB_DBNAME = "phpbb3"
PORTAL_DBNAME = "portal"
UGC_MAX_UPLOAD_FILE_SIZE = 20 * 1024000 # 20 mb
PASTEBIN_MAX_UPLOAD_FILE_SIZE = 5 * 1024000 # 5mb
PASTEBIN_TEXT_LENGTH = 512000
LOGIN_URI = '/login'
DONATIONS_URI = '/donate'
MIRRORS_URI = '/mirrors'
DASHBOARD_URI = '/community/my/dashboard'
SCREENSHOTS_IMAGES_URI = '/images/screenshots'
PASTEBIN_URI_PART = 'pasties/store'
FORUM_TOPIC_URI_PART = "viewtopic.php?t="
FEEDS = {
#    'overlay': "/home/sabayonlinux/public_html/rss/overlay.rss",
#    'projects': "/home/sabayonlinux/public_html/rss/projects.rss",
    'planet': "/home/sabayonlinux/public_html/rss/planet.rss",
}
ETP_REPOSITORY = "sabayonlinux.org"
ETP_REPOSITORY_DOWNLOAD_MIRRORS = [
    "ftp://ftp.nluug.nl/pub/os/Linux/distr/sabayonlinux/entropy/",
    "ftp://ftp.cc.uoc.gr/mirrors/linux/SabayonLinux/entropy/",
    "ftp://ftp.fsn.hu/pub/linux/distributions/sabayon/entropy/",
    "ftp://mirror.internode.on.net/pub/sabayonlinux/entropy/"
]
MY_ETP_DBDIR = "database"
MY_ETP_PKGDIR = "packages"
RSS_NEWS_FILE = "news.rss"
RSS_NEWS_PATH = "/home/sabayonlinux/public_html/www.sabayonlinux.org/www/www/public/feeds/"+RSS_NEWS_FILE
RSS_NEWS_URI = os.path.join(SITE_URI,"feeds/",RSS_NEWS_FILE)
rss_news_feed_title = _('Sabayon Linux Distribution News')
rss_news_feed_description = _('The Official Sabayon Linux News Feed - For all the p33pl3 of tha W0rlD')
rss_news_read_link = os.path.join(SITE_URI, 'pages/show/id/')

# packages.* options
# XXX hacky thing to support old URLs
default_branch = "5"
default_product = "standard"
available_products = {
    "standard": _("Sabayon Linux Standard"),
}
available_arches = {
    "amd64": "amd64",
    "x86": "x86",
}
disabled_repositories = [
    "itsme",
    "community0",
    "community1",
    "jenna",
]
repository_feeds_uri = "http://pkg.sabayon.org/"

# UGC #

community_repos_ugc_connection_data = {}

ugc_store_path = "/home/sabayonlinux/public_html/community.sabayon.org/ugc"
ugc_store_url = "http://community.sabayon.org/ugc"
ugc_args = [ugc_connection_data,ugc_store_path,ugc_store_url]

# UGC #

random_yt_vids = [
    "zbKV4nhYeJE",
    "_i3fQUu_wQE",
    "AEqH78DC7Zw"
]
random_welcome_messages = [
    _("how are you doing?"),
    _("how is it going?"),
    _("welcome back my friend"),
    _("w00t, you are back!")
]
random_encouraging_sentences = [
    _("You are gold for us, do it"),
    _("We love you already, just the last step now"),
    _("It's so nice helping people registering"),
    _("Our hearths belong to you"),
    _("All the best from our crew")
]

uri_path = "/"
small_dir_shots_name = "small"

def is_https(request):
    return "HTTPS" in request.headers

def get_http_protocol(request):
    if is_https(request):
        return "https"
    return "http"

def setup_all(model, c, session, request):
    setup_session(session)
    setup_misc_vars(c, request)
    setup_login_data(model, c, session)
    setup_permission_data(model, c, session)
    session.save()

def setup_internal(model, c, session, request):
    setup_session(session)
    setup_misc_vars(c, request)
    setup_login_data(model, c, session)
    setup_permission_data(model, c, session)
    session.save()

def setup_login_data(model, c, session):
    import www.model.UGC as ugc
    myugc = ugc.UGC()
    c.front_page_distro_stats = myugc.get_distribution_stats()
    if session.get('logged_in') and session.get('entropy'):
        session['entropy']['random_welcome_message'] = random_welcome_messages[int(random.random()*100%len(random_welcome_messages))]
        if session['entropy'].get('entropy_user_id'):
            c.front_page_user_stats = myugc.get_user_stats(session['entropy']['entropy_user_id'])
    myugc.disconnect()
    del myugc

def setup_permission_data(model, c, session):
    if session.get('entropy') and session.get('logged_in'):
        if session['entropy'].get('entropy_user_id'):
            import www.model.Portal
            portal = www.model.Portal.Portal()
            c.is_user_administrator = portal.check_admin(session['entropy']['entropy_user_id'])
            c.is_user_moderator = portal.check_moderator(session['entropy']['entropy_user_id'])
            portal.disconnect()
            del portal

def setup_session(session):
    session.setdefault('site_messages', {}):
    #cookie_timer = datetime.timedelta(30)
    session.cookie_expires = False
    #session.timeout = 604800*3 # 3 weeks
    session.cookie_domain = '.sabayon.org'

def setup_misc_vars(c, request):
    c.encouraging_sentence = random_encouraging_sentences[int(random.random()*100%len(random_encouraging_sentences))]
    if is_https(request):
        c.site_uri = SITE_URI_SSL
    else:
        c.site_uri = SITE_URI

    c.main_site_uri = MAIN_SITE_URI
    c.login_uri = LOGIN_URI
    c.donations_uri = DONATIONS_URI
    c.dashboard_uri = DASHBOARD_URI
    c.mirrors_uri = MIRRORS_URI
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
