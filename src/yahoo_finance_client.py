import pandas as pd
import yfinance as yf
from src.interfaces import MarketDataProvider

class YahooFinanceClient(MarketDataProvider):
    def obtener_precio_actual(self, ticker: str) -> float:
        try:
            t = yf.Ticker(ticker)
            precio = t.fast_info.get("last_price")

            if precio is None:
                hist = t.history(period="5d")
                if hist.empty:
                    raise ValueError(f"No se encontró precio para {ticker}")
                precio = hist["Close"].iloc[-1]

            return float(precio)

        except Exception as e:
            raise ConnectionError(
                f"Error al obtener el precio actual de {ticker}: {e}"
            )

    def obtener_historia(self, ticker: str) -> pd.DataFrame:
        try:
            t = yf.Ticker(ticker)
            historia = t.history(period="1y")

            if historia.empty:
                raise ValueError(f"No se encontró historial para {ticker}")

            return historia

        except Exception as e:
            raise ConnectionError(
                f"Error al obtener historial de {ticker}: {e}"
            )