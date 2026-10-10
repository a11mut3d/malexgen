from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from ..utils.logger import logger


@dataclass
class SandboxEvent:

    timestamp: datetime
    event_type: str
    source: str
    details: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "timestamp": self.timestamp.isoformat(),
            "event_type": self.event_type,
            "source": self.source,
            "details": self.details,
        }


class Sandbox:

    def __init__(self, ext_dir: Path | str):
        self.ext_dir = Path(ext_dir)
        self.events: list[SandboxEvent] = []
        self.started_at = datetime.now()
        self.ended_at: datetime | None = None

        logger.info(f"Sandbox initialized for: {self.ext_dir}")

    def log_event(
        self,
        event_type: str,
        source: str,
        **details,
    ) -> None:
        event = SandboxEvent(
            timestamp=datetime.now(),
            event_type=event_type,
            source=source,
            details=details,
        )
        self.events.append(event)
        logger.debug(f"[Sandbox] {event_type}: {source}")

    def log_network(self, url: str, method: str = "GET", **kwargs) -> None:
        self.log_event("network", url, method=method, **kwargs)

    def log_storage(self, key: str, action: str = "read", **kwargs) -> None:
        self.log_event("storage", key, action=action, **kwargs)

    def log_cookie(self, name: str, action: str = "read", **kwargs) -> None:
        self.log_event("cookie", name, action=action, **kwargs)

    def log_dom(self, selector: str, action: str = "read", **kwargs) -> None:
        self.log_event("dom", selector, action=action, **kwargs)

    def log_injection(self, target: str, **kwargs) -> None:
        self.log_event("injection", target, **kwargs)

    def stop(self) -> None:
        self.ended_at = datetime.now()
        logger.info(
            f"Sandbox stopped. Events: {len(self.events)}, "
            f"Duration: {self.duration_seconds():.1f}s"
        )

    def duration_seconds(self) -> float:
        end = self.ended_at or datetime.now()
        return (end - self.started_at).total_seconds()

    def summary(self) -> dict:
        by_type: dict[str, int] = {}
        for event in self.events:
            by_type[event.event_type] = by_type.get(event.event_type, 0) + 1

        return {
            "started_at": self.started_at.isoformat(),
            "ended_at": self.ended_at.isoformat() if self.ended_at else None,
            "duration_seconds": self.duration_seconds(),
            "total_events": len(self.events),
            "by_type": by_type,
            "extension": self.ext_dir.name,
        }

    def report(self) -> str:
        summary = self.summary()

        lines = [
            "=" * 60,
            "SANDBOX REPORT",
            "=" * 60,
            f"Extension: {summary['extension']}",
            f"Started:   {summary['started_at']}",
            f"Ended:     {summary['ended_at'] or 'running'}",
            f"Duration:  {summary['duration_seconds']:.1f}s",
            f"Events:    {summary['total_events']}",
            "",
            "By type:",
        ]

        for event_type, count in summary["by_type"].items():
            lines.append(f"  {event_type}: {count}")

        lines.append("")
        lines.append("-" * 60)
        lines.append("EVENTS:")
        lines.append("-" * 60)

        for event in self.events[-50:]:
            lines.append(
                f"[{event.timestamp.strftime('%H:%M:%S')}] "
                f"{event.event_type:12} {event.source}"
            )

        if len(self.events) > 50:
            lines.append(f"... и ещё {len(self.events) - 50} событий")

        lines.append("=" * 60)
        return "\n".join(lines)

    def save_report(self, path: Path | str | None = None) -> Path:
        if path is None:
            path = self.ext_dir / "SANDBOX_REPORT.txt"

        path = Path(path)
        path.write_text(self.report(), encoding="utf-8")
        logger.info(f"Sandbox report saved: {path}")
        return path


__all__ = ["Sandbox", "SandboxEvent"]
