'''
    Hello BUFriends
'''
import tkinter as tk
from tkinter import ttk,messagebox
from PIL import Image, ImageTk
from data import mbtiData
import assets

def bu_friends():
    def init_assets():
        assets = ["assets/png/EQgrown.png", "assets/png/BUF.png"]
        for path in assets:
            origin = Image.open(path).resize((160, 160), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(origin)
            img = Image
            imglst.append(img)
    def init_root():
        root = tk.Tk()
        root.title("BU Friends  | ")
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        x = (screenwidth/2)-(1600/2)
        y = (screenheight/2-50)-(800/2)
        root.geometry("{}x{}+{}+{}".format(1600,800,int(x),int(y)))
        root.iconbitmap("assets/icon/BUF.ico")
        root.resizable(0,0)
        return root
    def init_layout():
        pass

    imglst = []
    root = init_root()
    init_assets()
    root.mainloop()

bu_friends()