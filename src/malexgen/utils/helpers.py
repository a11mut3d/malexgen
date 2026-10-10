import re
import yaml
from datetime import datetime
from pathlib import Path
from typing import Any


def ensure_dir(path: Path | str) -> Path:
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def safe_filename(name: str) -> str:
    name = re.sub(r"[^\w\s-]", "", name)
    name = re.sub(r"[-\s]+", "_", name)
    return name.strip("_").lower()


def format_timestamp(dt: datetime | None = None) -> str:
    if dt is None:
        dt = datetime.now()
    return dt.strftime("%Y%m%d_%H%M%S")


def read_yaml(path: Path | str) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def write_yaml(path: Path | str, data: dict[str, Any]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False)


def truncate(text: str, max_len: int = 50) -> str:
    if len(text) <= max_len:
        return text
    return text[: max_len - 3] + "..."


__all__ = [
    "ensure_dir",
    "safe_filename",
    "format_timestamp",
    "read_yaml",
    "write_yaml",
    "truncate",
]
