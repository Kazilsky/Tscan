class DiskCheck:

    def get_smart_info(self):
        raise NotImplementedError(
            "Получение SMART-данных ещё не реализовано."
        )

    def check_filesystem(self):
        raise NotImplementedError(
            "Проверка файловой системы ещё не реализована."
        )