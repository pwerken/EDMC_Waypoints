type Pos = list[float]
type MaybePos = Pos | None

class Nearest:

    _current: MaybePos = None
    _locations: dict[str, Pos] = {}
    _header: list[str] = ['system name', 'x', 'y', 'z']

    def active(self) -> bool:
        if self._current is None:
            return False
        return len(self._locations) > 0

    def set_location(self, xyz: MaybePos) -> bool:
        if xyz is None or self.distance_2(xyz) < 0.1:
            return False
        self._current = xyz
        return True

    def clear(self) -> None:
        self._locations.clear()

    def at_system(self, system: str) -> bool:
        xyz = self.get_system(system)
        return self.distance_2(xyz) < 0.1

    def del_system(self, system: str) -> MaybePos:
        return self._locations.pop(system, None)

    def get_system(self, system: str) -> MaybePos:
        return self._locations.get(system, None)

    def cmp(self, system: str) -> float:
        return self.distance_2(self.get_system(system))

    def distance_2(self, xyz: MaybePos) -> float:
        if self._current is None or xyz is None:
            return 100000**2
        d = 0.0
        for i in range(0, 3):
            d += (self._current[i] - xyz[i])**2
        return d

    def check_header(self, splits: list[str]) -> bool:
        if len(splits) < 4:
            return False
        for i in range(0, 4):
            if splits[i].casefold() != self._header[i]:
                return False
        return True

    def parse_line(self, splits: list[str]) -> bool:
        if len(splits) < 4:
            self.clear()
            return False

        self._locations[splits[0]] = []
        for i in range(0, 3):
            self._locations[splits[0]].append(float(splits[i + 1]))
        return True

    def header_line(self) -> str:
        if len(self._locations) == 0:
            return self._header[0] + '\n'
        return ','.join(self._header) + '\n'

    def system_line(self, system: str) -> str:
        if system not in self._locations:
            return f'{system}\n'
        xyz = self._locations[system]
        return f'{system},{xyz[0]},{xyz[1]},{xyz[2]}\n'
