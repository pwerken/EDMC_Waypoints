# -*- coding: utf-8 -*-

import sys

from waypoints import Waypoints
from plugin_gui import PluginGui


this = sys.modules[__name__]
this.gui   = None
this.route = None

def plugin_start(plugin_dir):
	this.route = Waypoints(plugin_dir)

def plugin_app(parent):
	this.gui = PluginGui(parent, this.route)

def journal_entry(cmdr, is_beta, system, station, entry, state):
	if (entry['event'] in ['StartUp', 'FSDJump', 'Location', 'SupercruiseEntry', 'SupercruiseExit']):
		s = entry["StarSystem"]
	elif entry['event'] == 'FSSDiscoveryScan':
		s = entry['SystemName']
	else:
		return

	if this.route.reached(s):
		this.gui.update_UI()
