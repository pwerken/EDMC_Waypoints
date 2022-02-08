import os

from plugin_gui import PluginGui

class Waypoints:

    def __init__(self, plugin_dir):
        self._gui = None
        self._route = []
        self._save_route = os.path.join(plugin_dir, 'save_route.txt')
        self.load(self._save_route)

    def __len__(self):
        return len(self._route)

    def create_ui(self, parent):
        if self._gui is None:
            self._gui = PluginGui(parent, self)
        return self._gui.get_ui()

    def target(self):
        return '' if len(self) == 0 else self._route[0]

    def reached(self, system):
        if len(self) == 0 or system.lower() != self.target().lower():
            return
        del self._route[0]
        self.save()
        self._gui.update_ui()

    def clear(self):
        self._route = []
        self._nearest = None
        if os.path.isfile(self._save_route):
            os.remove(self._save_route)

    def load(self, filename):
        if len(filename) == 0:
            return False
        if not os.path.isfile(filename):
            return False

        try:
            with open(filename, 'r') as f:
                for line in f:
                    clean = line.rstrip(' \r\n').replace('"', '')
                    s = clean.replace('|', ',').split(',')

                    if len(s[0]) == 0 or s[0][0] == '#':
                        continue
                    if s[0] == 'System Name':
                        continue
                    self._route.append(s[0])
            self.save()
        except IOError:
            print("Failed to read file {}".format(filename))
            self._route = []
            return False

        return True

    def save(self):
        try:
            with open(self._save_route, 'w') as f:
                f.write('System Name\n')
                for i in range(0, len(self._route)):
                    f.write(self._route[i])
                    f.write('\n')
        except IOError:
            print("Failed to save current route")
