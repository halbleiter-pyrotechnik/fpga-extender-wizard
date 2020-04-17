import tkinter as tk                  #create the GUI
from tkinter import filedialog, Text  #filedialog pick the app
import os                             #run the app


root = tk.Tk()                         #body everything will be attached to it
apps = [] # multiple apps

#if os.path.isfile('save.txt', 'r') as f: # if there is a file calles save.txt
 #   with open('save.txt') as f:
  #      tempapps = f.read()
   #     print(tempapps)


def addApp():


    for widget in frame.winfo_children():   #widget giving access to everything attached to frame; this case labels
        widget.destroy()                    # deletes first entry of filename


    filename = filedialog.askopenfilename(initialdir = "/", title = "Wähl mal eine Datei, wenn du Lust hast",
                                          filetype = (("Alle Ordner, Savage", "*.*"), ("Pythons Files", "*.py")))
    apps.append(filename)
    print(filename)
    for ass in apps:                                        #
        label = tk.Label(frame, text = ass, bg = "gray")    # location of the file is ass, looping over apps
        label.pack()


def runapps():
    for ass in apps:                    #looping over apps
        os.startfile(ass)




canvas = tk.Canvas(root, height=700, width=700, bg="#263D42") #surface for graphical elements
canvas.pack()

frame = tk.Frame(root, bg = "white")
frame.place(relwidth=0.8, relheight= 0.8, relx = 0.1, rely = 0.1)

openFile1 = tk.Button(root, text = "Datei öffnen", padx = 30, pady = 10
                 , fg = "white", bg = "#263D42", command = addApp) #command: Funktion aufrufen
openFile1.pack()

runapp = tk.Button(root, text = "Starte Programm", padx = 30, pady = 10
                 , fg = "white", bg = "#263D40", command = runapps)
runapp.pack()

root.mainloop()

with open('save.txt', 'w') as f:  #saves sources in a textfile
    for ass in apps:
        f.write(apps + '.')