import tkinter as tk
import sys

from tkinter    import filedialog
from subprocess import Popen, PIPE
from config     import config

class WaypointsGUI(tk.Label):
    def __init__(self, parent: tk.Frame, route):
        super().__init__(parent, text='', anchor=tk.W)

        self._parent = parent
        self._route = route

        self._popup = tk.Menu(parent, tearoff=0)
        self._popup.add_command(label='Waypoints', state=tk.DISABLED)
        self._popup.add_command(command=self._popup_cmd)

        self.bind('<Button-1>', self._to_clipboard)
        self.bind('<Button-3>', self._toggle_popup)
        self.update()

    def update(self, copy_to_clipboard: bool = False) -> None:
        waypoints = len(self._route)
        if waypoints == 0:
            self['text'] = 'no waypoints'
            self._popup.entryconfigure(1, label='load route')
        else:
            self['text'] = f'{waypoints} : {self._route.next()}'
            self._popup.entryconfigure(1, label='clear route')

        if copy_to_clipboard:
            self._to_clipboard()

    def _toggle_popup(self, event) -> None:
        if self._popup.winfo_ismapped():
            self._popup.unpost()
        else:
            self._popup.post(event.x_root, event.y_root)

    def _to_clipboard(self, _event = None) -> None:
        if len(self._route) == 0:
            return

        target = self._route.next()
        if sys.platform in ("linux", "linux2"):
            command = Popen(["xclip", "-selection", "c"], stdin=PIPE)
            command.communicate(input=target.encode(), timeout=1)
        else:
            self._parent.clipboard_clear()
            self._parent.clipboard_append(target)
            self._parent.update()

    def _popup_cmd(self, _event = None) -> None:
        if len(self._route) > 0:
            self._route.clear()
            self.update()
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
            self.update()
