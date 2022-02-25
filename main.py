'''
    Hello BUFriends (lifestyle personalities etc.)
    ehe ehe ehe I will have order to kiss you in theatre <3
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
            imglst.append(img)
    def init_root():
        root = tk.Tk()
        root.title("BU Friends  | ")
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        w,h = 900,600
        x = (screenwidth/2)-(w/2)
        y = (screenheight/2-50)-(h/2)
        root.geometry("{}x{}+{}+{}".format(w,h,int(x),int(y)))
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
