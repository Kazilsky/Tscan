from rich.console import Console
from system.fastfetch import Fastfetch
from ui.menu import Menu
from system.btop import Btop
from checks.internet.connectivity import ConnectivityCheck


class Application:

    def __init__(self):
        self.fastfetch = Fastfetch()
        self.btop = Btop()
        self.connectivity_check = ConnectivityCheck()
        self.console = Console()
        self.menu = Menu(self.console)
        self.running = True

    def run(self):
        while self.running:
            self.console.clear()
            self.menu.display_main()

            choice = self.menu.get_choice()

            if choice == "0":
                self.running = False

            elif choice == "1":
                self.show_btop()

            elif choice == "2":
                self.show_submenu(
                    "Проверка интернет-соединения",
                    [
                        "Проверка доступности интернета",
                        "Проверка открытых портов",
                        "Проверка DNS leak",
                        "Проверка WebRTC leak",
                        "Проверка VPN-соединения",
                    ],
                )

            elif choice == "3":
                self.show_placeholder("Тест оперативной памяти")

            elif choice == "4":
                self.show_placeholder("Диагностика диска")

            elif choice == "5":
                self.show_submenu(
                    "Проверка безопасности системы",
                    [
                        "Проверка процессов",
                        "Проверка служб systemd",
                        "Проверка температуры",
                        "Проверка файловой системы",
                        "Проверка обновлений",
                        "Проверка системного журнала",
                    ],
                )

            elif choice == "6":
                self.show_fastfetch()
            else:
                self.console.print(
                    "[red]Неизвестный пункт меню.[/red]"
                )
                self.pause()

        self.console.clear()
        self.console.print("[bold cyan]Tuscan завершил работу.[/bold cyan]")

    def show_placeholder(self, title):
        self.console.clear()
        self.console.print(f"[bold cyan]{title}[/bold cyan]\n")
        self.console.print(
            "[yellow]Этот модуль пока не реализован.[/yellow]"
        )
        self.pause()

    def show_submenu(self, title, options):
        while True:
            self.console.clear()
            self.console.print(f"[bold cyan]{title}[/bold cyan]\n")

            for index, option in enumerate(options, start=1):
                self.console.print(f"[cyan]{index}.[/cyan] {option}")

            self.console.print("\n[cyan]0.[/cyan] Назад")

            choice = self.menu.get_choice()

            if choice == "0":
                return

            if choice.isdigit() and 1 <= int(choice) <= len(options):
                selected = options[int(choice) - 1]

                if selected == "Проверка доступности интернета":
                    self.show_internet_check()
                else:
                    self.show_placeholder(selected)
            else:
                self.console.print("[red]Неверный выбор.[/red]")
                self.pause()

    def pause(self):
        self.console.input("\n[dim]Нажмите Enter для продолжения...[/dim]")

    def show_fastfetch(self):
        self.console.clear()

        if not self.fastfetch.is_available():
            self.console.print("[red]Fastfetch не найден.[/red]")
            self.console.print(
                "Установи: sudo pacman -S fastfetch"
            )
            self.pause()
            return

        self.fastfetch.run()

        self.console.input(
            "\n[dim]Нажмите Enter для возврата в меню...[/dim]"
        )

    def show_btop(self):
        self.console.clear()

        if not self.btop.is_available():
            self.console.print(
                "[red]btop не найден.[/red]"
            )
            self.console.print(
                "Установи его: sudo pacman -S btop"
            )
            self.pause()
            return

        self.btop.run()

        self.console.clear()

    def show_internet_check(self):
        self.console.clear()
        self.console.print(
            "[bold cyan]Tscan | Проверка доступности интернета[/bold cyan]\n"
        )
        self.console.print("Проверяем контрольные узлы...\n")

        results = self.connectivity_check.check()

        from rich.table import Table

        table = Table()
        table.add_column("Узел")
        table.add_column("Статус")
        table.add_column("HTTP")
        table.add_column("Задержка")

        for result in results:
            status = (
                "[green]Доступен[/green]"
                if result["available"]
                else "[red]Недоступен[/red]"
            )

            http_status = (
                str(result["status"])
                if result["status"] is not None
                else "—"
            )

            latency = (
                f'{result["latency_ms"]} мс'
                if result["latency_ms"] is not None
                else "—"
            )

            table.add_row(
                result["name"],
                status,
                http_status,
                latency,
            )

        self.console.print(table)

        available = sum(r["available"] for r in results)

        if available == len(results):
            self.console.print("\n[bold green]Интернет доступен.[/bold green]")
        elif available:
            self.console.print(
                "\n[bold yellow]Частичная доступность интернета.[/bold yellow]"
            )
        else:
            self.console.print(
                "\n[bold red]Доступность интернета не подтверждена.[/bold red]"
            )

        self.pause()
