import pytest
from src.modelos import Posicion
from src.portafolio import PosicionNoExisteError
import csv
import json
from src.reportes import ReportadorFinanciero

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
    
def test_imprimir_resumen_muestra_titulos_y_total(portafolio_con_posiciones, capsys):
    reportador = ReportadorFinanciero()

    reportador.imprimir_resumen(portafolio_con_posiciones)

    salida = capsys.readouterr().out

    assert "RESUMEN DEL PORTAFOLIO" in salida
    assert "Total de posiciones: 2" in salida
    assert "TSLA" in salida
    assert "US10Y" in salida


def test_exportar_csv_crea_archivo_con_encabezado_y_filas(portafolio_con_posiciones, tmp_path):
    reportador = ReportadorFinanciero()
    ruta = tmp_path / "reporte.csv"

    reportador.exportar_csv(portafolio_con_posiciones, str(ruta))

    assert ruta.exists()

    with open(ruta, newline="", encoding="utf-8") as f:
        reader = list(csv.reader(f))

    # encabezado + 2 filas
    assert reader[0] == ["ticker", "tipo", "sector", "cantidad", "precio_entrada"]
    assert len(reader) == 3
    assert reader[1][0] == "TSLA"
    assert reader[2][0] == "US10Y"


def test_exportar_json_crea_lista_de_diccionarios(portafolio_con_posiciones, tmp_path):
    reportador = ReportadorFinanciero()
    ruta = tmp_path / "reporte.json"

    reportador.exportar_json(portafolio_con_posiciones, str(ruta))

    assert ruta.exists()

    with open(ruta, encoding="utf-8") as f:
        data = json.load(f)

    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["ticker"] == "TSLA"
    assert data[1]["ticker"] == "US10Y"    