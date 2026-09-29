class Estudiante:
    def __init__(self, nombre):
        self.nombre = nombre


class EquipoOficial:
    def __init__(self, nombre):
        self.nombre = nombre


class ReservaRegular:
    def __init__(self, cancha, fecha, hora_inicio, hora_fin, solicitante):
        self.cancha = cancha
        self.fecha = fecha
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self.solicitante = solicitante

    def confirmar(self):
        return f"Reserva confirmada para {self.solicitante.nombre}"


class ReservaPrioridad:
    def __init__(self, cancha, fecha, hora_inicio, hora_fin, solicitante):
        self.cancha = cancha
        self.fecha = fecha
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self.solicitante = solicitante

    def confirmar(self):
        return f"Reserva con prioridad confirmada para {self.solicitante.nombre}"


def reservar_desde_web(cancha, fecha, hora_inicio, hora_fin, solicitante):
    creador = FabricaReservas.elegir_creador(solicitante)
    reserva = creador.crear_reserva(cancha, fecha, hora_inicio, hora_fin, solicitante)
    return reserva


def reservar_desde_hall():
    pass


class CreadorReserva():
    def crear_reserva(self, cancha, fecha, hora_inicio, hora_fin, solicitante):
        raise NotImplementedError


class CreadorReservaRegular(CreadorReserva):
    def crear_reserva(self, cancha, fecha, hora_inicio, hora_fin, solicitante):
        return ReservaRegular(cancha, fecha, hora_inicio, hora_fin, solicitante)


class CreadorReservaPrioritaria(CreadorReserva):
    def crear_reserva(self, cancha, fecha, hora_inicio, hora_fin, solicitante):
        return ReservaPrioridad(cancha, fecha, hora_inicio, hora_fin, solicitante)


class FabricaReservas():
    @staticmethod
    def elegir_creador(solicitante):
        if isinstance(solicitante, Estudiante):
            return CreadorReservaRegular()

        if isinstance(solicitante, EquipoOficial):
            return CreadorReservaPrioritaria()


def main():
    estudiante = Estudiante("Pepe")
    capitan = EquipoOficial("Jose")

    reserva1 = reservar_desde_web(
        "Cancha de futbol",
        "2026-09-27",
        "18:00",
        "20:00",
        estudiante
    )

    print(reserva1.confirmar())

    reserva2 = reservar_desde_web(
        "Cancha de Basket",
        "2026-09-27",
        "14:00",
        "16:00",
        capitan
    )

    print(reserva2.confirmar())


if __name__ == "__main__":
    main()