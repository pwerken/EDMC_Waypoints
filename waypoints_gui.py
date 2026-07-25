from subprocess import Popen, PIPE
import sys

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

from config import config
from theme import theme

class WaypointsGUI:

    _route = None

    _parent = None
    _label = None
    _popup = None

    def __init__(self, parent, route):
        self._route = route

        self._parent = parent

        self._popup = tk.Menu(parent, tearoff = 0);
        self._popup.add_command(label='Waypoints', state=tk.DISABLED)
        self._popup.add_command(command=self._popup_cmd)

        self._label = tk.Label(parent, text='', anchor=tk.W)
        self._label.bind('<Button-1>', self._to_clipboard)
        self._label.bind('<Button-3>', self._toggle_popup)

        self.update_ui(True)

    def get_ui(self):
        return self._label

    def update_ui(self, copyToClipboard=False):
        waypoints = len(self._route)
        if waypoints == 0:
            self._label['text'] = 'no waypoints'
            self._popup.entryconfigure(1, label='load route')
        else:
            self._label['text'] = f'{waypoints} : {self._route.next()}'
            self._popup.entryconfigure(1, label='clear route')

        if copyToClipboard:
            self._to_clipboard()

    def _toggle_popup(self, event):
        if self._popup.winfo_ismapped():
            self._popup.unpost()
        else:
            self._popup.post(event.x_root, event.y_root)

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

    def _popup_cmd(self, event=None):
        if len(self._route) > 0:
            self._route.clear()
            self.update_ui()
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
        if self._route.readfile(filename):
            self.update_ui()
