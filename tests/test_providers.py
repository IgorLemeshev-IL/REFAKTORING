import pytest
from unittest.mock import patch, Mock
import os

from models.crypto_asset import CryptoAsset
from providers.base import CryptoProvider
from providers.coinmarketcap import CoinMarketCapProvider
from providers.coingecko import CoinGeckoProvider


class TestCoinGeckoProvider:
    """Тесты для CoinGeckoProvider с моками HTTP-запросов"""
    
    def test_get_assets_success(self, mock_requests_get_coingecko, mock_coingecko_response):
        """Успешное получение активов от CoinGecko"""
        provider = CoinGeckoProvider()
        assets = provider.get_assets()
        
        assert isinstance(assets, list)
        assert len(assets) == 3
        
        for asset in assets:
            assert isinstance(asset, CryptoAsset)
        
        assert assets[0].name == "Bitcoin"
        assert assets[0].symbol == "btc"
        assert assets[0].price == 50000.0
        assert assets[0].change_24h == 2.5
        
        mock_requests_get_coingecko.assert_called_once()
        call_args = mock_requests_get_coingecko.call_args
        assert call_args[0][0] == "https://api.coingecko.com/api/v3/coins/markets"
        assert call_args[1]["params"]["vs_currency"] == "usd"
        assert call_args[1]["params"]["per_page"] == 10
    
    def test_get_assets_inherits_from_crypto_provider(self):
        """CoinGeckoProvider должен наследоваться от CryptoProvider"""
        provider = CoinGeckoProvider()
        assert isinstance(provider, CryptoProvider)
    
    def test_get_assets_returns_correct_type(self, mock_requests_get_coingecko):
        """get_assets возвращает list[CryptoAsset]"""
        provider = CoinGeckoProvider()
        assets = provider.get_assets()
        
        assert isinstance(assets, list)
        assert all(isinstance(a, CryptoAsset) for a in assets)
    
    def test_get_assets_empty_response(self):
        """Обработка пустого ответа от API"""
        with patch("requests.get") as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = []
            mock_get.return_value = mock_response
            
            provider = CoinGeckoProvider()
            assets = provider.get_assets()
            
            assert assets == []
            assert isinstance(assets, list)


class TestCoinMarketCapProvider:
    """Тесты для CoinMarketCapProvider с моками HTTP-запросов"""
    
    def test_get_assets_success(self, mock_requests_get, mock_cmc_response, mock_env_api_key):
        """Успешное получение активов от CoinMarketCap"""
        provider = CoinMarketCapProvider()
        assets = provider.get_assets()
        
        assert isinstance(assets, list)
        assert len(assets) == 3
        
        for asset in assets:
            assert isinstance(asset, CryptoAsset)
        
        assert assets[0].name == "Bitcoin"
        assert assets[0].symbol == "BTC"
        assert assets[0].price == 50000.0
        assert assets[0].change_24h == 2.5
        
        assert assets[1].name == "Ethereum"
        assert assets[1].symbol == "ETH"
        assert assets[1].price == 3000.0
        assert assets[1].change_24h == -1.2
        
        mock_requests_get.assert_called_once()
        call_args = mock_requests_get.call_args
        assert call_args[0][0] == "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
        assert call_args[1]["headers"]["X-CMC_PRO_API_KEY"] == "test-api-key-123"
        assert call_args[1]["params"]["limit"] == 10
        assert call_args[1]["params"]["convert"] == "USD"
    
    def test_get_assets_uses_api_key_from_env(self, mock_env_api_key):
        """API ключ должен браться из переменной окружения"""
        provider = CoinMarketCapProvider()
        assert provider.api_key == "test-api-key-123"
    
    def test_get_assets_missing_api_key(self):
        """Ошибка если API ключ не установлен"""
        with patch.dict(os.environ, {}, clear=True):
            provider = CoinMarketCapProvider()
            assert provider.api_key is None
    
    def test_get_assets_handles_malformed_response(self, mock_env_api_key):
        """Обработка некорректного ответа от API"""
        with patch("requests.get") as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = {"data": []}
            mock_get.return_value = mock_response
            
            provider = CoinMarketCapProvider()
            assets = provider.get_assets()
            
            assert assets == []
    
    def test_get_assets_with_missing_quote_field(self, mock_env_api_key):
        """Обработка ответа с отсутствующими полями (edge case)"""
        with patch("requests.get") as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = {
                "data": [
                    {
                        "name": "Bitcoin",
                        "symbol": "BTC",
                    }
                ]
            }
            mock_get.return_value = mock_response
            
            provider = CoinMarketCapProvider()
            
            with pytest.raises(KeyError):
                provider.get_assets()


class TestProviderPolymorphism:
    """Тесты полиморфизма - оба провайдера должны работать одинаково"""
    
    def test_both_providers_implement_get_assets(self):
        """Оба провайдера реализуют метод get_assets"""
        cg = CoinGeckoProvider()
        cmc = CoinMarketCapProvider()
        
        assert hasattr(cg, "get_assets")
        assert hasattr(cmc, "get_assets")
        assert callable(cg.get_assets)
        assert callable(cmc.get_assets)
    
    def test_providers_return_same_structure(self, mock_env_api_key):
        """Оба провайдера возвращают данные в одинаковом формате (list[CryptoAsset])"""
        
        # Мокаем CoinGecko отдельно
        with patch("requests.get") as mock_get_cg:
            mock_response_cg = Mock()
            mock_response_cg.json.return_value = [
                {
                    "name": "Bitcoin",
                    "symbol": "btc",
                    "current_price": 50000.0,
                    "price_change_percentage_24h": 2.5
                }
            ]
            mock_get_cg.return_value = mock_response_cg
            
            cg = CoinGeckoProvider()
            cg_assets = cg.get_assets()
        
        # Мокаем CoinMarketCap отдельно
        with patch("requests.get") as mock_get_cmc:
            mock_response_cmc = Mock()
            mock_response_cmc.json.return_value = {
                "data": [
                    {
                        "name": "Bitcoin",
                        "symbol": "BTC",
                        "quote": {
                            "USD": {
                                "price": 50000.0,
                                "percent_change_24h": 2.5
                            }
                        }
                    }
                ]
            }
            mock_get_cmc.return_value = mock_response_cmc
            
            cmc = CoinMarketCapProvider()
            cmc_assets = cmc.get_assets()
        
        # Оба возвращают список
        assert isinstance(cg_assets, list)
        assert isinstance(cmc_assets, list)
        
        # Оба возвращают CryptoAsset объекты
        assert all(isinstance(a, CryptoAsset) for a in cg_assets)
        assert all(isinstance(a, CryptoAsset) for a in cmc_assets)
        
        # Одинаковое количество
        assert len(cg_assets) == len(cmc_assets) == 1
    
    def test_provider_substitution(self, mock_requests_get_coingecko):
        """Liskov Substitution Principle - можно подменить провайдер"""
        
        def analyze_with_provider(provider: CryptoProvider):
            assets = provider.get_assets()
            return len(assets)
        
        cg = CoinGeckoProvider()
        result = analyze_with_provider(cg)
        assert result == 3


class TestProviderIsolation:
    """Тесты изоляции - провайдеры не зависят друг от друга"""
    
    def test_coinmarketcap_independent_of_coingecko(self):
        """CMC провайдер не зависит от CoinGecko"""
        cmc = CoinMarketCapProvider()
        assert cmc is not None
        
        with patch("requests.get") as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = {
                "data": [
                    {
                        "name": "Test",
                        "symbol": "TST",
                        "quote": {"USD": {"price": 1.0, "percent_change_24h": 0.0}}
                    }
                ]
            }
            mock_get.return_value = mock_response
            
            with patch.dict(os.environ, {"CMC_API_KEY": "test"}):
                assets = cmc.get_assets()
                assert len(assets) == 1
    
    def test_coingecko_independent_of_coinmarketcap(self):
        """CoinGecko провайдер не зависит от CMC"""
        cg = CoinGeckoProvider()
        assert cg is not None
        
        with patch("requests.get") as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = [
                {"name": "Test", "symbol": "tst", "current_price": 1.0, "price_change_percentage_24h": 0.0}
            ]
            mock_get.return_value = mock_response
            
            assets = cg.get_assets()
            assert len(assets) == 1