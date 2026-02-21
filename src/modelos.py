from dataclasses import dataclass


@dataclass(frozen=True)
class Instrumento:
    ticker: str
    tipo: str
    sector: str

@dataclass
class Posicion:
    instrumento: Instrumento
    cantidad: float
    precio_entrada: float

    def __post_init__(self):
        if self.cantidad < 0:
            raise ValueError("La cantidad no puede ser negativa")

    def calcular_valor_actual(self, precio_mercado: float) -> float:
        return self.cantidad * precio_mercado

    def calcular_ganancia_no_realizada(self, precio_actual: float) -> float:
        return (precio_actual - self.precio_entrada) * self.cantidad
    