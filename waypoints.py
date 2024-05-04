import logging
import os

from config     import appname
from plugin_gui import PluginGui
from nearest    import Nearest

class Waypoints:

    _gui = None
    _next = None
    _route = list()
    _nearest = Nearest()
    _save_file = None

    def __init__(self, plugin_dir):
        self._logger = logging.getLogger(f'{appname}.Waypoints')
        self._save_file = os.path.join(plugin_dir, 'save_route.txt')
        self.load(self._save_file)

    def __len__(self):
        return len(self._route)

    def clear(self, remove_save=True):
        self._route.clear()
        self._next = None
        self._nearest.clear()
        if remove_save:
            self.save()

    def create_ui(self, parent):
        if self._gui is None:
            self._gui = PluginGui(parent, self)
        return self._gui.get_ui()

    def next(self):
        if self._next is None and len(self) > 0:
            if self._nearest.active():
                self._logger.debug('sorting...')
                self._route.sort(key=self._nearest.cmp)
            self._next = self._route[0]
            self._logger.debug(f'next={self._next}')
        return self._next

    def reached(self, system):
        if system is None or self._next is None:
            return
        if system.casefold() != self._next.casefold():
            return

        self._logger.debug(f'reached {system}')
        del self._route[0]
        self._next = None
        if len(self) == 0:
            self.clear()
        else:
            self._nearest.set_location(self._nearest.del_system(system))
            self.save()
        self._gui.update_ui()

    def star_pos(self, star_pos):
        if not self._nearest.set_location(star_pos):
            return
        if len(self) == 0:
            return
        if self._nearest.at_system(self._route[0]):
            self._nearest.del_system(self._route[0])
            del self.route[0]
        self._next = None
        self.save()
        self._gui.update_ui()

    def load(self, filename):
        if len(filename) == 0 or not os.path.isfile(filename):
            return False
        try:
            self.clear(remove_save=False)
            xyz = False
            self._logger.info(f'load={filename}')
            with open(filename, 'r') as f:
                for line in f:
                    clean = line.rstrip(' \r\n').replace('"', '')
                    s = clean.replace('|', ',').split(',')

                    if len(s[0]) == 0 or s[0][0] == '#':
                        continue
                    if s[0].casefold() == 'system name':
                        xyz = self._nearest.check_header(s)
                        self._logger.info(f'xyz={xyz}')
                        continue
                    self._route.append(s[0])
                    if xyz and not self._nearest.parse_line(s):
                        self._logger.error(f'Failed: {s[0]} has missing xyz')
                        self._nearest.clear()
                        xyz = False
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
                f.write(self._nearest.header_line())
                for i in range(0, len(self)):
                    f.write(self._nearest.system_line(self._route[i]))
        except IOError:
            self._logger.error("Failed to save current route")
