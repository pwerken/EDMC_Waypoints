from subprocess import Popen, PIPE
import sys

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

from config import config
from theme import theme

class PluginGui:

    _route = None
    _button = None
    _target = None

    def __init__(self, parent, route):
        self._route = route

        self._button = tk.Frame(parent)
        g = {'row': 1, 'column': 1, 'sticky': tk.NSEW}
        self._button_open = ttk.Button(self._button)
        self._button_open.grid(g)
        self._button_open.configure(command=self._load_route)
        self._button_open.bind('<Double-Button-1>', self._clear_route)

        self._button_theme = tk.Label(self._button)
        self._button_theme.bind('<Double-Button-1>', self._clear_route)
        theme.register_alternate((self._button_open, self._button_theme), g)
        theme.button_bind(self._button_theme, self._load_route)

        self._target = tk.Label(parent, text='', anchor=tk.W)
        self._target.bind('<Button-1>', self._to_clipboard)

        self.update_ui()

    def get_ui(self):
        return (self._button, self._target)

    def update_ui(self):
        waypoints = len(self._route)
        if waypoints == 0:
            self._button_open['text'] = '  Open  '
            self._target['text'] = 'no waypoints'
        else:
            self._button_open['text'] = f'{waypoints}'
            self._target['text'] = self._route.next()
        self._button_theme['text'] = self._button_open['text']
        self._to_clipboard()

    def _to_clipboard(self, event=None):
        if len(self._route) == 0:
            return

        target = self._route.next()
        if sys.platform == "linux" or sys.platform == "linux2":
            command = Popen(["xclip", "-selection", "c"], stdin=PIPE)
            command.communicate(input=target.encode(), timeout=1)
        else:
            self._parent.clipboard_clear()
            self._parent.clipboard_append(target)
            self._parent.update()

    def _clear_route(self, event=None):
        self._route.clear()
        self.update_ui()

    def _load_route(self, event=None):
        if len(self._route) > 0:
            return

        ftypes = [
            ('All supported files', '*.csv *.txt'),
            ('CSV files', '*.csv'),
            ('Text files', '*.txt'),
        ]
        logdir = config.get_str('journaldir',
                                default=config.default_journal_dir)
        filename = filedialog.askopenfilename(initialdir=logdir,
                                              filetypes=ftypes)
        if self._route.load(filename):
            self.update_ui()
