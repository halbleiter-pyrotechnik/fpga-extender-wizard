from config import Config
import os

#
# hier kommt hin, was die dropdown button machen sollen
#
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

def runapps():
    for app in apps:                    #looping over apps
        os.startfile(app)


def addApp():

    for widget in frame.winfo_children():   #widget giving access to everything attached to frame; this case labels
        widget.destroy()                    # deletes first entry of filename


    filename = filedialog.askopenfilename(initialdir = "/", title = "Wähl mal einen Datei, wenn du Lust hast",
                                          filetype = (("Alle Ordner, Savage", "*.*"), ("Pythons Files", "*.py")))
    apps.append(filename)
    print(filename)
    for app in apps:                                        #
        label = tk.Label(frame, text = app, bg = "gray")    # location of the file is ass, looping over apps
        label.pack()




if __name__ == "__main__":

    hallo = Config()
    print(hallo)


    def doSumting(event):
        # clicked1.set()
        choice = tk.Label(canvas, textvariable=clicked1.get())
        choice.pack()
        choice.place(x=m, y=115)

# config.setPort()
