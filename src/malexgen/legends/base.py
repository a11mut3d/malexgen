from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class Legend:

    id: str
    name: str
    description: str
    icon: str
    permissions: list[str] = field(default_factory=list)
    popup_title: str = ""
    popup_description: str = ""
    color_scheme: dict[str, str] = field(default_factory=dict)

    def __post_init__(self):
        if not self.popup_title:
            self.popup_title = self.name
        if not self.color_scheme:
            self.color_scheme = {
                "primary": "#4CAF50",
                "secondary": "#81C784",
                "text": "#FFFFFF",
                "background": "#FFFFFF",
            }


class BaseLegend(ABC):

    @abstractmethod
    def get_legend(self) -> Legend:
        ...

    @abstractmethod
    def get_popup_html(self) -> str:
        ...

    def get_popup_css(self) -> str:
        legend = self.get_legend()
        colors = legend.color_scheme
        return f"""
        body {{
            margin: 0;
            padding: 0;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: {colors.get('background', '#FFFFFF')};
            color: {colors.get('text', '#333333')};
            width: 320px;
            min-height: 200px;
        }}
        .container {{
            padding: 16px;
        }}
        h1 {{
            font-size: 18px;
            margin: 0 0 12px 0;
            color: {colors.get('primary', '#4CAF50')};
        }}
        button {{
            background: {colors.get('primary', '#4CAF50')};
            color: white;
            border: none;
            padding: 10px 16px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
            width: 100%;
        }}
        button:hover {{
            background: {colors.get('secondary', '#81C784')};
        }}
        """


__all__ = ["Legend", "BaseLegend"]
