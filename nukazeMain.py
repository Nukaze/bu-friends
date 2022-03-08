'''
    Nukaze BU Friends
'''
from asyncio import events
from tkinter import *
from tkinter import ttk,messagebox
from tkinter.font import Font
from sqlite3 import Error
import sqlite3
import os
import hashlib
import datetime
from turtle import clear

from gevent import config

def BUFriends_Time():
    timeFull = datetime.datetime.now()
    timeNow = timeFull.strftime("%d-%b-%Y") + " " + timeFull.strftime("( %H:%M:%S )")
    print(timeFull, timeNow)
    return timeNow


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

    def execute_sql(conn, sql):
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
    

class BUcontrollerFrame(Tk):

    def __init__(self):
        Tk.__init__(self)
        self.frame = None
        self.width, self.height = 900, 600
        self.x = ((self.winfo_screenwidth()//2) - (self.width // 2))
        self.y = ((self.winfo_screenheight()//2-50) - (self.height // 2))
        self.geometry("{}x{}+{}+{}".format(self.width, self.height, self.x, self.y))
        self.resizable(0,0)
        self.title("BU Friends  |")
        self.iconbitmap('assets/icons/bufriends.ico')
        self.fontHeading = Font(family="leelawadee",size=36,weight="bold")
        self.fontBody = Font(family="leelawadee",size=16)
        self.option_add('*font',self.fontBody)
        self.switch_frame(SignIn)

    def switch_frame(self, frame_class):
        print("switching to {}".format(frame_class))
        new_frame = frame_class(self)
        if self.frame is not None:
            self.frame.destroy()
        self.frame = new_frame
        self.configure(bg=self.frame.bgColor)
        self.frame.pack(side=BOTTOM, fill=BOTH, expand=TRUE)
        
    def get_image(self, _path):
        img = PhotoImage(file = _path)
        return img
    

class SignIn(Frame):

    def __init__(self, controllerFrame):
        Frame.__init__(self, controllerFrame)
        self.bgColor,self.fg = "#B6E0F7","#cc07e6"
        Frame.configure(self,bg=self.bgColor)
        self.pack()
        self.SignInContent(self, controllerFrame)

    class SignInContent:
        
        def __init__(self, root, controllerFrame):
            self.bg,self.bgentry,self.fghead,self.fg,self.fgHolder = "#B6E0F7","#ffffff","#000000","#333333","#999999"
            self.controllerFrame = controllerFrame
            self.root = root
            self.controllerFrame.title("BU Friends  |  Sign-In")
            self.timeNow = BUFriends_Time()
            #BannerCanva
            def zone_canvas():
                self.canvasFrame = Canvas(root,width=400,height=600,bd=-2)
                self.canvasFrame.pack(side=LEFT,expand=1,fill="both")
                pathLst = ['assets/images/banner.png','assets/images/character.png']
                self.imgLst = []
                for i,data in enumerate(pathLst):
                    self.imgLst.append(self.controllerFrame.get_image(data))
                    self.canvasFrame.create_image(0,0,image=self.imgLst[i],anchor="nw")
            #widgetAll
            def zone_entrys():    
                self.signinFrame = Frame(root,bg=self.bg,width=500,height=600)
                self.signinFrame.propagate(0)
                self.mainFrame = Frame(self.signinFrame,bg=self.bg)
                Label(self.mainFrame,text="BU Friends",font=self.controllerFrame.fontHeading,bg=self.bg,fg=self.fghead,justify="left")\
                    .pack(side=TOP,expand=1,padx=30,pady=2)
                self.entryFrame = Frame(self.mainFrame,bg=self.bg)
                self.entryImg = self.controllerFrame.get_image('assets/entrys/entry1rz.png')
                self.entryicon1 = self.controllerFrame.get_image('assets/icons/user.png')
                self.entryicon2 = self.controllerFrame.get_image('assets/icons/lock.png')
                self.icon1 = Label(root,image=self.entryicon1,bg=self.bgentry)
                self.icon2 = Label(root,image=self.entryicon2,bg=self.bgentry)
                self.icon1.place(relx=0.55,rely=0.38)
                self.icon2.place(relx=0.55,rely=0.485)
                Label(self.entryFrame,image=self.entryImg,bg=self.bg).pack(pady=10)
                Label(self.entryFrame,image=self.entryImg,bg=self.bg,width=350,height=50).pack()
                self.userName = Entry(self.entryFrame,width=25,justify="left",relief="flat")
                self.userPass = Entry(self.entryFrame,width=25,show="*",justify="left",relief="flat")
                self.userEntryLst = [[self.userName,"Enter BU-Mail"],[self.userPass,"Enter Password"]]
                def binding_events():
                    def clear_event(index):    
                        self.userEntryLst[index][0].delete(0,END)
                        self.userEntryLst[index][0].config(fg=self.fg)
                    def key_event(index):
                        self.userEntryLst[index][0].config(fg=self.fg)
                    def entry_binding(i):
                        self.userEntryLst[i][0].insert(0,self.userEntryLst[i][1])
                        self.userEntryLst[i][0].config(fg=self.fgHolder)
                        self.userEntryLst[i][0].bind('<Button-1>',lambda e,index=i:clear_event(i))
                        self.userEntryLst[i][0].bind('<Key>',lambda e,index=i:key_event(i))
                    for i in range(len(self.userEntryLst)):
                        entry_binding(i)
                binding_events()
                self.userName.place(relx=0.17,rely=0.18)
                self.userPass.place(relx=0.17,rely=0.70)
                    
            def zone_buttons():
                self.frameBtn = Frame(self.mainFrame, bg=self.bg)
                self.imgBtn = self.controllerFrame.get_image('assets/buttons/buttonRaw.png')
                self.loginBtn = Button(self.frameBtn, text="Log-in", command=self.login_req, image=self.imgBtn
                                       , foreground="white", bg=self.bg,
                                    activebackground=self.bg,activeforeground="white",bd=0,compound="center")
                self.loginBtn.pack(side=TOP,pady=10,ipady=0,padx=3,expand=1)
                self.frameDonthave = Frame(self.frameBtn,bg=self.bg)
                Label(self.frameDonthave,text="Don't have an account?",font="leelawadee 10",bg=self.bg).pack(side="left",expand=1)
                self.signupBtn = Label(self.frameDonthave,text="Sign-Up",font="leelawadee 10 underline",bg=self.bg,fg="#0000ff")
                self.signupBtn.bind('<Enter>',self.signup_mouseover)
                self.signupBtn.bind('<Leave>',self.signup_mouseleave)
                self.signupBtn.bind('<Button-1>',self.signup_req)
            #callwidgets
            zone_canvas()
            zone_entrys()
            zone_buttons()
            #displayFrame
            self.signinFrame.pack(side="top",expand=1,fill="both")
            self.mainFrame.pack(expand=1,pady=50,ipady=50)
            self.entryFrame.pack(side="top",expand=1)
            self.frameBtn.pack(side="top", pady=0, expand=1)
            self.frameDonthave.pack(side="bottom",expand=1)
            self.signupBtn.pack(side=LEFT,padx=3)
        
        def signup_mouseover(self,e):
            self.signupBtn.config(fg="#7700ff")
        def signup_mouseleave(self,e):
            self.signupBtn.config(fg="#0000ff")
        
        def login_req(self):
            print(self.userName.get())
            print(self.userPass.get())
            self.controllerFrame.switch_frame(DashBoard)
        
        def login_submit(self):
            pass
        
        def signup_req(self,e):
                self.controllerFrame.switch_frame(SignUp)
            

class SignUp(Frame):

    def __init__(self,controllerFrame):
        Frame.__init__(self,controllerFrame)
        self.bgColor = "#ccefff"
        Frame.configure(self,bg=self.bgColor)
        self.pack()
        self.SignUpContent(self,controllerFrame)

    class SignUpContent:
        def __init__(self, root, controllerFrame):
            self.controllerFrame = controllerFrame
            self.root = root
            self.controllerFrame.title("BU Friends |  Sign-Up")
            self.bg,self.fgHead,self.fg,self.fgHolder = "#ccefff","#000000","#333333","#999999"
            self.regisInfoLst = ["Enter your BU-Mail", "enter Password1", "enter Password2", "Enter your Display Name"]
            self.regisVarData,self.regisDataSubmit = [],[]         
            self.canvasFrame = Canvas(root,width=900,height=600,bd=0)
            self.canvasFrame.pack(expand=1,fill="both")
            self.bgImg = self.controllerFrame.get_image("assets/images/regisbg.png")
            self.canvasFrame.create_image(0,0,image=self.bgImg,anchor="nw")
            self.canvasFrame.create_text(450,80,text="Registration",font="leelawadee 36 bold", fill=self.fgHead)
            def zone_widgets():
                self.entryLst = []
                self.entryimg = self.controllerFrame.get_image('assets/entrys/entry2rz.png')
                for i in range(len(self.regisInfoLst)):
                    self.regisVarData.append(StringVar())
                    self.entryLst.append(self.signup_form(self.root, i, self.regisVarData[i]))
                    x,y = 260,70*(i+2)
                    self.canvasFrame.create_image(x,y,image=self.entryimg,anchor="nw")
                    self.entryLst[i].place(x=x+20,y=y+10)
                def events():
                    def clear_event(index):
                        self.entryLst[index].delete(0,END)
                        self.entryLst[index].config(fg=self.fg)
                    def key_event(index):
                        self.entryLst[index].config(fg=self.fg)
                    def entry_binding(i):
                        self.entryLst[i].bind('<Button-1>',lambda e, index=i:clear_event(i))
                        self.entryLst[i].bind('<Key>', lambda e, index=i:key_event(i))
                    for i in range(len(self.entryLst)):
                        entry_binding(i)
                events()                
            zone_widgets()
            def zone_buttons():
                self.imgBtn = self.controllerFrame.get_image('assets/buttons/signuprz.png')
                self.imgBtn2 = self.controllerFrame.get_image('assets/buttons/buttonGreyrz.png')
                self.signupBtn = Button(root, text="Sign Up", command=self.signup_submit, image=self.imgBtn,fg="#ffffff"
                                       ,bd=-10,compound="center")
                self.backBtn = Button(root, text="Cancel", command=lambda:self.controllerFrame.switch_frame(SignIn), image=self.imgBtn2
                                       , foreground="white",bd=-10,compound="center")
                self.signupWin = self.canvasFrame.create_window(240,430,anchor="nw",window=self.signupBtn)
                self.backWin = self.canvasFrame.create_window(500,445,anchor="nw",window=self.backBtn)
            zone_buttons() 
            
        def signup_form(self,_root, _idx, _entVar):
            entry = Entry(_root, textvariable=_entVar, justify="left",relief="flat",fg=self.fgHolder,width=30)
            entry.insert(0,self.regisInfoLst[_idx])
            if _idx == 1 or _idx == 2:
                entry.config(show="*")
            return entry
            
        def signup_submit(self):
                def register_error(errorFormat="unknow error"):
                    self.regisVarData.clear()
                    self.regisDataSubmit.clear()
                    messagebox.showinfo('Sign Up Error', '{}\nPlease Register Form Again'.format(errorFormat))
                    self.controllerFrame.switch_frame(SignUp)
               
                def signup_validate(self):
                    for i,data in enumerate(self.regisVarData):
                        if data.get() == "" or data.get().isspace():
                            register_error("Register Form Information not Complete")
                            break
                    signup_email_validate(self)

                def signup_email_validate(self):
                    if "@bumail.net" not in self.regisVarData[0].get():
                        register_error("BU controllerFrame Exclusive for BU Mail only")
                    signup_password_validate(self)
                            
                def signup_password_validate(self):
                    for i,data in enumerate(self.regisVarData):
                        if self.regisVarData[1].get() != self.regisVarData[2].get():
                            register_error("Password is not Matching")
                            break
                        else:self.regisDataSubmit.append(data.get())
                    self.regisDataSubmit.pop(2)    #remove second password
                    signup_confirm(self)
                    
                def signup_confirm(self):
                    print(self.regisDataSubmit)
                    # sqlSignupUser = """INSERT INTO user (email, password, displayname)
                    #                                 VALUES({},{},{});""".format(self.sign)
                    # conn = DBController()
                    # conn.execute_sql(sqlSignupUser)
                    messagebox.showinfo('Sign Up Successfully'
                                        ,"BUMail : {} Password1 {}\nDisplayName : {}".format(*self.regisDataSubmit))
                    messagebox.showinfo('Redirecting',"Going to BU Friends  | Sign-in")
                    self.controllerFrame.switch_frame(SignIn)
                for i,data in enumerate(self.regisVarData):
                    print(data.get())
                    
                signup_validate(self)


class DashBoard(Frame):

    def __init__(self,controllerFrame):
        Frame.__init__(self,controllerFrame)
        self.bgColor = "grey"
        Frame.configure(self,bg=self.bgColor)
        self.pack(expand=1)
        self.DashBoardContent(self,controllerFrame)

    class DashBoardContent:

        def __init__(self, root,controllerFrame):
            self.bg,self.fg = "#ccefff","#cc07e6"
            self.controllerFrame = controllerFrame
            self.controllerFrame.title("BU Friends  |  Dashboard")
            Label(root, text="Dashboard",font=self.controllerFrame.fontHeading).pack()
            self.entryFrame = Canvas(root,bg=self.bg,width=500,height=500)
            self.entryFrame.propagate(0)
            self.entryImg = self.controllerFrame.get_image('assets/entrys/entry1.png')
            Label(self.entryFrame,image=self.entryImg,bg=self.bg).place(relx=0.5,rely=0.5,anchor="center")
            Label(self.entryFrame,image=self.entryImg,bg=self.bg).place(relx=0.5,rely=0.5,anchor="center")
            Label(root,image=self.entryImg,bg="pink").pack(expand=1,fill=BOTH)
            self.entryFrame.pack(expand=1)

        def ehe(self):
            print("ehe nun dayo")


if __name__ == '__main__':
    sqlnewtable = """ CREATE TABLE IF NOT EXISTS testTable(
                                    id integer(20) PRIMARY KEY,
                                    bumail text(50) NOT NULL,
                                    passwordx password NOT NULL,
                                    displayname varchar(50) NOT NULL
                                    );"""
                                    
    sqlinto = """INSERT INTO user (email, password, displayname)
                                    VALUES("{}","{}","{}");""".format("hehe@bumail","12345","Woohoo~")
                                    
    sqldel = """DELETE FROM user WHERE id={}"""#.format(needDel) 
    sqldrop = """ DROP TABLE testTable;"""
    conn = DBController.create_connection()
    if conn is not None:
        print("connection complete!")
        #DBController.execute_sql(conn, sqlinto)
    else:
        print("Error Connection incomplete!")
    BUcontrollerFrame().mainloop()