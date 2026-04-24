from typing import List
from models.crypto_asset import CryptoAsset


class CryptoPortfolio:
    def __init__(self, assets: List[CryptoAsset]):
        self.assets = assets

    def top_gainers(self, n: int = 3) -> List[CryptoAsset]:
        return sorted(
            self.assets,
            key=lambda x: x.change_24h,
            reverse=True
        )[:n]

    def top_losers(self, n: int = 3) -> List[CryptoAsset]:
        return sorted(
            self.assets,
            key=lambda x: x.change_24h
        )[:n]

    def total_volume(self) -> float:
        """Суммарный объём (price) всех активов"""
        return sum(a.price for a in self.assets)

    def filter_positive(self) -> List[CryptoAsset]:
        return [a for a in self.assets if a.change_24h > 0]

    def filter_negative(self) -> List[CryptoAsset]:
        return [a for a in self.assets if a.change_24h < 0]

    def __len__(self):
        return len(self.assets)

    def __iter__(self):
        return iter(self.assets)

    def __getitem__(self, index):
        """Доступ по индексу: portfolio[0]"""
        return self.assets[index]