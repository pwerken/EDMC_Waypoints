import os

from plugin_gui import PluginGui

class Waypoints:

    _gui = None
    _route = list()
    _save_route = None

    def __init__(self, plugin_dir):
        self._save_route = os.path.join(plugin_dir, 'save_route.txt')
        self.load(self._save_route)

    def __len__(self):
        return len(self._route)

    def clear(self, remove_save=True):
        self._route.clear()
        if remove_save:
            self.save()

    def create_ui(self, parent):
        if self._gui is None:
            self._gui = PluginGui(parent, self)
        return self._gui.get_ui()

    def target(self):
        return '' if len(self) == 0 else self._route[0]

    def reached(self, system):
        if len(self) == 0 or system is None:
            return
        if system.lower() != self.target().lower():
            return
        del self._route[0]
        self.save()
        self._gui.update_ui()

    def load(self, filename):
        if len(filename) == 0 or not os.path.isfile(filename):
            return False

        try:
            self.clear(remove_save=False)
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
            print("Failed to read file {}".format(filename))
            self.clear()
            return False

    def save(self):
        if len(self) == 0:
            if os.path.isfile(self._save_route):
                os.remove(self._save_route)
            return
        try:
            with open(self._save_route, 'w') as f:
                f.write('System Name\n')
                for i in range(0, len(self)):
                    f.write(self._route[i])
                    f.write('\n')
        except IOError:
            print("Failed to save current route")
