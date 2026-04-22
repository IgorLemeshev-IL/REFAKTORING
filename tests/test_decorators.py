import pytest
from unittest.mock import Mock, patch
import requests

from decorators import retry


class TestRetryDecorator:
    """Тесты для декоратора @retry"""
    
    def test_retry_success_first_attempt(self):
        """Успешное выполнение с первой попытки"""
        mock_func = Mock(return_value="success")
        
        @retry(max_attempts=3, delay=0.1)
        def test_func():
            return mock_func()
        
        result = test_func()
        
        assert result == "success"
        assert mock_func.call_count == 1
    
    def test_retry_success_after_failures(self):
        """Успех после нескольких неудач"""
        mock_func = Mock(side_effect=[ValueError, ValueError, "success"])
        
        @retry(max_attempts=3, delay=0.1, exceptions=(ValueError,))
        def test_func():
            return mock_func()
        
        with patch("time.sleep") as mock_sleep:
            result = test_func()
        
        assert result == "success"
        assert mock_func.call_count == 3
        assert mock_sleep.call_count == 2
    
    def test_retry_all_attempts_fail(self):
        """Все попытки неудачны - пробрасывается исключение"""
        mock_func = Mock(side_effect=ValueError("error"))
        
        @retry(max_attempts=3, delay=0.1, exceptions=(ValueError,))
        def test_func():
            return mock_func()
        
        with patch("time.sleep"):
            with pytest.raises(ValueError, match="error"):
                test_func()
        
        assert mock_func.call_count == 3
    
    def test_retry_max_attempts_respected(self):
        """Проверка что количество попыток не превышает max_attempts"""
        mock_func = Mock(side_effect=ValueError)
        
        @retry(max_attempts=5, delay=0.01, exceptions=(ValueError,))
        def test_func():
            return mock_func()
        
        with patch("time.sleep"):
            with pytest.raises(ValueError):
                test_func()
        
        assert mock_func.call_count == 5
    
    @pytest.mark.parametrize("max_attempts", [1, 2, 3, 5, 10])
    def test_retry_various_max_attempts(self, max_attempts):
        """Параметризованный тест с разным количеством попыток"""
        mock_func = Mock(side_effect=ValueError)
        
        @retry(max_attempts=max_attempts, delay=0.01, exceptions=(ValueError,))
        def test_func():
            return mock_func()
        
        with patch("time.sleep"):
            with pytest.raises(ValueError):
                test_func()
        
        assert mock_func.call_count == max_attempts
    
    def test_retry_delay_between_attempts(self):
        """Проверка задержки между попытками"""
        mock_func = Mock(side_effect=[ValueError, ValueError, "success"])
        
        @retry(max_attempts=3, delay=0.5, exceptions=(ValueError,))
        def test_func():
            return mock_func()
        
        with patch("time.sleep") as mock_sleep:
            test_func()
        
        assert mock_sleep.call_count == 2
        mock_sleep.assert_called_with(0.5)
    
    def test_retry_only_specified_exceptions(self):
        """Повтор только для указанных исключений"""
        mock_func = Mock(side_effect=KeyError)
        
        @retry(max_attempts=3, delay=0.1, exceptions=(ValueError,))
        def test_func():
            return mock_func()
        
        with pytest.raises(KeyError):
            test_func()
        
        assert mock_func.call_count == 1
    
    def test_retry_preserves_function_metadata(self):
        """Декоратор сохраняет метаданные функции"""
        
        @retry(max_attempts=3)
        def my_test_function():
            """Test docstring"""
            return "ok"
        
        assert my_test_function.__name__ == "my_test_function"
        assert my_test_function.__doc__ == "Test docstring"
    
    def test_retry_with_args_and_kwargs(self):
        """Декоратор корректно передаёт аргументы"""
        mock_func = Mock(return_value="ok")
        
        @retry(max_attempts=2)
        def test_func(a, b, c=None):
            return mock_func(a, b, c=c)
        
        result = test_func(1, 2, c=3)
        
        assert result == "ok"
        mock_func.assert_called_with(1, 2, c=3)


class TestRetryWithRealProviders:
    """Интеграционные тесты retry с провайдерами"""
    
    def test_coingecko_retry_on_request_exception(self):
        """CoinGecko повторяет попытки при RequestException"""
        from providers.coingecko import CoinGeckoProvider
        
        with patch("requests.get") as mock_get:
            mock_response_success = Mock()
            mock_response_success.json.return_value = [
                {"name": "Bitcoin", "symbol": "btc", "current_price": 50000.0, "price_change_percentage_24h": 2.5}
            ]
            
            mock_get.side_effect = [
                requests.RequestException("Error 1"),
                requests.RequestException("Error 2"),
                mock_response_success
            ]
            
            provider = CoinGeckoProvider()
            
            with patch("time.sleep") as mock_sleep:
                assets = provider.get_assets()
            
            assert len(assets) == 1
            assert assets[0].name == "Bitcoin"
            assert mock_get.call_count == 3
            assert mock_sleep.call_count == 2
    
    def test_coinmarketcap_retry_on_request_exception(self, mock_env_api_key):
        """CoinMarketCap повторяет попытки при RequestException"""
        from providers.coinmarketcap import CoinMarketCapProvider
        
        with patch("requests.get") as mock_get:
            mock_response_success = Mock()
            mock_response_success.json.return_value = {
                "data": [
                    {
                        "name": "Bitcoin",
                        "symbol": "BTC",
                        "quote": {"USD": {"price": 50000.0, "percent_change_24h": 2.5}}
                    }
                ]
            }
            
            mock_get.side_effect = [
                requests.RequestException("Error 1"),
                requests.RequestException("Error 2"),
                mock_response_success
            ]
            
            provider = CoinMarketCapProvider()
            
            with patch("time.sleep"):
                assets = provider.get_assets()
            
            assert len(assets) == 1
            assert mock_get.call_count == 3