from config import Config
import os
from view import View
from tkinter import *
from tkinter import filedialog, Text    #filedialog pick the app

#
# hier kommt hin, was die dropdown button machen sollen
#

class Controller:

    def __init__(self):
        self.config = Config()
        self.view = View(self)


    def machwasbitte(value):
        print(value)
        return "machwasbitte ausgeführt"


    def dachwasbitte(eintrag):
        # print(option)
        lol = 18 * [None]
        print(eintrag)
        return "machwasbitte ausgeführt"


    def please():
        print("hallo")
        return "42"

    def runapps(self):
        for app in apps:                    #looping over apps
            os.startfile(app)

    def getDefaultValue(self):
        defaultValue = self.config.getDefaultValue()
        return defaultValue

    def getPortOptions(self):
        options = self.config.getPortOptions()
        return options


# def addApp():
#
#     for widget in frame.winfo_children():   #widget giving access to everything attached to frame; this case labels
#         widget.destroy()                    # deletes first entry of filename
#
#
#     filename = filedialog.askopenfilename(initialdir = "/", title = "Choose file to open",
#                                           filetype = (("All files", "*.*"), ("Text files", "*.txt"), ("CSV files", "*.csv")))
#     apps.append(filename)
#     print(filename)

    def saveFile(self):
        self.config.saveFile()

    def input(self, index, value):
        self.config.setPortRole(portIndex=index, role=value)

    def doSumting(event):
        # clicked1.set()
        choice = tk.Label(canvas, textvariable=clicked1.get())
        choice.pack()
        choice.place(x=m, y=115)

# def openFile:
#     filename = filedialog.askopenfilename(initialdir="/", title="Choose file to open",
#                                               filetype = (("All files", "*.*"), ("Text files", "*.txt"), ("CSV files", "*.csv")))



if __name__ == "__main__":

    hallo = Controller()
    print(hallo)

