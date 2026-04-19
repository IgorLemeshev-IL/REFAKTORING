class CryptoAsset:
    # Класс представляет ОДНУ криптовалюту.
    # Почему отдельный класс:
    # - инкапсулируем данные (всё про одну монету в одном месте)
    def __init__(self, name: str, symbol: str, price: float, change_24h: float):
        # обычный инициализатор: нужные атрибуты в нем.
        # - соблюдаем принцип Single Responsibility (SRP)
        self.name = name
        self.symbol = symbol
        self.price = price
        self.change_24h = change_24h

    def __str__(self):
        # Определяем, как объект печатается через print().
        return f"{self.name} ({self.symbol}): ${self.price:.2f} ({self.change_24h:+.2f}%)"

    def __repr__(self):
        # магический метод вывода информации для разработчика удобен для работы
        return (
            f"CryptoAsset(name={self.name}, "
            f"symbol={self.symbol}, "
            f"price={self.price}, "
            f"change_24h={self.change_24h})"
        )

    def __lt__(self, other):
        # Маг метод для сравнения экз.классов.
        # - нужно для сортировки (sorted)
        # - используется в top losers
        # Важно:
        # - сравниваем ТОЛЬКО change_24h, а не всю структуру
        if not isinstance(other, CryptoAsset):
            return NotImplemented
        return self.change_24h < other.change_24h

    def __gt__(self, other):
        # Магический метод сравнения.
        # "Больше чем" (>)
        # - для сортировки в обратном порядке (top gainers)
        if not isinstance(other, CryptoAsset):
            return NotImplemented
        return self.change_24h > other.change_24h