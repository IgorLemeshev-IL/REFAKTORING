import requests
from providers.base import CryptoProvider
from models.crypto_asset import CryptoAsset
from decorators import retry


class CoinGeckoProvider(CryptoProvider):
    @retry(max_attempts=3, delay=0.1, exceptions=(requests.RequestException,))
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