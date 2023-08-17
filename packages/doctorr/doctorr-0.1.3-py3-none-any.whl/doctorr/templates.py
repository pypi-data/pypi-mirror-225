from pathlib import Path

from jinja2 import Environment, PackageLoader, select_autoescape


class TemplateRenderer:
    def __init__(
        self,
        theme_name,
        *,
        theme_dir=Path("templates/themes"),
        package_name="doctorr",
    ):
        self.env = Environment(
            loader=PackageLoader(
                package_name=package_name, package_path=theme_dir / theme_name
            ),
            autoescape=select_autoescape(
                default_for_string=False,
                default=False,
            ),
            trim_blocks=True,
        )

    def render(self, template_name, context):
        template = self.env.get_template(template_name)
        return template.render(context)
