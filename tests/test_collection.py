import pytest
from models.crypto_asset import CryptoAsset
from models.portfolio import CryptoPortfolio


class TestCryptoPortfolioInit:
    """Тесты конструктора CryptoPortfolio"""
    
    def test_create_empty_portfolio(self):
        """Создание пустого портфеля"""
        portfolio = CryptoPortfolio([])
        assert len(portfolio) == 0
        assert portfolio.assets == []

    def test_create_portfolio_with_assets(self, sample_assets_list):
        """Создание портфеля с активами"""
        portfolio = CryptoPortfolio(sample_assets_list)
        assert len(portfolio) == 5
        assert portfolio.assets == sample_assets_list

    def test_portfolio_does_not_modify_original_list(self, sample_assets_list):
        """Портфель хранит ссылку, а не копию (важно для тестов)"""
        original_len = len(sample_assets_list)
        portfolio = CryptoPortfolio(sample_assets_list)
        
        # Изменяем оригинальный список
        sample_assets_list.append(
            CryptoAsset("NewCoin", "NEW", 10.0, 1.0)
        )
        
        # Портфель "видит" изменения (хранит ссылку)
        assert len(portfolio) == original_len + 1


class TestCryptoPortfolioLenAndIter:
    """Тесты __len__ и __iter__"""
    
    def test_len_empty(self):
        """__len__ для пустого портфеля"""
        portfolio = CryptoPortfolio([])
        assert len(portfolio) == 0

    def test_len_with_assets(self, sample_assets_list):
        """__len__ с активами"""
        portfolio = CryptoPortfolio(sample_assets_list)
        assert len(portfolio) == 5

    def test_iter_empty(self):
        """__iter__ для пустого портфеля"""
        portfolio = CryptoPortfolio([])
        items = list(portfolio)
        assert items == []

    def test_iter_with_assets(self, sample_assets_list):
        """__iter__ возвращает все активы в правильном порядке"""
        portfolio = CryptoPortfolio(sample_assets_list)
        items = list(portfolio)
        assert items == sample_assets_list
        assert len(items) == 5

    def test_for_loop_iteration(self, sample_assets_list):
        """Проверка итерации через for loop"""
        portfolio = CryptoPortfolio(sample_assets_list)
        symbols = []
        for asset in portfolio:
            symbols.append(asset.symbol)
        assert symbols == ["BTC", "ETH", "SOL", "ADA", "XRP"]


class TestCryptoPortfolioTopGainers:
    """Тесты метода top_gainers"""
    
    def test_top_gainers_default_n(self, sample_assets_list):
        """top_gainers с n по умолчанию (3)"""
        portfolio = CryptoPortfolio(sample_assets_list)
        gainers = portfolio.top_gainers()
        
        assert len(gainers) == 3
        # SOL (+5.8), BTC (+2.5), XRP (+0.5)
        assert gainers[0].symbol == "SOL"
        assert gainers[1].symbol == "BTC"
        assert gainers[2].symbol == "XRP"

    @pytest.mark.parametrize("n,expected_symbols", [
        (1, ["SOL"]),
        (2, ["SOL", "BTC"]),
        (3, ["SOL", "BTC", "XRP"]),
        (5, ["SOL", "BTC", "XRP", "ETH", "ADA"]),  # все
        (10, ["SOL", "BTC", "XRP", "ETH", "ADA"]),  # больше чем есть
    ])
    def test_top_gainers_parametrized(self, sample_assets_list, n, expected_symbols):
        """Параметризованный тест top_gainers с разными n"""
        portfolio = CryptoPortfolio(sample_assets_list)
        gainers = portfolio.top_gainers(n)
        
        assert len(gainers) == min(n, 5)
        assert [a.symbol for a in gainers] == expected_symbols

    def test_top_gainers_empty_portfolio(self):
        """top_gainers для пустого портфеля"""
        portfolio = CryptoPortfolio([])
        gainers = portfolio.top_gainers()
        assert gainers == []

    def test_top_gainers_all_negative(self):
        """top_gainers когда все активы падают"""
        assets = [
            CryptoAsset("A", "A", 10.0, -1.0),
            CryptoAsset("B", "B", 10.0, -2.0),
            CryptoAsset("C", "C", 10.0, -0.5),
        ]
        portfolio = CryptoPortfolio(assets)
        gainers = portfolio.top_gainers(3)
        
        # Сортировка от большего к меньшему (наименее отрицательные впереди)
        assert gainers[0].symbol == "C"  # -0.5
        assert gainers[1].symbol == "A"  # -1.0
        assert gainers[2].symbol == "B"  # -2.0


class TestCryptoPortfolioTopLosers:
    """Тесты метода top_losers"""
    
    def test_top_losers_default_n(self, sample_assets_list):
        """top_losers с n по умолчанию (3)"""
        portfolio = CryptoPortfolio(sample_assets_list)
        losers = portfolio.top_losers()
        
        assert len(losers) == 3
        # ADA (-3.1), ETH (-1.2), XRP (+0.5) - от меньшего к большему
        assert losers[0].symbol == "ADA"
        assert losers[1].symbol == "ETH"
        assert losers[2].symbol == "XRP"

    @pytest.mark.parametrize("n,expected_symbols", [
        (1, ["ADA"]),
        (2, ["ADA", "ETH"]),
        (3, ["ADA", "ETH", "XRP"]),
        (5, ["ADA", "ETH", "XRP", "BTC", "SOL"]),
    ])
    def test_top_losers_parametrized(self, sample_assets_list, n, expected_symbols):
        """Параметризованный тест top_losers с разными n"""
        portfolio = CryptoPortfolio(sample_assets_list)
        losers = portfolio.top_losers(n)
        
        assert len(losers) == min(n, 5)
        assert [a.symbol for a in losers] == expected_symbols

    def test_top_losers_empty_portfolio(self):
        """top_losers для пустого портфеля"""
        portfolio = CryptoPortfolio([])
        losers = portfolio.top_losers()
        assert losers == []

    def test_top_losers_all_positive(self):
        """top_losers когда все активы растут"""
        assets = [
            CryptoAsset("A", "A", 10.0, 1.0),
            CryptoAsset("B", "B", 10.0, 2.0),
            CryptoAsset("C", "C", 10.0, 0.5),
        ]
        portfolio = CryptoPortfolio(assets)
        losers = portfolio.top_losers(3)
        
        # Сортировка от меньшего к большему (наименее растущие впереди)
        assert losers[0].symbol == "C"  # 0.5
        assert losers[1].symbol == "A"  # 1.0
        assert losers[2].symbol == "B"  # 2.0


class TestCryptoPortfolioFilters:
    """Тесты методов filter_positive и filter_negative"""
    
    def test_filter_positive(self, sample_assets_list):
        """filter_positive возвращает только растущие активы"""
        portfolio = CryptoPortfolio(sample_assets_list)
        positive = portfolio.filter_positive()
        
        assert len(positive) == 3
        symbols = [a.symbol for a in positive]
        assert "BTC" in symbols  # +2.5
        assert "SOL" in symbols  # +5.8
        assert "XRP" in symbols  # +0.5

    def test_filter_positive_empty(self):
        """filter_positive когда нет растущих"""
        assets = [
            CryptoAsset("A", "A", 10.0, -1.0),
            CryptoAsset("B", "B", 10.0, -2.0),
        ]
        portfolio = CryptoPortfolio(assets)
        positive = portfolio.filter_positive()
        assert positive == []

    def test_filter_positive_edge_zero(self):
        """filter_positive: 0 не считается положительным"""
        assets = [
            CryptoAsset("Zero", "ZRO", 10.0, 0.0),
            CryptoAsset("Positive", "POS", 10.0, 0.1),
        ]
        portfolio = CryptoPortfolio(assets)
        positive = portfolio.filter_positive()
        assert len(positive) == 1
        assert positive[0].symbol == "POS"

    def test_filter_negative(self, sample_assets_list):
        """filter_negative возвращает только падающие активы"""
        portfolio = CryptoPortfolio(sample_assets_list)
        negative = portfolio.filter_negative()
        
        assert len(negative) == 2
        symbols = [a.symbol for a in negative]
        assert "ETH" in symbols  # -1.2
        assert "ADA" in symbols  # -3.1

    def test_filter_negative_empty(self):
        """filter_negative когда нет падающих"""
        assets = [
            CryptoAsset("A", "A", 10.0, 1.0),
            CryptoAsset("B", "B", 10.0, 2.0),
        ]
        portfolio = CryptoPortfolio(assets)
        negative = portfolio.filter_negative()
        assert negative == []

    def test_filter_negative_edge_zero(self):
        """filter_negative: 0 не считается отрицательным"""
        assets = [
            CryptoAsset("Zero", "ZRO", 10.0, 0.0),
            CryptoAsset("Negative", "NEG", 10.0, -0.1),
        ]
        portfolio = CryptoPortfolio(assets)
        negative = portfolio.filter_negative()
        assert len(negative) == 1
        assert negative[0].symbol == "NEG"


class TestCryptoPortfolioEdgeCases:
    """Граничные случаи для CryptoPortfolio"""
    
    def test_large_portfolio(self):
        """Портфель с большим количеством активов"""
        assets = [
            CryptoAsset(f"Coin{i}", f"C{i}", 1.0, i - 500)
            for i in range(1000)
        ]
        portfolio = CryptoPortfolio(assets)
        
        assert len(portfolio) == 1000
        gainers = portfolio.top_gainers(5)
        assert len(gainers) == 5
        assert gainers[0].change_24h == 499  # i=999
        
    def test_duplicate_assets(self):
        """Портфель с дубликатами (одинаковые активы)"""
        btc1 = CryptoAsset("Bitcoin", "BTC", 50000.0, 2.5)
        btc2 = CryptoAsset("Bitcoin", "BTC", 50000.0, 2.5)
        portfolio = CryptoPortfolio([btc1, btc2])
        
        assert len(portfolio) == 2
        gainers = portfolio.top_gainers(2)
        assert len(gainers) == 2