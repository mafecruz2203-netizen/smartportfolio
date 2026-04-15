from dataclasses import dataclass, field
import pandas as pd
from sklearn.linear_model import LinearRegression

from src.interfaces import MarketDataProvider

@dataclass(frozen=True)
class Instrumento:
    ticker: str
    tipo: str
    sector: str


# oraculo
@dataclass
class InstrumentoOracle:
    ticker: str
    tipo: str
    sector: str
    data_provider: MarketDataProvider

    _history: pd.DataFrame = field(default_factory=pd.DataFrame, init=False)
    _modelo: LinearRegression = field(default_factory=LinearRegression, init=False)
    _entrenado: bool = field(default=False, init=False)

    def entrenar_modelo(self) -> None:
        if self._history.empty:
            self._history = self.data_provider.obtener_historia(self.ticker)

        df = self._history.reset_index(drop=True)

        x = df.index.values.reshape(-1, 1)
        y = df["Close"].values

        self._modelo.fit(x, y)
        self._entrenado = True

    def predecir_tendencia(self, dias_futuros: int = 7) -> float:
        if not self._entrenado:
            self.entrenar_modelo()

        dia_objetivo = len(self._history) + dias_futuros
        prediccion = self._modelo.predict([[dia_objetivo]])

        return float(prediccion[0])

    def obtener_precio_actual(self) -> float:
        return self.data_provider.obtener_precio_actual(self.ticker)

# oraculo
@dataclass
class Posicion:
    instrumento: InstrumentoOracle
    cantidad: float
    precio_entrada: float
    alerta_riesgo: bool = field(default=False, init=False)

    def __post_init__(self):
        if self.cantidad < 0:
            raise ValueError("La cantidad no puede ser negativa")

    def calcular_valor_actual(self, precio_mercado: float) -> float:
        return self.cantidad * precio_mercado

    def calcular_ganancia_no_realizada(self, precio_actual: float) -> float:
        return (precio_actual - self.precio_entrada) * self.cantidad

    def evaluar_riesgo(self) -> bool:
        precio_actual = self.instrumento.obtener_precio_actual()
        perdida = (self.precio_entrada - precio_actual) / self.precio_entrada

        self.alerta_riesgo = perdida > 0.10
        return self.alerta_riesgo