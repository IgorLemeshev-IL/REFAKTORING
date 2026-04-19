from formatters.base import OutputFormatter


class ConsoleFormatter(OutputFormatter):
    def format(self, assets):
        for asset in assets:
            print(asset)