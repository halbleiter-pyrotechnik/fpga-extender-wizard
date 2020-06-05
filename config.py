import tkinter as tk
from tkinter import filedialog

class Config:

    EMPTY = "Empty"
    ADC = "ADC"
    DAC = "DAC"
    NUCLEO = "Nucleo"

    options = [EMPTY, ADC, DAC, NUCLEO]
    array = 18 * [None]

    def __init__(self):
        self.ports = 18 * ["Empty"]

    def __str__(self):
        return str(self.ports)



    # def getPort(self, portindex):
    #     return self.ports[portindex]

    def setPort(self, portindex, setting):
        # To-Do
        self.ports[portindex] = setting
        # print("Somebody has changed the value of port", +portindex, "to " +setting)

    def getPort(self, portindex):
        return self.ports[portindex]

    def getPortOptions(self):
        return self.options

    def getDefaultValue(self):
        return self.options[0]

    # def save(self, filename, filetype):
    #     with open(filename)

    def saveFile(self):
        print(self.ports)

        fout = filedialog.asksaveasfilename(initialdir="/", defaultextension='.txt', initialfile = "FPGA-Extender_settings",
                                            filetypes = (("Textfile","*.txt"),("JSON File","*.json"),("CSV File","*.csv")))
        try:
            with open(fout, 'w') as output:
                for x in self.ports:
                    # output.write(x.get())
                    output.write("%s\n" % x)
        except FileNotFoundError:
            print("Cancelled save or error in filename")

if __name__ == "__main__":

    hallo = Config()
    print(hallo)
