from formatters.console import ConsoleFormatter
from formatters.json import JSONFormatter
from formatters.csv import CSVFormatter


class FormatterFactory:
    @staticmethod
    def create(name: str):
        if name == "console":
            return ConsoleFormatter()
        if name == "json":
            return JSONFormatter()
        if name == "csv":
            return CSVFormatter()

        raise ValueError("Unknown formatter")