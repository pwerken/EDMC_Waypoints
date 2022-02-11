import sys
import logging

from config import appname
from waypoints import Waypoints

this = sys.modules[__name__]
this.route = None

def plugin_start3(plugin_dir):
    plugin_name = 'Waypoints'
    logger = logging.getLogger(f'{appname}.{plugin_name}')
    this.route = Waypoints(plugin_dir, logger)
    return plugin_name

def plugin_start(plugin_dir):
    return plugin_start3(plugin_dir)

def plugin_app(parent):
    return this.route.create_ui(parent)

def journal_entry(cmdr, is_beta, system, station, entry, state):
    this.route.reached(system)
