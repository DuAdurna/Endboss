# Importing tkinter,tkinter.ttk and utilities
import sys
import tkinter as tk
from tkinter import ttk
from util import gameData
import pyperclip

# Create the window
root = tk.Tk()
root.title('Endboss - Was wollen wir spielen?')

# Place the window in the center of the screen
windowWidth = 650
windowHeight = 530
screenWidth = root.winfo_screenwidth()
screenHeight = root.winfo_screenheight()
xCordinate = int((screenWidth / 2) - (windowWidth / 2))
yCordinate = int((screenHeight / 2) - (windowHeight / 2))
root.geometry("{}x{}+{}+{}".format(windowWidth, windowHeight, xCordinate, yCordinate))

# Create a style
style = ttk.Style(root)

# Import the tcl file
root.tk.call('source', 'azure-dark.tcl')

# Set theme
style.theme_use('azure-dark')

# Create control variables
a = tk.IntVar()
b = tk.IntVar()
c = tk.IntVar()
d = tk.IntVar()
e = tk.IntVar()
f = tk.IntVar()
g = tk.IntVar()
h = tk.IntVar()
i = tk.IntVar()
j = tk.IntVar()
k = tk.IntVar()
w = tk.IntVar()
x = tk.IntVar()
y = tk.IntVar()
z = tk.IntVar()

ausgewaehlteSpieler = []
sortierModus = tk.BooleanVar()
sortierModus.set(True)
sortierName = tk.StringVar()
sortierName.set("Sortiert nach der Spielzeit der letzten 2 Wochen")

# Create a frame for the Checkbuttons
checkframe = ttk.LabelFrame(root, text='Spieler', width=210, height=500)
checkframe.place(x=20, y=12)


# Callback function for Checkbuttons
def buttonCallback(value):
    if a.get() == 1:
        if value == 1:
            if "Manu" not in ausgewaehlteSpieler:
                ausgewaehlteSpieler.append("Manu")
    if b.get() == 1:
        if value == 2:
            if "Jan" not in ausgewaehlteSpieler:
                ausgewaehlteSpieler.append("Jan")
    if c.get() == 1:
        if value == 3:
            if "Simon" not in ausgewaehlteSpieler:
                ausgewaehlteSpieler.append("Simon")
    if d.get() == 1:
        if value == 4:
            if "Max" not in ausgewaehlteSpieler:
                ausgewaehlteSpieler.append("Max")
    if e.get() == 1:
        if value == 5:
            if "Maido" not in ausgewaehlteSpieler:
                ausgewaehlteSpieler.append("Maido")
    if f.get() == 1:
        if value == 6:
            if "Felix" not in ausgewaehlteSpieler:
                ausgewaehlteSpieler.append("Felix")
    if g.get() == 1:
        if value == 7:
            if "Dome" not in ausgewaehlteSpieler:
                ausgewaehlteSpieler.append("Dome")
    if h.get() == 1:
        if value == 8:
            if "Moritz" not in ausgewaehlteSpieler:
                ausgewaehlteSpieler.append("Moritz")
    #Leute wieder aus der liste nehemn wenn haken raus gemacht wird!
    if a.get() == 0:
        if value == 1:
            if "Manu" in ausgewaehlteSpieler:
                ausgewaehlteSpieler.remove("Manu")
    if b.get() == 0:
        if value == 2:
            if "Jan" in ausgewaehlteSpieler:
                ausgewaehlteSpieler.remove("Jan")
    if c.get() == 0:
        if value == 3:
            if "Simon" in ausgewaehlteSpieler:
                ausgewaehlteSpieler.remove("Simon")
    if d.get() == 0:
        if value == 4:
            if "Max" in ausgewaehlteSpieler:
                ausgewaehlteSpieler.remove("Max")
    if e.get() == 0:
        if value == 5:
            if "Maido" in ausgewaehlteSpieler:
                ausgewaehlteSpieler.remove("Maido")
    if f.get() == 0:
        if value == 6:
            if "Felix" in ausgewaehlteSpieler:
                ausgewaehlteSpieler.remove("Felix")
    if g.get() == 0:
        if value == 7:
            if "Dome" in ausgewaehlteSpieler:
                ausgewaehlteSpieler.remove("Dome")
    if h.get() == 0:
        if value == 8:
            if "Moritz" in ausgewaehlteSpieler:
                ausgewaehlteSpieler.remove("Moritz")

    if i.get() == 1:
        if value == 9:
            if "Leon" not in ausgewaehlteSpieler:
                ausgewaehlteSpieler.append("Leon")
    if j.get() == 1:
        if value == 10:
            if "Kilian" not in ausgewaehlteSpieler:
                ausgewaehlteSpieler.append("Kilian")

    if i.get() == 0:
        if value == 9:
            if "Leon" in ausgewaehlteSpieler:
                ausgewaehlteSpieler.remove("Leon")
    if j.get() == 0:
        if value == 10:
            if "Kilian" in ausgewaehlteSpieler:
                ausgewaehlteSpieler.remove("Kilian")

    if k.get() == 1:
        if value == 11:
            if "Paul" not in ausgewaehlteSpieler:
                ausgewaehlteSpieler.append("Paul")
    if k.get() == 0:
        if value == 11:
            if "Paul" in ausgewaehlteSpieler:
                ausgewaehlteSpieler.remove("Paul")


# Checkbuttons
check1 = ttk.Checkbutton(checkframe, text='Manu', variable=a, command=lambda: buttonCallback(1))
check1.place(x=20, y=20)

check2 = ttk.Checkbutton(checkframe, text='Jan', variable=b, command=lambda: buttonCallback(2))
check2.place(x=20, y=60)

check3 = ttk.Checkbutton(checkframe, text='Simon', variable=c, command=lambda: buttonCallback(3))
check3.place(x=20, y=100)

check4 = ttk.Checkbutton(checkframe, text='Max', variable=d, command=lambda: buttonCallback(4))
check4.place(x=20, y=140)

check5 = ttk.Checkbutton(checkframe, text='Maido', variable=e, command=lambda: buttonCallback(5))
check5.place(x=20, y=180)

check6 = ttk.Checkbutton(checkframe, text='Felix', variable=f, command=lambda: buttonCallback(6))
check6.place(x=20, y=220)

check7 = ttk.Checkbutton(checkframe, text='Dome', variable=g, command=lambda: buttonCallback(7))
check7.place(x=20, y=260)

check8 = ttk.Checkbutton(checkframe, text='Moritz', variable=h, command=lambda: buttonCallback(8))
check8.place(x=20, y=300)

check9 = ttk.Checkbutton(checkframe, text='Leon',variable=i,command=lambda: buttonCallback(9))
check9.place(x=20, y=340)

check10 = ttk.Checkbutton(checkframe, text='Kilian',variable=j,command=lambda: buttonCallback(10))
check10.place(x=20, y=380)

check11 = ttk.Checkbutton(checkframe, text='Paul',variable=k,command=lambda: buttonCallback(11))
check11.place(x=20, y=420)

# Create a frame for the Treeview
treex = 250
treeFrame = ttk.Frame(root)
treeFrame.place(x=treex, y=21)  # hehe <-- Nice :D <-- leider nimmer nice wegen der neuen buttons

# Scrollbar
treeScroll = ttk.Scrollbar(treeFrame)
treeScroll.pack(side='right', fill='y')

# Treeview setup
treeview = ttk.Treeview(treeFrame, selectmode="extended", height=12)
treeview.pack()
treeview.column("#0", width=360)
treeview.heading("#0", text="DAS wollen wir spielen", anchor='center')


# Insert data into Treeview

def insertData(DATA):
    treeview.delete(*treeview.get_children())
    parent = treeview.insert(parent='', index='end', iid=1, text="Common Games")
    for x in DATA[0]:
        treeview.insert(1, tk.END, text=x)
    parent = treeview.insert(parent='', index='end', iid=2, text="Remote Play Games")
    for x in DATA[1]:
        treeview.insert(2, tk.END, text=x)


# Copy games to clipboard
def copyGamestoCB(*data):
    pyperclip.copy(str(data))


# Button callback
def accentCallback():
    if ausgewaehlteSpieler:
        spieleDaten = gameData(gameDataFile="gameData.json", failDataFile="requestFails.json")
        DATA = spieleDaten.getRankedGames(ausgewaehlteSpieler,sortierModus.get()) #wenn hier false steht wird gesamtspielzeit als ranking genutzt
        insertData(DATA)
        if (z.get() == 1):
            button = ttk.Button(root, text='Copy Games', command=lambda: copyGamestoCB(DATA), width = 12)
            button.place(x=treex+200, y=320)

    else:
        z.set(0)


def copyGamestoCB(*data):
    pyperclip.copy(str(data))

def updateGames():
    spieleDaten = gameData(gameDataFile="gameData.json", failDataFile="requestFails.json")
    spieleDaten.updateGameData()
    spieleDaten.spielerAnzahlEintragen()

def addGameByHand():
    spieleDaten = gameData(gameDataFile="gameData.json", failDataFile="requestFails.json")
    spielerAuswahlen = input("Spieler sind: "+ str(ausgewaehlteSpieler) + " stimmt das so? Bitte mit \"ja\" bestätigen:")
    if spielerAuswahlen == "ja":
        player = ausgewaehlteSpieler
    else:
        print("Es wurde nichts Hinzugefügt")
        return
    name = input("Spiel Name bitte eingeben: ")
    numSpieler = int(input("Anzahl der Spieler bitte eingeben: "))
    gameId = input("Bitte falls vorhanden die Game ID eingeben, falls hier keine zahl ist bitte leer lassen:  ")
    if gameId == "":
        gameId = "Keine Game ID spezifiziert"
    else:
        gameId=int(gameId)

    abfrage = input("Es wird also für die Spieler: " + str(player) +
          " das Spiel: " + str(name) +
          " mit einer Spieleranzahl von: " +  str(numSpieler) +
          " und der Game Id: " + str(gameId) +
          " hinzugefügt. Stimmen diese daten mit \"ja\" bestätigen: ")
    if gameId == "Keine Game ID spezifiziert":
        gameId = None
    if abfrage == "ja":
        spieleDaten.addGameByHand(player, gameName=name, spielerAnzahl=numSpieler, gameID=gameId)
        spieleDaten.save()
    else:
        print("Es wurde, wegen nicht erfolgter Bestätigung, kein Spiel hinzugefügt")

def sortSwitch():
    if sortierModus.get():
        sortierModus.set(False)
        sortierName.set("Sortiert nach der Gesamtspielzeit")
    else:
        sortierModus.set(True)
        sortierName.set("Sortiert nach der Spielzeit der letzten 2 Wochen")




# AccentButton
accentbutton = ttk.Checkbutton(root,text='Gib Games',style='AccentButton',variable=z,width=12,command=accentCallback)
accentbutton.place(x=treex+300, y=320)

#Update button
updateButton = ttk.Button(root, text="Update Spiele", command=updateGames,width = 12)
updateButton.place(x=treex+100,y=320)

#Add Game by hand Button
addGameButton = ttk.Button(root, text='Add Game', command=addGameByHand, width = 12)
addGameButton.place(x=treex,y=320)

#toggle von sortierung als button
sortierArt = ttk.Checkbutton(root, textvariable=sortierName, style= "Switch", command=sortSwitch, variable=w)
sortierArt.place(x=treex, y=360)

root.mainloop()
