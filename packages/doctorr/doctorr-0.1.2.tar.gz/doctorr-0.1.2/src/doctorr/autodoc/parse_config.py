from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Union

from doctorr.parse_config import _parse_yaml, _read_file


@dataclass
class PropertyEntry:
    name: str


@dataclass
class MethodEntry:
    name: str


@dataclass
class FunctionEntry:
    name: str


@dataclass
class ClassEntry:
    name: str
    members: List[Union[MethodEntry, PropertyEntry]]


@dataclass
class PageConfig:
    title: str
    output_name: str
    module_source: str
    content: List[Union[ClassEntry, FunctionEntry]]
    include_module_docstring: Optional[bool] = False


def _create_page_config(cfg: dict) -> PageConfig:
    content_list = []
    for item in cfg.pop("content"):
        if "class" in item:
            class_name = item["class"]
            members = []
            for member in item["members"]:
                if "method" in member:
                    members.append(MethodEntry(name=member["method"]))
                elif "property" in member:
                    members.append(PropertyEntry(name=member["property"]))
            content_list.append(ClassEntry(name=class_name, members=members))
        elif "function" in item:
            content_list.append(FunctionEntry(name=item["function"]))

    return PageConfig(content=content_list, **cfg)


def main(config_path: str) -> List[PageConfig]:
    file_content = _read_file(config_path)
    config = _parse_yaml(file_content)
    return config["autodoc"]


def parse_page_configs(config):
    return [_create_page_config(page_cfg) for page_cfg in config["pages"]]


def parse_watch_config(config):
    return [Path(p) for p in config["watch"]]


def parse_output_dir(config):
    return Path(config["output_dir"])
