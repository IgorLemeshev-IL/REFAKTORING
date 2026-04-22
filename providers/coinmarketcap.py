# import os
# import requests
# from dotenv import load_dotenv

# from models.crypto_asset import CryptoAsset

# load_dotenv()

# # источник данных (API) откуда взять крипту Provider = “доставщик данных”
# class CoinMarketCapProvider:
#     def __init__(self):
#         self.api_key = os.getenv("CMC_API_KEY")

#     def get_assets(self):
#         url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"

#         headers = {
#             "X-CMC_PRO_API_KEY": self.api_key
#         }

#         params = {
#             "limit": 10,
#             "convert": "USD"
#         }

#         response = requests.get(url, headers=headers, params=params)
#         data = response.json()["data"]

#         assets = []

#         for item in data:
#             quote = item["quote"]["USD"]

#             assets.append(
#                 CryptoAsset(
#                     name=item["name"],
#                     symbol=item["symbol"],
#                     price=quote["price"],
#                     change_24h=quote["percent_change_24h"]
#                 )
#             )

#         return assets

import os
import requests
from dotenv import load_dotenv

from models.crypto_asset import CryptoAsset
from decorators import retry  # <-- ДОБАВИТЬ ЭТУ СТРОКУ

load_dotenv()

# источник данных (API) откуда взять крипту Provider = "доставщик данных"
class CoinMarketCapProvider:
    def __init__(self):
        self.api_key = os.getenv("CMC_API_KEY")

    @retry(max_attempts=3, delay=0.1, exceptions=(requests.RequestException,))  # <-- ДОБАВИТЬ ЭТУ СТРОКУ
    def get_assets(self):
        url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"

        headers = {
            "X-CMC_PRO_API_KEY": self.api_key
        }

        params = {
            "limit": 10,
            "convert": "USD"
        }

        response = requests.get(url, headers=headers, params=params)
        data = response.json()["data"]

        assets = []

        for item in data:
            quote = item["quote"]["USD"]

            assets.append(
                CryptoAsset(
                    name=item["name"],
                    symbol=item["symbol"],
                    price=quote["price"],
                    change_24h=quote["percent_change_24h"]
                )
            )

        return assets