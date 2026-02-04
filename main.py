from src.modelos import Instrumento, Posicion
from src.portafolio import Portafolio
from src.reportes import ReportadorFinanciero


def main():
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


if __name__ == "__main__":
    main()