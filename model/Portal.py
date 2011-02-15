# -*- coding: utf-8 -*-
import os
import config

from pylons.i18n import _

from www.lib.base import convert_to_unicode

import MySQLdb, _mysql_exceptions
from MySQLdb.constants import FIELD_TYPE
from MySQLdb.converters import conversions

class ServiceConnectionError(Exception):
    """Cannot connect to service"""

class RemoteDbSkelInterface:

    def escape_fake(self, mystr):
        return mystr

    def __init__(self):
        self.dbconn = None
        self.cursor = None
        self.plain_cursor = None
        self.escape_string = self.escape_fake
        self.connection_data = {}
        self.mysql = MySQLdb
        self.mysql_exceptions = _mysql_exceptions
        self.FIELD_TYPE = FIELD_TYPE
        self.conversion_dict = conversions.copy()
        self.conversion_dict[self.FIELD_TYPE.DECIMAL] = int
        self.conversion_dict[self.FIELD_TYPE.LONG] = int
        self.conversion_dict[self.FIELD_TYPE.FLOAT] = float
        self.conversion_dict[self.FIELD_TYPE.NEWDECIMAL] = float

    def check_connection(self):
        if self.dbconn is None:
            raise ServiceConnectionError("not connected to service")
        self._check_needed_reconnect()

    def _check_needed_reconnect(self):
        if self.dbconn is None:
            return
        try:
            self.dbconn.ping()
        except self.mysql_exceptions.OperationalError as e:
            if e[0] != 2006:
                raise
            else:
                self.connect()
                return True
        return False

    def _raise_not_implemented_error(self):
        raise NotImplementedError('NotImplementedError: %s' % (
            _('method not implemented'),))

    def set_connection_data(self, data):
        self.connection_data = data.copy()
        if 'converters' not in self.connection_data and self.conversion_dict:
            self.connection_data['converters'] = self.conversion_dict.copy()

    def connect(self):
        kwargs = {}
        keys = [
            ('host', "hostname"),
            ('user', "username"),
            ('passwd', "password"),
            ('db', "dbname"),
            ('port', "port"),
            ('conv', "converters"), # mysql type converter dict
        ]
        for ckey, dkey in keys:
            if dkey not in self.connection_data:
                continue
            kwargs[ckey] = self.connection_data.get(dkey)

        try:
            self.dbconn = self.mysql.connect(**kwargs)
        except self.mysql_exceptions.OperationalError as e:
            raise ServiceConnectionError(repr(e))
        self.plain_cursor = self.dbconn.cursor()
        self.cursor = self.mysql.cursors.DictCursor(self.dbconn)
        self.escape_string = self.dbconn.escape_string
        return True

    def disconnect(self):
        self.check_connection()
        self.escape_string = self.escape_fake
        if hasattr(self.cursor, 'close'):
            self.cursor.close()
        if hasattr(self.dbconn, 'close'):
            self.dbconn.close()
        self.dbconn = None
        self.cursor = None
        self.plain_cursor = None
        self.connection_data.clear()
        return True

    def commit(self):
        self.check_connection()
        return self.dbconn.commit()

    def execute_script(self, myscript):
        pty = None
        for line in myscript.split(";"):
            line = line.strip()
            if not line:
                continue
            pty = self.cursor.execute(line)
        return pty

    def execute_query(self, *args):
        return self.cursor.execute(*args)

    def execute_many(self, query, myiter):
        return self.cursor.executemany(query, myiter)

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchmany(self, *args, **kwargs):
        return self.cursor.fetchmany(*args, **kwargs)

    def lastrowid(self):
        return self.cursor.lastrowid

    def table_exists(self, table):
        self.check_connection()
        self.cursor.execute("show tables like %s", (table,))
        rslt = self.cursor.fetchone()
        if rslt:
            return True
        return False

    def column_in_table_exists(self, table, column):
        t_ex = self.table_exists(table)
        if not t_ex:
            return False
        self.cursor.execute("show columns from "+table)
        data = self.cursor.fetchall()
        for row in data:
            if row['Field'] == column:
                return True
        return False

    def fetchall2set(self, item):
        mycontent = set()
        for x in item:
            mycontent |= set(x)
        return mycontent

    def fetchall2list(self, item):
        content = []
        for x in item:
            content += list(x)
        return content

    def fetchone2list(self, item):
        return list(item)

    def fetchone2set(self, item):
        return set(item)

    def _generate_sql(self, action, table, data, where = ''):
        sql = ''
        keys = sorted(data.keys())
        if action == "update":
            sql += 'UPDATE %s SET ' % (self.escape_string(table),)
            keys_data = []
            for key in keys:
                keys_data.append("%s = '%s'" % (
                        self.escape_string(key),
                        self.escape_string(
                            convert_to_unicode(data[key], 'utf-8').encode('utf-8')).decode('utf-8')
                    )
                )
            sql += ', '.join(keys_data)
            sql += ' WHERE %s' % (where,)
        elif action == "insert":
            sql = 'INSERT INTO %s (%s) VALUES (%s)' % (
                self.escape_string(table),
                ', '.join([self.escape_string(x) for x in keys]),
                ', '.join(["'" + \
                    self.escape_string(
                    convert_to_unicode(data[x], 'utf-8').encode('utf-8')).decode('utf-8') + \
                    "'" for x in keys])
            )
        return sql

class Portal(RemoteDbSkelInterface):

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
        RemoteDbSkelInterface.__init__(self)
        self.set_connection_data(config.portal_connection_data)
        self.connect()
        if do_init:
            self.initialize_tables()
            self.initialize_pastebin_syntaxes()
            self.initialize_pastebin_doctypes()
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

    def insert_pastebin(self, user_ip, expiration_days, pastebin_syntax_id, pastebin_doctypes_id, content, do_commit = False):

        valid = self.validate_pastebin_user_ip(user_ip)
        if not valid:
            return False,_('You are too fast, try again later')
        self.execute_query('INSERT INTO pastebin VALUES (%s,%s,%s,%s,%s,%s,%s,%s)', (
                None,
                0, # user_id
                0, # pastebin_permissions_id
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
        if 'content' in item:
            item['content_clean'] = config.htmlencode(item['content'])

    def _is_pastebin_id_available(self, pastebin_id):
        rows = self.execute_query('SELECT pastebin_id FROM pastebin WHERE pastebin_id = %s', (pastebin_id,))
        if rows: return True
        return False

    def get_pastebin(self, pastebin_id):
        self.execute_query('SELECT SQL_CACHE '+config.PORTAL_DBNAME+'.pastebin.* FROM '+config.PORTAL_DBNAME+'.pastebin WHERE '+config.PORTAL_DBNAME+'.pastebin.user_id = 0 AND '+config.PORTAL_DBNAME+'.pastebin.pastebin_id = %s', (pastebin_id,))
        data = self.fetchone()
        if not isinstance(data,dict):
            return 1, {}
        self._expand_pastebin(data)
        return 0, data

    def get_latest_pastebins(self, count = 10):
        if not isinstance(count, int):
            count = 10 # take this l000sers
        if count > 100:
            count = 1
        self.execute_query("""
        SELECT SQL_CACHE
            %s.pastebin.pastebin_id, %s.pastebin.pastebin_doctypes_id,
            %s.pastebin.orig_ts, %s.pastebin.pastebin_syntax_id,
            %s.pastebin.expiration_days, %s.pastebin_syntax.syntax_name
        FROM %s.pastebin
        LEFT JOIN %s.pastebin_syntax ON ( 
            %s.pastebin.pastebin_syntax_id = %s.pastebin_syntax.pastebin_syntax_id
        )
        WHERE
        %s.pastebin.user_id = 0
        ORDER BY %s.pastebin.orig_ts DESC
        LIMIT %s
        """ % (config.PORTAL_DBNAME, config.PORTAL_DBNAME, config.PORTAL_DBNAME,
        config.PORTAL_DBNAME, config.PORTAL_DBNAME, config.PORTAL_DBNAME, config.PORTAL_DBNAME,
        config.PORTAL_DBNAME, config.PORTAL_DBNAME, config.PORTAL_DBNAME,
        config.PORTAL_DBNAME, config.PORTAL_DBNAME, count))
        # config.PORTAL_DBNAME, count
        data = self.fetchall()
        mydata = []
        for item in data:
            self._expand_pastebin(item)
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
        if do_commit:
            self.commit()
        return True

    def get_pastebin_syntaxes(self):
        self.execute_query('SELECT * FROM pastebin_syntax')
        data = self.fetchall()
        mydata = {}
        for item in data:
            mydata[item['pastebin_syntax_id']] = item['syntax_name']
        return mydata

    def get_pastebin_doctypes(self):
        self.execute_query('SELECT * FROM pastebin_doctypes')
        data = self.fetchall()
        mydata = {}
        for item in data:
            mydata[item['pastebin_doctypes_id']] = item['doctype_name']
        return mydata
