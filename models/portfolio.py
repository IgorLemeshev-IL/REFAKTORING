from typing import List
from models.crypto_asset import CryptoAsset

# portfolio ---> корзина крипты -- анализ данных (НЕ ХРАНИМ)
class CryptoPortfolio:
    def __init__(self, assets: List[CryptoAsset]):
        # список криптоактивов, пришедший из provider
        self.assets = assets

    def top_gainers(self, n: int = 3) -> List[CryptoAsset]:
        # топ по росту (от большего к меньшему)
        return sorted(
            self.assets,
            key=lambda x: x.change_24h,
            reverse=True
        )[:n]

    def top_losers(self, n: int = 3) -> List[CryptoAsset]:
        # топ по падению (от меньшего к большему)
        return sorted(
            self.assets,
            key=lambda x: x.change_24h
        )[:n]

    def filter_positive(self) -> List[CryptoAsset]:
        # только растущие активы
        return [a for a in self.assets if a.change_24h > 0]

    def filter_negative(self) -> List[CryptoAsset]:
        # только падающие активы
        return [a for a in self.assets if a.change_24h < 0]

    def __len__(self):
        # количество активов в портфеле
        return len(self.assets)

    def __iter__(self):
        # чтобы можно было делать for asset in portfolio
        return iter(self.assets)