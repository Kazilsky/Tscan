# Инициализация базовой графики
from .lib import *

# Инициализация нужных сервисов
from modules.btop import Btop

class MonitoringPopup(ModalScreen):
    # CSS прямо внутри класса, чтобы отцентровать окно и задать размеры
    CSS = """
    MonitoringPopup {
        align: center middle;
        background: rgba(0, 0, 0, 0.5); /* Затемнение заднего фона */
    }

    #popup-container {
        width: 50;
        height: 30;
        border: double cyan;
        background: $surface;
    }
    """

    def compose(self) -> ComposeResult:
        # Оборачиваем OptionList в контейнер, чтобы он не растягивался на весь экран
        with Container(id="popup-container"):
            yield Header(name="Проверка соединения")
            yield OptionList(
                Option("Проверка доступности интернета", id="btop"),
                Option("Проверка открытых портов", id="test2"),
                Option("Проверка DNS leak", id="test3"),
                Option("Проверка VPN-соединения", id="test4"),
                Option("Назад (Esc)", id="back"),  # Добавили подсказку про Esc
            )
            yield Footer()

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        # INFO: event нужно ибо тип на текстуал настолько развитый что все хочет в 1 обработчик 
        event.stop()
        match event.option.id:
            case "btop":
                btop = Btop()
                if not btop.is_available():
                    self.notify("Btop не найден.")
                else:
                    btop.run()

                
            case "back":
                self.dismiss()

