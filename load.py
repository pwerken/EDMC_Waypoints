import sys

from waypoints import Waypoints

this = sys.modules[__name__]
this.route = None

def plugin_start3(plugin_dir):
    this.route = Waypoints(plugin_dir)
    return 'Waypoints'

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
