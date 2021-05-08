# -*- coding: utf-8 -*-

from subprocess import Popen, PIPE
import sys

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

from config import config
from theme import theme

class PluginGui:

    _route = None
    _parent = None

    def __init__(self, parent, route):
        self._route = route
        self._parent = parent

        frame = tk.Frame(parent)

        self.open = ttk.Button(frame, width=2)
        self.open.grid(row=1, column=1, sticky=tk.NSEW)
        self.open_theme = tk.Label(frame, width=3)
        self.open_theme.grid(row=1, column=1, sticky=tk.NSEW)
        self.open['text'] = self.open_theme['text'] = 'O'
        theme.register_alternate((self.open, self.open_theme, self.open_theme), {'row':1,'column':1,'sticky':tk.NSEW})
        self.open.configure(command=self._load_route)
        theme.button_bind(self.open_theme, self._load_route)

        self.prev = ttk.Button(frame, width=2)
        self.prev.grid(row=1, column=2, sticky=tk.NSEW)
        self.prev_theme = tk.Label(frame, width=3)
        self.prev_theme.grid(row=1, column=2, sticky=tk.NSEW)
        self.prev['text'] = self.prev_theme['text'] = '<'
        theme.register_alternate((self.prev, self.prev_theme, self.prev_theme), {'row':1,'column':2,'sticky':tk.NSEW})
        self.prev.configure(command=self._prev_wp)
        theme.button_bind(self.prev_theme, self._prev_wp)

        self.target = tk.Label(frame, text='- / -', justify=tk.CENTER)
        self.target.grid(row=1, column=3, sticky=tk.NSEW)
        self.target.bind('<Button-1>', self._to_clipboard)

        self.next = ttk.Button(frame, width=2)
        self.next.grid(row=1, column=4, sticky=tk.NSEW)
        self.next_theme = tk.Label(frame, width=3)
        self.next_theme.grid(row=1, column=4, sticky=tk.NSEW)
        self.next['text'] = self.next_theme['text'] = '>'
        theme.register_alternate((self.next, self.next_theme, self.next_theme), {'row':1,'column':4,'sticky':tk.NSEW})
        self.next.configure(command=self._next_wp)
        theme.button_bind(self.next_theme, self._next_wp)

        frame.columnconfigure(3, weight=1)
        self.frame = frame
        self.update_UI()

    def update_UI(self):
        note = self._route.note()
        if len(note) == 0:
            note = '{} / {}'.format(self._route.pos(), len(self._route))

        if len(self._route) == 0:
            self.open['text'] = 'O'
            self.target['text'] = 'no waypoints'
        else:
            self.open['text'] = 'X'
            self.target['text'] = self._route.target() + '\n' + note

        self.prev['state']  = 'normal' if self._route.has_prev() else 'disabled'
        self.next['state']  = 'normal' if self._route.has_next() else 'disabled'
        self.open_theme['text'] = self.open['text'];
        self.prev_theme['state'] = self.prev['state'];
        self.next_theme['state'] = self.next['state'];

        self._to_clipboard()

    def _to_clipboard(self, event=None):
        target = self._route.target()
        if len(target) == 0:
            return

        if sys.platform == "linux" or sys.platform == "linux2":
            command = Popen(["xclip", "-selection", "c"], stdin=PIPE)
            command.communicate(input=target.encode(), timeout=1)
        else:
            self._parent.clipboard_clear()
            self._parent.clipboard_append(target)
            self._parent.update()

    def _next_wp(self, event=None):
        if self._route.next():
            self.update_UI()

    def _prev_wp(self, event=None):
        if self._route.prev():
            self.update_UI()

    def _load_route(self, event=None):
        if len(self._route) > 0:
            self._route.clear()
            self.update_UI()
            return

        ftypes = [
            ('All supported files', '*.csv *.txt'),
            ('CSV files', '*.csv'),
            ('Text files', '*.txt'),
        ]
        logdir = config.get('journaldir')
        filename = filedialog.askopenfilename(initialdir=logdir, filetypes=ftypes)
        if self._route.load(filename):
            self.update_UI()

