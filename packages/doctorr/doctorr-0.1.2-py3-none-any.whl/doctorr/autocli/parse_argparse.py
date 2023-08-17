import argparse
import os


def parse_parser(parser, data=None, **kwargs):
    """Enhanced parser function to handle complex argparse structures."""
    if data is None:
        data = {
            "name": "",
            "usage": parser.format_usage().strip(),
            "bare_usage": _format_usage(parser),
            "prog": parser.prog,
        }

    data.setdefault("description", getattr(parser, "description", None))
    data.setdefault("epilog", getattr(parser, "epilog", None))

    arguments = []
    for action in parser._actions:
        if isinstance(action, argparse._SubParsersAction):
            subparsers = []

            for i, (choice, subparser) in enumerate(action.choices.items()):
                subparser_data = parse_parser(subparser)
                subparser_data["name"] = choice
                subparser_data["subcommand_usage"] = _format_usage(subparser)
                subparsers.append(subparser_data)
                subparser_data["description"] = getattr(subparser, "description", None)
                subparser_data["help"] = action._choices_actions[i].help
            data["subcommands"] = subparsers
        else:
            argument_data = {
                "name": action.dest,
                "help": action.help,
                "default": action.default,
                "choices": action.choices,
            }
            arguments.append(argument_data)

    data["arguments"] = arguments
    return data


def _format_usage(parser):
    usage_lines = _get_usage(parser).strip().split("\n")
    indent = len("usage: ")
    usage_lines = [line[indent:] for line in usage_lines]
    return "\n".join(usage_lines)


def _set_terminal_column_width(col_width):
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Store the original COLUMNS value
            original_columns = os.environ.get("COLUMNS")
            # Set a custom terminal width
            os.environ["COLUMNS"] = "80"
            # decorated function call
            ret = func(*args, **kwargs)
            # Restore the original COLUMNS value
            if original_columns:
                os.environ["COLUMNS"] = original_columns
            else:
                os.environ.pop("COLUMNS", None)
            return ret

        return wrapper

    return decorator


@_set_terminal_column_width(80)
def _get_usage(parser):
    return parser.format_usage()  # takes in consideration terminal's width
