# -*- coding: utf-8 -*-

import os

class Waypoints:

	def __init__(self, plugin_dir):
		self._route = []
		self._index = 0

		self._save_route = os.path.join(plugin_dir, 'save_route.txt')
		self._save_index = os.path.join(plugin_dir, 'save_index.txt')

		if self.load(self._save_route):
			self._load_index()

	def clear(self):
		self._route = []
		self._index = 0

		if os.path.isfile(self._save_route):
			os.remove(self._save_route)
		if os.path.isfile(self._save_index):
			os.remove(self._save_index)

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
		self.save()
		return True

	def prev(self):
		if not self.has_prev(): return False
		self._index -= 1
		self.save()
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
			print("Failed to read file {}".format(filename))
			self._route = []
			return False

		return True

	def _load_index(self):
		try:
			with open(self._save_index, 'r') as f:
				self._index = int(f.readline())
		except IOError:
			print("Failed to read saved route index")

	def save(self):
		try:
			with open(self._save_route, 'w') as f:
				f.write('System Name\n')
				for s in self._route:
					f.write(s)
					f.write('\n')

			with open(self._save_index, 'w') as f:
				f.write(str(self._index))
				f.write('\n')
		except IOError:
			print("Failed to save current route")
