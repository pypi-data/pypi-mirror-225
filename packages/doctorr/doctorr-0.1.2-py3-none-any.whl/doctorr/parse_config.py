from dataclasses import dataclass
from pathlib import Path

import yaml

from doctorr.utils import _get


def _read_file(path) -> str:
    return Path(path).read_text()


def _parse_yaml(text) -> str:
    return yaml.load(text, Loader=yaml.FullLoader)


@dataclass
class IncludeConfig:
    original: Path
    destination: Path

    def __post_init__(self):
        self.original = Path(self.original)
        self.destination = Path(self.destination)


def parse_include_config(config):
    return [IncludeConfig(**c) for c in _get("include", config, [])]


# todo: watch parsing should probably be there too.
