import requests
from providers.base import CryptoProvider
from models.crypto_asset import CryptoAsset

# реализовал OCP (Open/Closed Principle)
# теперь:
# код НЕ трогаешь
# просто добавляешь новый класс
# Провайдер для CoinGecko API

class CoinGeckoProvider(CryptoProvider):
    def get_assets(self) -> list[CryptoAsset]:
        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": 10,
            "page": 1,
            "sparkline": False
        }

        response = requests.get(url, params=params)
        data = response.json()

        assets = []

        for item in data:
            asset = CryptoAsset(
                name=item["name"],
                symbol=item["symbol"],
                price=item["current_price"],
                change_24h=item["price_change_percentage_24h"]
            )
            assets.append(asset)

        return assets