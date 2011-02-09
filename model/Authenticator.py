import os
import config
from entropy.const import *
etpConst['entropygid'] = config.DEFAULT_WEB_GID
from entropy.services.auth_interfaces import phpBB3Auth as phpBB3AuthInterface

class Authenticator(phpBB3AuthInterface):

    def __init__(self):
        phpBB3AuthInterface.__init__(self)
        self.set_connection_data(config.phpbb_connection_data)
        self.connect()

    def get_user_id(self, username):
        self.check_connection()
        self.execute_query('SELECT user_id FROM phpbb_users WHERE username_clean = %s OR username = %s', (username,username,))
        data = self.fetchone()
        user_id = None
        if isinstance(data,dict):
            user_id = data.get('user_id')
        return user_id

    def __del__(self):
        if hasattr(self,'disconnect'):
            self.disconnect()