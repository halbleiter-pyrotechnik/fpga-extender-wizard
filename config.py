class Config:

    EMPTY = "Empty"
    ADC = "ADC"
    DAC = "DAC"
    NECLEO = "Nucleo"

    def __init__(self):
        self.ports = 18 * ["Empty"]

    def __str__(self):
        return str(self.ports)

    def getPort(self, portindex):
        return self.ports[portindex]

    def setPort(self, portindex, setting):
        # To-Do
        self.ports[portindex] = setting

if __name__ == "__main__":

    hallo = Config()
    print(hallo)
