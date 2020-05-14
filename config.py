import tkinter as tk

class Config:

    EMPTY = "Empty"
    ADC = "ADC"
    DAC = "DAC"
    NUCLEO = "Nucleo"

    options = [EMPTY, ADC, DAC, NUCLEO]
    array = 18 * [None]

    def __init__(self):
        self.ports = 18 * ["Empty"]


    # def initialValue(self, zahl):
    #     self.var = tk.StringVar()
    #     self.var.set(self.options[0])
    #     self.var.trace('w', self.change)
    #     return self.var

    def __str__(self):
        return str(self.ports)

    def getPort(self, portindex):
        print(ports)
        return self.ports[portindex]

    def setPort(self, portindex, setting):
        # To-Do
        self.ports[portindex] = setting

if __name__ == "__main__":

    hallo = Config()
    print(hallo)
