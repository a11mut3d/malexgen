from rich.console import Console
from rich.panel import Panel
from rich.text import Text


console = Console()


DISCLAIMER_TEXT = (
    "Этот инструмент создаёт [bold]ДЕМОНСТРАЦИОННЫЕ[/bold] расширения\n"
    "для обучения безопасности.\n\n"
    "[bold yellow]ВНИМАНИЕ:[/bold yellow] Если C2 включён (указан токен бота),\n"
    "сгенерированные расширения [bold]ОТПРАВЛЯЮТ данные[/bold]\n"
    "(куки, формы, сессии) [bold]в Telegram-бота[/bold].\n\n"
    "[yellow]Используйте только:[/yellow]\n"
    "[yellow]  • на СВОИХ системах[/yellow]\n"
    "[yellow]  • с письменного разрешения[/yellow]\n"
    "[yellow]  • в образовательных целях[/yellow]\n\n"
    "[bold red]Автор не несёт ответственности за незаконное использование.[/bold red]"
)


def print_disclaimer() -> None:
    console.print(Panel.fit(
        DISCLAIMER_TEXT,
        title="Дисклеймер",
        border_style="red",
    ))


def print_banner() -> None:
    banner = Text()
    banner.append("🎭 MalExtGenerator", style="bold magenta")
    banner.append(" v1.0.0\n", style="dim")
    banner.append("Образовательный генератор расширений браузера", style="italic")
    banner.append("\nУправление — через Telegram-бота", style="dim")
    console.print(Panel.fit(banner, border_style="magenta"))


def print_success(message: str) -> None:
    console.print(f"[bold green]✅ {message}[/bold green]")


def print_error(message: str) -> None:
    console.print(f"[bold red]❌ {message}[/bold red]")


def print_info(message: str) -> None:
    console.print(f"[bold blue]ℹ️  {message}[/bold blue]")


def print_warning(message: str) -> None:
    console.print(f"[bold yellow]⚠️  {message}[/bold yellow]")


__all__ = [
    "console",
    "print_disclaimer",
    "print_banner",
    "print_success",
    "print_error",
    "print_info",
    "print_warning",
]
