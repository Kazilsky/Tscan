from rich.panel import Panel
from rich.text import Text

from ui.screens import render_header


class Menu:

    def __init__(self, console):
        self.console = console

    def display_main(self):
        render_header(self.console, "Linux System Utility")

        menu_items = [
            ("1", "Мониторинг системы"),
            ("2", "Проверка интернет-соединения"),
            ("3", "Тест оперативной памяти"),
            ("4", "Диагностика диска"),
            ("5", "Проверка безопасности системы"),
            ("6", "Информация о системе"),
            ("0", "Выход"),
        ]

        content = Text()

        for number, title in menu_items:
            content.append(f"{number:>2}) ", style="bold cyan")
            content.append(f"{title}\n")

        self.console.print(
            Panel(
                content,
                title="[bold]Главное меню[/bold]",
                border_style="cyan",
                padding=(1, 2),
            )
        )

    def get_choice(self):
        return self.console.input(
            "\n[bold cyan]Выберите действие: [/bold cyan]"
        ).strip()