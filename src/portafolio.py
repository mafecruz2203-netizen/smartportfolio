from typing import List
from src.modelos import Posicion


class PosicionNoExisteError(Exception):
    pass


class Portafolio:
    def __init__(self):
        self.posiciones: List[Posicion] = []

    def agregar_posicion(self, posicion: Posicion) -> None:
        '''
        Agrega una posición al portafolio.
        '''
        self.posiciones.append(posicion)

    def remover_posicion(self, ticker: str) -> Posicion:
        for i, posicion in enumerate(self.posiciones):
            if posicion.instrumento.ticker == ticker:
                return self.posiciones.pop(i)

        raise PosicionNoExisteError(
            f"No existe posición con ticker {ticker}"
        )