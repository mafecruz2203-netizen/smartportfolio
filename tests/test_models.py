import pytest

from src.modelos import Posicion
from src.portafolio import PosicionNoExisteError


@pytest.mark.parametrize(
    "precio_entrada, precio_actual, cantidad, esperado",
    [
        (100, 150, 10, 500),
        (200, 180, 5, -100),
        (50, 50, 7, 0),
    ],
)
def test_calculo_ganancia_no_realizada(precio_entrada, precio_actual, cantidad, esperado, instrumento_test):
    posicion = Posicion(
        instrumento=instrumento_test,
        cantidad=cantidad,
        precio_entrada=precio_entrada,
    )

    resultado = posicion.calcular_ganancia_no_realizada(precio_actual=precio_actual)

    assert resultado == pytest.approx(esperado)


def test_remover_activo_inexistente_lanza_error(portafolio_vacio):
    with pytest.raises(PosicionNoExisteError):
        portafolio_vacio.remover_posicion("NFLX")

def test_calcular_valor_actual(instrumento_test):
    posicion = Posicion(instrumento=instrumento_test, cantidad=2, precio_entrada=100)
    assert posicion.calcular_valor_actual(precio_mercado=50) == 100


def test_posicion_cantidad_negativa_lanza_value_error(instrumento_test):
    with pytest.raises(ValueError):
        Posicion(instrumento=instrumento_test, cantidad=-1, precio_entrada=100)
def test_remover_posicion_existente_la_elimina_del_portafolio(portafolio_vacio, instrumento_test):
    posicion = Posicion(instrumento=instrumento_test, cantidad=1, precio_entrada=10)
    portafolio_vacio.agregar_posicion(posicion)

    removida = portafolio_vacio.remover_posicion("TSLA")

    assert removida == posicion
    assert len(portafolio_vacio.posiciones) == 0