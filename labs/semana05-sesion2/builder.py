import copy

class Computadora:
    def __init__(self):
        self.cpu = None
        self.ram = None
        self.disco = None
        self.gpu = None
        self.wifi = None

    def mostrar(self):
        print("CPU: ", self.cpu)
        print("ram: ", self.ram)
        print("disco: ", self.disco)
        print("gpu: ", self.gpu)
        print("wifi: ", self.wifi)

    def clonar(self):
        return copy.deepcopy(self)


class ComputadoraBuilder:
    def __init__(self):
        self.computadora = Computadora()

    def add_cpu(self, cpu):
        self.computadora.cpu = cpu
        return self

    def add_ram(self, ram):
        self.computadora.ram = ram
        return self
        
    def add_disco(self, disco):
        self.computadora.disco = disco
        return self

    def add_gpu(self, gpu):
        self.computadora.gpu = gpu
        return self

    def add_wifi(self, wifi):
        self.computadora.wifi = wifi
        return self

    def build(self):
        return self.computadora


def main():
    pc_builder = ComputadoraBuilder()
    pc_builder = pc_builder.add_ram(16).add_gpu(8)
    pc_builder = pc_builder.add_wifi(True)
    pc_gaming = pc_builder.add_cpu(10).add_disco(1).build()

    pc_gaming2 = pc_gaming.clonar()

    pc_gaming.mostrar()
    pc_gaming2.mostrar()

main()   