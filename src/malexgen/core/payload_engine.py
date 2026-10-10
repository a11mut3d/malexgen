from ..payloads import PAYLOADS, get_payload, list_payloads
from ..payloads.base import BasePayload, Payload
from ..utils.logger import logger


class PayloadEngine:

    def __init__(self):
        self._payloads = PAYLOADS

    def get(self, payload_id: str) -> BasePayload:
        payload = get_payload(payload_id)
        logger.debug(f"Payload loaded: {payload_id}")
        return payload

    def get_data(self, payload_id: str) -> Payload:
        return self.get(payload_id).get_payload()

    def list_ids(self) -> list[str]:
        return list_payloads()

    def list_all(self) -> list[Payload]:
        return [self.get_data(pid) for pid in self.list_ids()]

    def exists(self, payload_id: str) -> bool:
        return payload_id in self._payloads

    def count(self) -> int:
        return len(self._payloads)

    def by_risk(self, risk_level: str) -> list[Payload]:
        return [
            p for p in self.list_all()
            if p.risk_level == risk_level
        ]


__all__ = ["PayloadEngine"]
