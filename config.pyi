import pathlib
from typing import Any

# EDMarketConnector/config stub file
# it only contains what this plugin uses

class Config:
    def get_str(self, key: str, default: str = '') -> str: ...

    @property
    def default_journal_dir(self) -> str: ...

appname: str
config: Config
