import shutil

from doctorr.parse_config import IncludeConfig


def run_include(include_configs: list[IncludeConfig]):
    for config in include_configs:
        # Ensure the destination directory exists
        config.destination.parent.mkdir(parents=True, exist_ok=True)

        # Check if it's a file or directory
        if config.original.is_file():
            shutil.copy2(config.original, config.destination)
        elif config.original.is_dir():
            shutil.copytree(config.original, config.destination)
