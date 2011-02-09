"""Pylons environment configuration"""
import os

from mako.lookup import TemplateLookup
from pylons.error import handle_mako_error
from pylons import config
import pylons

import www.lib.app_globals as app_globals
import www.lib.helpers
from www.config.routing import make_map
from pylons.configuration import PylonsConfig

def load_environment(global_conf, app_conf):
    """Configure the Pylons environment via the ``pylons.config``
    object
    """
    config = PylonsConfig()
    # Pylons paths
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    paths = dict(root=root,
                 controllers=os.path.join(root, 'controllers'),
                 static_files=os.path.join(root, 'public'),
                 templates=[os.path.join(root, 'templates')])

    # Initialize config with the basic options
    config.init_app(global_conf, app_conf, package='www',
                    template_engine='mako', paths=paths)

    config['routes.map'] = make_map(config)
    config['pylons.app_globals'] = app_globals.Globals(config)
    config['pylons.strict_tmpl_context'] = False
    config['pylons.h'] = www.lib.helpers
    pylons.cache._push_object(config['pylons.app_globals'].cache)

    config['pylons.app_globals'].mako_lookup = TemplateLookup(
        directories=paths['templates'],
        error_handler=handle_mako_error,
        module_directory=os.path.join(app_conf['cache_dir'], 'templates'),
        input_encoding='utf-8', default_filters=['decode.utf8'],
        imports=[])

    # Customize templating options via this variable
    # DEPRECATED
    #tmpl_options = config['buffet.template_options']
    #tmpl_options['mako.input_encoding'] = 'utf-8'
    #tmpl_options['mako.default_filters'] = ['decode.utf8']

    # CONFIGURATION OPTIONS HERE (note: all config options will override
    # any Pylons config options)
    return config
