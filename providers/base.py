from abc import ABC, abstractmethod
from models.crypto_asset import CryptoAsset

# Теперь любой провайдер обязан вернуть list[CryptoAsset]
class CryptoProvider(ABC):
    # БАЗОВЫЙ интерфейс для всех провайдеров.
    # Почему это важно:
    # - мы НЕ завязываемся на конкретный API
    # - любой новый источник обязан следовать этому контракту
    
    @abstractmethod
    def get_assets(self) -> list[CryptoAsset]:
        # Должен вернуть список CryptoAsset
        # Это ОБЩЕЕ правило для всех провайдеров
        pass