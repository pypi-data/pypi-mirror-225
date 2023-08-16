from abc import ABC, abstractmethod


class Df(ABC):
    @abstractmethod
    def get_df(self):
        pass
