# -*- coding: utf-8 -*-

import subprocess
import sys

try:
	# Python 2
	import Tkinter as tk
	import ttk
	import tkFileDialog as filedialog
except ModuleNotFoundError:
	# Python 3
	import tkinter as tk
	from tkinter import ttk
	from tkinter import filedialog

from config import config
from theme import theme

class PluginGui:

	_route = None

	def __init__(self, parent, route):
		self._route = route

		frame = tk.Frame(parent)
		frame.columnconfigure(2, weight=1)

		self.prev = ttk.Button(frame, width=2)
		self.prev.grid(row=1, column=1, sticky=tk.NSEW)
		self.prev_theme = tk.Label(frame, width=3)
		self.prev_theme.grid(row=1, column=1, sticky=tk.NSEW)
		self.prev['text'] = self.prev_theme['text'] = '<'
		theme.register_alternate((self.prev, self.prev_theme, self.prev_theme), {'row':1,'column':1,'sticky':tk.NSEW})
		self.prev.configure(command=self._prev_wp)
		theme.button_bind(self.prev_theme, self._prev_wp)

		self.target = tk.Label(frame, text='- / -', justify=tk.CENTER)
		self.target.grid(row=1, column=2, sticky=tk.NSEW)
		self.target.bind('<Button-1>', self._to_clipboard)

		self.next = ttk.Button(frame, width=2)
		self.next.grid(row=1, column=3, sticky=tk.NSEW)
		self.next_theme = tk.Label(frame, width=3)
		self.next_theme.grid(row=1, column=3, sticky=tk.NSEW)
		self.next['text'] = self.next_theme['text'] = '>'
		theme.register_alternate((self.next, self.next_theme, self.next_theme), {'row':1,'column':3,'sticky':tk.NSEW})
		self.next.configure(command=self._next_wp)
		theme.button_bind(self.next_theme, self._next_wp)

		self.open = ttk.Button(frame, width=2)
		self.open.grid(row=1, column=4, sticky=tk.NSEW)
		self.open_theme = tk.Label(frame, width=3)
		self.open_theme.grid(row=1, column=4, sticky=tk.NSEW)
		self.open['text'] = self.open_theme['text'] = 'O'
		theme.register_alternate((self.open, self.open_theme, self.open_theme), {'row':1,'column':4,'sticky':tk.NSEW})
		self.open.configure(command=self._load_route)
		theme.button_bind(self.open_theme, self._load_route)

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
		self._to_clipboard()

	def _to_clipboard(self, event=None):
		if len(self._route) == 0:
			return

		target = self._route.target()
		if sys.platform == "linux" or sys.platform == "linux2":
			command = subprocess.Popen(["echo", "-n", target], stdout=subprocess.PIPE)
			subprocess.call(["xclip", "-selection", "c"], stdin=command.stdout)
		else:
			self.parent.clipboard_clear()
			self.parent.clipboard_append(target)
			self.parent.update()

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

