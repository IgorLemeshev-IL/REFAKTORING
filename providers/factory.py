from providers.coingecko import CoinGeckoProvider
from providers.coinmarketcap import CoinMarketCapProvider


class ProviderFactory:
    @staticmethod
    def create(name: str):
        if name == "coingecko":
            return CoinGeckoProvider()
        if name == "coinmarketcap":
            return CoinMarketCapProvider()

        raise ValueError("Unknown provider")