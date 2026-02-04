import json
import csv
from src.portafolio import Portafolio


class ReportadorFinanciero:
    """
    Clase responsable únicamente de generar reportes.
    No almacena datos ni lógica de negocio, solo transforma
    un Portafolio en salidas legibles o exportables.
    """

    def imprimir_resumen(self, portafolio: Portafolio) -> None:
        print("RESUMEN DEL PORTAFOLIO")
        print("-" * 40)

        for posicion in portafolio.posiciones:
            instrumento = posicion.instrumento
            print(
                f"{instrumento.ticker} | "
                f"{instrumento.tipo} | "
                f"{instrumento.sector} | "
                f"Cantidad: {posicion.cantidad} | "
                f"Precio entrada: {posicion.precio_entrada}"
            )

        print("-" * 40)
        print(f"Total de posiciones: {len(portafolio.posiciones)}")

    def exportar_csv(self, portafolio: Portafolio, ruta: str) -> None:
        with open(ruta, mode="w", newline="", encoding="utf-8") as archivo:
            writer = csv.writer(archivo)
            writer.writerow([
                "ticker", "tipo", "sector", "cantidad", "precio_entrada"
            ])

            for posicion in portafolio.posiciones:
                inst = posicion.instrumento
                writer.writerow([
                    inst.ticker,
                    inst.tipo,
                    inst.sector,
                    posicion.cantidad,
                    posicion.precio_entrada
                ])

    def exportar_json(self, portafolio: Portafolio, ruta: str) -> None:
        data = []

        for posicion in portafolio.posiciones:
            inst = posicion.instrumento
            data.append({
                "ticker": inst.ticker,
                "tipo": inst.tipo,
                "sector": inst.sector,
                "cantidad": posicion.cantidad,
                "precio_entrada": posicion.precio_entrada
            })

        with open(ruta, mode="w", encoding="utf-8") as archivo:
            json.dump(data, archivo, indent=4, ensure_ascii=False)
