from src.modelos import Instrumento, Posicion, InstrumentoOracle
from src.portafolio import Portafolio
from src.reportes import ReportadorFinanciero
from src.yahoo_finance_client import YahooFinanceClient

import json
from pathlib import Path


def flujo_portafolio():
    # 1) Definir instrumentos
    apple = Instrumento(ticker="AAPL", tipo="Accion", sector="Tecnologia")
    tesoro = Instrumento(ticker="US10Y", tipo="Bono", sector="Gobierno")

    # 2) Crear posiciones
    pos1 = Posicion(instrumento=apple, cantidad=10, precio_entrada=150)
    pos2 = Posicion(instrumento=tesoro, cantidad=5, precio_entrada=100)

    # 3) Gestionar portafolio
    fondo = Portafolio()
    fondo.agregar_posicion(pos1)
    fondo.agregar_posicion(pos2)

    # 4) Reportar
    reportador = ReportadorFinanciero()
    reportador.imprimir_resumen(fondo)


def flujo_oraculo():
    print("\n=== SMART PORTFOLIO ORÁCULO ===\n")

    ticker = input("Ingrese el ticker del activo: ").strip().upper()

    provider = YahooFinanceClient()

    instrumento = InstrumentoOracle(
        ticker=ticker,
        tipo="Accion",
        sector="Desconocido",
        data_provider=provider
    )

    print("\nConsultando precio actual...")
    precio_actual = instrumento.obtener_precio_actual()
    print(f"Precio actual de {ticker}: {precio_actual:.2f}")

    print("\nEntrenando modelo y generando predicción...")
    prediccion = instrumento.predecir_tendencia(7)
    print(f"Predicción estimada a 7 días: {prediccion:.2f}")

    decision = input("\n¿Desea comprar este activo? (s/n): ").strip().lower()

    if decision == "s":
        cantidad = float(input("Ingrese la cantidad: ").strip())

        posicion = Posicion(
            instrumento=instrumento,
            cantidad=cantidad,
            precio_entrada=precio_actual
        )

        posicion.evaluar_riesgo()

        datos = {
            "ticker": instrumento.ticker,
            "precio_actual": round(precio_actual, 2),
            "prediccion_7_dias": round(prediccion, 2),
            "cantidad": cantidad,
            "alerta_riesgo": posicion.alerta_riesgo
        }

        ruta = Path("portafolio.json")
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4)

        print("\nArchivo portafolio.json generado correctamente")

    else:
        print("\nNo se realizó compra")


def main():
    print("Seleccione una opción:")
    print("1. Ver portafolio tradicional")
    print("2. Usar Oráculo inteligente")

    opcion = input("Ingrese opción (1 o 2): ").strip()

    if opcion == "1":
        flujo_portafolio()
    elif opcion == "2":
        flujo_oraculo()
    else:
        print("Opción inválida")


if __name__ == "__main__":
    main()