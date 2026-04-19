import typer

from providers.factory import ProviderFactory
from formatters.factory import FormatterFactory
from models.portfolio import CryptoPortfolio


def run(
    source: str = "coingecko",
    output: str = "console",
    top: int = 3
):
    # 🔥 FIX: Typer передаёт строки
    top = int(top)

    # 1. provider
    provider = ProviderFactory.create(source)
    assets = provider.get_assets()

    # 2. portfolio (анализ)
    portfolio = CryptoPortfolio(assets)
    result = portfolio.top_gainers(top)

    # 3. formatter (вывод)
    formatter = FormatterFactory.create(output)
    formatter.format(result)


if __name__ == "__main__":
    typer.run(run)