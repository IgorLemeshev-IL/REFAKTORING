from typing import List
from models.crypto_asset import CryptoAsset

# Класс представляет КОЛЛЕКЦИЮ криптоактивов.
# - здесь находится логика анализа
class CryptoPortfolio:
    def __init__(self, assets: List[CryptoAsset]):
        # Принимаем список активов извне.
        # Почему так:
        # - не создаём данные внутри класса
        # - можно подставить любой источник (API, файл, тесты)
        # assets - список криптовалют (смотри параметры __init__)
        self.assets = assets

    def top_gainers(self, n: int = 3) -> List[CryptoAsset]:
        # Возвращает топ N активов с наибольшим ростом.
        # Как работает:
        # - sorted(..., reverse=True) использует __gt__ из CryptoAsset
        # - берём первые N элементов 3 штуки
        return sorted(self.assets, reverse=True)[:n]

    def top_losers(self, n: int = 3) -> List[CryptoAsset]:
        # Возвращает топ N активов с наибольшим падением.
        # Как работает:
        # - обычный sorted() (по возрастанию)
        # - берём первые N элементов (самые плохие) 3 штуки
        return sorted(self.assets)[:n]

    def filter_positive(self) -> List[CryptoAsset]:
        # Возвращает только те активы, у которых рост > 0.
        # Почему это здесь:
        # - это бизнес-логика (анализ)
        # - не относится к самому объекту CryptoAsset
        return [asset for asset in self.assets if asset.change_24h > 0]

    def filter_negative(self) -> List[CryptoAsset]:
        # Возвращает только падающие активы.
        return [asset for asset in self.assets if asset.change_24h < 0]

    def __len__(self):
        # Позволяет использовать len(portfolio)
        return len(self.assets)

    def __iter__(self):
        # Позволяет итерироваться:ет объект удобным в использовании
        return iter(self.assets)