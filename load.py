# -*- coding: utf-8 -*-

import sys

from waypoints import Waypoints
from plugin_gui import PluginGui


this = sys.modules[__name__]
this.gui = None
this.route = None


def plugin_start3(plugin_dir):
    """
    Load the plugin.
    :param plugin_dir: directory that contains the main .py file
    """
    this.route = Waypoints(plugin_dir)
    return "Waypoints"


def plugin_start(plugin_dir):
    """
    Legacy (python 2.7) method for loading the plugin.
    :param plugin_dir: directory that contains the main .py file
    """
    return plugin_start3(plugin_dir)


def plugin_app(parent):
    """
    Create mainwindow content and return it.
    :param parent: the parent frame for this entry.
    :returns: a tk Widget
    """
    this.gui = PluginGui(parent, this.route)
    return this.gui.frame


def journal_entry(cmdr, is_beta, system, station, entry, state):
    """
    Receive a journal entry.
    :param cmdr: The Cmdr name, or None if not yet known
    :param is_beta: whether the player is in a Beta universe.
    :param system: The current system, or None if not yet known
    :param station: The current station, or None if not docked or not yet known
    :param entry: The journal entry as a dictionary
    :param state: A dictionary containing info about the Cmdr, current ship and cargo
    """
    if (entry['event'] in ['StartUp', 'Location', 'Docked',
                           'CarrierJump', 'FSDJump',
                           'SupercruiseEntry', 'SupercruiseExit']):
        s = entry["StarSystem"]
    elif entry['event'] == 'FSSDiscoveryScan':
        s = entry['SystemName']
    else:
        return

    if this.route.reached(s):
        this.gui.update_UI()
