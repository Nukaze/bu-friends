'''
    demo BUFriends
'''
from cmath import exp
from email.mime import image
from tkinter import *
from tkinter import messagebox
from tkinter import font
from tkinter.font import Font
from webbrowser import get
import pyglet, tkinter
from PIL import Image,ImageTk
import os
import hashlib
import sqlite3
import datetime



def BUFriends_Time():
    timeFull = datetime.datetime.now()
    timeNow = timeFull.strftime("%d-%b-%Y") + " " + timeFull.strftime("( %H:%M:%S )")
    print(timeFull, timeNow)
    return timeNow

class DbController() :
    
    def create_connection():
        conn = None
        try:
            conn = sqlite3.connect(r"./database/BUFriends.db")
            print("sqlite version:",sqlite3.version)
        except sqlite3.Error as e:
            print("conn error",e)
        return conn

    def create_table(conn, create_table_sql):
        try:
            c = conn.cursor()
            c.execute(create_table_sql)
        except sqlite3.Error as e:
            print("create error",e)
    
    def request_createdb():
        pass
        
    def request_register():
        pass
    

class BUFriends(Tk):

    def __init__(self):
        Tk.__init__(self)
        self.frame = None
        self.width, self.height = 900, 600
        self.x = ((self.winfo_screenwidth()//2) - (self.width // 2))
        self.y = ((self.winfo_screenheight()//2-50) - (self.height // 2))
        self.geometry("{}x{}+{}+{}".format(self.width, self.height, self.x, self.y))
        self.resizable(0,0)
        self.title("BU Friends  |")
        self.iconbitmap('assets/icons/BUF.ico')
        self.switch_page(SignIn)

    def switch_page(self, frameClass):
        print("switching to {}".format(frameClass))
        newFrame = frameClass(self)
        if self.frame is not None:
            self.frame.destroy()
        self.frame = newFrame
        self.configure(bg=self.frame.bg)
        self.frame.pack()


class SignIn(Frame):

    def __init__(self, masterFrame):
        Frame.__init__(self, masterFrame)
        self.bg,self.fg = "#ccefff","#cc07e6"
        Frame.configure(self,bg=self.bg)
        self.pack()
        self.SignInContent(self,masterFrame)
        

    class SignInContent:
        def __init__(self, root, masterFrame):
            self.bg,self.fg = "lightblue","black"
            self.masterFrame = masterFrame
            self.masterFrame.title("BU Friends  |  Sign-In")
            self.fontHead = Font(family="leelawadee bold",size=30)
            self.font = Font(family="leelawadee bold",size=16)
            self.timeNow = BUFriends_Time()
            #CANVAS
            self.canvasFrame = Canvas(root,width=400,height=600)
            self.canvasFrame.pack(side=LEFT,expand=1,fill=BOTH)
            self.bannerImg = self.get_image('assets/widgets/banner.png')
            self.mascotImg = self.get_image('assets/widgets/character.png')
            self.canvasFrame.create_image(0,0,image=self.bannerImg,anchor="nw")
            self.canvasFrame.create_image(0,0,image=self.mascotImg,anchor="nw")
            #widget
            self.signinFrame = Frame(root,bg=self.bg,width=500,height=600)
            self.signinFrame.pack(side=LEFT,expand=1,fill=BOTH)
            self.signinFrame.propagate(0)
            self.titleFrame = Frame(self.signinFrame,bg=self.bg)
            self.titleFrame.pack(expand=1,pady=50)
            Label(self.titleFrame,text="BU Friends  |  Log-In",font=self.fontHead,bg=self.bg,foreground=self.fg,justify="left")\
                .pack(side=TOP,expand=1,padx=50,pady=0)
            userName, userPass = StringVar(), StringVar()
            self.userName = Entry(self.signinFrame, textvariable=userName,width=25, font=self.font,justify="center",relief="solid")
            self.userPass = Entry(self.signinFrame, textvariable=userPass,show="*",width=25, font=self.font,justify="center",relief="solid")
            self.userName.insert(0,"Enter BU-Mail")
            self.userPass.insert(0,"Enter Password")
            self.userName.bind('<Button-1>',self.clear_name)
            self.userPass.bind('<Button-1>',self.clear_pass)
            self.userName.pack(pady=6,ipadx=1,ipady=5)
            self.userPass.pack(pady=6,ipadx=1,ipady=5)
            self.frameBtn = Frame(self.signinFrame, bg=self.bg)
            self.frameBtn.pack(side=TOP, pady=20, expand=1)
            self.imgBtn = self.get_image('assets/widgets/raw_button.png')
            self.loginBtn = Button(self.frameBtn, text="Log-in", command=lambda :self.login_req(masterFrame)
                                   , image=self.imgBtn, font=self.font, foreground="white", bg=self.bg,
                                   activebackground=self.bg,activeforeground="white",bd=0,compound="center", )
            self.regisBtn = Button(self.frameBtn, text="Register", command=lambda :masterFrame.switch_page(Registration)
                                    , bg="#edffbf", font=self.font, relief="solid", width=25)
            self.clearBtn = Button(self.frameBtn, text="Quit", command=masterFrame.destroy, font=self.font, relief="solid", width=15)
            self.loginBtn.pack(side=TOP,pady=10,ipady=0,padx=3,expand=1,)
            #self.regisBtn.pack(side=LEFT,padx=3)
            
        def get_image(self,_path):
                #img = ImageTk.PhotoImage(Image.open(_path).resize((_width, _height), Image.ANTIALIAS))
                img = PhotoImage(file= _path)
                return img
            
        def clear_name(self,e):
            self.userName.delete(0, END)
        def clear_pass(self,e):
            self.userPass.delete(0, END)

        def login_req(self,masterFrame):
            print(self.userName.get())
            print(self.userPass.get())
            masterFrame.switch_page(DashBoard)
            #userPass
        
        def login_submit(self):
            pass


class Registration(Frame):

    def __init__(self, masterFrame):
        Frame.__init__(self, masterFrame)
        self.bg = "#ccefff"
        Frame.configure(self,bg=self.bg)
        self.pack()
        self.RegisterContent(self, masterFrame)

    class RegisterContent:

        def __init__(self, root, masterFrame):
            self.bg,self.fg = "#ccefff","#cc07e6"
            self.masterFrame = masterFrame
            self.masterFrame.title("BU Friends  |  Registration")
            self.fontHead = Font(family="fira code bold",size=36)
            self.font = Font(family="Futura",size=16)
            Label(root, text="BU Friends  |  Registration",font=self.fontHead,bg=self.bg,foreground=self.fg)\
                .pack(expand=1,pady=40)
            self.frameRegis = Frame(root,width=500,height=500,bg=self.bg)
            self.frameRegis.pack(expand=1,fill=BOTH,ipadx=10,ipady=10)
            self.regisInfoLst = ["BUMail", "Display Name", "Password", "Confirm Password"]
            self.regisVarData = []
            self.regisDataSubmit = []
            for i in range(len(self.regisInfoLst)):
                self.regisVarData.append(StringVar())
                self.regis_form(self.regisInfoLst[i], self.font, i, self.regisVarData[i])
            self.frameBtn = Frame(self.frameRegis,bg=self.bg)
            self.frameBtn.grid(row=4,column=0,columnspan=3,sticky="e")
            self.regisBtn = Button(self.frameBtn,text="Register!",command=self.regis_submit,relief="solid",width=30,height=3
                                   ,bg="#edffbf")
            self.regisBtn.grid(row=4,column=1,sticky="nsew",padx=2,pady=15)
            self.CancelBtn = Button(self.frameBtn,text="Cancel",command=lambda :self.masterFrame.switch_page(SignIn),relief="solid",width=20,height=2)
            self.CancelBtn.grid(row=4,column=2,sticky="nsew",padx=2,pady=15)

        def regis_form(self,_text,_font,_row,_entVar):
                Label(self.frameRegis, text=_text ,font=_font,anchor="w",bg=self.bg).grid(row=_row,column=0,sticky="nsew",padx=20,pady=10)
                Label(self.frameRegis, text=":", font=_font,anchor="e",bg=self.bg).grid(row=_row,column=1,sticky="nsew",pady=10)
                if _row == 2 or _row ==3:
                    Entry(self.frameRegis, textvariable=_entVar,show="*",font="Kanit 12",justify="left",relief="solid")\
                        .grid(row=_row, column=2, sticky="nsew",padx=5, pady=10,ipadx=80,ipady=2)
                else:
                    Entry(self.frameRegis, textvariable=_entVar, font="Kanit 10", justify="left",relief="solid")\
                        .grid(row=_row, column=2, sticky="nsew",padx=5, pady=10,ipadx=80,ipady=2)

        def regis_submit(self): 
            def register_error(errorFormat=""):
                self.regisVarData.clear()
                self.regisDataSubmit.clear()
                messagebox.showinfo('Register Error', '{}\nPlease Register Form Again'.format(errorFormat))
                self.masterFrame.switch_page(Registration)
            def register_validate(self):
                for i,data in enumerate(self.regisVarData):
                    if data.get() == "" or data.get().isspace():
                        register_error("Register Form Information not Complete")
                        break
                register_email_validate(self)

            def register_email_validate(self):
                if "@bumail.net" not in self.regisVarData[0].get():
                    register_error("BU Friends Exclusive for BU Mail only")
                register_password_validate(self)
                        
            def register_password_validate(self):
                for i,data in enumerate(self.regisVarData):
                    if self.regisVarData[2].get() != self.regisVarData[3].get():
                        register_error("Password is not Matching")
                        break
                    else:self.regisDataSubmit.append(data.get())
                self.regisDataSubmit.pop(-1)    #remove second password
                register_confirm(self)
                
            def register_confirm(self):
                print(self.regisDataSubmit)
                bufdb = DbController()
                bufdb.request_createdb
                bufdb.request_register(*self.regisDataSubmit)
                messagebox.showinfo('Register Successfully'
                                    ,"BUMail : {} DisplayName : {}\nPassword1 : {}\nPassword2 : {}".format(*self.regisDataSubmit))
                messagebox.showinfo('Redirecting',"Going to BU Friends | Log-in")
                self.masterFrame.switch_page(SignIn)
            register_validate(self)

class DashBoard(Frame):

    def __init__(self, masterFrame):
        Frame.__init__(self,masterFrame)
        self.bg = "grey"
        Frame.configure(self,bg=self.bg)
        self.pack(expand=1)
        self.DashBoardContent(self,masterFrame)

    class DashBoardContent:

        def __init__(self, root, masterFrame):
            x = 10
            self.masterFrame = masterFrame
            self.masterFrame.title("BU Friends  |  Dashboard")
            self.fontHead = Font(family="Leelawadee",size=40)
            self.font = Font(family="Futura",size=16)
            Label(root, text="Dashboard",font=self.fontHead).pack()

        def ehe(self):
            print("ehe nun dayo")


if __name__ == '__main__':
    sql = """ CREATE TABLE IF NOT EXISTS testTable(
                                    id integer PRIMARY KEY,
                                    bumail text NOT NULL,
                                    username varchar NOT NULL,
                                    password varchar NOT NULL
                                    );"""
    conn = DbController.create_connection()
    if conn is not None:
        print("connection complete!")
        DbController.create_table(conn, sql)
    else:
        print("Error Connection incomplete!")
    BUFriends().mainloop()