from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class Payload:

    id: str
    name: str
    description: str
    icon: str
    risk_level: str = "medium"  # low, medium, high, critical
    permissions: list[str] = field(default_factory=list)
    targets: list[str] = field(default_factory=list)
    demo_instructions: str = ""
    mitigation: list[str] = field(default_factory=list)

    def risk_emoji(self) -> str:
        return {
            "low": "🟢",
            "medium": "🟡",
            "high": "🟠",
            "critical": "🔴",
        }.get(self.risk_level, "⚪")

    def risk_color(self) -> str:
        return {
            "low": "green",
            "medium": "yellow",
            "high": "red",
            "critical": "bold red",
        }.get(self.risk_level, "white")


class BasePayload(ABC):
    @abstractmethod
    def get_payload(self) -> Payload:
        ...

    @abstractmethod
    def get_background_js(self) -> str:
        ...

    @abstractmethod
    def get_content_js(self) -> str:
        ...

    def get_popup_js(self) -> str:
        return "// Demo popup — no real logic\nconsole.log('[DEMO] Popup loaded');"


__all__ = ["Payload", "BasePayload"]
