from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape

from ..utils.logger import logger


class TemplateEngine:

    def __init__(self, templates_dir: Path | str | None = None):
        if templates_dir is None:
            templates_dir = Path(__file__).parent.parent / "templates"
        self.templates_dir = Path(templates_dir)

        if not self.templates_dir.exists():
            raise FileNotFoundError(
                f"Папка шаблонов не найдена: {self.templates_dir}"
            )

        self.env = Environment(
            loader=FileSystemLoader(str(self.templates_dir)),
            autoescape=select_autoescape(
                enabled_extensions=("html", "xml"),
                default_for_string=False,
                default=False,
            ),
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=True,
        )

        logger.debug(f"TemplateEngine initialized: {self.templates_dir}")

    def render(self, template_name: str, **context) -> str:
        try:
            template = self.env.get_template(template_name)
            result = template.render(**context)
            logger.debug(f"Rendered template: {template_name}")
            return result
        except Exception as e:
            logger.error(f"Failed to render {template_name}: {e}")
            raise

    def list_templates(self) -> list[str]:
        return sorted(
            p.name for p in self.templates_dir.iterdir() if p.is_file()
        )


__all__ = ["TemplateEngine"]
