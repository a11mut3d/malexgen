

import asyncio
import os
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from .handlers import router
from .middlewares import LoggingMiddleware, RateLimitMiddleware
from ..utils.logger import logger



BOT_CONFIG = {
    "token": None,
    "admin_chat_id": None,
}


def resolve_token(token: str | None = None) -> str:

    if token:
        return token.strip()

    env_token = os.environ.get("MALEXGEN_BOT_TOKEN", "").strip()
    if env_token:
        return env_token

    logger.error(
        "Токен бота не указан.\n\n"
        "Используй один из вариантов:\n"
        "  1. Через аргумент:\n"
        "     malexgen bot --token \"123456:ABC-DEF...\"\n\n"
        "  2. Через переменную окружения:\n"
        "     export MALEXGEN_BOT_TOKEN=\"123456:ABC-DEF...\"\n"
        "     malexgen bot"
    )
    sys.exit(1)


def resolve_chat_id(chat_id: str | None = None) -> str | None:

    if chat_id:
        return str(chat_id).strip()

    env_chat_id = os.environ.get("MALEXGEN_ADMIN_CHAT_ID", "").strip()
    if env_chat_id:
        return env_chat_id

    return None


async def main_async(
    token: str | None = None,
    chat_id: str | None = None,
) -> None:


    bot_token = resolve_token(token)
    admin_chat_id = resolve_chat_id(chat_id)

    BOT_CONFIG["token"] = bot_token
    BOT_CONFIG["admin_chat_id"] = admin_chat_id

    bot = Bot(
        token=bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    dp = Dispatcher(storage=MemoryStorage())

    dp.message.middleware(LoggingMiddleware())
    dp.callback_query.middleware(LoggingMiddleware())
    dp.message.middleware(RateLimitMiddleware(min_interval=0.3))
    dp.callback_query.middleware(RateLimitMiddleware(min_interval=0.3))

    dp.include_router(router)

    try:
        me = await bot.get_me()
        logger.info(f"Bot started: @{me.username} (id={me.id})")

        print()
        print("=" * 60)
        print(f"🤖 Бот запущен: @{me.username}")
        print(f"   ID бота: {me.id}")
        if admin_chat_id:
            print(f"   Admin chat_id: {admin_chat_id}")
        else:
            print("   Admin chat_id: не указан (уведомления не будут приходить)")
            print("   Получить свой chat_id: напиши @userinfobot")
        print()
        print("   Отправьте /start в Telegram")
        print("=" * 60)
        print()

    except Exception as e:
        logger.error(f"Failed to get bot info: {e}")
        print(f"\n❌ Ошибка подключения к Telegram: {e}")
        print("\nПроверьте:")
        print("  • Токен правильный")
        print("  • Есть интернет")
        print("  • Токен не отозван в @BotFather\n")
        sys.exit(1)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        logger.info("Bot stopped")


def main(
    token: str | None = None,
    chat_id: str | None = None,
) -> None:
    try:
        asyncio.run(main_async(token=token, chat_id=chat_id))
    except KeyboardInterrupt:
        print("\n\n👋 Бот остановлен")
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot error: {e}")
        print(f"\n❌ Ошибка: {e}\n")
        sys.exit(1)


def get_bot_config() -> dict:
    return BOT_CONFIG.copy()


if __name__ == "__main__":
    main()


__all__ = ["main", "main_async", "resolve_token", "resolve_chat_id", "get_bot_config", "BOT_CONFIG"]
