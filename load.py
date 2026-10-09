import tkinter as tk

from typing import Any
from waypoints import Waypoints

type Entry = dict[str, Any]
type State = dict[str, Any]
type PluginGui = tuple[tk.Widget, tk.Widget] | tk.Widget | None

class This:
    """Holds plugin globals."""
    def __init__(self) -> None:
        self.module: Waypoints | None = None

this = This()

def plugin_start3(plugin_dir: str) -> str:
    """
    Start the plugin.

    :param plugin_dir: Name of directory this was loaded from
    :return: Identifier string for this plugin
    """
    this.module = Waypoints(plugin_dir)
    return this.module.load()

def plugin_stop() -> None:
    """Stop this plugin."""
    this.module = None

def plugin_app(parent: tk.Frame) -> PluginGui:
    """Create TK widgets for the EDMarketConnector main window"""
    if this.module is None:
        return None

    return this.module.create_ui(parent)

def journal_entry(
    _cmdr: str,
    _is_beta: bool,
    system: str | None,
    _station: str | None,
    entry: Entry,
    _state: State,
) -> None:
    """
    Handle a new Journal event.

    :param cmdr: Current commander name
    :param is_beta: Is the game currently in beta
    :param system: Current system, if known
    :param station: Current station, if any
    :param entry: The journal event
    :param state: More info about the commander, their ship and their cargo
    """
    if this.module is None:
        return

    this.module.reached(system)

    if entry['event'] == 'NavRoute':
        this.module.star_pos(entry.get('Route', [{}])[0].get('StarPos'))
    else:
        this.module.star_pos(entry.get('StarPos'))
