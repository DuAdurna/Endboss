# Importing tkinter,tkinter.ttk and utilities
import tkinter as tk
from tkinter import ttk
from util import *
import pyperclip
# Create the window
root = tk.Tk()
root.title('Was wollen wir spielen?')

# Place the window in the center of the screen
windowWidth = 800
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
x = tk.IntVar()
y = tk.IntVar()
z = tk.IntVar()

ausgewaehlteSpieler = []

# Create a frame for the Checkbuttons
checkframe = ttk.LabelFrame(root, text='Spieler', width=210, height=460)
checkframe.place(x=20, y=12)

#Callback function for Checkbuttons
def buttonCallback(value):
    # if(manu[0].get() == 1):
    #     print('Manu callback')
    if a.get() ==1:
        if value == 1:
            ausgewaehlteSpieler.append("Manu")
    if b.get() == 1:
        if value == 2:
            ausgewaehlteSpieler.append("Jan")
    if c.get() == 1:
        if value == 3:
            ausgewaehlteSpieler.append("Simon")
    if d.get() == 1:
        if value == 4:
            ausgewaehlteSpieler.append("Max")
    if e.get() == 1:
        if value == 5:
            ausgewaehlteSpieler.append("Maido")
    if f.get() == 1:
        if value == 6:
            ausgewaehlteSpieler.append("Felix")
    if g.get() == 1:
        if value == 7:
            ausgewaehlteSpieler.append("Dome")

    if h.get() == 1:
        if value == 8:
            ausgewaehlteSpieler.append("Moritz")

    if i.get() == 1:
        if value == 9:
            ausgewaehlteSpieler.append("Leon")

    if j.get() == 1:
        if value == 10:
            ausgewaehlteSpieler.append("Kilian")



    #
    # if (b.get() == 1):
    #     print('Jan callback')
    #     ausgewaehlteSpieler.append("Jan")
    #
    #
    print(ausgewaehlteSpieler)


# Checkbuttons
check1 = ttk.Checkbutton(checkframe, text='Manu',variable=a,command=lambda: buttonCallback(1))
check1.place(x=20, y=20)


check2 = ttk.Checkbutton(checkframe, text='Jan',variable=b,command=lambda: buttonCallback(2))
check2.place(x=20, y=60)


check3 = ttk.Checkbutton(checkframe, text='Simon',variable=c,command=lambda: buttonCallback(3))

check3.place(x=20, y=100)
check4 = ttk.Checkbutton(checkframe, text='Max',variable=d,command=lambda: buttonCallback(4))
check4.place(x=20, y=140)

check5 = ttk.Checkbutton(checkframe, text='Maido',variable=e,command=lambda: buttonCallback(5))
check5.place(x=20, y=180)

check6 = ttk.Checkbutton(checkframe, text='Felix',variable=f,command=lambda: buttonCallback(6))
check6.place(x=20, y=220)

check7 = ttk.Checkbutton(checkframe, text='Dome',variable=g,command=lambda: buttonCallback(7))
check7.place(x=20, y=260)

check8 = ttk.Checkbutton(checkframe, text='Moritz',variable=h,command=lambda: buttonCallback(8))
check8.place(x=20, y=300)
check9 = ttk.Checkbutton(checkframe, text='Leon',variable=i,command=lambda: buttonCallback(9))
check9.place(x=20, y=340)
check10 = ttk.Checkbutton(checkframe, text='Kilian',variable=j,command=lambda: buttonCallback(10))
check10.place(x=20, y=380)



# Create a frame for the Treeview
treeFrame = ttk.Frame(root)
treeFrame.place(x=420, y=21) #hehe

# Scrollbar
treeScroll = ttk.Scrollbar(treeFrame)
treeScroll.pack(side='right', fill='y')

# Treeview setup
treeview = ttk.Treeview(treeFrame,selectmode="extended",height=12)
treeview.pack()
treeview.column("#0", width=333)
treeview.heading("#0", text="DAS wollen wir spielen", anchor='center')

# Insert data into Treeview

def insertData(DATA):
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
        DATA = spieleDaten.getCommonGames(ausgewaehlteSpieler)
        insertData(DATA)
        print(DATA)
        if(z.get() == 1):
            button = ttk.Button(root, text='Copy Games', command=lambda: copyGamestoCB(DATA))
            button.place(x=600, y=320)

    else: z.set(0)


def copyGamestoCB(*data):
    pyperclip.copy(str(data))




# AccentButton
accentbutton = ttk.Checkbutton(root, text='Gib Games', style='AccentButton', variable=z, command=accentCallback)
accentbutton.place(x=700, y=320)





root.mainloop()



