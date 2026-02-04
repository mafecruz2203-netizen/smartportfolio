from typing import List
from src.modelos import Posicion


class Portafolio:
    def __init__(self):
        self.posiciones: List[Posicion] = []

    def agregar_posicion(self, posicion: Posicion) -> None:
        '''
        Agrega una posición al portafolio.

        Parámetros:
        posicion (Posicion): objeto Posicion a incorporar.
        '''
        self.posiciones.append(posicion)