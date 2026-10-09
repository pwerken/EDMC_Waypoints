import logging
import os

from config        import appname
from waypoints_gui import WaypointsGUI
from nearest       import Nearest

class Waypoints:

    _gui = None
    _here_position = None
    _here_system = None
    _nearest = Nearest()
    _next: str | None = None
    _route: list[str] = []
    _save_file: str

    def __init__(self, plugin_dir: str) -> None:
        self._logger = logging.getLogger(f'{appname}.Waypoints')
        self._save_file = os.path.join(plugin_dir, 'save_route.txt')
        self.readfile(self._save_file)

    def load(self) -> str:
        return self.__class__.__name__

    def __len__(self) -> int:
        return len(self._route)

    def clear(self, remove_save: bool = True) -> None:
        self._route.clear()
        self._next = None
        self._nearest.clear()
        if remove_save:
            self.save()

    def create_ui(self, parent) -> WaypointsGUI:
        if not self._gui:
            self._gui = WaypointsGUI(parent, self)
        return self._gui

    def next(self) -> str | None:
        if self._next is None and len(self) > 0:
            if self._nearest.active():
                self._logger.debug('sorting...')
                self._route.sort(key=self._nearest.cmp)
            self._next = self._route[0]
            self._logger.debug('next=%s', self._next)
        return self._next

    def reached(self, system: str | None) -> None:
        self._here_system = system
        if system is None or self._next is None:
            return
        if system.casefold() != self._next.casefold():
            return

        self._logger.debug('reached %s', system)
        del self._route[0]
        self._next = None
        if len(self) == 0:
            self.clear()
        else:
            self._nearest.set_location(self._nearest.del_system(system))
            self.save()
        if self._gui:
            self._gui.update(True)

    def star_pos(self, star_pos) -> None:
        self._here_position = star_pos
        if len(self) == 0:
            return
        if not self._nearest.set_location(star_pos):
            return
        if self._nearest.at_system(self._route[0]):
            self.reached(self._route[0])

    def readfile(self, filename: str) -> bool:
        if len(filename) == 0 or not os.path.isfile(filename):
            return False
        try:
            self.clear(remove_save=False)
            xyz = False
            self._logger.info('readfile=%s', filename)
            with open(filename, 'r', encoding='utf8') as f:
                for line in f:
                    clean = line.rstrip(' \r\n').replace('"', '')
                    s = clean.replace('|', ',').split(',')

                    if len(s[0]) == 0 or s[0][0] == '#':
                        continue
                    if s[0].casefold() == 'system name':
                        xyz = self._nearest.check_header(s)
                        self._logger.info('xyz=%s', xyz)
                        continue
                    self._route.append(s[0])
                    if xyz and not self._nearest.parse_line(s):
                        self._logger.error('Failed: %s has missing xyz', s[0])
                        self._nearest.clear()
                        xyz = False
            self.save()
            return True
        except IOError:
            self.clear()
            return False

    def save(self) -> None:
        try:
            if len(self) == 0:
                if os.path.isfile(self._save_file):
                    os.remove(self._save_file)
                    self._logger.debug('deleted')
                return

            self._logger.debug('save')
            self.reached(self._here_system)
            self.star_pos(self._here_position)
            with open(self._save_file, 'w', encoding='utf8') as f:
                f.write(self._nearest.header_line())
                for i in range(0, len(self)):
                    f.write(self._nearest.system_line(self._route[i]))
        except IOError:
            self._logger.error('Failed to save current route')
