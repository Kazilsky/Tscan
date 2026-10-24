# Основные либы
from asyncio import sleep
from textual import work
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, OptionList
from textual.widgets.option_list import Option
from textual.screen import Screen

# INFO: Я чуть не умер изобретая блятские саб меню (06:04, все ниже было раньше чем 06:04)

# --- Ну я не хотел но сабки будут тут
class MonitoringSubMenu(Screen):
    def compose_sub(self) -> ComposeResult:
        yield Header(name="Проверка интернет-соединения")
        # INFO: Я когда монитор увидел чуть не умер я ваще хз что сюда добавлять
        yield OptionList( #TODO: Мне показывает что тут где то ошибка но я не могу понять где.
            Option("Проверка доступности интернета"),
            Option("Проверка открытых портов"),
            Option("Проверка DNS leak"),
            Option("Проверка WebRTC leak"),
            Option("Проверка VPN-соединения"),
        )
        yield Footer()

    # INFO: Я уже забыл зачем но раз есть в доке значит надо (06:05 да)
    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        if event.option.id == "back":
            self.app.pop_screen()

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


    # 1. Сам обработчик события оставляем обычным (синхронным)
    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        option_id = event.option.id

        match option_id:
            case "monitor":
                # Запускаем фоновый воркер, передавая туда нужный текст
                # TODO: Нужно подумать в обоих ли местах match делать или можно как то упростить
                self.run_worker(event.option.prompt)
            case _:
                self.exit()

    # INFO: Только с этим декларотивом textual достаточно не тупой чтобы понять что нужно перерисовать
    @work(exclusive=True)  # exclusive=True не даст запустить задачу дважды, если быстро кликать
    async def run_worker(self, option: str) -> None:
        # Первое уведомление вылетает мгновенно
        self.notify(f"Старт: {option}")
        
        # Этот слип теперь "засыпает" изолированно, не мешая основному интерфейсу рендериться
        await sleep(1)
        
        # Второе ДЕЙСТВИЕ и по сути обработка выбора меню
        match option:
            # INFO: Я хз почему но при выборе монитора уходит в защиту и зависает наглухо, остальное норм
            case "monitor":
                self.push_screen(MonitoringSubMenu())
            # TODO: Я В ТАКОМ АХУЕ, Я ЩАС НА ГИТХАБЕ ИЩУ ТВОЙ МОНИТОР И НИХУЯ НЕ НАХОЖУ
            # TODO: Спустя минут 10 понял, хардкодер ты жесткий конечно, я почти икону поставил
            
                

            # TODO: Нужно придумать обработку ЛЮБЫХ НЕПОДХОДЯЩИХ option_id (ну и плюс я не делал обработку exit ибо лень)
            case _:
                self.exit()


if __name__ == "__main__":
    app = LinuxUtilityApp()
    app.run()

