import os

from plugin_gui import PluginGui

class Waypoints:

    _gui = None
    _next = None
    _route = list()
    _save_file = None

    def __init__(self, plugin_dir, logger):
        self._logger = logger
        self._save_file = os.path.join(plugin_dir, 'save_route.txt')
        self.load(self._save_file)
        self._logger.debug('started')

    def __len__(self):
        return len(self._route)

    def clear(self, remove_save=True):
        self._route.clear()
        self._next = None
        if remove_save:
            self.save()

    def create_ui(self, parent):
        if self._gui is None:
            self._gui = PluginGui(parent, self)
        self._logger.debug('create_ui')
        return self._gui.get_ui()

    def next(self):
        if self._next is None and len(self) > 0:
            self._next = self._route[0]
        return self._next

    def reached(self, system):
        if system is None or self._next is None:
            return
        if system.casefold() != self._next.casefold():
            return

        self._logger.debug(f'reached {system}')
        del self._route[0]
        self._next = None

        self.save()
        self._gui.update_ui()

    def load(self, filename):
        if len(filename) == 0 or not os.path.isfile(filename):
            return False

        try:
            self.clear(remove_save=False)
            self._logger.info(f'load={filename}')
            with open(filename, 'r') as f:
                for line in f:
                    clean = line.rstrip(' \r\n').replace('"', '')
                    s = clean.replace('|', ',').split(',')

                    if len(s[0]) == 0 or s[0][0] == '#':
                        continue
                    if s[0].lower() == 'system name':
                        continue
                    self._route.append(s[0])
            self.save()
            return True
        except IOError:
            self.clear()
            return False

    def save(self):
        try:
            if len(self) == 0:
                if os.path.isfile(self._save_file):
                    os.remove(self._save_file)
                    self._logger.debug(f'deleted')
                return
            self._logger.debug(f'save')
            with open(self._save_file, 'w') as f:
                f.write('System Name\n')
                for i in range(0, len(self)):
                    f.write(self._route[i])
                    f.write('\n')
        except IOError:
            self._logger.error("Failed to save current route")
