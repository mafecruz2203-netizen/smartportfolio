import pandas as pd

from src.modelos import InstrumentoOracle, Posicion


class MockDataProvider:
    def obtener_precio_actual(self, ticker: str) -> float:
        return 100.0

    def obtener_historia(self, ticker: str) -> pd.DataFrame:
        return pd.DataFrame(
            {
                "Close": [90, 92, 94, 96, 98, 100]
            }
        )


class MockDataProviderPerdidaAlta:
    def obtener_precio_actual(self, ticker: str) -> float:
        return 80.0

    def obtener_historia(self, ticker: str) -> pd.DataFrame:
        return pd.DataFrame(
            {
                "Close": [100, 98, 95, 90, 85, 80]
            }
        )


def test_instrumento_oracle_predice_float():
    provider = MockDataProvider()
    instrumento = InstrumentoOracle(
        ticker="AAPL",
        tipo="Accion",
        sector="Tecnologia",
        data_provider=provider
    )

    prediccion = instrumento.predecir_tendencia(7)

    assert isinstance(prediccion, float)


def test_posicion_sin_alerta_riesgo():
    provider = MockDataProvider()
    instrumento = InstrumentoOracle(
        ticker="AAPL",
        tipo="Accion",
        sector="Tecnologia",
        data_provider=provider
    )

    posicion = Posicion(
        instrumento=instrumento,
        cantidad=5,
        precio_entrada=105.0
    )

    resultado = posicion.evaluar_riesgo()

    assert resultado is False
    assert posicion.alerta_riesgo is False


def test_posicion_con_alerta_riesgo():
    provider = MockDataProviderPerdidaAlta()
    instrumento = InstrumentoOracle(
        ticker="AAPL",
        tipo="Accion",
        sector="Tecnologia",
        data_provider=provider
    )

    posicion = Posicion(
        instrumento=instrumento,
        cantidad=5,
        precio_entrada=100.0
    )

    resultado = posicion.evaluar_riesgo()

    assert resultado is True
    assert posicion.alerta_riesgo is True