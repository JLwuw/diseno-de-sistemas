# TODO: 
# Vehiculo: mover()
# auto -> mueve por carretera
# bote -> mueve por mar
# Avion -> mueve por cielo

class MovementComponent():
    def move(self):
        raise NotImplementedError

class MovementGrond(MovementComponent):
    def move(self):
        print("Conduciendo por la carretera")

class MovementWater(MovementComponent):
    def move(self):
        print("Navegando por agua")

class MovementAir(MovementComponent):
    def move(self):
        print("Volando por el aire")

class Vehicle:
    def __init__(self, movement_component):
        self.movement_component = movement_component

    def move(self):
        self.movement_component.move()

class Car(Vehicle):
    def __init__(self):
        movement_ground = MovementGrond()
        super().__init__(movement_ground)


class Boat(Vehicle):
    def __init__(self):
        movement_water = MovementWater()
        super().__init__(movement_water)


class Plane(Vehicle):
    def __init__(self):
        movement_air = MovementAir()
        super().__init__(movement_air)

my_car = Car()
my_boat = Boat()
my_plane = Plane()

my_car.move()
my_boat.move()
my_plane.move()