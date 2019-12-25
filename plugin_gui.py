# -*- coding: utf-8 -*-

import subprocess
import sys

try:
	# Python 2
	import Tkinter as tk
#	import ttk
	import tkFileDialog as filedialog
except ModuleNotFoundError:
	# Python 3
	import tkinter as tk
#	from tkinter import ttk
	import tkFileDialog as filedialog


class PluginGui:

	_route = None

	def __init__(self, parent, route):
		self._route = route

		tk.Frame(parent, highlightthickness=1).grid(columnspan=2, sticky=tk.EW)
		row = parent.grid_size()[1]
		wp_label = tk.Label(parent)
		wp_label.grid(row=row, column=0, sticky=tk.W)
		wp_label['text'] = 'Next' + ':'

		self.target = tk.Label(parent, compound=tk.RIGHT, anchor=tk.W)
		self.target.grid(row=row, column=1, sticky=tk.EW)
		self.target['text'] = ''
		self.target.bind('<Button-1>', self._to_clipboard)

		frame = tk.Frame(parent)
		frame.grid(columnspan=2, sticky=tk.NSEW)
		frame.columnconfigure(2, weight=1)

		self.prev   = tk.Button(frame, text=[u'\u2190'], command=self._prev_wp)
		self.status	= tk.Label(frame, text='- / -', justify=tk.CENTER)
		self.next   = tk.Button(frame, text=[u'\u2192'], command=self._next_wp)
#		self.ff     = tk.Button(frame, text=[u'\u21A0'], command=skip_forward)
		self.clear  = tk.Button(frame, text='X', command=self._clear_route)
		self.open   = tk.Button(frame, text='O', command=self._load_route)

		self.prev.grid(row=1, column=1, sticky=tk.W)
		self.status.grid(row=1, column=2, sticky=tk.NSEW)
		self.next.grid(row=1, column=3, sticky=tk.E)
#		self.ff.grid(row=1, column=4, sticky=tk.E)
		self.clear.grid(row=1, column=5, sticky=tk.E)
		self.open.grid(row=1, column=6, sticky=tk.E)

		self.update_UI()

	def update_UI(self):
		self.target['text'] = self._route.target()
		self.prev['state']  = 'normal' if self._route.has_prev() else 'disabled'
		self.status['text'] = '{} / {}'.format(self._route.pos(), self._route.len())
		self.next['state']  = 'normal' if self._route.has_next() else 'disabled'
#		self.ff['state']    = 'normal' if False else 'disabled'
		self.clear['state'] = 'normal' if self._route.len() > 0 else 'disabled'
		self._to_clipboard()

	def _to_clipboard(self, event = None):
		if self._route.len() == 0:
			return

		target = self._route.target()
		if sys.platform == "linux" or sys.platform == "linux2":
			command = subprocess.Popen(["echo", "-n", target], stdout=subprocess.PIPE)
			subprocess.call(["xclip", "-selection", "c"], stdin=command.stdout)
		else:
			self.parent.clipboard_clear()
			self.parent.clipboard_append(target)
			self.parent.update()

	def _next_wp(self):
		if self._route.next():
			self.update_UI()

	def _prev_wp(self):
		if self._route.prev():
			self.update_UI()

#	def skip_forward():
#		sys.stderr.write("skipForward\n")

	def _load_route(self):
		ftypes = [
			('All supported files', '*.csv *.txt'),
			('CSV files', '*.csv'),
			('Text files', '*.txt'),
		]
		filename = filedialog.askopenfilename(filetypes = ftypes)
		if self._route.load(filename):
			self.update_UI()

	def _clear_route(self):
		self._route.clear()
		self.update_UI()

