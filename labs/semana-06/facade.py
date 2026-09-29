
class Inventario:
    def verificar(self, producto):
        print(f"Verificando el stock de {producto}")
        return True


class Pago:
    def procesar(self, monto):
        print(f"Procesando pago {monto}")
        return monto


class Envio:
    def crear_envio(self, producto):
        print(f"Preparando el envio de {producto}")
        return True


class Notificacion:
    def crear_notificacion(self, producto):
        print(f"Se compro el producto {producto} con exito")


class TiendaFacade:
    def __init__(self):
        self.inventario = Inventario()
        self.pago = Pago()
        self.envio = Envio()
        self.notificacion = Notificacion()

    def comprar(self, producto, precio):
        if not self.inventario.verificar(producto):
            print("No hay stock")
            return

        if not self.pago.procesar(precio):
            print("Fallo el pago")
            return

        self.envio.crear_envio(producto)
        print("Compra completada")

        self.notificacion.crear_notificacion(producto)


def main():
    producto1 = "Laptop"
    precio = 1500

    tienda = TiendaFacade()
    tienda.comprar(producto1, precio)

main()