import argparse
from pathlib import Path

from doctorr.autocli import AutoCliDefault, run_autocli
from doctorr.autodoc import AutoDocDefault, run_autodoc


def main():
    """CLI entrypoint"""
    args = _parse_command()
    command = TARGET_COMMANDS[args.target]
    return command(args)


def _parse_command():
    args = _get_parser().parse_args()
    return args


def autodoc_command(cli_args):
    run_autodoc(**vars(cli_args))


def autocli_command(cli_args):
    run_autocli(**vars(cli_args))


TARGET_COMMANDS = {"autodoc": autodoc_command, "autocli": autocli_command}


def _get_parser(*subcommands):
    parser = argparse.ArgumentParser(
        description="doctorr - next level autodoc tooling for python pros",
        prog="doctorr",
    )

    targets = parser.add_subparsers(title="targets", dest="target")

    autodoc = targets.add_parser(
        "autodoc", help="Generate documentation from docstrings automatically."
    )

    autodoc.add_argument(
        "-c",
        "--config_path",
        default=AutoDocDefault.CONFIG_PATH.value,
        type=Path,
        help="Path to the yaml config file for generating package documentation.",
    )

    autodoc.add_argument(
        "-t",
        "--theme",
        default=AutoDocDefault.THEME.value,
        help="Name of the default theme to use.",
    )

    autodoc.add_argument(
        "-o",
        "--output_dir",
        required=False,
        type=Path,
        help="Path to desired output directory for the generated files.",
    )

    autodoc.add_argument(
        "-w",
        "--watch",
        action="store_true",
        help="When the the content of the path changes, will rebuild the doc.",
    )

    autocli = targets.add_parser(
        "autocli", help="Generate documentation from cli parser automatically."
    )

    autocli.add_argument(
        "-c",
        "--config_path",
        default=AutoCliDefault.CONFIG_PATH.value,
        type=Path,
        help="Path to the yaml config file for generating CLI documentation.",
    )

    autocli.add_argument(
        "-t",
        "--theme",
        default=AutoCliDefault.THEME.value,
        help="Name of the default theme to use.",
    )

    autocli.add_argument(
        "-o",
        "--output_dir",
        type=Path,
        required=False,
        help="Path to desired output directory for the generated files.",
    )

    autocli.add_argument(
        "-w",
        "--watch",
        action="store_true",
        help="When the the content of the path changes, will rebuild the doc.",
    )

    return parser
