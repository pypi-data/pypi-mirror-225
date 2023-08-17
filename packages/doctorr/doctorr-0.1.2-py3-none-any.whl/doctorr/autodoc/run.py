from enum import Enum
from shutil import rmtree

from doctorr.autodoc.docstring import process_page
from doctorr.autodoc.inspection import import_and_inspect
from doctorr.autodoc.parse_config import main as parse_config
from doctorr.autodoc.parse_config import parse_output_dir, parse_page_configs
from doctorr.autodoc.templates import render_page
from doctorr.include import run_include
from doctorr.parse_config import parse_include_config
from doctorr.templates import TemplateRenderer
from doctorr.watchmode import main as watchmode


class AutoDocDefault(Enum):
    CONFIG_PATH = "./doctorr.yml"
    THEME = "md_basic"


def run_autodoc(config_path, theme, output_dir, watch, **_):
    config = parse_config(config_path)
    _run_autodoc(config_path, theme, output_dir, watch)
    if watch and "watch" in config:
        watchmode(lambda: _run_autodoc(config_path, theme, output_dir, watch), config)


def _run_autodoc(config_path, theme, output_dir, watch):
    config = parse_config(config_path)
    page_configs = parse_page_configs(config)
    inspected_pages = [import_and_inspect(page, watch) for page in page_configs]
    processed_pages = [process_page(page) for page in inspected_pages]
    renderer = TemplateRenderer(theme)
    rendered_pages = [render_page(page, renderer) for page in processed_pages]

    output_dir = output_dir or parse_output_dir(config)

    rmtree(output_dir, ignore_errors=True)
    output_dir.mkdir(parents=True, exist_ok=True)
    for page, text in zip(processed_pages, rendered_pages):
        (output_dir / page.output_name).write_text(text)

    include_configs = parse_include_config(config)
    run_include(include_configs)
