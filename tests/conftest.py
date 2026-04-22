import pytest
from unittest.mock import Mock, patch

from models.crypto_asset import CryptoAsset


# ========== ТЕСТОВЫЕ ДАННЫЕ ==========

@pytest.fixture
def sample_asset():
    """Одиночный тестовый актив"""
    return CryptoAsset(
        name="Bitcoin",
        symbol="BTC",
        price=50000.0,
        change_24h=2.5
    )


@pytest.fixture
def sample_assets_list():
    """Список тестовых активов для коллекции"""
    return [
        CryptoAsset(name="Bitcoin", symbol="BTC", price=50000.0, change_24h=2.5),
        CryptoAsset(name="Ethereum", symbol="ETH", price=3000.0, change_24h=-1.2),
        CryptoAsset(name="Solana", symbol="SOL", price=100.0, change_24h=5.8),
        CryptoAsset(name="Cardano", symbol="ADA", price=0.5, change_24h=-3.1),
        CryptoAsset(name="Ripple", symbol="XRP", price=0.8, change_24h=0.5),
    ]


# ========== MOCK ОТВЕТЫ API ==========

@pytest.fixture
def mock_cmc_response():
    """Мок-ответ от CoinMarketCap API"""
    return {
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
            },
            {
                "name": "Ethereum",
                "symbol": "ETH",
                "quote": {
                    "USD": {
                        "price": 3000.0,
                        "percent_change_24h": -1.2
                    }
                }
            },
            {
                "name": "Solana",
                "symbol": "SOL",
                "quote": {
                    "USD": {
                        "price": 100.0,
                        "percent_change_24h": 5.8
                    }
                }
            }
        ]
    }


@pytest.fixture
def mock_coingecko_response():
    """Мок-ответ от CoinGecko API"""
    return [
        {
            "name": "Bitcoin",
            "symbol": "btc",
            "current_price": 50000.0,
            "price_change_percentage_24h": 2.5
        },
        {
            "name": "Ethereum",
            "symbol": "eth",
            "current_price": 3000.0,
            "price_change_percentage_24h": -1.2
        },
        {
            "name": "Solana",
            "symbol": "sol",
            "current_price": 100.0,
            "price_change_percentage_24h": 5.8
        }
    ]


# ========== MOCK HTTP ЗАПРОСОВ ==========

@pytest.fixture
def mock_requests_get(mock_cmc_response):
    """Мок для requests.get - возвращает успешный ответ CMC"""
    with patch("requests.get") as mock_get:
        mock_response = Mock()
        mock_response.json.return_value = mock_cmc_response
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        yield mock_get


@pytest.fixture
def mock_requests_get_coingecko(mock_coingecko_response):
    """Мок для requests.get - возвращает успешный ответ CoinGecko"""
    with patch("requests.get") as mock_get:
        mock_response = Mock()
        mock_response.json.return_value = mock_coingecko_response
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        yield mock_get


@pytest.fixture
def mock_requests_get_failure():
    """Мок для requests.get - возвращает ошибку (для тестов retry)"""
    with patch("requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.raise_for_status.side_effect = Exception("API Error")
        mock_get.return_value = mock_response
        yield mock_get