# Основные либы
import asyncio
from textual import work
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, OptionList
from textual.widgets.option_list import Option

# INFO: Я чуть не умер изобретая блятские саб меню (06:04, все ниже было раньше чем 06:04)

# Основные подключаемые модули
from modules.btop import Btop

# Основное подключение popup, важно что оно тут
from ui.popup import MonitoringPopup

# Основные прописанные модули
class LinuxUtilityApp(App):
    TITLE = "Linux System Utility"
    CSS = """
    OptionList {
        border: round cyan;
        margin: 2 4;
        padding: 1;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        # Готовый список с навигацией стрелками и мышкой
        yield OptionList(
            Option("Мониторинг системы", id="monitor"),
            Option("Проверка интернет-соединения", id="net"),
            Option("Тест оперативной памяти", id="ram"),
            Option("Диагностика диска", id="disk"),
            Option("Проверка безопасности", id="sec"),
            Option("Информация о системе", id="info"),
            Option("Выход", id="exit"),
        )
        yield Footer()

    # Метод срабатывает при выборе пункта (Enter или двойной клик)
    # TODO: ОДНАКО я учел и надобность уведомлять человека о работоспособности проги поэтому этот вариант остается здесь в истоках как не самый удачный
    # TODO: Ниже есть вариант который работает с точки зрения информирования, к сожалению из-за ассинхронизация вынужден на 2 фунцкции делить, хардкод гов-

    # async def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        # option_id = event.option.id
        # if option_id == "exit":
        #     self.exit()
        # else:
        #     # Тут логика переключения экранов
        #     self.notify(f"Запускаем: {event.option.prompt}")

        # INFO: Можно как угодно считывать по айди, это вполне простой способ с док
        # match option_id:
        #     # TODO: Я сделаю лишь один на теории, так как щас 4 утра ура, но что то из разряда:
        #     case "monitor":
        #         # INFO: Просто красивое уведомление с слипом чтобы человек успел прочитать, это можно и убрать если нужно
        #         self.notify(f"Старт: {event.option.prompt}")

        #     # INFO: Тут я сразу дефолт делаю (буквально до остальных), это что будет при не отработке остальных айди, позже сюда можно вывести лог неправильного айди и просьбы обновиться
        #     case _:
        #         self.exit()


    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        option_id = event.option.id

        match option_id:
            case "exit":
                self.exit()
            
            case "monitor":
                # Только для мониторинга запускаем тяжелый асинхронный воркер
                self.run_monitor_worker()
                
            case _:
                # Все нереализованные пункты обрабатываем МГНОВЕННО здесь.
                # Это не вешает поток и не создает конфликтов с @work
                self.notify(f"Модуль '{event.option.prompt}' ещё не реализован", severity="warning")

    @work(exclusive=True)
    async def run_monitor_worker(self) -> None:
        self.notify("Запуск модуля мониторинга...")
        
        # Безопасный sleep. Если пользователь кликнет на другой пункт, 
        await asyncio.sleep(1)
        
        # Переключаем экран напрямую
        self.push_screen(MonitoringPopup())


if __name__ == "__main__":
    app = LinuxUtilityApp()
    app.run()

