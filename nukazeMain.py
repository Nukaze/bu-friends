'''
    Nukaze BUFriends
'''
from tkinter import *
from tkinter import ttk,messagebox
from tkinter.font import Font
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
            conn = sqlite3.connect("./database/BUFriends.db")
            print("sqlite version:",sqlite3.version)
        except sqlite3.Error as e:
            print("conn error",e)
        return conn

    def execute_sql(conn, sqlCommand):
        try:
            c = conn.cursor()
            c.execute(sqlCommand)
            print("{}\n Complete!".format(sqlCommand))
        except sqlite3.Error as e:
            print("execute sql error",e)
    
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
        #self.resizable(0,0)
        self.title("BU Friends  |")
        self.iconbitmap('assets/icons/bufriends.ico')
        self.switch_frame(SignIn)

    def switch_frame(self, frameClass):
        print("switching to {}".format(frameClass))
        newFrame = frameClass(self)
        if self.frame is not None:
            self.frame.destroy()
        self.frame = newFrame
        self.configure(bg=self.frame.bg)
        self.frame.pack()
        
    def get_imageraw(self, _path):
        img = PhotoImage(file = _path)
        return img
    
    def get_imagerz(self,_path, _width, _height):
        img = ImageTk.PhotoImage(Image.open(_path))
        img = PhotoImage(file= _path).subsample(_width,_height)
        return img


class SignIn(Frame):

    def __init__(self, masterFrame):
        Frame.__init__(self, masterFrame)
        self.bg,self.fg = "#B6E0F7","#cc07e6"
        Frame.configure(self,bg=self.bg)
        self.pack()
        self.Style = ttk.Style()
        self.SignInContent(self,masterFrame)

    class SignInContent:
        
        def __init__(self, root, masterFrame):
            self.bg,self.fg,self.fghead = "#B6E0F7","#444444","black"
            self.masterFrame = masterFrame
            self.masterFrame.title("BU Friends  |  Sign-In")
            self.fontHead = Font(family="leelawadee bold",size=36)
            self.font = Font(family="leelawadee",size=16)
            self.timeNow = BUFriends_Time()
            #BannerCanva
            def zone_canvas():
                self.canvasFrame = Canvas(root,width=400,height=600)
                self.canvasFrame.pack(side=LEFT,expand=1,fill=BOTH)
                self.bannerImg = self.masterFrame.get_imageraw('assets/widgets/banner.png')
                self.mascotImg = self.masterFrame.get_imageraw('assets/widgets/character.png')
                self.canvasFrame.create_image(0,0,image=self.bannerImg,anchor="nw")
                self.canvasFrame.create_image(0,0,image=self.mascotImg,anchor="nw")
            #widgetAll
            def zone_entry():    
                self.signinFrame = Frame(root,bg=self.bg,width=500,height=600)
                self.signinFrame.propagate(0)
                self.mainFrame = Frame(self.signinFrame,bg=self.bg)
                Label(self.mainFrame,text="BU Friends",font=self.fontHead,bg=self.bg,fg=self.fghead,justify="left")\
                    .pack(side=TOP,expand=1,padx=30,pady=2)
                self.entryFrame = Frame(self.mainFrame,bg=self.bg)
                self.entryImg = self.masterFrame.get_imageraw('assets/1signin/entry1rz.png')
                self.entryicon1 = self.masterFrame.get_imageraw('assets/1signin/user.png')
                self.entryicon2 = self.masterFrame.get_imageraw('assets/1signin/lock.png')   
                self.icon1 = Label(root,image=self.entryicon1,bg="white")
                self.icon2 = Label(root,image=self.entryicon2,bg="white")
                self.icon1.place(relx=0.55,rely=0.38)
                self.icon2.place(relx=0.55,rely=0.485)
                Label(self.entryFrame,image=self.entryImg,bg=self.bg).pack(pady=10)
                Label(self.entryFrame,image=self.entryImg,bg=self.bg,width=350,height=50).pack()
                self.userName = Entry(self.entryFrame,width=25,font=self.font,justify="left",relief="flat",fg=self.fg)
                self.userPass = Entry(self.entryFrame,width=25, font=self.font,show="*",justify="left",relief="flat",fg=self.fg)
                self.userName.insert(0,"Enter BU-Mail")
                self.userPass.insert(0,"Enter Password")
                self.userName.bind('<Button-1>',self.clear_name)
                self.userPass.bind('<Button-1>',self.clear_pass)
                self.userName.place(relx=0.17,rely=0.18)
                self.userPass.place(relx=0.17,rely=0.7)
            def zone_button():
                self.frameBtn = Frame(self.mainFrame, bg=self.bg)
                self.imgBtn = self.masterFrame.get_imageraw('assets/widgets/raw_button.png')
                self.loginBtn = Button(self.frameBtn, text="Log-in", command=lambda :self.login_req(masterFrame)
                                    , image=self.imgBtn, font=self.font, foreground="white", bg=self.bg,
                                    activebackground=self.bg,activeforeground="white",bd=0,compound="center", )
                self.loginBtn.pack(side=TOP,pady=10,ipady=0,padx=3,expand=1)
                self.frameDonthave = Frame(self.frameBtn,bg=self.bg)
                Label(self.frameDonthave,text="Don't have an account?",bg=self.bg).pack(side="left",expand=1)
                self.signupBtn = Label(self.frameDonthave,text="Sign-Up",font="leelawadee 10 underline",bg=self.bg,fg="blue")
                self.signupBtn.bind('<Button-1>',self.signup_req)
            #displaywidgets
            zone_canvas()
            zone_entry()
            zone_button()
            #displayFrame
            self.signinFrame.pack(side="top",expand=1,fill=BOTH)
            self.mainFrame.pack(expand=1,pady=50,ipady=50)
            self.entryFrame.pack(side="top",expand=1)
            self.frameBtn.pack(side="top", pady=0, expand=1)
            self.frameDonthave.pack(side="bottom",expand=1)
            self.signupBtn.pack(side=LEFT,padx=3)
            
        def clear_name(self,e):
            self.userName.delete(0, END)
        def clear_pass(self,e):
            self.userPass.delete(0, END)

        def login_req(self,masterFrame):
            print(self.userName.get())
            print(self.userPass.get())
            masterFrame.switch_frame(DashBoard)
            #userPass
        
        def login_submit(self):
            pass
        
        def signup_req(self,e):
                print("signup-request")
                self.masterFrame.switch_frame(SignUp)



class SignUp(Frame):

    def __init__(self, masterFrame):
        Frame.__init__(self, masterFrame)
        self.bg = "#ccefff"
        Frame.configure(self,bg=self.bg)
        self.pack()
        self.SignUpContent(self, masterFrame)

    class SignUpContent:

        def __init__(self, root, masterFrame):
            self.bg,self.fg = "#ccefff","#cc07e6"
            self.masterFrame = masterFrame
            self.masterFrame.title("BU Friends  |  Sign-In")
            self.fontHead = Font(family="leelawadee bold",size=40)
            self.font = Font(family="leelawadee bold",size=16)
            Label(root, text="BU Friends  |  Sign-Up",font=self.fontHead,bg=self.bg,foreground=self.fg)\
                .pack(expand=1,pady=40)
            self.frameRegis = Frame(root,width=500,height=500,bg=self.bg)
            self.frameRegis.pack(expand=1,fill=BOTH,ipadx=10,ipady=10)
            self.regisInfoLst = ["BUMail", "Display Name", "Password", "Confirm Password"]
            self.regisVarData = []
            self.regisDataSubmit = []
            for i in range(len(self.regisInfoLst)):
                self.regisVarData.append(StringVar())
                self.signup_form(self.regisInfoLst[i], self.font, i, self.regisVarData[i])
            self.frameBtn = Frame(self.frameRegis,bg=self.bg)
            self.frameBtn.grid(row=4,column=0,columnspan=3,sticky="e")
            self.regisBtn = Button(self.frameBtn, text="Register!", command=self.signup_submit, relief="solid", width=30, height=3
                                   , bg="#edffbf")
            self.regisBtn.grid(row=4,column=1,sticky="nsew",padx=2,pady=15)
            self.CancelBtn = Button(self.frameBtn, text="Cancel", command=lambda :self.masterFrame.switch_frame(SignIn), relief="solid", width=20, height=2)
            self.CancelBtn.grid(row=4,column=2,sticky="nsew",padx=2,pady=15)

        def signup_form(self, _text, _font, _row, _entVar):
                Label(self.frameRegis, text=_text ,font=_font,anchor="w",bg=self.bg).grid(row=_row,column=0,sticky="nsew",padx=20,pady=10)
                Label(self.frameRegis, text=":", font=_font,anchor="e",bg=self.bg).grid(row=_row,column=1,sticky="nsew",pady=10)
                if _row == 2 or _row ==3:
                    Entry(self.frameRegis, textvariable=_entVar,show="*",font="Kanit 12",justify="left",relief="solid")\
                        .grid(row=_row, column=2, sticky="nsew",padx=5, pady=10,ipadx=80,ipady=2)
                else:
                    Entry(self.frameRegis, textvariable=_entVar, font="Kanit 10", justify="left",relief="solid")\
                        .grid(row=_row, column=2, sticky="nsew",padx=5, pady=10,ipadx=80,ipady=2)

        def signup_submit(self):
            def register_error(errorFormat=""):
                self.regisVarData.clear()
                self.regisDataSubmit.clear()
                messagebox.showinfo('Register Error', '{}\nPlease Register Form Again'.format(errorFormat))
                self.masterFrame.switch_frame(SignUp)
            def signup_validate(self):
                for i,data in enumerate(self.regisVarData):
                    if data.get() == "" or data.get().isspace():
                        register_error("Register Form Information not Complete")
                        break
                signup_email_validate(self)

            def signup_email_validate(self):
                if "@bumail.net" not in self.regisVarData[0].get():
                    register_error("BU Friends Exclusive for BU Mail only")
                signup_password_validate(self)
                        
            def signup_password_validate(self):
                for i,data in enumerate(self.regisVarData):
                    if self.regisVarData[2].get() != self.regisVarData[3].get():
                        register_error("Password is not Matching")
                        break
                    else:self.regisDataSubmit.append(data.get())
                self.regisDataSubmit.pop(-1)    #remove second password
                signup_confirm(self)
                
            def signup_confirm(self):
                print(self.regisDataSubmit)
                bufdb = DbController()
                bufdb.request_register(*self.regisDataSubmit)
                messagebox.showinfo('Register Successfully'
                                    ,"BUMail : {} DisplayName : {}\nPassword1 : {}\nPassword2 : {}".format(*self.regisDataSubmit))
                messagebox.showinfo('Redirecting',"Going to BU Friends | Log-in")
                self.masterFrame.switch_frame(SignIn)
            signup_validate(self)

class DashBoard(Frame):

    def __init__(self, masterFrame):
        Frame.__init__(self,masterFrame)
        self.bg = "grey"
        Frame.configure(self,bg=self.bg)
        self.pack(expand=1)
        self.DashBoardContent(self,masterFrame)

    class DashBoardContent:

        def __init__(self, root, masterFrame):
            self.bg,self.fg = "#ccefff","#cc07e6"
            self.masterFrame = masterFrame
            self.masterFrame.title("BU Friends  |  Dashboard")
            self.fontHead = Font(family="leelawadee bold",size=30)
            self.font = Font(family="leelawadee bold",size=16)
            Label(root, text="Dashboard",font=self.fontHead).pack()
            self.entryFrame = Canvas(root,bg=self.bg,width=500,height=500)
            self.entryFrame.propagate(0)
            self.entryImg = self.masterFrame.get_imageraw('assets/1signin/entry1.png')
            Label(self.entryFrame,image=self.entryImg,bg=self.bg).place(relx=0.5,rely=0.5,anchor="center")
            Label(self.entryFrame,image=self.entryImg,bg=self.bg).place(relx=0.5,rely=0.5,anchor="center")
            Label(root,image=self.entryImg,bg="pink").pack(expand=1,fill=BOTH)
            self.entryFrame.pack(expand=1)

        def ehe(self):
            print("ehe nun dayo")


if __name__ == '__main__':
    sql = """ CREATE TABLE IF NOT EXISTS testTable(
                                    id integer(20) PRIMARY KEY,
                                    bumail text(50) NOT NULL,
                                    passwordx password NOT NULL,
                                    displayname varchar(50) NOT NULL
                                    );"""
    insert = """ INSERT INTO testTable VALUES (
                                    01230123012301000100,
                                    bubuaddbumail.net,
                                    passsxdpk3o2o04,
                                    Ehe<3                                
                                    );"""
    sqld = """ DROP TABLE testTable;"""
    conn = DbController.create_connection()
    if conn is not None:
        print("connection complete!")
        #DbController.execute_sql(conn, insert)
    else:
        print("Error Connection incomplete!")
    BUFriends().mainloop()