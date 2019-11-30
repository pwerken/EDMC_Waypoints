# -*- coding: utf-8 -*-

import os


class Waypoints:

	def __init__(self, plugin_dir):
		self._route = []
		self._index = 0

		self._save_route = os.path.join(plugin_dir, 'save_route.txt')
		self._save_index = os.path.join(plugin_dir, 'save_index.txt')

	def clear(self):
		self._route = []
		self._index = 0

	def len(self):
		return self._route.__len__()

	def pos(self):
		return 0 if self.len() == 0 else self._index + 1

	def target(self):
		return '' if self.len() == 0 else self._route[self._index]

	def has_next(self):
		return self._index + 1 < self.len()

	def has_prev(self):
		return self._index > 0

	def next(self):
		if not self.has_next(): return False
		self._index += 1
		return True

	def prev(self):
		if not self.has_prev(): return False
		self._index -= 1
		return True

	def reached(self, system):
		if system.lower() != self.target().lower(): return False
		self.next()
		return True

	def load(self, filename):
		if filename.__len__() == 0: return False
		if not os.path.isfile(filename): return False

		self._route = []
		self._index = 0
		try:
			with open(filename, 'r') as f:
				for line in f:
					s = line.rstrip(' \r\n').replace('|',',').split(',')[0]
					if s == 'System Name':
						continue

					self._route.append(s)
		except IOError:
			print "Failed to read file {}".format(filename)
			self._route = []
			return False

		return True

