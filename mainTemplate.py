import sqlite3
import hashlib
import random
import os
from sqlite3 import Error
from tkinter import *
from tkinter import ttk,messagebox
from tkinter.font import Font
from PIL import Image, ImageTk
            
class BUFriends(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.frame = None
        self.uid = 0
        self.uidSelect = 0
        self.mbtiCode = ""
        self.width, self.height = 900, 600
        self.x = ((self.winfo_screenwidth()//2) - (self.width // 2))
        self.y = ((self.winfo_screenheight()//2-50) - (self.height // 2))
        self.geometry("{}x{}+{}+{}".format(self.width, self.height, self.x, self.y))
        self.resizable(0,0)
        self.title("BU Friends  |")
        self.iconbitmap(r'./assets/icons/bufriends.ico')
        self.fontHeading = Font(family="leelawadee",size=36,weight="bold")
        self.fontBody = Font(family="leelawadee",size=16)
        self.option_add('*font',self.fontBody)
        self.switch_frame(PageOne)
# switch page event
    def switch_frame(self, frameClass):
        print("switching to {} \n=|with uid = {}".format(frameClass, self.uid))
        new_frame = frameClass(self)
        if self.frame is not None:
            self.frame.destroy()
        self.frame = new_frame
        self.config(bg = self.frame.bgColor)
        self.frame.pack(side=BOTTOM, fill=BOTH, expand=TRUE)
# Database Connection
    def create_connection(self):
        try:
            self.conn = sqlite3.connect(r"./database/BUFriends.db")
            self.conn.execute("PRAGMA foreign_keys = 1")                 # Allow Foreign Key
            print(sqlite3.version)
        except Error as e:
            print(e)
        return self.conn
    
    def execute_sql(self, sql, values=None):
        if values is None:
            try:
                self.c = self.conn.cursor()
                self.c.execute(sql)
                self.conn.commit()
            except Error as e:
                print(e)
        else:
            try:
                self.c = self.conn.cursor()
                self.c.execute(sql, values)
                self.conn.commit()
            except Error as e:
                print(e)
        return self.c
    
# get image raw and resize from path
    def get_image(self, _path, _width=None, _height=None):
            if _width is not None and _height is not None:
                ori = Image.open(_path).resize((_width,_height),Image.ANTIALIAS)
                img = ImageTk.PhotoImage(ori)
            else:
                
                img = PhotoImage(file = _path)
            return img
    
    def password_encryptioncheck(self, _password, _salt):
            stdhash = 'sha256'
            stdencode = 'utf-8'
            passkey = hashlib.pbkdf2_hmac(stdhash, _password.encode(stdencode), _salt, 161803)
            return passkey
    
class ScrollFrame():
    def __init__(self,root,scrollable,bgColor='white'):
        # creating
        self.root = root
        self.bgColor = bgColor
        self.scrollable = scrollable
        self.scrollbar = Scrollbar(self.root, orient=VERTICAL,width=0)
        #self.scrollbar.pack(fill=Y, side=RIGHT, expand=0)
        self.canvas = Canvas(self.root,bg=self.bgColor, highlightthickness=0, yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=1)
        self.scrollbar.config(command=self.canvas.yview)
        # reset the view
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = Frame(self.canvas,bg=self.bgColor)
        self.interior_id = self.canvas.create_window(0, 0, window=self.interior,anchor=NW)

        self.interior.bind('<Configure>', self._configure_interior)
        self.canvas.bind('<Configure>', self._configure_canvas)
        self.canvas.bind('<Enter>', self._bind_to_mousewheel)
        self.canvas.bind('<Leave>', self._unbind_from_mousewheel)
        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar

    def _configure_interior(self, event):
        # update the scrollbars to match the size of the inner frame
        size = (self.interior.winfo_reqwidth(), self.interior.winfo_reqheight())
        self.canvas.config(scrollregion="0 0 %s %s" % size)

        if self.interior.winfo_reqwidth() != self.root.winfo_width():
            # update the canvas's width to fit the inner frame
            self.canvas.config(width=self.interior.winfo_reqwidth())

    def _configure_canvas(self, event):
        if self.interior.winfo_reqwidth() != self.root.winfo_width():
            # update the inner frame's width to fill the canvas
            self.canvas.itemconfigure(self.interior_id, width=self.root.winfo_width())

    # This can now handle either windows or linux platforms
    def _on_mousewheel(self, event):
        if self.scrollable == TRUE :
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        else :
            self.canvas.yview_scroll(0, "units")
    def _bind_to_mousewheel(self, event):
        self.root.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_from_mousewheel(self, event):
        self.root.unbind_all("<MouseWheel>")
        
        
class PageOne(Frame):
    def __init__(self,controller):
        Frame.__init__(self,controller)
        self.bgColor = 'lightblue'
        self.controller = controller
        Frame.configure(self,bg=self.bgColor)
        scroll = ScrollFrame(self,TRUE)
        master = scroll.interior
        # widget หลังจากนี้จะทำเป็น def หรือ class หรือเป็นพรืดก็ตามสะดวกใจเลย
        # ex.ปุ่มดปลี่ยนหน้าแบบพรืด
        for index in range(50):
            item = Entry(master)
            item.insert(0, index)
            item.pack(side=TOP, fill=X, expand=TRUE)
        Button(master, text="Go to second page",
                  command=lambda: self.controller.switch_frame(PageTwo)).pack()  
        
        
class PageTwo(Frame):
    def __init__(self,controller):
        Frame.__init__(self,controller)
        self.bgColor = 'lightpink'
        self.controller = controller
        Frame.configure(self,bg=self.bgColor)
        scroll = ScrollFrame(self,FALSE)
        master = scroll.interior
        # widget หลังจากนี้จะทำเป็น def หรือ class หรือเป็นพรืดก็ตามสะดวกใจเลย
        # ex.ปุ่มดปลี่ยนหน้าแบบdef
        self.widget(master)
    def widget(self,root) :
        Label(root, text="Page two", font=self.controller.fontHeaing).pack(side="top", pady=5)
        Button(root, text="Go to third page",
                  command=lambda: self.controller.switch_frame(PageThree)).pack() 
        
        
class PageThree(Frame):
    def __init__(self,controller):
        Frame.__init__(self,controller)
        self.bgColor = 'lightblue'
        self.controller = controller
        Frame.configure(self,bg=self.bgColor)
        scroll = ScrollFrame(self,TRUE)
        master = scroll.interior  
        # widget หลังจากนี้จะทำเป็น def หรือ class หรือเป็นพรืดก็ตามสะดวกใจเลย
        # ex.ปุ่มดปลี่ยนหน้าแบบclass
        self.widget(master,controller)
        
    class widget() :
        def __init__(self,master,controller):
            self.controller = controller
            for index in range(100):
                item = Label(master,text=index)
                item.pack(side=TOP, fill=X, expand=TRUE)
            Button(master, text="Go to first page",
                    command=lambda: self.controller.switch_frame(PageOne)).pack() 
 
if __name__ == '__main__':
    BUFriends().mainloop()
