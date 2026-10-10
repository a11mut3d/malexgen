from ..legends import LEGENDS
from ..payloads import PAYLOADS


def validate_legend_id(legend_id: str) -> bool:
    if not legend_id:
        raise ValueError("legend_id не может быть пустым")
    if legend_id not in LEGENDS:
        raise ValueError(
            f"Неизвестная легенда: '{legend_id}'. "
            f"Доступные: {', '.join(LEGENDS.keys())}"
        )
    return True


def validate_payload_id(payload_id: str) -> bool:
    if not payload_id:
        raise ValueError("payload_id не может быть пустым")
    if payload_id not in PAYLOADS:
        raise ValueError(
            f"Неизвестный payload: '{payload_id}'. "
            f"Доступные: {', '.join(PAYLOADS.keys())}"
        )
    return True


def validate_output_name(name: str) -> bool:

    if not name:
        return True
    if len(name) > 100:
        raise ValueError("Имя не должно превышать 100 символов")
    forbidden = set('<>:"/\\|?*')
    if any(c in forbidden for c in name):
        raise ValueError(f"Имя содержит запрещённые символы: {forbidden}")
    return True


__all__ = [
    "validate_legend_id",
    "validate_payload_id",
    "validate_output_name",
]
