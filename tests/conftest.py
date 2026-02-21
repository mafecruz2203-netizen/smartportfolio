import pytest

from src.modelos import Instrumento
from src.portafolio import Portafolio


@pytest.fixture
def instrumento_test():
    return Instrumento(
        ticker="TSLA",
        tipo="Accion",
        sector="Automotriz"
    )


@pytest.fixture
def portafolio_vacio():
    return Portafolio()
from src.modelos import Posicion


@pytest.fixture
def portafolio_con_posiciones(portafolio_vacio, instrumento_test):
    pos1 = Posicion(instrumento=instrumento_test, cantidad=10, precio_entrada=150)

    inst2 = Instrumento(ticker="US10Y", tipo="Bono", sector="Gobierno")
    pos2 = Posicion(instrumento=inst2, cantidad=5, precio_entrada=100)

    portafolio_vacio.agregar_posicion(pos1)
    portafolio_vacio.agregar_posicion(pos2)

    return portafolio_vacio