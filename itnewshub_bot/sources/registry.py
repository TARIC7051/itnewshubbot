class SourceRegistry:
    def __init__(self):
        # Словарь: имя источника → объект загрузчика
        self._sources = {}

    def register(self, name: str, loader):
        """
        Регистрирует источник.

        name — строковый ключ (например: "igromania")
        loader — объект загрузчика (RSSLoader / HTMLLoader / APILoader)
        """
        self._sources[name] = loader

    def get(self, name: str):
        """
        Возвращает загрузчик по имени.
        Если источник не найден — возвращает None.
        """
        return self._sources.get(name)

    def list(self):
        """
        Возвращает список зарегистрированных источников.
        """
        return list(self._sources.keys())


# Глобальный реестр
registry = SourceRegistry()
