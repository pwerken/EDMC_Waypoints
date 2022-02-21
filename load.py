import sys
import os
import logging

from config import appname
from waypoints import Waypoints

this = sys.modules[__name__]
this.route = None

def plugin_start3(plugin_dir):
    plugin_name = os.path.basename(os.path.dirname(__file__))
    logger = logging.getLogger(f'{appname}.{plugin_name}')
    this.route = Waypoints(plugin_dir, logger)
    return plugin_name

def plugin_start(plugin_dir):
    return plugin_start3(plugin_dir)

def plugin_app(parent):
    return this.route.create_ui(parent)

def journal_entry(cmdr, is_beta, system, station, entry, state):
    this.route.reached(system)

    if entry['event'] == 'NavRoute':
        this.route.star_pos(entry.get('Route')[0].get('StarPos'))
    else:
        this.route.star_pos(entry.get('StarPos'))
