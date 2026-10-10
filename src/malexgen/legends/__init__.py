from .base import BaseLegend, Legend
from .vpn import VPNLegend
from .adblock import AdBlockLegend
from .translator import TranslatorLegend
from .password_manager import PasswordManagerLegend
from .dark_theme import DarkThemeLegend
from .screenshot import ScreenshotLegend
from .notes import NotesLegend
from .coupons import CouponsLegend
from .weather import WeatherLegend
from .pdf_converter import PDFConverterLegend


LEGENDS: dict[str, type[BaseLegend]] = {
    "vpn": VPNLegend,
    "adblock": AdBlockLegend,
    "translator": TranslatorLegend,
    "password_manager": PasswordManagerLegend,
    "dark_theme": DarkThemeLegend,
    "screenshot": ScreenshotLegend,
    "notes": NotesLegend,
    "coupons": CouponsLegend,
    "weather": WeatherLegend,
    "pdf_converter": PDFConverterLegend,
}


def get_legend(legend_id: str) -> BaseLegend:
    if legend_id not in LEGENDS:
        raise ValueError(
            f"Неизвестная легенда: '{legend_id}'. "
            f"Доступные: {', '.join(LEGENDS.keys())}"
        )
    return LEGENDS[legend_id]()


def list_legends() -> list[str]:
    return list(LEGENDS.keys())


__all__ = [
    "BaseLegend",
    "Legend",
    "LEGENDS",
    "get_legend",
    "list_legends",
]
