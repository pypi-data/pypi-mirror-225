def render_cli(parsed_cli, renderer):
    return renderer.render("cli.jinja2", parsed_cli)
