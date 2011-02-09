# -*- coding: utf-8 -*-
import os
import config
from entropy.const import *
etpConst['entropygid'] = config.DEFAULT_WEB_GID
from entropy.services.skel import Authenticator as DistributionAuthInterface
from entropy.services.skel import RemoteDatabase as RemoteDbSkelInterface
from entropy.misc import RSS
from Authenticator import Authenticator
from Forum import Forum
import entropy.exceptions as etp_exceptions
try:
    from entropy.services.exceptions import ServiceConnectionError
except ImportError:
    ServiceConnectionError = Exception
import entropy.tools as entropy_tools

class Portal(DistributionAuthInterface,RemoteDbSkelInterface):

    PASTEBIN_SYNTAXES = ['ASM (NASM based)', 'ASP', 'ActionScript', 'ActionScript 3', 'Ada', 'Apache Log File', 'Apache Configuration File', 'AppleScript', 'Bash', 'C', 'C for Macs', 'C#', 'C++', 'CAD DCL', 'CAD Lisp', 'CSS', 'ColdFusion', 'D', 'DOS', 'Delphi', 'Diff', 'Eiffel', 'Fortran', 'FreeBasic', 'Game Maker', 'HTML', 'INI file', 'Java', 'Javascript', 'Lisp', 'Lua', 'MPASM', 'MatLab', 'MySQL', 'NullSoft Installer', 'OCaml', 'Objective C', 'Openoffice.org BASIC', 'Oracle 8', 'PHP', 'Pascal', 'Perl', 'Plain text', 'Python', 'Python 3', 'QBasic/QuickBASIC', 'Robots', 'Ruby', 'SQL', 'Scheme', 'Smarty', 'TCL', 'VB.NET', 'VisualBasic', 'VisualFoxPro', 'XML']
    PASTEBIN_SYNTAXES_MAP = {
        'ASM (NASM based)': 'asm',
        'ASP': 'asp',
        'ActionScript': 'as',
        'ActionScript 3': 'as3',
        'Ada': 'text',
        'Apache Log File': 'text',
        'Apache Configuration File': 'apache',
        'AppleScript': 'applescript',
        'Bash': 'bash',
        'C': 'c',
        'C for Macs': 'c',
        'C#': 'csharp',
        'C++': 'cpp',
        'CAD DCL': 'text',
        'CAD Lisp': 'text',
        'CSS': 'css',
        'ColdFusion': 'text',
        'D': 'd',
        'DOS': 'bat',
        'Delphi': 'delphi',
        'Diff': 'diff',
        'Eiffel': 'text',
        'Fortran': 'fortran',
        'FreeBasic': 'text',
        'Game Maker': 'text',
        'HTML': 'html',
        'INI file': 'ini',
        'Java': 'java',
        'Javascript': 'js',
        'Lisp': 'common-lisp',
        'Lua': 'lua',
        'MPASM': 'text',
        'MatLab': 'matlab',
        'MySQL': 'mysql',
        'NullSoft Installer': 'text',
        'OCaml': 'ocaml',
        'Objective C': 'objective-c',
        'Openoffice.org BASIC': 'text',
        'Oracle 8': 'sql',
        'PHP': 'php',
        'Pascal': 'pascal',
        'Perl': 'perl',
        'Plain text': 'text',
        'Python': 'python',
        'Python 3': 'python3',
        'QBasic/QuickBASIC': 'text',
        'Robots': 'text',
        'Ruby': 'ruby',
        'SQL': 'sql',
        'Scheme': 'scheme',
        'Smarty': 'html+smarty',
        'TCL': 'tcl',
        'VB.NET': 'vb.net',
        'VisualBasic': 'vb.net',
        'VisualFoxPro': 'text',
        'XML': 'xml',
    }
    PASTEBIN_DOCTYPES = {
        'text': 1,
        'image': 2,
        'file': 3,
    }
    PASTEBIN_DOCTYPES_DESC = {
        1: _('Text'),
        2: _('Image'),
        3: _('File'),
    }
    PASTEBIN_PERMISSIONS = {
        'public': 0,
        'user_priv': 1,
        'registered_users': 2,
    }
    PASTEBIN_PERMISSIONS_DESC = {
        0: _('Public'),
        1: _('User private'),
        2: _('Registered users'),
    }

    PASTEBIN_LAG_SECONDS = 20

    SQL_TABLES = {
        'pastebin_syntax': """
            CREATE TABLE pastebin_syntax (
                pastebin_syntax_id INT NOT NULL AUTO_INCREMENT,
                syntax_name VARCHAR(255),
                PRIMARY KEY (pastebin_syntax_id)
            ) CHARACTER SET utf8 COLLATE utf8_bin;
        """,
        'pastebin_doctypes': """
            CREATE TABLE pastebin_doctypes (
                pastebin_doctypes_id INT NOT NULL AUTO_INCREMENT,
                doctype_name VARCHAR(255),
                PRIMARY KEY (pastebin_doctypes_id)
            ) CHARACTER SET utf8 COLLATE utf8_bin;
        """,
        'pastebin_permissions': """
            CREATE TABLE pastebin_permissions (
                pastebin_permissions_id INT NOT NULL AUTO_INCREMENT,
                permission_name VARCHAR(255),
                PRIMARY KEY (pastebin_permissions_id)
            ) CHARACTER SET utf8 COLLATE utf8_bin;
        """,
        'pastebin_recent': """
            CREATE TABLE pastebin_recent (
                pastebin_recent_id INT NOT NULL AUTO_INCREMENT,
                user_ip VARCHAR(15),
                ts TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                KEY `user_ip` (`user_ip`),
                PRIMARY KEY (pastebin_recent_id)
            ) CHARACTER SET utf8 COLLATE utf8_bin;
        """,
        'pastebin': """
            CREATE TABLE pastebin (
                pastebin_id INT NOT NULL AUTO_INCREMENT,
                user_id INT,
                permissions TINYINT,
                orig_ts TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                expiration_days INT NOT NULL,
                pastebin_syntax_id INT NOT NULL,
                pastebin_doctypes_id INT NOT NULL,
                content TEXT,
                PRIMARY KEY (pastebin_id),
                FOREIGN KEY  (pastebin_syntax_id) REFERENCES pastebin_syntax (pastebin_syntax_id),
                FOREIGN KEY  (pastebin_doctypes_id) REFERENCES pastebin_doctypes (pastebin_doctypes_id)
            ) CHARACTER SET utf8 COLLATE utf8_bin;
        """,
    }

    def __init__(self, do_init = False):
        import entropy.tools as entropyTools
        self.authenticator = Authenticator
        DistributionAuthInterface.__init__(self)
        RemoteDbSkelInterface.__init__(self)
        self.set_connection_data(config.portal_connection_data)
        self.connect()
        if do_init:
            self.initialize_tables()
            self.initialize_pastebin_syntaxes()
            self.initialize_pastebin_doctypes()
            self.initialize_pastebin_permissions()
        self.dbconn.set_character_set('utf8')

    def __del__(self):
        if hasattr(self,'disconnect'):
            try:
                self.disconnect()
            except ServiceConnectionError:
                pass

    def check_connection(self):
        pass

    def initialize_tables(self):
        notable = False
        for table in self.SQL_TABLES:
            if self.table_exists(table):
                continue
            notable = True
            self.execute_script(self.SQL_TABLES[table])
        if notable:
            self.commit()

    def initialize_pastebin_permissions(self):
        for perm in self.PASTEBIN_PERMISSIONS:
            if self.is_pastebin_permissions_id_available(self.PASTEBIN_PERMISSIONS[perm]):
                continue
            self.insert_pastebin_permissions_id(self.PASTEBIN_PERMISSIONS[perm],perm)

    def is_pastebin_permissions_id_available(self, pastebin_permissions_id):

        rows = self.execute_query('SELECT pastebin_permissions_id FROM pastebin_permissions WHERE pastebin_permissions_id = %s', (pastebin_permissions_id,))
        if rows: return True
        return False

    def insert_pastebin_permissions_id(self, pastebin_permissions_id, permission_name, do_commit = False):

        self.execute_query('INSERT INTO pastebin_permissions VALUES (%s,%s)', (pastebin_permissions_id,permission_name,))
        if do_commit: self.commit()

    def initialize_pastebin_doctypes(self):
        for doctype in self.PASTEBIN_DOCTYPES:
            if self.is_pastebin_doctypes_id_available(self.PASTEBIN_DOCTYPES[doctype]):
                continue
            self.insert_pastebin_doctypes_id(self.PASTEBIN_DOCTYPES[doctype],doctype)

    def is_pastebin_doctypes_id_available(self, pastebin_doctypes_id):

        rows = self.execute_query('SELECT `pastebin_doctypes_id` FROM pastebin_doctypes WHERE `pastebin_doctypes_id` = %s', (pastebin_doctypes_id,))
        if rows: return True
        return False

    def insert_pastebin_doctypes_id(self, pastebin_doctypes_id, doctype_name, do_commit = False):

        self.execute_query('INSERT INTO pastebin_doctypes VALUES (%s,%s)', (pastebin_doctypes_id,doctype_name,))
        if do_commit: self.commit()

    def is_pastebin_syntax_available(self, syntax):

        rows = self.execute_query('SELECT pastebin_syntax_id FROM pastebin_syntax WHERE syntax_name = %s', (syntax,))
        if rows: return True
        return False

    def insert_pastebin_syntax(self, syntax_name, do_commit = False):

        self.execute_query('INSERT INTO pastebin_syntax VALUES (%s,%s)', (None,syntax_name,))
        if do_commit: self.commit()
        return self.lastrowid()

    def initialize_pastebin_syntaxes(self):
        for syntax in self.PASTEBIN_SYNTAXES:
            if self.is_pastebin_syntax_available(syntax):
                continue
            self.insert_pastebin_syntax(syntax)

    def _get_unique_id(self):
        import md5
        m = md5.new()
        m2 = md5.new()
        rnd = str(abs(hash(os.urandom(20))))
        rnd2 = str(abs(hash(os.urandom(20))))
        m.update(rnd)
        m2.update(rnd2)
        m.update(rnd2)
        m2.update(rnd)
        x = m.hexdigest() + m2.hexdigest()
        del m, m2
        return x

    def get_user_birthday(self, user_id):
        auth = self.authenticator()
        self.do_fake_authenticator_login(auth, user_id)
        user_birthday = auth.get_user_birthday()
        auth.disconnect()
        del auth
        return user_birthday

    def get_user_email(self, user_id):
        auth = self.authenticator()
        self.do_fake_authenticator_login(auth, user_id)
        email = auth.get_email()
        auth.disconnect()
        del auth
        return email

    def update_user_password_hash(self, user_id, password_hash):
        auth = self.authenticator()
        self.do_fake_authenticator_login(auth, user_id)
        valid = auth.update_password_hash(password_hash)
        auth.disconnect()
        del auth
        return valid

    def do_fake_authenticator_login(self, authenticator, user_id):
        data = {
            'user_id': user_id,
            'username': '###fake###',
            'password': '###fake###'
        }
        authenticator.set_login_data(data)
        authenticator.logged_in = True

    def check_admin(self, user_id):
        auth = self.authenticator()
        self.do_fake_authenticator_login(auth, user_id)
        valid = auth.is_administrator()
        auth.disconnect()
        del auth
        return valid

    def check_moderator(self, user_id):
        auth = self.authenticator()
        self.do_fake_authenticator_login(auth, user_id)
        valid = auth.is_moderator()
        auth.disconnect()
        del auth
        return valid

    def check_user(self, user_id):
        auth = self.authenticator()
        self.do_fake_authenticator_login(auth, user_id)
        valid = auth.is_user()
        auth.disconnect()
        del auth
        return valid

    def check_user_credentials(self, username, password):

        login_data = {
            'username': username,
            'password': password.encode('utf-8')
        }

        myauth = self.authenticator()
        myauth.set_login_data(login_data)
        try:
            logged = myauth.login()
        except etp_exceptions.PermissionDenied, e:
            logged = False
        myauth.disconnect()
        del myauth
        return logged

    def get_username(self, user_id):

        self.execute_query('SELECT '+config.PHPBB_DBNAME+'.phpbb_users.username as username FROM '+config.PHPBB_DBNAME+'.phpbb_users WHERE '+config.PHPBB_DBNAME+'.phpbb_users.user_id = %s', (user_id,))
        username = 'Anonymous'
        data = self.fetchone()
        if isinstance(data,dict):
            if data.has_key('username'):
                username = data.get('username')
        return username

    def get_user_id(self, username):

        self.execute_query('SELECT '+config.PHPBB_DBNAME+'.phpbb_users.user_id as user_id FROM '+config.PHPBB_DBNAME+'.phpbb_users WHERE '+config.PHPBB_DBNAME+'.phpbb_users.username = %s', (username,))
        data = self.fetchone()
        user_id = 0
        if isinstance(data,dict):
            if data.has_key('user_id'):
                user_id = data.get('user_id')
        return user_id

    def _remove_html_tags(self, data):
        import re
        p = re.compile(r'<.*?>')
        return p.sub('', data)

    def _get_ts(self):
        from datetime import datetime
        import time
        return datetime.fromtimestamp(time.time())

    def validate_pastebin_user_ip(self, user_ip):

        self.execute_query('SELECT user_ip, ts FROM pastebin_recent WHERE user_ip = %s ORDER BY ts DESC LIMIT 1', (user_ip,))
        data = self.fetchone()
        if not data: return True
        if not isinstance(data,dict): return True
        if not data.has_key('user_ip'): return True
        if not data.get('ts'): return True
        cur_ts = self._get_ts()
        cur_delta = cur_ts - data['ts']
        if (cur_delta.days > 0) or (cur_delta.seconds > self.PASTEBIN_LAG_SECONDS):
            return True
        return False

    def insert_pastebin_recent_user_ip(self, user_ip, do_commit = False):

        self.execute_query('INSERT INTO pastebin_recent VALUES (%s,%s,%s)', (
                None,
                user_ip,
                None,
            )
        )
        if do_commit: self.commit()

    def insert_pastebin(self, user_id, user_ip, pastebin_permissions_id, expiration_days, pastebin_syntax_id, pastebin_doctypes_id, content, do_commit = False):

        valid = self.validate_pastebin_user_ip(user_ip)
        if not valid:
            return False,_('You are too fast, try again later')
        if not user_id: user_id = 0
        self.execute_query('INSERT INTO pastebin VALUES (%s,%s,%s,%s,%s,%s,%s,%s)', (
                None,
                user_id,
                pastebin_permissions_id,
                None, # current ts
                expiration_days,
                pastebin_syntax_id,
                pastebin_doctypes_id,
                content,
            )
        )
        if do_commit: self.commit()
        pastebin_id = self.lastrowid()
        self.insert_pastebin_recent_user_ip(user_ip)
        return True, pastebin_id

    def _expand_pastebin(self, item):
        if item.has_key('content'):
            item['content_clean'] = config.htmlencode(item['content'])

    def _check_pastebin_permissions(self, permissions, pastie_user_id, user_id):
        if user_id:
            if self.check_admin(user_id):
                return True
        if permissions == self.PASTEBIN_PERMISSIONS['public']:
            return True
        elif permissions == self.PASTEBIN_PERMISSIONS['registered_users']:
            if user_id: return True
            else: return False
        elif permissions == self.PASTEBIN_PERMISSIONS['user_priv']:
            if pastie_user_id == user_id: return True
            else: return False
        return False

    def _is_pastebin_id_available(self, pastebin_id):

        rows = self.execute_query('SELECT pastebin_id FROM pastebin WHERE pastebin_id = %s', (pastebin_id,))
        if rows: return True
        return False

    def get_pastebin(self, pastebin_id, user_id, check_permissions = True):

        self.execute_query('SELECT SQL_CACHE '+config.PHPBB_DBNAME+'.phpbb_users.username as username, '+config.PORTAL_DBNAME+'.pastebin.* FROM '+config.PORTAL_DBNAME+'.pastebin LEFT JOIN '+config.PHPBB_DBNAME+'.phpbb_users ON '+config.PORTAL_DBNAME+'.pastebin.user_id = '+config.PHPBB_DBNAME+'.phpbb_users.user_id WHERE ('+config.PORTAL_DBNAME+'.pastebin.user_id = '+config.PHPBB_DBNAME+'.phpbb_users.user_id OR '+config.PORTAL_DBNAME+'.pastebin.user_id = 0) AND '+config.PORTAL_DBNAME+'.pastebin.pastebin_id = %s', (pastebin_id,))
        data = self.fetchone()
        if not isinstance(data,dict):
            return 1,{}
        elif check_permissions:
            if not self._check_pastebin_permissions(data.get('permissions'), data.get('user_id'), user_id):
                return 2,{}
        self._expand_pastebin(data)
        return 0,data

    def get_user_id_pastebins(self, user_id, offset = 0, count = 15):

        self.execute_query('SELECT SQL_CACHE '+config.PHPBB_DBNAME+'.phpbb_users.username as username, '+config.PORTAL_DBNAME+'.pastebin.pastebin_id, '+config.PORTAL_DBNAME+'.pastebin.pastebin_doctypes_id FROM '+config.PORTAL_DBNAME+'.pastebin LEFT JOIN '+config.PHPBB_DBNAME+'.phpbb_users ON '+config.PORTAL_DBNAME+'.pastebin.user_id = '+config.PHPBB_DBNAME+'.phpbb_users.user_id WHERE '+config.PORTAL_DBNAME+'.pastebin.user_id = %s AND '+config.PORTAL_DBNAME+'.pastebin.user_id = '+config.PHPBB_DBNAME+'.phpbb_users.user_id ORDER BY '+config.PORTAL_DBNAME+'.pastebin.orig_ts DESC LIMIT %s,%s', (user_id,offset,count,))
        data = self.fetchall()
        mydata = []
        for item in data:
            self._expand_pastebin(item)
            mydata.append(item)
        return mydata

    def get_latest_pastebins(self, count = 10, user_id = None):

        if not isinstance(count,int):
            count = 10 # take this l000sers
        self.execute_query('SELECT SQL_CACHE '+config.PHPBB_DBNAME+'.phpbb_users.username as username, '+config.PORTAL_DBNAME+'.pastebin.pastebin_id, '+config.PORTAL_DBNAME+'.pastebin.pastebin_doctypes_id, '+config.PORTAL_DBNAME+'.pastebin.user_id, '+config.PORTAL_DBNAME+'.pastebin.permissions FROM '+config.PORTAL_DBNAME+'.pastebin LEFT JOIN '+config.PHPBB_DBNAME+'.phpbb_users ON '+config.PORTAL_DBNAME+'.pastebin.user_id = '+config.PHPBB_DBNAME+'.phpbb_users.user_id WHERE (portal.pastebin.user_id = '+config.PHPBB_DBNAME+'.phpbb_users.user_id OR '+config.PORTAL_DBNAME+'.pastebin.user_id = 0) ORDER BY '+config.PORTAL_DBNAME+'.pastebin.orig_ts DESC LIMIT 0,%s',(count,))
        data = self.fetchall()
        mydata = []
        for item in data:
            self._expand_pastebin(item)
            if not self._check_pastebin_permissions(item.get('permissions'), item.get('user_id'), user_id):
                continue
            mydata.append(item)
        return mydata

    def get_expired_pastebins(self):

        self.execute_query('SELECT * FROM pastebin WHERE (DATE_ADD(orig_ts,INTERVAL `expiration_days` DAY) < CURDATE())')
        data = self.fetchall()
        return data

    def delete_pastebin_recent(self):

        self.execute_query('DELETE FROM pastebin_recent')
        self.commit()

    def delete_pastebin(self, pastebin_id, do_commit = False):

        self.execute_query('DELETE FROM pastebin WHERE pastebin_id = %s', (pastebin_id,))
        if do_commit: self.commit()
        return True

    def get_pastebin_syntaxes(self):

        self.execute_query('SELECT * FROM pastebin_syntax')
        data = self.fetchall()
        mydata = {}
        for item in data:
            mydata[item['pastebin_syntax_id']] = item['syntax_name']
        return mydata

    def get_pastebin_permissions(self):

        self.execute_query('SELECT * FROM pastebin_permissions')
        data = self.fetchall()
        mydata = {}
        for item in data:
            mydata[item['pastebin_permissions_id']] = item['permission_name']
        return mydata

    def get_pastebin_doctypes(self):

        self.execute_query('SELECT * FROM pastebin_doctypes')
        data = self.fetchall()
        mydata = {}
        for item in data:
            mydata[item['pastebin_doctypes_id']] = item['doctype_name']
        return mydata
