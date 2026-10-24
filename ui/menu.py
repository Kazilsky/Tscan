
import sys
import tty
import termios
from rich.panel import Panel
from rich.text import Text
from rich.live import Live
from rich.console import Console

# Функция для чтения одного нажатия клавиши в Linux без Enter
def get_key():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
        if ch == '\x1b':  # Навегационные клавиши (Esc / стрелки)
            ch += sys.stdin.read(2)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

class Menu:
    def __init__(self):
        self.console = Console()
        self.menu_items = [
            "Мониторинг системы",
            "Проверка интернет-соединения",
            "Тест оперативной памяти",
            "Диагностика диска",
            "Проверка безопасности системы",
            "Информация о системе",
            "Выход",
        ]
        self.current_idx = 0

    def make_menu_content(self) -> Panel:
        content = Text()
        for idx, title in enumerate(self.menu_items):
            if idx == self.current_idx:
                # Подсвечиваем выбранный стрелками пункт
                content.append(f"> {title}\n", style="bold reverse cyan")
            else:
                content.append(f"  {title}\n", style="white")
        
        return Panel(
            content,
            title="[bold]Linux System Utility[/bold]",
            border_style="cyan",
            padding=(1, 2),
        )

    def navigate(self):
        # Live позволяет обновлять картинку на месте
        with Live(self.make_menu_content(), console=self.console, screen=True) as live:
            while True:
                key = get_key()
                
                if key == '\x1b[A':  # Стрелка Вверх
                    self.current_idx = (self.current_idx - 1) % len(self.menu_items)
                elif key == '\x1b[B':  # Стрелка Вниз
                    self.current_idx = (self.current_idx + 1) % len(self.menu_items)
                elif key == '\r':  # Enter
                    return self.current_idx
                elif key == '\x03':  # Ctrl+C
                    return len(self.menu_items) - 1 # Выход

if __name__ == "__main__":
    menu = Menu()
    choice = menu.navigate()
    print(f"Вы выбрали пункт индекс: {choice}")

