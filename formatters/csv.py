import csv
from formatters.base import OutputFormatter


class CSVFormatter(OutputFormatter):
    def format(self, assets):
        with open("output.csv", "w", newline="") as f:
            writer = csv.writer(f)

            writer.writerow(["name", "symbol", "price", "change_24h"])

            for a in assets:
                writer.writerow([a.name, a.symbol, a.price, a.change_24h])