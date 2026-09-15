from singleton import GestorConfiguracion, reserva_permitida

def test_rechaza_reserva():
    config = GestorConfiguracion.obtener_objeto()
    config.modo_mantenimiento = True

    assert reserva_permitida(config) is False

def test_reserva_aceptada():
    config = GestorConfiguracion.obtener_objeto()
    # El problema aqui es que es un Singleton. En la primera prueba, pusimos modo_mantenimiento = True
    # Este cambio se ve reflejado en la siguiente prueba dado que solo trabajamos con
    # una instancia del objeto, saltando un error
    
    config.modo_mantenimiento = False

    assert reserva_permitida(config) is True