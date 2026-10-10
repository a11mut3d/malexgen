import click

from .. import __version__
from .commands import cmd_bot


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(version=__version__, prog_name="malexgen")
def cli() -> None:
    pass


@cli.command("bot")
@click.option(
    "--token", "-t",
    help="Токен Telegram-бота (от @BotFather)",
)
@click.option(
    "--chat-id", "-c",
    "chat_id",
    help="Ваш chat_id (для уведомлений, узнать у @userinfobot)",
)
def bot_cmd(token: str | None, chat_id: str | None) -> None:
    cmd_bot(token=token, chat_id=chat_id)


if __name__ == "__main__":
    cli()
