import pytest
from models.crypto_asset import CryptoAsset


class TestCryptoAssetValidation:
    """Тесты валидации данных в __init__"""

    def test_empty_name_raises_error(self):
        """Пустое имя вызывает ValueError"""
        with pytest.raises(ValueError, match="name"):
            CryptoAsset("", "BTC", 100.0, 1.0)

    def test_empty_symbol_raises_error(self):
        """Пустой символ вызывает ValueError"""
        with pytest.raises(ValueError, match="symbol"):
            CryptoAsset("Bitcoin", "", 100.0, 1.0)

    def test_none_name_raises_error(self):
        """None вместо имени вызывает ValueError"""
        with pytest.raises(ValueError, match="name"):
            CryptoAsset(None, "BTC", 100.0, 1.0)

    def test_none_symbol_raises_error(self):
        """None вместо символа вызывает ValueError"""
        with pytest.raises(ValueError, match="symbol"):
            CryptoAsset("Bitcoin", None, 100.0, 1.0)

    def test_invalid_price_type_raises_error(self):
        """Цена строкой вызывает TypeError"""
        with pytest.raises(TypeError, match="price"):
            CryptoAsset("Bitcoin", "BTC", "invalid", 1.0)

    def test_invalid_change_24h_type_raises_error(self):
        """change_24h строкой вызывает TypeError"""
        with pytest.raises(TypeError, match="change_24h"):
            CryptoAsset("Bitcoin", "BTC", 100.0, "invalid")

    @pytest.mark.parametrize("name,symbol,price,change", [
        ("Bitcoin", "BTC", 50000.0, 2.5),
        ("Ethereum", "ETH", 3000.0, -1.2),
        ("A" * 100, "X", 0.0001, 999.9),
        ("Test", "TST-USDT", 1.0, 0.0),
        ("ビットコイン", "₿", 50000.0, 2.5),
    ])
    def test_valid_data_passes_validation(self, name, symbol, price, change):
        """Корректные данные проходят валидацию"""
        asset = CryptoAsset(name=name, symbol=symbol, price=price, change_24h=change)
        assert asset.name == name
        assert asset.symbol == symbol
        assert asset.price == price
        assert asset.change_24h == change


class TestCryptoAssetInit:
    """Тесты конструктора __init__"""

    def test_create_valid_asset(self):
        """Создание актива с корректными данными"""
        asset = CryptoAsset(
            name="Bitcoin",
            symbol="BTC",
            price=50000.0,
            change_24h=2.5
        )
        assert asset.name == "Bitcoin"
        assert asset.symbol == "BTC"
        assert asset.price == 50000.0
        assert asset.change_24h == 2.5

    @pytest.mark.parametrize("name,symbol,price,change", [
        ("Bitcoin", "BTC", 50000.0, 2.5),
        ("Ethereum", "ETH", 3000.0, -1.2),
        ("A" * 100, "X", 0.0001, 999.9),
    ])
    def test_create_asset_parametrized(self, name, symbol, price, change):
        """Параметризованный тест создания актива"""
        asset = CryptoAsset(name=name, symbol=symbol, price=price, change_24h=change)
        assert asset.name == name
        assert asset.symbol == symbol
        assert asset.price == price
        assert asset.change_24h == change

    def test_asset_types(self, sample_asset):
        """Проверка типов атрибутов"""
        assert isinstance(sample_asset.name, str)
        assert isinstance(sample_asset.symbol, str)
        assert isinstance(sample_asset.price, float)
        assert isinstance(sample_asset.change_24h, float)


class TestCryptoAssetMagicMethods:
    """Тесты магических методов __str__, __repr__, __lt__, __gt__"""

    def test_str_method(self, sample_asset):
        """__str__ должен возвращать читаемое представление"""
        result = str(sample_asset)
        assert "Bitcoin" in result
        assert "BTC" in result
        assert "50000.00" in result
        assert "+2.50%" in result

    @pytest.mark.parametrize("price,change,expected_str", [
        (50000.0, 2.5, "Bitcoin (BTC): $50000.00 (+2.50%)"),
        (3000.0, -1.2, "Ethereum (ETH): $3000.00 (-1.20%)"),
        (0.5, 0.0, "Cardano (ADA): $0.50 (+0.00%)"),
    ])
    def test_str_method_parametrized(self, price, change, expected_str):
        """Параметризованный тест форматирования строки"""
        asset = CryptoAsset(
            name=expected_str.split()[0],
            symbol=expected_str.split()[1].strip("()"),
            price=price,
            change_24h=change
        )
        str_result = str(asset)
        assert f"${price:.2f}" in str_result
        assert f"{change:+.2f}%" in str_result

    def test_repr_method(self, sample_asset):
        """__repr__ должен возвращать строку для разработчика"""
        result = repr(sample_asset)
        assert "CryptoAsset(" in result
        assert "name=Bitcoin" in result
        assert "symbol=BTC" in result
        assert "price=50000.0" in result
        assert "change_24h=2.5" in result

    def test_lt_method_true(self):
        """__lt__: актив с меньшим change_24h должен быть меньше"""
        btc = CryptoAsset("Bitcoin", "BTC", 50000.0, 2.5)
        eth = CryptoAsset("Ethereum", "ETH", 3000.0, -1.2)
        assert eth < btc
        assert not (btc < eth)

    def test_lt_method_equal(self):
        """__lt__: равные значения change_24h"""
        btc = CryptoAsset("Bitcoin", "BTC", 50000.0, 2.5)
        btc2 = CryptoAsset("Bitcoin2", "BTC2", 40000.0, 2.5)
        assert not (btc < btc2)
        assert not (btc2 < btc)

    def test_lt_method_not_implemented(self, sample_asset):
        """__lt__: сравнение с другим типом возвращает NotImplemented"""
        with pytest.raises(TypeError):
            sample_asset < "not an asset"

    def test_gt_method_true(self):
        """__gt__: актив с большим change_24h должен быть больше"""
        btc = CryptoAsset("Bitcoin", "BTC", 50000.0, 2.5)
        eth = CryptoAsset("Ethereum", "ETH", 3000.0, -1.2)
        assert btc > eth
        assert not (eth > btc)

    def test_gt_method_equal(self):
        """__gt__: равные значения change_24h"""
        btc = CryptoAsset("Bitcoin", "BTC", 50000.0, 2.5)
        btc2 = CryptoAsset("Bitcoin2", "BTC2", 40000.0, 2.5)
        assert not (btc > btc2)
        assert not (btc2 > btc)

    def test_gt_method_not_implemented(self, sample_asset):
        """__gt__: сравнение с другим типом возвращает NotImplemented"""
        with pytest.raises(TypeError):
            sample_asset > 123


class TestCryptoAssetEdgeCases:
    """Тесты граничных случаев"""

    def test_negative_price(self):
        """Отрицательная цена (теоретически невозможна, но проверяем)"""
        asset = CryptoAsset("Test", "TST", -100.0, 0.0)
        assert asset.price == -100.0

    def test_very_large_numbers(self):
        """Очень большие числа"""
        asset = CryptoAsset("Large", "LRG", 1e18, 1e6)
        assert asset.price == 1e18
        assert asset.change_24h == 1e6

    def test_very_small_numbers(self):
        """Очень маленькие числа"""
        asset = CryptoAsset("Small", "SML", 1e-10, -1e-10)
        assert asset.price == 1e-10
        assert asset.change_24h == -1e-10

    def test_unicode_in_name(self):
        """Юникод в названии"""
        asset = CryptoAsset("ビットコイン", "₿", 50000.0, 2.5)
        assert asset.name == "ビットコイン"
        assert asset.symbol == "₿"

    def test_special_characters_in_symbol(self):
        """Спецсимволы в символе"""
        asset = CryptoAsset("Test", "TST-USDT", 1.0, 0.0)
        assert asset.symbol == "TST-USDT"


class TestCryptoAssetSorting:
    """Тесты сортировки с использованием __lt__ и __gt__"""

    def test_sort_ascending(self, sample_assets_list):
        """Сортировка по возрастанию change_24h (losers)"""
        sorted_assets = sorted(sample_assets_list)
        changes = [a.change_24h for a in sorted_assets]
        assert changes == sorted(changes)
        assert sorted_assets[0].change_24h == -3.1
        assert sorted_assets[-1].change_24h == 5.8

    def test_sort_descending(self, sample_assets_list):
        """Сортировка по убыванию change_24h (gainers)"""
        sorted_assets = sorted(sample_assets_list, reverse=True)
        changes = [a.change_24h for a in sorted_assets]
        assert changes == sorted(changes, reverse=True)
        assert sorted_assets[0].change_24h == 5.8
        assert sorted_assets[-1].change_24h == -3.1