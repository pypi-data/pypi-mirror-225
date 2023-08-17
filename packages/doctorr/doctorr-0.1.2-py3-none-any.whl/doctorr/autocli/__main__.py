if __name__ == "__main__":
    from doctorr.cli import _get_parser

    from .run import generate_cli_documentation

    parser = _get_parser()
    markdown = generate_cli_documentation(parser)
    print(markdown)
