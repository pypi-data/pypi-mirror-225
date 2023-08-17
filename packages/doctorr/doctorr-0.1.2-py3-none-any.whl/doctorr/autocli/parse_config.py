from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

from doctorr.include import IncludeConfig
from doctorr.parse_config import _parse_yaml, _read_file


@dataclass
class CLIConfig:
    module_source: str
    getter: str
    prog: str
    output_name: str
    output_dir: Optional[Path] = None
    watch: List[str] = field(default_factory=list)
    include: List[IncludeConfig] = field(default_factory=list)

    def __post_init__(self):
        self.output_dir = self.output_dir and Path(self.output_dir)


def main(config_path):
    file_content = _read_file(config_path)
    full_config = _parse_yaml(file_content)
    autocli_config = full_config["autocli"]
    return CLIConfig(**autocli_config)
