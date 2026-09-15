class GestorConfiguracion:
    _objeto = None

    def __init__(self):
        GestorConfiguracion._objeto = self
        self.modo_mantenimiento =  False

    @staticmethod
    def obtener_objeto():
        if GestorConfiguracion._objeto is None:
            GestorConfiguracion()
        return GestorConfiguracion._objeto


def reserva_permitida(gestor):
    return not gestor.modo_mantenimiento
