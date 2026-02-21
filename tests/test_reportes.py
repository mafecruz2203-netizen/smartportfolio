import csv
import json

from src.reportes import ReportadorFinanciero


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