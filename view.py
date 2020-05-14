import tkinter as tk                      #create the GUI
from tkinter import filedialog, Text    #filedialog pick the app
from PIL import ImageTk, Image
from config import Config
import controller

# derrived class by putting tk.Tk
class View(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        self.createBackground()
        self.config = Config()
        self.createButtons()
        self.dropDown()
        self.apps = []
        self.run()

    #
    # import background
    #
    def createBackground(self):
        self.canvas = tk.Canvas(self, width=784, height=805, bg="#263D42")
        self.image = ImageTk.PhotoImage(Image.open("C:\\Program Files\\Git\\test-repo\\FPGA-Extender.PNG"))
        self.canvas.create_image(0, 0, anchor='nw', image=self.image)
        self.canvas.pack(expand=1, fill='both')

    #
    # populating buttons on background
    #
    def createButtons(self):
        # self.addapp = tk.Button(self, text="Datei öffnen", padx=30, pady=10
        #                       , fg="white", bg="#263D42", command=controller.addApp)  # command: Funktion aufrufen

        # self.runapp = tk.Button(self, text="Starte Programm", padx=30, pady=10
        #                , fg="white", bg="#263D40", command=controller.runapps)
        # self.runapp.pack()

        self.buttonQuit = tk.Button(self, text='Close Program', padx = 400, pady = 20, command=self.quit)
        self.buttonQuit.pack()

        # self.openFile = tk.Button(self, text="Datei öffnen", padx=30, pady=10
        #                       , fg="white", bg="#263D42", command=controller.addApp)  # command: Funktion aufrufen
        # self.openFile.pack()




    #
    # populating 18 dropdown menues, placing them on background
    #
    def dropDown(self):

        xPos = 5 * [100] + 5 * [603] + 4 * [325] + 4 * [420]

        yPos = [89, 190, 293, 396, 499]
        yPos = yPos + [yPos[0], yPos[1], yPos[2], yPos[3], yPos[4]] + [142, 245, 348, 451]
        yPos = yPos + [yPos[10], yPos[11], yPos[12], yPos[13]]

        self.arrayOptionmenu = 18 * [None]
        self.var = 18 * ["Empty"]
        self.varnames = 18 * [None]

        # catches an update in OptionMenu and provide dropdown number in index and chosen option in value
        # each time trace sees a change, the argument will be given to function change with args looking like this:
        # ('PY_VAR0', '', 'w') - example for updated change of first dropdown
        def change(*args):
            # saving the first argument of args in varname: 'PY_VAR0'
            varname = args[0]
            # gets value of recently updated argument
            value = self.getvar(varname)
            # finds the position of varname (for example 'PY_VAR0') in self.varnames array
            # saves position in variable index
            index = self.varnames.index(varname)
            # common to run prints on the first run to see if we get the correct return
            print(index)
            print(value)
            return(True)

        for i in range(18):
            # giving argument self to StringVar class of tkinter instead of normally root
            self.var[i] = tk.StringVar(self)
            # saves var entry as a name (string) in varnames array
            self.varnames[i] = self.var[i]._name
            # attaches 'w' (write) & change function as argument
            # trace a method of StringVar
            # changed the order: first trace, then set -> initial value will be set and calls function change 18 times
            # trace method is registering an update of var[i]
            self.var[i].trace('w', change)
            # for-loop: each increment calls change funtion -> updates var[i] entry
            self.var[i].set(self.config.options[0])
            # populating array of tk.OptionMenues
            # attaching to canvas
            # "*" means giving each entry of options (defined in config.py) as choice for OptionMenu
            self.arrayOptionmenu[i] = tk.OptionMenu(self.canvas, self.var[i], *self.config.options)
            self.arrayOptionmenu[i].config(width= 6)
            self.arrayOptionmenu[i].pack()
            self.arrayOptionmenu[i].place(x = xPos[i], y = yPos[i])

    def run(self):
        self.mainloop()









                        #body everything will be attached to it
 # multiple apps

#if os.path.isfile('save.txt', 'r') as f: # if there is a file calles save.txt
 #   with open('save.txt') as f:
  #      tempapps = f.read()
   #     print(tempapps)



#with open('save.txt', 'w') as f:  #saves sources in a textfile
 #   for app in apps:


if __name__ == "__main__":
    #f.write(apps + '.')

    hello = View()
    print("Programm geschlossen")
