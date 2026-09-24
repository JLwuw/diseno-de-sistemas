from abc import ABC, abstractmethod


class EstrategiaDescuento(ABC):
    @abstractmethod
    def aplicar(self, precio_base):
        pass


class SinDescuento(EstrategiaDescuento):
    def aplicar(self, precio_base):
        return precio_base


class DescuentoVIP(EstrategiaDescuento):
    def aplicar(self, precio_base):
        return precio_base * 0.8


class DescuentoEstudiante(EstrategiaDescuento):
    def aplicar(self, precio_base):
        return precio_base * 0.95

class DescuentoEmpleado(EstrategiaDescuento):
    def aplicar(self, precio_base):
        return precio_base * 0.75
        
class Compra:
    def __init__(self, estrategia_descuento: EstrategiaDescuento):
        self.estrategia_descuento = estrategia_descuento

    def calcular_total(self, precio):
        return self.estrategia_descuento.aplicar(precio)


def main():
    compra1 = Compra(SinDescuento())
    compra2 = Compra(DescuentoEstudiante())
    compra3 = Compra(DescuentoVIP())
    compra4 = Compra(DescuentoEmpleado())

    print(compra1.calcular_total(100))
    print(compra2.calcular_total(20))
    print(compra3.calcular_total(10000))
    print(compra4.calcular_total(30))


main()