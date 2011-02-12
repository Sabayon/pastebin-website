# -*- coding: utf-8 -*-
"""Routes configuration

The more specific and detailed routes should be defined first so they
may take precedent over the more generic routes. For more information
refer to the routes manual at http://routes.groovie.org/docs/
"""
# from pylons import config
from routes import Mapper

def make_map(config):
    """Create, configure and return the routes Mapper"""
    map = Mapper(directory=config['pylons.paths']['controllers'],
                 always_scan=config['debug'])
    map.explicit = False
    map.minimization = True

    # The ErrorController route (handles 404/500 error pages); it should
    # likely stay at the top, ensuring it can always be resolved
    map.connect('/error/{action}/{id}', controller='error')

    # CUSTOM ROUTES HERE

    map.connect('/', controller='pastebin', action='index')
    map.connect('/latest', controller='pastebin', action='latest')
    map.connect('/doc', controller='pastebin', action='doc')
    map.connect('/send', controller='pastebin', action='send')
    map.connect('/pastie/{pastebin_id}', controller='pastebin', action='show_pastie')
    map.connect('/{controller}/{action}/{id}')
    map.connect('/{controller}/{action}')
    map.connect('/{controller}', action='index')
    map.connect('*url', controller='template', action='view')

    return map
