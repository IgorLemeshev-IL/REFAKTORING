import json
from formatters.base import OutputFormatter


class JSONFormatter(OutputFormatter):
    def format(self, assets):
        data = [
            {
                "name": a.name,
                "symbol": a.symbol,
                "price": a.price,
                "change_24h": a.change_24h
            }
            for a in assets
        ]

        print(json.dumps(data, indent=2))