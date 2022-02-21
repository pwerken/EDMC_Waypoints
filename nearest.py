class Nearest:

    _current = None
    _locations = dict()
    _header = ['system name', 'x', 'y', 'z']

    def active(self):
        if self._current is None:
            return False
        return len(self._locations) > 0

    def set_location(self, xyz):
        if xyz is None or self.distance_2(xyz) < 0.1:
            return False
        self._current = xyz
        return True

    def clear(self):
        self._locations.clear()

    def at_system(self, system):
        xyz = self.get_system(system)
        return self.distance_2(xyz) < 0.1

    def del_system(self, system):
        return self._locations.pop(system, None)

    def get_system(self, system):
        return self._locations.get(system, None)

    def cmp(self, system):
        return self.distance_2(self.get_system(system))

    def distance_2(self, xyz):
        if self._current is None or xyz is None:
            return 100000**2
        d = 0
        for i in range(0, 3):
            d += (self._current[i] - xyz[i])**2
        return d

    def check_header(self, splits):
        if len(splits) < 4:
            return False
        for i in range(0, 4):
            if splits[i].casefold() != self._header[i]:
                return False
        return True

    def parse_line(self, splits):
        if len(splits) < 4:
            self.clear()
            return False

        self._locations[splits[0]] = []
        for i in range(0, 3):
            self._locations[splits[0]].append(float(splits[i + 1]))
        return True

    def header_line(self):
        if len(self._locations) == 0:
            return self._header[0] + '\n'
        return ','.join(self._header) + '\n'

    def system_line(self, system):
        if system not in self._locations:
            return f'{system}\n'
        xyz = self._locations[system]
        return f'{system},{xyz[0]},{xyz[1]},{xyz[2]}\n'
