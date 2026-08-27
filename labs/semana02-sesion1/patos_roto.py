class ComportamientoVuelo:
    def volar(self):
        raise NotImplementedError

class VuelaConAlas(ComportamientoVuelo):
    def volar(self):
        print ("Volando con alas")

class NoVuela(ComportamientoVuelo):
    def volar(self):
        print ("No vuela.")

class Pato:
    def __init__(self, comportamiento_vuelo):
        self.comportamiento_vuelo = comportamiento_vuelo
         
    def nadar(self):
        print ("Nadando.")

    def graznar(self):
        print ("Cuac!")

    def volar(self):
        self.comportamiento_vuelo.volar()

class PatoSalvaje(Pato):
    def __init__(self):
        vuela_alas = VuelaConAlas()
        super().__init__(VuelaConAlas())

class PatoDeGoma(Pato):
    def __init__(self):
        no_vuela = NoVuela()
        super().__init__(no_vuela)

    def granzanar (self):
        print ("Chirrido de goma.")

#    def volar(self):            #Mala practica
#         print("No vuela.")

if __name__ == "__main__":
    salvaje = PatoSalvaje()
    salvaje.nadar()
    salvaje.graznar()
    salvaje.volar()

    print()

    goma = PatoDeGoma()
    goma.nadar()
    goma.granzanar()
    goma.volar()     #Un pato de goma no vuela Por que este código lo permite?

