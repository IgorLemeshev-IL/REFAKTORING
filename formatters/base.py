from abc import ABC, abstractmethod


class OutputFormatter(ABC):
    @abstractmethod
    def format(self, assets):
        pass