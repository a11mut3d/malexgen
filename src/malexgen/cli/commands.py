from rich.panel import Panel
from rich.prompt import Prompt, Confirm

from .ui import (
    console,
    print_banner,
    print_disclaimer,
    print_info,
    print_error,
)


def cmd_bot(token: str | None = None, chat_id: str | None = None) -> None:
    print_banner()
    console.print()

    if not token:
        console.print(Panel.fit(
            "🤖 <b>Настройка Telegram-бота</b>\n\n"
            "Для запуска нужен токен бота.\n"
            "Получите его у @BotFather в Telegram.\n\n"
            "Также нужен ваш chat_id для получения уведомлений.\n"
            "Узнать: напишите @userinfobot",
            title="Telegram Bot",
            border_style="cyan",
        ))
        console.print()

        token = Prompt.ask(
            "[bold cyan]Токен бота[/bold cyan]",
            password=True,
        ).strip()

        if not token:
            print_error("Токен обязателен.")
            return

    if not chat_id:
        chat_id = Prompt.ask(
            "[bold cyan]Ваш chat_id[/bold cyan] "
            "[dim](для уведомлений, можно пропустить)[/dim]",
            default="",
        ).strip()

    console.print()
    print_disclaimer()
    console.print()

    if not Confirm.ask("[bold]Запустить бота?[/bold]", default=True):
        print_info("Отменено.")
        return

    import os
    os.environ["MALEXGEN_BOT_TOKEN"] = token
    if chat_id:
        os.environ["MALEXGEN_ADMIN_CHAT_ID"] = chat_id

    try:
        from ..telegram.bot import main as bot_main
        print_info("Запуск Telegram-бота...")
        console.print()
        bot_main(token=token, chat_id=chat_id)
    except ImportError as e:
        print_error(f"Не удалось импортировать Telegram-бота: {e}")
        print_info("Убедитесь, что aiogram установлен: pip install aiogram")
    except Exception as e:
        print_error(f"Ошибка запуска бота: {e}")


__all__ = ["cmd_bot"]
