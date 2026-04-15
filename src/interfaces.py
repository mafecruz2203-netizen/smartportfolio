from abc import ABC, abstractmethod
import pandas as pd

class MarketDataProvider(ABC):
    @abstractmethod
    def obtener_precio_actual(self, ticker: str) -> float:
        pass

    @abstractmethod
    def obtener_historia(self, ticker: str) -> pd.DataFrame:
        pass