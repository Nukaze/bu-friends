import sqlite3
from sqlite3 import Error
from tkinter import *
# connecting to database
class DBController() :
    def create_connection():
        conn = None
        try:
            conn = sqlite3.connect(r"./database/BUFriends.db")
            conn.execute("PRAGMA foreign_keys = 1")
            print(sqlite3.version)
        except Error as e:
            print(e)
        return conn

    def exucute_sql(conn, sql):
        try:
            c = conn.cursor()
            c.execute(sql)
            conn.commit()
        except Error as e:
            print(e)
    ''' เวลาเรียกใช้
        conn = DBController.create_connection()
        sql = """คำสั่ง SQL"""
    if conn is not None:
            DBController.exucute_sql(conn, sql)
    else:
        print("Error! cannot create the database connection.")'''
# set a main window 
class BUFriends(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.frame = None
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        w,h = 900,600
        x = (screenwidth//2)-(w//2)
        y = (screenheight//2-50)-(h//2)
        self.geometry("{}x{}+{}+{}".format(w,h,x,y))
        self.iconbitmap("assets/icons/BUF.ico")
        self.resizable(0,0)
        self.switch_frame(PageOne)
# switch page event
    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self.frame is not None:
            self.frame.destroy()
        self.frame = new_frame
        self.configure(bg = self.frame.bgColor)
        self.frame.pack()
# page 1
class PageOne(Frame):
    def __init__(self, master):
        self.bgColor = 'lightblue'
        Frame.__init__(self, master)
        Frame.configure(self,bg=self.bgColor)
        # widget หลังจากนี้จะทำเป็น def หรือ class หรือเป็นพรืดก็ตามสะดวกใจเลย
        # ex.ปุ่มดปลี่ยนหน้าแบบเป็นพรืด
        Label(self, text="Page one", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
        Button(self, text="Go to second page",
                  command=lambda: master.switch_frame(PageTwo)).pack()      
# page 2
class PageTwo(Frame):
    def __init__(self, master):
        self.master = master
        self.bgColor = 'lightpink'
        Frame.__init__(self, master)
        Frame.configure(self,bg="black")
        # widget หลังจากนี้จะทำเป็น def หรือ class หรือเป็นพรืดก็ตามสะดวกใจเลย
        # ex.ปุ่มดปลี่ยนหน้าแบบdef
        self.widget(self)
    def widget(self,root) :
        Label(root, text="Page one", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
        Button(root, text="Go to third page",
                  command=lambda: self.master.switch_frame(PageThree)).pack()  
# page 3
class PageThree(Frame):
    def __init__(self, master):
        self.master = master
        self.bgColor = 'lightgreen'
        Frame.__init__(self, master)
        Frame.configure(self,bg=self.bgColor)
        # widget หลังจากนี้จะทำเป็น def หรือ class หรือเป็นพรืดก็ตามสะดวกใจเลย
        # ex.ปุ่มดปลี่ยนหน้าแบบclass
        self.widget(self,master)
    class widget() :
        def __init__(self, root,controller):
            Label(root, text="Page Three", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
            Button(root, text="Go to first page",
                    command=lambda: controller.switch_frame(PageOne)).pack()  

if __name__ == "__main__":
    app = BUFriends()
    app.mainloop()