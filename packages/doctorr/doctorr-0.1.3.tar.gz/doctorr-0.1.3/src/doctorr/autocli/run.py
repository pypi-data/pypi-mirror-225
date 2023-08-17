from enum import Enum
from shutil import rmtree

from doctorr.autocli.inspection import get_parser
from doctorr.autocli.parse_argparse import parse_parser
from doctorr.autocli.parse_config import main as read_config
from doctorr.autocli.templates import render_cli
from doctorr.include import run_include
from doctorr.parse_config import parse_include_config
from doctorr.templates import TemplateRenderer
from doctorr.watchmode import main as watchmode


class AutoCliDefault(Enum):
    CONFIG_PATH = "./doctorr.yml"
    THEME = "md_basic"


def run_autocli(config_path, theme, output_dir, watch, **_):
    config = read_config(config_path)
    _run_autocli(config_path, theme, output_dir)
    if watch and config.watch:
        watchmode(lambda: _run_autocli(config_path, theme, output_dir), config)


def _run_autocli(config_path, theme, output_dir):
    config = read_config(config_path)
    parser = get_parser(config)
    renderer = TemplateRenderer(theme)
    text = generate_cli_documentation(parser, renderer)

    output_dir = output_dir or config.output_dir
    assert output_dir, "Please provide through cli or through the yaml"

    rmtree(output_dir, ignore_errors=True)
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / config.output_name).write_text(text)

    include_configs = parse_include_config(config)
    run_include(include_configs)


def generate_cli_documentation(parser, renderer):
    parsed_data = parse_parser(parser)
    markdown_doc = render_cli(parsed_data, renderer)
    return markdown_doc
