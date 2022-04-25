# -*- coding:utf-8 -*-
from tkinter import *
from tkinter import ttk,messagebox
from tkinter import font
from tkinter.font import Font
from datetime import datetime
from dateutil import tz
from PIL import Image, ImageTk
from sqlite3 import Error
import sqlite3
import hashlib
import random
import os
import assets.mbti.mbtiData as mbtiData

class BUFriends(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.frame = None
        self.width, self.height = 900, 600
        self.x = ((self.winfo_screenwidth()//2) - (self.width // 2))
        self.y = ((self.winfo_screenheight()//2-50) - (self.height // 2))
        self.geometry(f"{self.width}x{self.height}+{self.x}+{self.y}")
        self.resizable(0,0)
        self.title("BU Friends  |")
        self.iconbitmap(r'./assets/icons/bufriends.ico')
        self.fontHeading = Font(family="leelawadee",size=36,weight="bold")
        self.fontBody = Font(family="leelawadee",size=16)
        self.option_add('*font',self.fontBody)
        self.uid, self.uidSelect = 0,0
        self.newUserFlow, self.matchFilter = 0,0
        self.mbtiCode = None
        self.ridSelect, self.requestReport = None, None
        self.uuidLst, self.uinfoLst, self.udnameLst = [],[],[]
        self.update_blacklist()
        self.init_sessions()
    
    def init_sessions(self):
        def relogin_sessions():
            self.uid,self.ssid = 0,0
            self.set_sessions()
            self.switch_frame(SignIn)
        with open(r'./database/sessions.txt','r')as ss:
            try:
                self.ssid = int(ss.read())
            except ValueError as ve:
                self.uid,self.ssid = 0,0
                self.set_sessions()
                self.switch_frame(SignIn)
                return
        if self.ssid != 0:
            self.uid = self.ssid
            conn = self.create_connection()
            if conn is None:
                print("Cannot Connecting to Database")
                return
            sqlLastUid = """SELECT Uid FROM UsersTag ORDER BY Uid DESC LIMIT 1;"""
            lastUid = self.execute_sql(sqlLastUid).fetchone()[0]
            print("lastuid in database =",lastUid)
            if self.ssid > lastUid:                # check over uid
                self.uid,self.ssid = 0,0
                self.set_sessions()
                self.switch_frame(SignIn)
                return
            sqlgetUserExist = """SELECT * FROM Users WHERE Uid = ?;"""
            userExisted = self.execute_sql(sqlgetUserExist, [self.ssid])
            try:
                userExisted.fetchone()[0]           # catch deactivate user
            except TypeError:
                relogin_sessions()
                return
            sqlgetDname = """SELECT DisplayName FROM Users WHERE Uid = ?;"""
            dname = self.execute_sql(sqlgetDname, [self.ssid]).fetchone()[0]
            sqlgetStatus = """SELECT Status, StartDate, EndDate FROM Blacklists WHERE Uid = ?;"""
            uStat = self.execute_sql(sqlgetStatus, [self.ssid])
            try:
                uStat.row_factory = sqlite3.Row
                userStatus = uStat.fetchone()        # catch banned user
            except TypeError as te: print(te)
            if userStatus is None:                   # have no data history in Blacklist = white User
                pass 
            elif userStatus['Status'] == 1:          # have data in Blacklist and status == 1
                print("blacklist =",*userStatus)
                uStartDate = self.timezone_converter(userStatus['StartDate'], _strftime=1)
                uEndDate = self.timezone_converter(userStatus['EndDate'], _strftime=1)
                if messagebox.showerror("BU Friends  |  Banned",
                                        f"{dname} has been banned from BU Friends\nFrom [ {uStartDate} ] \nUntill [ {uEndDate} ]"):
                    relogin_sessions()
                return
            
            sqlgetSessionType = """SELECT UserType FROM UsersTag WHERE Uid = ?;"""
            sessionType = self.execute_sql(sqlgetSessionType, [self.ssid]).fetchone()[0]
            conn.close()
            self.set_sessions(self.uid)         # remember session uid
            if sessionType == None:             # have no do the test mbti
                self.switch_frame(Matching)
                messagebox.showinfo('BU Friends  |  Welcome ',
                                    f"""{(" "*5)}Welcome back! [ {dname} ]{(" "*5)}""")
                return
            elif sessionType == "ADMIN":
                self.uid = self.ssid
                self.switch_frame(Administration)
                messagebox.showinfo('BU Friends  |  Welcome',
                                    f"""{(" "*5)}Welcome back Admin!!! [ {dname} ]{(" "*5)}""")
                return
            else:                               # do the test mbti and have 16 type of user
                self.switch_frame(Matching)
                messagebox.showinfo('BU Friends  |  Welcome ',
                                    f"""{(" "*5)}Welcome back! [ {dname} ]{(" "*5)}""")
        else:
            self.switch_frame(SignIn)
                
    def set_sessions(self, _session=0):
        with open(r'./database/sessions.txt','w')as ss:
            ss.write(f"{_session}")
    
    def update_blacklist(self) :
        sql = """
        UPDATE Blacklists SET Status=0, StartDate=NULL, EndDate=NULL WHERE EndDate <= datetime("now");"""
        conn = self.create_connection()
        if conn is not None:
            c = self.execute_sql(sql)
            conn.close()

    def switch_frame(self, frame_class):
        print(f"switching to {frame_class} \n==| My uid = {self.uid} |==")
        new_frame = frame_class(self)
        if self.frame is not None:
            self.frame.destroy()
        self.frame = new_frame
        self.config(bg=self.frame.bgColor)
        self.frame.pack_propagate(False)
        self.frame.pack(side=BOTTOM, fill=BOTH, expand=TRUE)
        
    def create_connection(self):
        try:
            self.conn = sqlite3.connect(r"./database/BUFriends.db")
            self.conn.execute("PRAGMA foreign_keys = 1")                 # Allow Foreign Key
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
  
    def timezone_converter(self, _timeRawStr, _localzone="Asia/Bangkok", _strftime=None):
        print("time raw str =",_timeRawStr)
        print("time raw str type =",_timeRawStr)
        timeData = datetime.strptime(_timeRawStr, "%Y-%m-%d %H:%M:%S")
        tzFromUtc = tz.gettz("UTC")
        tzToLocal = tz.gettz(_localzone)
        timeData = timeData.replace(tzinfo=tzFromUtc)
        timeConvertedObj = timeData.astimezone(tzToLocal)
        if _strftime is not None:
            timeConvertedObj = timeConvertedObj.strftime("%d-%B-%Y %H:%M")
        return timeConvertedObj
        
    def update_text_limit(self, _input, _output, _limit, _title):
        def update_text_length(event):
            txtLen = len(_input.get(1.0,"end-1c"))
            _output.config(text=f"{txtLen}/{_limit}")
            if txtLen > _limit:
                overLimit = (txtLen-_limit)+5
                messagebox.showwarning("BU Friends  |  Warning",f"{_title} cannot be longer than {_limit} characters.\nPlease try again.")
                _input.delete(f"end-{overLimit}c",END)
                txtLen = len(_input.get(1.0,"end-1c"))
                _output.config(text=f"{txtLen}/{_limit}")
                return
        _input.bind('<KeyPress>',lambda event:update_text_length(event))
        _input.bind('<KeyRelease>',lambda event:update_text_length(event))
    
class ScrollFrame():
    def __init__(self,root,bgColor='white'):
        self.root = root
        self.bgColor = bgColor
        self.canvas = Canvas(self.root, bg=self.bgColor,highlightthickness=0)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=1)
        # reset the view
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)
        # create a frame inside the canvas which will be scrolled with it
        self.interior = Frame(self.canvas,bg=self.bgColor)
        self.interior_id = self.canvas.create_window(0, 0, window=self.interior,anchor=NW)
        self.interior.bind('<Configure>', self.configure_interior)
        self.canvas.bind('<Configure>', self.configure_canvas)
        self.canvas.bind('<Enter>', self.bind_to_mousewheel)
        self.canvas.bind('<Leave>', self.unbind_from_mousewheel)
        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar

    def configure_interior(self, event):
        # update the scrollbars to match the size of the inner frame
        size = (self.interior.winfo_reqwidth(), self.interior.winfo_reqheight())
        self.canvas.config(scrollregion="0 0 %s %s" % size)
        if self.interior.winfo_reqwidth() != self.root.winfo_width():
            # update the canvas's width to fit the inner frame
            self.canvas.config(width=self.interior.winfo_reqwidth())

    def configure_canvas(self, event):
        if self.interior.winfo_reqwidth() != self.root.winfo_width():
            # update the inner frame's width to fill the canvas
            self.canvas.itemconfigure(self.interior_id, width=self.root.winfo_width())
    # This can now handle either windows or linux platforms
    def on_mousewheel(self, event):
        # condition to scrollable : content > 600
        if self.interior.winfo_reqheight() > 600:
            """print(event.delta)"""
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        else :
            self.canvas.yview_scroll(0, "units")
    def bind_to_mousewheel(self, event):
        self.root.bind_all("<MouseWheel>", self.on_mousewheel)

    def unbind_from_mousewheel(self, event):
        self.root.unbind_all("<MouseWheel>")
        
class SignIn(Frame):
    def __init__(self, controllerFrame):
        Frame.__init__(self, controllerFrame)
        self.bgColor,self.fg = "#B6E0F7","#cc07e6"
        Frame.config(self, bg=self.bgColor)
        self.pack()
        self.root = ScrollFrame(self).interior
        self.SignInContent(self.root, controllerFrame)

    class SignInContent:
        def __init__(self, root, controllerFrame):
            self.bg,self.bgentry,self.fghead,self.fg,self.fgHolder = "#B6E0F7","#ffffff","#000000","#333333","#999999"
            self.controller = controllerFrame
            self.controller.uid = 0
            self.controller.title("BU Friends  |  Sign-In")
            self.root = root
            self.loginDict = {"usermail":"",
                              "userpass":""}
            def zone_canvas():
                self.canvasFrame = Canvas(root, width=400, height=600, bd=0,highlightthickness=0)
                self.canvasFrame.pack(side=LEFT,expand=1,fill="both")
                pathLst = [r'./assets/images/banner.png',r'./assets/images/character.png']
                self.imgLst = []
                for i,data in enumerate(pathLst):
                    self.imgLst.append(self.controller.get_image(data))
                    self.canvasFrame.create_image(0,0,image=self.imgLst[i],anchor="nw")
            #widgetAll
            def zone_entrys():    
                self.signinFrame = Frame(root,bg=self.bg,width=500,height=600)
                self.signinFrame.propagate(0)
                self.mainFrame = Frame(self.signinFrame,bg=self.bg)
                Label(self.mainFrame,text="BU Friends",font=self.controller.fontHeading,bg=self.bg,fg=self.fghead,justify="left")\
                    .pack(side=TOP,expand=1,padx=30,pady=2)
                self.entryFrame = Frame(self.mainFrame,bg=self.bg)
                self.entryImg = self.controller.get_image(r'./assets/entrys/entry1rz.png')
                self.entryicon1 = self.controller.get_image(r'./assets/icons/user.png')
                self.entryicon2 = self.controller.get_image(r'./assets/icons/lock.png')
                self.icon1 = Label(root,image=self.entryicon1,bg=self.bgentry)
                self.icon2 = Label(root,image=self.entryicon2,bg=self.bgentry)
                self.icon1.place(relx=0.55,rely=0.38)
                self.icon2.place(relx=0.55,rely=0.485)
                Label(self.entryFrame,image=self.entryImg,bg=self.bg).pack(pady=10)
                Label(self.entryFrame,image=self.entryImg,bg=self.bg,width=350,height=50).pack()
                self.userName = Entry(self.entryFrame,font="leelawadee 14",width=27,justify="left",relief="flat")
                self.userPass = Entry(self.entryFrame,font="leelawadee 14",width=27,justify="left",relief="flat")
                self.userEntryLst = [[self.userName,"Enter Your BU-Mail"],[self.userPass,"Enter Your Password"]]
                self.userName.place(relx=0.17,rely=0.18)
                self.userPass.place(relx=0.17,rely=0.68)
                def binding_events():
                    def clear_event(index):    
                        if index == 1:
                            if self.userEntryLst[index][0].get() == self.userEntryLst[index][1]:
                                pass
                            else:
                                self.userEntryLst[index][0].config(show="*")
                        self.userEntryLst[index][0].config(fg=self.fg)
                        if self.userEntryLst[index][0].get() == self.userEntryLst[index][1]:
                            self.userEntryLst[index][0].delete(0,END)
                    def key_event(index):
                        if index == 1:
                            self.userEntryLst[index][0].config(show="*")
                        self.userEntryLst[index][0].config(fg=self.fg)
                    def access_event(index):
                        if index == 1:
                            self.login_request()
                    def entry_binding(index):
                        self.userName.focus_force()
                        self.userName.select_range(0,END)
                        self.userEntryLst[index][0].insert(0,self.userEntryLst[index][1])
                        self.userEntryLst[index][0].config(fg=self.fgHolder)
                        self.userEntryLst[index][0].bind('<Button-1>',lambda e,index=index: clear_event(index))
                        self.userEntryLst[index][0].bind('<Key>',lambda e,index=index: key_event(index))
                        self.userEntryLst[index][0].bind('<Return>',lambda e, index=index: access_event(index))
                    for i in range(len(self.userEntryLst)):
                        entry_binding(i)
                binding_events()
            def zone_buttons():
                self.frameBtn = Frame(self.mainFrame, bg=self.bg)
                self.imgBtn = self.controller.get_image(r'./assets/buttons/buttonRaw.png')
                self.loginBtn = Button(self.frameBtn, text="Sign-In", command=self.login_request
                                       , image=self.imgBtn, fg="#ffffff", bg=self.bg,activebackground=self.bg
                                       , activeforeground="white",bd=0,compound="center",font="leelawadee 16 bold")
                self.loginBtn.pack(side=TOP,pady=10,ipady=0,padx=3,expand=1)
                self.frameDonthave = Frame(self.frameBtn,bg=self.bg)
                Label(self.frameDonthave,text="Don't have an account?",font="leelawadee 10",bg=self.bg).pack(side="left",expand=1)
                self.signupBtn = Label(self.frameDonthave,text="Sign-Up",font="leelawadee 10 underline",bg=self.bg,fg="#0000ff")
                self.signupBtn.bind('<Enter>',self.signup_mouseover)    
                self.signupBtn.bind('<Leave>',self.signup_mouseleave)
                self.signupBtn.bind('<Button-1>',self.goto_signup)
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
        def goto_signup(self,e):
            self.controller.switch_frame(SignUp)
        
        def login_request(self):
            self.controller.update_blacklist()
            conn = self.controller.create_connection()
            if conn is None:
                print("DB Can't Connect!")
                return
            else:
                self.loginDict['usermail'] = (self.userName.get())
                sqlPerma = """SELECT Email FROM PermanentBanned WHERE Email = ?;"""
                permaBanned = self.controller.execute_sql(sqlPerma, [self.userName.get()]).fetchone()
                if permaBanned is not None:
                    messagebox.showerror("BU Friends  |  Banned",f"[ {self.userName.get()} ] has been Permanently Banned")
                    return
                sqlQuery = """SELECT Uid, PassHash, PassSalt, DisplayName FROM Users WHERE Email = ?;"""
                q = self.controller.execute_sql(sqlQuery, [self.userName.get()])
                rowExist = q.fetchall()
                if rowExist == []:
                    messagebox.showwarning('BU Friends  |  Failure', f"[ {self.userName.get()} ] does not exist \nPlease check bu-mail carefully and try again")
                    self.userName.focus_force()
                    self.userName.select_range(0,END)
                    return
                else:
                    self.row = rowExist[0]
                    self.login_validation()
                conn.close()
            
        def login_validation(self):
            logPasskey = self.controller.password_encryptioncheck(self.userPass.get(), self.row[2])
            print(f"login-hash {logPasskey}")
            print(type(logPasskey))
            self.loginDict['userpass'] = logPasskey
            if self.loginDict['userpass'] == self.row[1]:
                self.controller.uid = self.row[0]
                conn = self.controller.create_connection()
                conn.row_factory = sqlite3.Row
                if conn is None: 
                    print("cannot Connecting Database")
                    return 
                sqlBlacklist = """SELECT * FROM Blacklists WHERE Uid = ?;"""
                userBlacklist = self.controller.execute_sql(sqlBlacklist, [self.controller.uid]).fetchone()
                conn.close()
                if userBlacklist is None:
                    messagebox.showinfo('BU Friends  |  Welcome',f"Welcome Back [ {self.row[3]} ] \nHave a great time in BU Friends.")
                    self.login_submit()
                    return
                elif userBlacklist['Status'] == 1:
                    print("blacklist =",*userBlacklist)
                    uStartDate = self.controller.timezone_converter(userBlacklist['StartDate'], _strftime=1)
                    uEndDate = self.controller.timezone_converter(userBlacklist['EndDate'], _strftime=1)
                    messagebox.showerror("BU Friends  |  Banned",
                                            f"{self.loginDict['usermail']} has been banned from BU Friends\nFrom [ {uStartDate} ] \nUntill [ {uEndDate} ]")
                    return
                else:
                    messagebox.showinfo('BU Friends  |  Welcome',f"Welcome Back [ {self.row[3]} ] \nHave a great time in BU Friends")
                    self.login_submit()
                    return
            else:
                messagebox.showwarning('BU Friends  |  Failure', "Incorrect Password! Please Try Again.")
                self.userPass.focus_force()
                self.userPass.select_range(0,END)
        
        def login_submit(self):
            conn = self.controller.create_connection()
            conn.row_factory = sqlite3.Row
            if conn is None: 
                print("cannot Connecting Database")
                return 
            sqlUsertype = """SELECT * FROM UsersTag WHERE Uid = ?;"""
            user = self.controller.execute_sql(sqlUsertype, [self.controller.uid]).fetchone()
            conn.close()
            self.controller.set_sessions(self.controller.uid)       # remember session uid
            if user['UserType'] is None: 
                self.controller.switch_frame(Matching)
            elif user['UserType'] == "ADMIN": 
                self.controller.switch_frame(Administration)
            else: 
                self.controller.switch_frame(Matching)
         
class SignUp(Frame):
    def __init__(self, controllerFrame):
        Frame.__init__(self, controllerFrame)
        self.bgColor = "#ccefff"
        Frame.config(self,bg=self.bgColor)
        self.pack()
        self.controller = controllerFrame
        self.controller.uid = 0
        self.root = ScrollFrame(self).interior
        self.SignUpContent(self.root, controllerFrame)

    class SignUpContent:
        def __init__(self, root, controllerFrame):
            self.controller = controllerFrame
            self.root = root
            self.controller.title("BU Friends  |  Sign-Up")
            self.bg,self.fgHead,self.fg,self.fgHolder = "#ccefff","#000000","#333333","#999999"
            self.canvasFrame = Canvas(self.root,width=900,height=600,bd=0,bg="#ffffff",highlightthickness=0)
            self.canvasFrame.option_add('*font',self.controller.fontBody)
            self.canvasFrame.pack(expand=1,fill=BOTH)
            self.bgCanvaImg = self.controller.get_image(r"./assets/images/regisbg.png")
            self.canvasFrame.create_image(0,0,image=self.bgCanvaImg,anchor="nw")
            self.canvasFrame.create_text(450,90,text="Registration",font="leelawadee 36 bold", fill=self.fgHead)
            self.regisInfoLst = ["Enter your BU-Mail", "Enter Your Password", "Confirm Your Password", "Enter your Display Name"]
            self.regisSubmitDict  = {'bumail': "",
                                    'passhash':"",
                                    'salt':"",
                                    'displayname':"",
                                    'bio':""}
            self.entryLst = []
            def zone_widgets():
                self.entryimg = self.controller.get_image(r'./assets/entrys/entry2rz.png')
                for i in range(len(self.regisInfoLst)):
                    self.entryLst.append(self.signup_form(self.canvasFrame, i))
                    x,y = 260,70*(i+2)
                    self.canvasFrame.create_image(x,y,image=self.entryimg,anchor="nw")
                    self.entryLst[i].place(x=x+20, y=y+10)
                def events():
                    def clear_event(index):
                        if index == 1 or index == 2:
                            self.entryLst[index].config(show="*")
                        if self.entryLst[index].get() == self.regisInfoLst[index]:
                            self.entryLst[index].delete(0,END)
                        self.entryLst[index].config(fg=self.fg)
                    def key_event(index):
                        if index == 1 or index == 2:
                            self.entryLst[index].config(show="*")
                        self.entryLst[index].config(fg=self.fg)
                    def entry_binding(index):
                        self.entryLst[0].focus_force()
                        self.entryLst[0].select_range(0,END)
                        self.entryLst[index].bind('<Button-1>',lambda e, index=index:clear_event(index))
                        self.entryLst[index].bind('<Key>', lambda e, index=index:key_event(index))
                    for i in range(len(self.entryLst)):
                        entry_binding(i)
                events()        
            def zone_buttons():
                self.imgBtn = self.controller.get_image(r'./assets/buttons/signup_newrz.png')
                self.imgBtn2 = self.controller.get_image(r'./assets/buttons/back_newrz.png')
                self.signupBtn = Button(root, text="Sign Up", command=lambda: self.signup_reqvalidation(), image=self.imgBtn,fg="#ffffff"
                                   ,bg="#ffffff",bd=-10,compound="center",activebackground="#ffffff")
                self.backBtn = Button(root, text="Cancel", command=lambda:self.controller.switch_frame(SignIn), image=self.imgBtn2
                                    ,bg="#ffffff", foreground="white",bd=-10,compound="center",activebackground="#ffffff")
                self.canvasFrame.create_window(250,430,anchor="nw",window=self.signupBtn)
                self.canvasFrame.create_window(455,430,anchor="nw",window=self.backBtn)
            zone_widgets()
            zone_buttons() 
            
        def signup_form(self,_root, _index):
            entry = Entry(_root, justify="left",relief="flat",fg=self.fgHolder,width=32)
            entry.insert(0,self.regisInfoLst[_index])
            return entry
        
        def register_error(self, errorFormat="Error, Please contact moderater", fatal=None):
            print("[SignUp Validator Reject]")
            if fatal is not None:
                messagebox.showerror("BU Friends  |  Incomplete", f"{errorFormat}\nPlease sign up form again")
                return
            else:
                messagebox.showwarning("BU Friends  |  Incomplete", f"{errorFormat}\nPlease sign up form again")
                return
               
        def signup_reqvalidation(self):
            print("Signup-Validtion")
            limitDname = 24
            limitPass = 8
            try:
                for i,data in enumerate(self.entryLst):
                    if data.get() == "" or data.get().isspace() or " " in self.entryLst[0].get():
                        self.register_error("Information cannot be empty")
                        self.entryLst[i].focus_force()
                        self.entryLst[i].select_range(0,END)
                        return
                if "@bumail.net" not in self.entryLst[0].get():
                    self.register_error("BU Friends exclusive for Bangkok University\nUse student mail  [ bumail.net ]  only")
                    self.entryLst[0].focus_force()
                    self.entryLst[0].select_range(0,END)
                    return
                elif self.entryLst[1].get() != self.entryLst[2].get():
                    self.register_error("Password do not matching")
                    self.entryLst[1].focus_force()
                    self.entryLst[1].select_range(0,END)
                    self.entryLst[2].delete(0,END)
                    return
                elif len(self.entryLst[1].get()) < limitPass:
                    self.register_error(
                        f"Invalid password!\n[ Required ] At Least {limitPass} Characters \n[ Required ] Mixture of Letters and Numbers\n[ Optional ] Special Characters\nYour password have {len(self.entryLst[1].get())} characters")
                    self.entryLst[1].focus_force()
                    self.entryLst[1].select_range(0,END)
                    return
                elif not self.check_alnumpass(self.entryLst[1].get()):
                    self.register_error("Invalid password!\n[ Required ] Mixture of Letters and Numbers\n[ Optional ] Special Characters")
                    return
                elif len(self.entryLst[3].get()) > limitDname :
                    self.register_error(f"Display name cannot be longer than {limitDname} characters")
                    self.entryLst[3].focus_force()
                    self.entryLst[3].select_range(0,END)
                    return
                else:
                    self.regisSubmitDict['bumail']=self.entryLst[0].get()
                    self.regisSubmitDict['displayname']=self.entryLst[3].get()
                    self.regisSubmitDict['bio']= ""
                    print(self.regisSubmitDict)
                    def database_validator(self):
                        conn = self.controller.create_connection()
                        if conn is None: 
                            print("DB Can't Create Connection in db validator.")
                            return
                        else:
                            try:
                                print("query bumail..")   
                                bumail = self.regisSubmitDict['bumail'] 
                                sqlPerma = """SELECT * FROM PermanentBanned WHERE Email = ?;"""
                                userPermaBanned = None
                                try:
                                    userPermaBanned = self.controller.execute_sql(sqlPerma, [bumail]).fetchone()[0]
                                except TypeError as te: pass
                                if userPermaBanned is not None:
                                    self.register_error(f"[ {bumail} ] has been Permanently Banned",fatal=1)
                                    return
                                sqlquery = """SELECT * FROM Users WHERE Email = ?;"""
                                cur = self.controller.execute_sql(sqlquery, [bumail])
                                rowbumail = cur.fetchall()
                                print("rowbumail = ",rowbumail)
                                if rowbumail != []: 
                                    self.register_error(f"[ {bumail} ] has already existed")
                                    return
                                else: self.password_encryption();conn.close()
                            except sqlite3.Error as e :print(f"catch!!! {e}")
                    database_validator(self)
            except ValueError as ve: print(ve)
            
        def check_alnumpass(self,_pass):
            return any(c.isdigit() == True for c in _pass) and any(c.isalpha() == True for c in _pass)
        
        def password_encryption(self):
            print("password encryption")
            stdhash = 'sha256'
            stdencode = 'utf-8'
            salt = os.urandom(32)
            password = self.entryLst[1].get()
            passkey = hashlib.pbkdf2_hmac(stdhash, password.encode(stdencode), salt, 161803)
            self.regisSubmitDict['passhash'], self.regisSubmitDict['salt'] = passkey, salt
            self.signup_commit()
                   
        def signup_commit(self):
            print("signup commit")
            sqlRegis = """INSERT INTO Users(Email, PassHash, PassSalt, DisplayName, Bio)  
                                VALUES(?, ?, ?, ?, NULL);"""
            userinfoValues = (self.regisSubmitDict['bumail'],
                              self.regisSubmitDict['passhash'],
                              self.regisSubmitDict['salt'],
                              self.regisSubmitDict['displayname'])
            
            sqlGetuid = """SELECT Uid FROM Users WHERE Email = ?;"""
            sqlMail = (self.regisSubmitDict['bumail'])          
            
            sqlAddUserTag = """INSERT INTO UsersTag VALUES(NULL,NULL,NULL,NULL,NULL,NULL);"""
            print(type(self.regisSubmitDict['passhash']))
            print(type(self.regisSubmitDict['salt']))
            conn = self.controller.create_connection()
            if conn is None:
                print("DB can't connect in signup commit.")
                messagebox.showerror("BU Friends  |  Database Error","Can't access BU Friends\nPlease try again later")
                return
            else:
                try:
                    userAffected = self.controller.execute_sql(sqlRegis, userinfoValues)
                    userTagAffected = self.controller.execute_sql(sqlAddUserTag)
                    print("User affected =",userAffected.rowcount)
                    print("UserTag affected =",userTagAffected.rowcount)
                    if userAffected.rowcount > 0 and userTagAffected.rowcount > 0:
                        cur = self.controller.execute_sql(sqlGetuid, [sqlMail])
                        getUid = (cur.fetchall())[0]
                        self.controller.uid = getUid[0]
                        conn.close()
                        messagebox.showinfo("BU Friends  |  Successful"
                                            ,f"Welcome to BU Friends [ {self.regisSubmitDict['displayname']} ] \nHave a great time in BU Friends")
                        self.signup_complete()
                        return
                    else:
                        conn.close()
                        messagebox.showwarning("BU Friends | Failure","Failed to SignUp Please try again later.")
                        return
                        
                except Error as e :print(f"catch!!! {e}")

        def signup_complete(self):
            self.controller.title("BU Friends  |  Sign-Up Complete!")
            self.canvasFrame.delete(ALL)
            for widget in self.entryLst:
                widget.destroy()
            bgComplete = "#fbf6ce"
            font = Font(family="leelawadee",size= 14,weight="bold")
            self.canvasFrame.config(bg=bgComplete,bd=0,highlightthickness=0)
            self.canvasFrame.propagate(0)
            self.completeImg = self.controller.get_image(r'./assets/images/regiscompleterz.png')
            self.canvasFrame.create_image(0, 0, image=self.completeImg, anchor="nw")
            self.widgetLst = [["Personality Test ( MBTI ){}".format(" "*22)],["Let's Go! Have fun in BU Friends.{}".format(" "*8)]]
            redirectLst = [lambda:self.controller.switch_frame(Mbti), lambda:self.controller.switch_frame(Matching)]
            imgPathLst = [r'./assets/buttons/rectangleGreen.png',r'./assets/buttons/rectangleWhite.png']
            self.controller.newUserFlow = 1
            for i,path in enumerate(imgPathLst):
                img = self.controller.get_image(path)
                self.widgetLst[i].append(img)
            def get_widget(_index,_command):
                return Button(self.canvasFrame, text=self.widgetLst[_index][0], image=self.widgetLst[_index][1], command=_command
                       , compound=CENTER, justify=LEFT, bd=0, font=font,bg=bgComplete,activebackground=bgComplete)
            x,y1,y2 = 440, 335,435
            self.canvasFrame.create_window(x,y1,anchor="nw",window=get_widget(0,redirectLst[0]))
            self.canvasFrame.create_window(x,y2,anchor="nw",window=get_widget(1,redirectLst[1]))

class Mbti(Frame):
    def __init__(self, controllerFrame):
        Frame.__init__(self, controllerFrame)
        self.bgColor = "#155748"
        Frame.config(self, bg=self.bgColor)
        self.pack()
        self.root = ScrollFrame(self).interior
        self.MbtiContent(self.root, controllerFrame)
        
    class MbtiContent:
        def __init__(self, root, controllerFrame):
            self.root = root
            self.controller = controllerFrame
            self.controller.title("BU Friends  |  MBTi Test")
            bg = "#ffffff"
            backbg = "#D6E6F1"
            fontQuiz = Font(family="leelawadee",size=22,weight="bold")
            font = Font(family="leelawadee",size=14,weight="bold")
            self.mbtiFrame = Canvas(self.root,width=900,bd=0,highlightthickness=0,bg="#d0eeff")
            self.mbtiFrame.option_add("*font",font)
            self.mbtiFrame.pack(expand=1,fill=BOTH)
            self.bannerFrame = Frame(self.root)
            self.bannerMbti = self.controller.get_image(r'./assets/mbti/mbtiBanner.png')
            Label(self.mbtiFrame, image=self.bannerMbti,bd=0).pack(side=TOP,expand=1,fill=X)
            self.mbtiFrame.image = self.bannerMbti
            self.backImg =  self.controller.get_image(r'./assets/icons/goback.png')
            self.back = Button(self.mbtiFrame,command=lambda:self.controller.switch_frame(EditPage), image=self.backImg,bg=backbg,
                               relief="flat",bd=0, activebackground=backbg)
            if self.controller.newUserFlow == 1:
                self.back.config(command=lambda:self.controller.switch_frame(Matching))
            self.back.place(x=30,y=10 ,anchor="nw")
            self.mbtiProgress = {'ie':[],
                                 'ns':[],
                                 'ft':[],
                                 'pj':[]
                                 }
            self.mbtiCodeLst = []
            self.quizLst = mbtiData.get_quiz_TH()
            self.answLst = mbtiData.get_answer_TH()
            self.answVar = [StringVar() for i in range(len(self.quizLst))]
            self.answSubmitLst = []
            self.randLst = random.sample(range(len(self.quizLst)), len(self.quizLst))
            def request_quiz(_i):
                r = self.randLst[_i]
                bg = "#d0eeff"
                bgbtn = "#2E3033"
                btnfg = "#486edf"
                self.mainFrame = Frame(self.mbtiFrame)
                self.mainFrame.pack(expand=1,fill=BOTH)
                Label(self.mainFrame ,text=f"[{i+1}] {self.quizLst[r][1]}",font=fontQuiz,bg=bg,fg="#000000")\
                    .pack(expand=1,fill=X,ipady=200)
                self.subFrame = Frame(self.mainFrame,height=155)
                self.subFrame.propagate(0)
                self.subFrame.pack(expand=1,fill=X)
                self.a1 = Radiobutton(self.subFrame ,variable=self.answVar[r],value=self.answLst[r][0],text=f"A : {self.answLst[r][2]}"\
                    ,bg=bgbtn,fg=btnfg,font=font,indicatoron=0,activebackground=btnfg,width=40)
                self.a1.pack(side=LEFT,expand=1,fill=Y,ipady=60)
                self.a2 = Radiobutton(self.subFrame ,variable=self.answVar[r],value=self.answLst[r][1],text=f"B : {self.answLst[r][3]}"\
                    ,bg=bgbtn,fg=btnfg,font=font,indicatoron=0,activebackground=btnfg,width=40)
                self.a2.pack(side=LEFT,expand=1,fill=Y,ipady=60)
            for i in range(len(self.quizLst)):
                request_quiz(i)
            self.btnImg = self.controller.get_image(r'./assets/buttons/buttonRaw.png')
            bgSubmit = "#d0eeff"
            self.mbtiSubmitBtn = Button(self.mbtiFrame, text="Submit!", command=self.mbti_calculator, image=self.btnImg, compound="center",
                                  bd=0,bg=bgSubmit,fg="#ffffff",activebackground=bgSubmit,activeforeground="#ffffff")
            self.mbtiSubmitBtn.image = self.btnImg
            self.mbtiSubmitBtn.pack(expand=1,pady=30)
    
        def reset_values(self):
            self.answLst.clear()
            self.mindLst.clear()
            self.energyLst.clear()
            self.natureLst.clear()
            self.tacticLst.clear()
            self.mbtiProgress.clear()
            self.controller.mbtiCode,self.mbtiCodeLst = "",[]
            self.mbtiProgress = {'ie':[],
                                 'ns':[],
                                 'ft':[],
                                 'pj':[]}
        
        def mbti_calculator(self):
            for i,data in enumerate(self.answVar):
                if "I" in data.get():self.mbtiProgress["ie"].append(0)
                elif "E" in data.get():self.mbtiProgress["ie"].append(1)
                elif "N" in data.get():self.mbtiProgress["ns"].append(0)
                elif "S" in data.get():self.mbtiProgress["ns"].append(1)
                elif "F" in data.get():self.mbtiProgress["ft"].append(0)
                elif "T" in data.get():self.mbtiProgress["ft"].append(1)
                elif "P" in data.get():self.mbtiProgress["pj"].append(0)
                elif "J" in data.get():self.mbtiProgress["pj"].append(1)
                else:
                    print("out of mbti letter")
            self.mindLst = self.mbtiProgress.get('ie')
            self.energyLst = self.mbtiProgress.get('ns')
            self.natureLst = self.mbtiProgress.get('ft')
            self.tacticLst = self.mbtiProgress.get('pj')
            print(f"\n  Mind{self.mindLst}")
            print(f"Energy{self.energyLst}")
            print(f"Nature{self.natureLst}")
            print(f"Tactic{self.tacticLst}")
            nowAnswer = len(self.mindLst)+len(self.energyLst)+len(self.natureLst)+len(self.tacticLst)
            quizLength = len(self.quizLst)
            try:
                if nowAnswer != quizLength:
                    self.reset_values()
                    messagebox.showwarning("BU Friends  |  Incomplete",f"Please answer MBTi Quiz completely\nYou are left with [ {(quizLength-nowAnswer)} ] Quiz answers that must be answered.")
                    return
                else:
                    if sum(self.mindLst) > 3:self.mbtiCodeLst.append("E")
                    else:self.mbtiCodeLst.append("I")
                    if sum(self.energyLst) > 3:self.mbtiCodeLst.append("S")
                    else:self.mbtiCodeLst.append("N")
                    if sum(self.natureLst) > 3:self.mbtiCodeLst.append("T")
                    else:self.mbtiCodeLst.append("F")
                    if sum(self.tacticLst) > 3:self.mbtiCodeLst.append("J")
                    else:self.mbtiCodeLst.append("P")
                    self.controller.mbtiCode = "".join(self.mbtiCodeLst)
                    print(f"{self.controller.mbtiCode}")
                    self.mindLst.clear()
                    self.energyLst.clear()
                    self.natureLst.clear()
                    self.tacticLst.clear()
                    self.mbti_commit()
            except ValueError as ve: print(f"mbti calculator catch!!! {ve}")   
        
        def mbti_commit(self):
            conn = self.controller.create_connection()
            if conn is None:
                print("DB Cannot Connect!")
                return
            sqlMbti = """UPDATE UsersTag SET UserType = ? WHERE Uid = ? ;"""
            self.controller.execute_sql(sqlMbti, (self.controller.mbtiCode, self.controller.uid))
            print("mbti commited !")
            self.controller.switch_frame(MbtiSuccessfully)
class MbtiSuccessfully(Frame):
    def __init__(self, controllerFrame):
        Frame.__init__(self, controllerFrame)
        self.bgColor = "#d0eeff"
        Frame.config(self,bg=self.bgColor)
        self.pack(expand=1,fill=BOTH)
        self.root = ScrollFrame(self).interior
        self.controller = controllerFrame
        self.controller.title("BUFriends  |  MBTi Test Successfully!")
        self.content_geometry()
    
    def get_mbti_characters(self, _mbtiCode):
        mbtiImg = self.controller.get_image(f"./assets/mbti/{(_mbtiCode.upper())}.png",900,596)
        return mbtiImg
    
    def content_geometry(self):
        mbtiCode = (self.controller.mbtiCode).upper()
        bgPallette = ["#E0D7E6","#CBD4C2","#D6E6F1","#E8E2CA"]
        letterCode = [["N","T"],
                      ["N","F"],
                      ["S","J"],
                      ["S","P"]]
        for i, letter in enumerate(letterCode):
            if letter[0] in mbtiCode and letter[1] in mbtiCode:
                activeBg = bgPallette[i]
                break
        self.frame = Frame(self.root,bd=0,highlightthickness=0)
        self.frame.option_add('*font',"leelawadee 16 bold")
        self.frame.pack(expand=1,fill=BOTH)
        miniGrey = self.controller.get_image(r'./assets/buttons/miniGrey.png',260,107)
        miniWhite = self.controller.get_image(r'./assets/buttons/miniWhite.png',260,107)
        mbtiImg = self.get_mbti_characters(mbtiCode)
        mbti = Label(self.frame, image=mbtiImg)
        mbti.image = mbtiImg
        mbti.pack(expand=1)
        xplace,yplace = 600,400
        if self.controller.newUserFlow == 1:
            matchingBtn = Button(self.frame,text="MATCHING",command=lambda:self.controller.switch_frame(Matching),
                                image=miniWhite, compound=CENTER,bg=activeBg, bd=0,activebackground=activeBg)
            matchingBtn.image = miniWhite
            matchingBtn.place(x=xplace-100, y=yplace)
            return
        matchingBtn = Button(self.frame,text="MATCHING",command=lambda:self.controller.switch_frame(Matching),
                            image=miniWhite, compound=CENTER,bg=activeBg, bd=0,activebackground=activeBg)
        matchingBtn.image = miniWhite
        matchingBtn.place(x=xplace, y=yplace)
        editprofileBtn = Button(self.frame,text="EDIT PROFILE",command=lambda:self.controller.switch_frame(EditPage),
                                image=miniGrey, compound=CENTER,bg=activeBg,fg="#ffffff", bd=0,activebackground=activeBg,
                                activeforeground="#ffffff")
        editprofileBtn.image = miniGrey
        editprofileBtn.place(x=xplace-250, y=yplace)

class Matching(Frame):
    def __init__(self, controllerFrame):
        Frame.__init__(self, controllerFrame)
        self.bgColor = "#FFFFFF"
        Frame.config(self,bg=self.bgColor)
        self.pack(expand=1,fill=BOTH)
        self.root = ScrollFrame(self).interior
        self.controller = controllerFrame
        self.controller.newUserFlow = 0
        self.controller.title("BU Friends  |  Matching")
        self.bgCanva = "#FFFFFF"
        self.canvasMain = Canvas(self.root, width=900, height=6000 ,bg=self.bgCanva,bd=0, highlightthickness=0)
        self.canvasMain.pack(expand=1,fill=BOTH)
        # widgetzone 
        self.filterFrame = None
        self.headBgImg = self.controller.get_image(r'./assets/images/banner.png')
        self.headingBg = Label(self.canvasMain,image=self.headBgImg,compound=CENTER, bg=self.bgCanva,width=900,height=20)
        self.headingBg.pack(side=TOP,pady=30)
        self.searchBarImg = self.controller.get_image(r'./assets/entrys/searchtabrz.png')
        self.searchBar = Button(self.canvasMain, text="#Hashtags Filter", command=lambda: self.filter_tags(), image=self.searchBarImg,
                            font="leelawadee 18 bold",fg="#000000",bg=self.bgCanva,bd=0,activebackground=self.bgCanva, compound=CENTER)
        self.searchBar.image = self.searchBarImg
        self.searchBar.place(x=35,y=10,anchor=NW)
        self.myImg = self.controller.get_image(r'./assets/icons/profileXs.png')
        self.myProfile = Button(self.canvasMain, image=self.myImg, command=lambda:self.goto_my_profile(),bg=self.bgCanva,bd=0,activebackground=self.bgCanva, compound=CENTER)
        self.myProfile.image = self.myImg
        self.myProfile.place(x=815,y=11,anchor=NW)
        #Display user filter result
        print("checklen uuid ",len(self.controller.uuidLst))
        self.usersFrame = Frame(self.canvasMain,width=900,height=1400,bg=self.bgCanva)
        self.usersFrame.pack(side=TOP,expand=1)
        self.uuidFilter = []
        self.cntLoop = 0
        self.usersTabFrame = []
        if self.controller.matchFilter == 1:
            self.display_users()
            return
        else:
            self.request_users_infomation()
            self.display_users()
        
            
    def get_tagname(self):
        self.tagnameLst = []
        sql = """SELECT Tid,TagName FROM Tags"""
        self.conn = self.controller.create_connection()
        self.conn.row_factory = sqlite3.Row
        if self.conn is None:
            return
        else:
            cur = self.controller.execute_sql(sql)
            row = cur.fetchone()
            while row:
                self.tagnameLst.append({'tid':row['Tid'],'tagName':row['TagName']})
                row = cur.fetchone()
            print(f"We have {len(self.tagnameLst)} tag in Database.")
            self.conn.close()
            return self.tagnameLst
    
    def filter_tags(self):
        def destroy_frame():
            self.endFrame.destroy()
            self.tagsFrame.destroy()
            self.mbtiFrame.destroy()
            self.filterFrame.destroy()
            self.filterFrame = None
        bg = "#ffffff"
        fg = "#555555"
        if self.filterFrame is not None and self.mbtiFrame is not None and self.tagsFrame is not None and self.endFrame:
            destroy_frame()
        else:
            wfilter = 720
            self.filterFrame = Frame(self.root,bg=bg,width=wfilter,relief=FLAT,highlightthickness=0)
            self.filterFrame.place(x=50,y=75,anchor=NW)
            self.mbtiFrame = LabelFrame(self.filterFrame,bg=bg,width=wfilter,height=360,highlightthickness=0)
            self.mbtiFrame.pack(side=TOP,fill=X)
            ttFrame = Frame(self.mbtiFrame,bg=bg,width=740)
            ttFrame.pack(side=TOP,pady=25)
            xmbti, ymbti = 64, 20
            Label(self.mbtiFrame, text="MBTI",bg=bg,fg=fg).place(x=xmbti,y=ymbti,anchor=NW)
            Label(self.mbtiFrame, text="( more specific )",bg=bg,fg=fg,font="leelawadee 12").place(x=xmbti+60,y=ymbti+2,anchor=NW)
            content = Frame(self.mbtiFrame,bg=bg,width=740)
            content.pack(side=TOP,fill=BOTH,pady=15)
            self.matchAllTags = []
            self.tagWidgets = []
            self.mbtiWidgets = []
            self.mbtiLst = mbtiData.get_mbti_code()
            self.tagsFrame = LabelFrame(self.filterFrame,bg=bg,width=wfilter)
            self.tagsFrame.pack(side=TOP,fill=BOTH,ipady=5)
            self.tagnameLst.clear()
            self.tagnameLst = self.get_tagname()
            w,h = 140, 50
            def show_mbti(_i, _utype):
                if "N" in _utype and "T" in _utype: letter = "NT";self.userTagImg = self.controller.get_image(r'./assets/buttons/mbtiPurple2.png', w, h)
                elif "N" in _utype and "F" in _utype: letter = "NF";self.userTagImg = self.controller.get_image(r'./assets/buttons/mbtiGreen2.png', w, h)
                elif "S" in _utype and "J" in _utype: letter = "SJ";self.userTagImg = self.controller.get_image(r'./assets/buttons/mbtiCyan2.png', w, h)
                elif "S" in _utype and "P" in _utype: letter = "SP";self.userTagImg = self.controller.get_image(r'./assets/buttons/mbtiYellow2.png', w, h)
                btn = Button(content,command=lambda:self.selection_tag(_utype,letter),text=_utype,
                                image=self.userTagImg,fg=fg,bg=bg,bd=0,
                                activebackground=bg,compound=CENTER)
                btn.image = self.userTagImg
                btn.grid(row=r,column=c,padx=18,pady=10, sticky=NSEW)
                self.mbtiWidgets.append({"status":0, 
                                            "widget":btn, 
                                            "userType":_utype})
            def show_tag(_i, _tag):
                self.userTagImg = self.controller.get_image(r'./assets/buttons/tagButton2.png',w,h)
                btnTag = Button(self.tagsFrame, text=_tag['tagName'],command=lambda:self.selection_tag(_tag['tagName']),
                                image=self.userTagImg,bd=0,bg=bg,fg=fg,font="leelawadee 12 bold",
                                activebackground=bg, compound=CENTER)
                btnTag.image = self.userTagImg
                btnTag.grid(row=r,column=c,padx=18,pady=10, sticky=NSEW)
                self.tagWidgets.append({"status":0, 
                                        "widget":btnTag,
                                        "tid":_tag['tid'], 
                                        "tagName":_tag['tagName']})
            r,c = 0,0
            for i,tag in enumerate(self.mbtiLst):
                show_mbti(i,tag)
                c+=1
                if c==4:
                    c = 0
                    r +=1
            r,c = 0,0
            for i,tag in enumerate(self.tagnameLst):
                show_tag(i, tag)
                c+=1
                if c==4:
                    c = 0
                    r +=1
            
            self.endFrame = LabelFrame(self.filterFrame,bg=bg,width=wfilter)
            self.endFrame.pack(side=BOTTOM,fill=X)
            self.endBtn = Frame(self.endFrame,bg=bg)
            self.endBtn.pack(side=LEFT,expand=1,fill=Y,pady=15)
            imgBtn = self.controller.get_image(r'./assets/buttons/buttonRaw.png')
            matchBtn = Button(self.endBtn,command=lambda:self.match_tags_commit(),text="Match!!",
                                image=imgBtn,fg="#ffffff",bg=bg,compound=CENTER,bd=0,activebackground=bg,activeforeground="#ffffff")
            matchBtn.image = imgBtn
            matchBtn.pack(side=RIGHT,padx=10)
            imgBtn2 = self.controller.get_image(r'./assets/buttons/buttonDice.png')
            def random_filter():
                self.controller.matchFilter = 0
                self.controller.switch_frame(Matching)
            randBtn = Button(self.endBtn, text=f"""{" "*6}Random!""", command=lambda: random_filter(),
                                image=imgBtn2,font="leelawadee 12 bold",fg="#ffffff",bg=bg,compound=CENTER,bd=0,activebackground=bg,activeforeground="#ffffff")
            randBtn.image = imgBtn2
            randBtn.pack(side=RIGHT,padx=10)
            def close_leave(e):
                closeBtn.config(bd=0,image=imgBtn3)
            def close_hover(e):
                imgBtn31 = self.controller.get_image(r'./assets/buttons/closeRed.png')
                closeBtn.config(bd=0,image=imgBtn31)
                closeBtn.image = imgBtn31
            def close_frame(e):
                destroy_frame()
            cframe = Frame(self.endFrame,bg=bg)
            cframe.pack(side=LEFT,expand=1)
            imgBtn3 = self.controller.get_image(r'./assets/buttons/closeGrey.png')
            closeBtn = Label(cframe, image=imgBtn3,bd=0,compound=CENTER,bg=bg)
            closeBtn.image = imgBtn3
            closeBtn.bind('<Enter>',lambda e: close_hover(e))
            closeBtn.bind('<Leave>',lambda e: close_leave(e))
            closeBtn.bind('<Button-1>',lambda e: close_frame(e))
            closeBtn.pack(side=RIGHT,padx=10)
    
    def selection_tag(self, tag, _mbtiLetter=None):
        limitTag = 8
        w,h = 140, 50
        if _mbtiLetter:
            if _mbtiLetter == "NT": 
                selectMbtiImg = self.controller.get_image(r'./assets/buttons/mbtiPurple.png', w, h)
                unselectMbtiImg = self.controller.get_image(r'./assets/buttons/mbtiPurple2.png', w, h)
            elif _mbtiLetter == "NF": 
                selectMbtiImg = self.controller.get_image(r'./assets/buttons/mbtiGreen.png', w, h)
                unselectMbtiImg = self.controller.get_image(r'./assets/buttons/mbtiGreen2.png', w, h)
            elif _mbtiLetter == "SJ": 
                selectMbtiImg = self.controller.get_image(r'./assets/buttons/mbtiCyan.png', w, h)
                unselectMbtiImg = self.controller.get_image(r'./assets/buttons/mbtiCyan2.png', w, h)
            elif _mbtiLetter == "SP": 
                selectMbtiImg = self.controller.get_image(r'./assets/buttons/mbtiYellow.png', w, h)
                unselectMbtiImg = self.controller.get_image(r'./assets/buttons/mbtiYellow2.png', w, h)

            for i,select in enumerate(self.mbtiWidgets):
                if select['userType'] == tag:
                    select['widget'].config(image=selectMbtiImg,compound=CENTER,fg="#eeeeee")
                    select['widget'].image = selectMbtiImg
                    if select['status'] == 0:
                        if len(self.matchAllTags) < limitTag:
                            self.matchAllTags.append(select['userType'])
                            select['status'] = 1
                        else:
                            select['widget'].config(image=unselectMbtiImg,compound=CENTER,fg="#555555")
                            select['widget'].image = unselectMbtiImg
                            select['status'] = 0    
                            messagebox.showwarning("BU Friends  |  Warning",f"You can select tag at most {limitTag} tags")
                    elif select['status'] == 1:
                        if select['userType'] in self.matchAllTags:
                            self.matchAllTags.remove(select['userType'])
                        select['widget'].config(image=unselectMbtiImg,compound=CENTER,fg="#555555")
                        select['widget'].image = unselectMbtiImg
                        select['status'] = 0    
        else:
            selectTagImg = self.controller.get_image(r'./assets/buttons/tagButton.png',w,h)
            for i,select in enumerate(self.tagWidgets):
                if select['tagName'] == tag:
                    select['widget'].config(image=selectTagImg,compound=CENTER,fg="#eeeeee")
                    select['widget'].image = selectTagImg
                    if select['status'] == 0:
                        if len(self.matchAllTags) < limitTag:
                            self.matchAllTags.append(select['tid'])
                            select['status'] = 1
                        else:
                            select['widget'].config(image=self.userTagImg,compound=CENTER,fg="#555555")
                            select['widget'].image = self.userTagImg
                            select['status'] = 0    
                            messagebox.showwarning("BU Friends  |  Warning",f"You can select tag at most {limitTag} tags")
                            
                    elif select['status'] == 1:
                        if select['tid'] in self.matchAllTags:
                            self.matchAllTags.remove(select['tid'])
                        select['widget'].config(image=self.userTagImg,compound=CENTER,fg="#555555")
                        select['widget'].image = self.userTagImg
                        select['status'] = 0    
        print(self.matchAllTags)

    def gen_qmark(self,_rangelimit):
        questionMarkSet = ("?"+" ,?"*(_rangelimit-1))
        return questionMarkSet        

    def match_tags_commit(self):
        if self.filterFrame is not None:
            self.filterFrame.destroy()
            self.filterFrame = None
        if self.matchAllTags == []:
            messagebox.showinfo("BU Friends  |  Warning","You did not select any tags\nPlease try again")
            return
        else:
            self.controller.matchFilter = 1
            self.uuidFilter.clear()
            print("\n\nMatchFilter = ",self.controller.matchFilter)
            # Resorting str & int in All Tags
            self.matchAllTags = list(map(int,filter(lambda x:x.isdigit(),sorted(map(str,self.matchAllTags)))))+list(filter(lambda x:x.isalpha(),sorted(map(str,self.matchAllTags))))
            print(self.matchAllTags)
            self.matchTagsLst,self.matchMbtiLst = None, None
            try:
                #remap list -> str
                if any(isinstance(tag, str) for tag in self.matchAllTags):
                    self.matchMbtiLst = [tag for tag in self.matchAllTags if isinstance(tag, str)]
                    print(self.matchMbtiLst)
                if any(isinstance(tag, int) for tag in self.matchAllTags):
                    self.matchTagsLst = [tag for tag in self.matchAllTags if isinstance(tag, int)]
                    self.matchTagsLst = ", ".join(map(str,self.matchTagsLst))
                    print(self.matchTagsLst)
            except ValueError as ve: print(ve); return 
            conn = self.controller.create_connection()
            conn.row_factory = sqlite3.Row
            sqlMatch = None
            if conn is None:
                print('Cant connect DB')
                return
            if self.matchMbtiLst:
                limitRangeMbti = len(self.matchMbtiLst)
                qMbtiSet = self.gen_qmark(limitRangeMbti)
                if self.matchTagsLst:
                    sqlMatch = f"""SELECT uniA.* FROM(SELECT * FROM UsersTag ut1 WHERE ut1.Tid1 in ({self.matchTagsLst}) 
                                                UNION SELECT * FROM UsersTag ut2 WHERE ut2.Tid2 in ({self.matchTagsLst}) 
                                                UNION SELECT * FROM UsersTag ut3 WHERE ut3.Tid3 in ({self.matchTagsLst}) 
                                                UNION SELECT * FROM UsersTag ut4 WHERE ut4.Tid4 in ({self.matchTagsLst})
                                                )uniA WHERE uniA.UserType in ({qMbtiSet}) 
                                                AND (uniA.Uid in (SELECT Users.Uid FROM Users
                                                LEFT JOIN Blacklists ON Users.Uid=Blacklists.Uid WHERE Blacklists.Status=0) 
                                                OR uniA.Uid not in (SELECT Uid FROM Blacklists))
                                                EXCEPT SELECT * FROM UsersTag WHERE Uid = {self.controller.uid};"""
                else:
                    sqlMatch = f"""SELECT uniA.* FROM (SELECT * FROM UsersTag WHERE userType in ({qMbtiSet})
                                                )uniA WHERE(uniA.Uid in (SELECT Users.Uid FROM Users
                                                LEFT JOIN Blacklists ON Users.Uid=Blacklists.Uid WHERE Blacklists.Status=0) 
                                                OR uniA.Uid not in (SELECT Uid FROM Blacklists))
                                                EXCEPT SELECT * FROM UsersTag WHERE Uid = {self.controller.uid};"""
            else:
                sqlMatch = f"""SELECT uniA.* FROM(SELECT * FROM UsersTag ut1 WHERE ut1.Tid1 in ({self.matchTagsLst}) 
                                            UNION SELECT * FROM UsersTag ut2 WHERE ut2.Tid2 in ({self.matchTagsLst}) 
                                            UNION SELECT * FROM UsersTag ut3 WHERE ut3.Tid3 in ({self.matchTagsLst}) 
                                            UNION SELECT * FROM UsersTag ut4 WHERE ut4.Tid4 in ({self.matchTagsLst})
                                            ) uniA WHERE(uniA.Uid in (SELECT Users.Uid FROM Users
                                            LEFT JOIN Blacklists ON Users.Uid=Blacklists.Uid WHERE Blacklists.Status=0) 
                                            OR uniA.Uid not in (SELECT Uid FROM Blacklists))
                                            EXCEPT SELECT * FROM UsersTag WHERE Uid = {self.controller.uid};"""
            curr = self.controller.execute_sql(sqlMatch, self.matchMbtiLst).fetchall()
            for data in curr:
                self.uuidFilter.append(data['Uid'])
            if self.uuidFilter == []:
                messagebox.showinfo("BU Friends  |  Notification","Currently no one matches your tags required\nTry to changing the tags again \n\u2764\ufe0f Don't give up and you'll meet new friends \u2764\ufe0f")
            else:
                self.controller.uuidLst.clear()
                if len(self.uuidFilter) > 12:
                    print("uuid filter more than 12 uuid")
                    randLst = random.sample(range(len(self.uuidFilter)),12)
                    for i,indexdata in enumerate(randLst):
                        self.controller.uuidLst.append(self.uuidFilter[indexdata])
                    self.uuidFilter = self.controller.uuidLst
                elif len(self.uuidFilter) > 0:
                    print("uuidfilter <= 12")
                    self.controller.uuidLst = self.uuidFilter
                messagebox.showinfo("BU Friends  |  Notification",f"""{" "*18}Matched!!!{" "*18}""")
                print("final uuidlst select random",self.controller.uuidLst)
                self.controller.matchFilter = 1
                self.request_users_infomation()
            
    def reset_list_data(self):
        self.controller.uuidLst.clear()
        self.controller.uinfoLst.clear()
        self.controller.udnameLst.clear()
        
    def request_users_infomation(self):
        self.controller.update_blacklist()
        self.conn = self.controller.create_connection()
        self.conn.row_factory = sqlite3.Row
        if self.conn is None:
            print("DB connot connect")   
            return         
        else:
            # filter matching sequence
            if self.controller.matchFilter == 1:
                self.controller.uinfoLst.clear()
                self.controller.udnameLst.clear()
                qmark = self.gen_qmark(len(self.controller.uuidLst))
                sqlGetTag = f"""SELECT * FROM UsersTag WHERE Uid IN ({qmark});"""
                sqlGetDisplayName = f"""SELECT DisplayName FROM Users WHERE Uid IN ({qmark})"""
                infoRows = self.controller.execute_sql(sqlGetTag, self.controller.uuidLst).fetchall()
                dnameRows = self.controller.execute_sql(sqlGetDisplayName, self.controller.uuidLst).fetchall()
                for i,info in enumerate(infoRows):
                    self.controller.uinfoLst.append(info)
                for dname in dnameRows:
                    self.controller.udnameLst.append(dname['DisplayName'])
                self.conn.close()
                self.controller.switch_frame(Matching)
                return
            # random matching sequence
            else:
                self.reset_list_data()
                blacklstUid = []
                sqlBlacklist = """SELECT * FROM Blacklists WHERE status = 1;"""
                c = self.conn.cursor().execute(sqlBlacklist).fetchall()
                for i,data in enumerate(c):
                    blacklstUid.append(data['Uid'])
                print(blacklstUid)
                sqlRandUtype = """SELECT Uid, UserType FROM UsersTag EXCEPT SELECT Uid, UserType FROM UsersTag WHERE UserType = "ADMIN";"""
                cur = self.controller.execute_sql(sqlRandUtype)
                userObj = (cur.fetchall())
                provideLst = []
                for i,data in enumerate(userObj):
                    provideLst.append(data['Uid'])
                # my uid & blacklist uid detection sequence
                provideLst.remove(self.controller.uid)
                print(provideLst)
                if len(blacklstUid) > 0:
                    for i,blUid in enumerate(blacklstUid):
                        if blUid in provideLst:
                            provideLst.remove(blUid)
                        else:pass
                    print("removed blacklist uid")
                randLst = []
                randLst = random.sample(provideLst, 12)
                print(f"{randLst}\n")
                sqlRandMatch = """SELECT * FROM UsersTag WHERE Uid IN (?,?,?,?,?,?,
                                                                       ?,?,?,?,?,?);"""
                cur = self.controller.execute_sql(sqlRandMatch, randLst)
                infoRows = cur.fetchall()
                for i, row in enumerate(infoRows):
                    if row['UserType'] is None:
                        pass
                    elif "ADMIN" in row['UserType']:
                        self.cntLoop +=1
                        self.reset_list_data()
                        randLst.clear()
                        self.conn.close()
                        self.request_users_infomation()
                        break
                    self.controller.uinfoLst.append(row)
                    self.controller.uuidLst.append(infoRows[i]['Uid'])    
                sqlDisplayName = """SELECT DisplayName FROM Users WHERE Uid IN (?,?,?,?,?,?,
                                                                                ?,?,?,?,?,?);"""
                curr = self.controller.execute_sql(sqlDisplayName, self.controller.uuidLst)
                dnameRows = curr.fetchall()
                self.controller.udnameLst.clear()
                for i,row in enumerate(dnameRows):
                    self.controller.udnameLst.append(row['DisplayName'])
                
    def display_users(self):
        self.get_tagname()
        self.userTabBtnImg = self.controller.get_image(r'./assets/images/rectangle.png',820,180)
        self.idxRandLst = random.sample(range(len(self.controller.uuidLst)), len(self.controller.uuidLst))
        print("Display random index of uuidlst",self.idxRandLst)
        print("now show usertab id =",self.controller.uuidLst)
        for i in range(len(self.controller.uuidLst)):
            self.get_users_tab(i)
        minimumDisplay = 7
        if len(self.controller.uuidLst) < minimumDisplay:
            uuidFillSpace = minimumDisplay-(len(self.controller.uuidLst))
            for i in range(uuidFillSpace):
                self.get_blank_tab(i)
            
    def get_users_tab(self,_i):
        bgRectangle = "#e6eefd"
        ir = self.idxRandLst[_i]
        self.tabFrame = Frame(self.usersFrame,bg=self.bgCanva)
        self.tabFrame.pack(pady=10)
        self.tabFrame.option_add("*font","leelawadee 15 bold")
        self.tabFrame.option_add("*foreground","#ffffff")
        self.userTabBtn = Button(self.tabFrame, command=lambda:self.goto_review_profile(self.controller.uuidLst[ir]), 
                                    image=self.userTabBtnImg, justify=LEFT,bg=self.bgCanva, 
                                    bd=0,compound=CENTER,activebackground=self.bgCanva,
                                relief=FLAT)
        self.userTabBtn.pack(pady=10,anchor=W)
        self.userDisname = Label(self.tabFrame, text=self.controller.udnameLst[ir],bg=bgRectangle, font="leelawadee 20 bold",fg="#000000")
        self.userDisname.place(x=210,y=40)
        self.img = self.controller.get_image(r'./assets/images/avt{}.png'.format(self.controller.uuidLst[ir]%6),138,144)
        self.profileImg = Label(self.tabFrame, image=self.img ,bg=bgRectangle,bd=0)
        self.profileImg.image = self.img
        self.profileImg.place(x=40,y=20,anchor=NW)
        xplace = 200
        w,h = 140,45
        for i, tag in enumerate((self.controller.uinfoLst[ir])):
            self.userTagImg = self.controller.get_image(r'./assets/buttons/tagButton.png', w,h)
            if i < 1: continue          # Skip Uid  info
            if i == 1:                  # MBTi Check
                if tag is None: continue
                elif "N" in tag and "T" in tag: self.userTagImg = self.controller.get_image(r'./assets/buttons/mbtiPurple.png', w, h)
                elif "N" in tag and "F" in tag: self.userTagImg = self.controller.get_image(r'./assets/buttons/mbtiGreen.png', w, h)
                elif "S" in tag and "J" in tag: self.userTagImg = self.controller.get_image(r'./assets/buttons/mbtiCyan.png', w, h)
                elif "S" in tag and "P" in tag: self.userTagImg = self.controller.get_image(r'./assets/buttons/mbtiYellow.png', w, h)
            if i > 4: break             # stop tag place
            if tag is None:             # didnt show None Tag 
                if i == 1:              # except Mbti
                    self.userTag = Label(self.tabFrame, text=f"{tag}", image=self.userTagImg,
                                        bg=bgRectangle, compound=CENTER)
                    self.userTag.image = self.userTagImg
                    self.userTag.place(x=xplace,y=110)
                else:pass
            elif isinstance(tag, str):
                self.userTag = Label(self.tabFrame, text=f"{(self.controller.uinfoLst[ir][i])}", image=self.userTagImg,
                                    bg=bgRectangle, compound=CENTER)
                self.userTag.image = self.userTagImg
                self.userTag.place(x=xplace,y=110)
            else:
                tag = self.tagnameLst[(self.controller.uinfoLst[ir][i])-1]
                self.userTag = Label(self.tabFrame, text=f"{(tag['tagName'])}", image=self.userTagImg,
                                    bg=bgRectangle, compound=CENTER)
                self.userTag.image = self.userTagImg
                self.userTag.place(x=xplace,y=110)
            xplace += 150
        nextIcon = self.controller.get_image(r'./assets/icons/next.png')
        self.next = Button(self.tabFrame,command=lambda:self.goto_review_profile(self.controller.uuidLst[ir]), image=nextIcon, 
                            bd=0, bg=bgRectangle, activebackground=bgRectangle)
        self.next.image = nextIcon
        self.next.place(x=720,y=45, anchor=NW)
        pass
       
    def get_blank_tab(self,_i):
        self.tabFrame = Frame(self.usersFrame,bg=self.bgCanva)
        self.tabFrame.pack(pady=10)
        self.tabFrame.option_add("*font","leelawadee 14 bold")
        self.tabFrame.option_add("*foreground","#bbbbbb")
        b = Button(self.tabFrame,bd=0, justify=LEFT,bg=self.bgCanva,relief=FLAT,state=DISABLED)
        if _i == 0:
            b.config(text="Search results only include your filter MBTi & Tags visible to You.")
        b.pack(ipady=55,pady=15,anchor=W)
            
    def goto_review_profile(self,_uidselect):
        self.controller.uidSelect = _uidselect
        print("uid select review",self.controller.uidSelect)
        self.controller.option_add('*foreground',"#000000")
        self.controller.switch_frame(ProfileReviewPage)
    def goto_my_profile(self):
        print("myuid select",self.controller.uid)
        self.controller.option_add('*foreground',"#000000")
        self.controller.switch_frame(ProfilePage)
  
class ProfileReviewPage(Frame):
    def __init__(self,controller):
        Frame.__init__(self,controller)
        self.bgColor = 'white'
        self.controller = controller
        Frame.config(self,bg=self.bgColor)
        scroll = ScrollFrame(self)
        self.root = scroll.interior
        self.controller.title("BU Friends  |  Profile Review")
        self.profile = InfoOnProfile(self.root,self.bgColor,self.controller,1,self.controller.uidSelect)
        PostOnProfile(self.root,self.bgColor,self.controller,self.controller.uidSelect)

class AdminReviewPage(Frame):
    def __init__(self,controller):
        Frame.__init__(self,controller)
        self.bgColor = 'white'
        self.controller = controller
        Frame.config(self,bg=self.bgColor)
        scroll = ScrollFrame(self)
        self.root = scroll.interior
        self.profile = InfoOnProfile(self.root,self.bgColor,self.controller,3,self.controller.uidSelect)
        PostOnProfile(self.root,self.bgColor,self.controller,self.controller.uidSelect)

class ProfilePage(Frame):
    def __init__(self,controller):
        Frame.__init__(self,controller)
        self.bgColor = 'white'
        self.controller = controller
        Frame.config(self,bg=self.bgColor)
        scroll = ScrollFrame(self)
        self.root = scroll.interior
        self.controller.title("BU Friends  |  My Profile")
        self.profile = InfoOnProfile(self.root,self.bgColor,self.controller,2,self.controller.uid)
        self.create_post_frame()
        PostOnProfile(self.root,self.bgColor,self.controller,self.controller.uid)
    def post_event(self):
        txt = self.post.get(1.0,END)
        self.limitPostlen = 300
        if txt.isspace() :
            messagebox.showwarning("BU Friends  |  Warning","Your post cannot be empty")
        elif len(txt) > self.limitPostlen :
            messagebox.showwarning("BU Friends  |  Warning","Your post cannot be longer than 300 characters")
        else :
            conn = self.controller.create_connection()
            sql = """INSERT INTO Postings(Detail,Uid) VALUES (?,?)"""
            if conn is not None:
                c = self.controller.execute_sql(sql,[txt,self.controller.uid])
                self.controller.switch_frame(ProfilePage)
            else:
                print("Error! cannot create the database connection.")
            conn.close()
    def create_post_frame(self) :
        self.img3 = self.controller.get_image('./assets/buttons/buttonPurplerz.png',200,65)
        frame = Frame(self.root,bg=self.bgColor)
        fontTag = Font(family='leelawadee',size=13)
        frame.option_add('*font',fontTag)
        Label(frame,text="Create Post",font="leelawadee 20 bold",bg=self.bgColor).pack(anchor=W,padx=25,pady=5)
        self.post = Text(frame,width=90,height=4,relief=GROOVE,bd=2)
        self.post.pack()
        Button(frame,text="Post",font='leelawadee 13 bold',fg='white',
        activeforeground='white',image=self.img3,compound=CENTER,bd=0,
        bg=self.bgColor,activebackground=self.bgColor,command=self.post_event).pack(side=RIGHT,padx=35,pady=10)
        limit = 300
        self.postLenNow = Label(frame,text=f"0/{limit}",bg="#ffffff",fg="#666666")
        self.postLenNow.pack(side=RIGHT,pady=10,ipadx=3)
        self.controller.update_text_limit(self.post, self.postLenNow, limit, "Post")
        frame.pack(fill=X)   
     
class EditPage(Frame):
    def __init__(self,controller):
        Frame.__init__(self,controller)
        self.bgColor = 'white'
        self.controller = controller
        self.nameStr = None
        self.bioStr = None
        self.searchEntryBox = None
        self.mainFrame = None
        self.tagData = ProfilePage(self.controller).profile
        Frame.configure(self,bg=self.bgColor)
        scroll = ScrollFrame(self)
        self.root = scroll.interior
        fontTag = Font(family='leelawadee',size=13,weight='bold')
        self.option_add('*font',fontTag)
        self.imgList = {}
        imgPathList = [
            {'name':'back','path':'./assets/icons/goback.png','x':50,'y':50},
            {'name':'entry','path':'./assets/entrys/entry2rz.png','x':440,'y':50},
            {'name':'longentry','path':'./assets/entrys/searchtabrz.png','x':760,'y':50},
            {'name':'search','path':'./assets/icons/Search.png','x':35,'y':35},
            {'name':'tag','path':'./assets/buttons/tagEdit.png','x':130,'y':45},
            {'name':'add','path':'./assets/buttons/addTag.png','x':130,'y':45},
            {'name':'yellow','path':'./assets/buttons/mbtiYellowEdit.png','x':130,'y':45},
            {'name':'blue','path':'./assets/buttons/mbtiBlueEdit.png','x':130,'y':45},
            {'name':'green','path':'./assets/buttons/mbtiGreenEdit.png','x':130,'y':45},
            {'name':'purple','path':'./assets/buttons/mbtiPurpleEdit.png','x':130,'y':45},
            {'name':'longtag','path':'./assets/buttons/tagEditLong.png','x':180,'y':45},
            {'name':'button','path':'./assets/buttons/buttonPurplerz.png','x':200,'y':65},
            {'name':'cancel','path':'./assets/buttons/back_newrz.png','x':180,'y':40},
            {'name':'entry2','path':'./assets/entrys/entry3.png','x':440,'y':80},
            {'name':'box','path':'./assets/buttons/rectangleBlue.png','x':200,'y':60},
            {'name':'selectBox','path':'./assets/buttons/rectangleDarkBlue.png','x':200,'y':60}]

        for i,data in enumerate(imgPathList) :
            img = self.controller.get_image(data['path'],data['x'],data['y'])
            self.imgList[data['name']] = img 
        if self.tagData.tagList[0] is not None :
            if self.tagData.tagList[0][1] == "N" :
                if self.tagData.tagList[0][2] == "T" :
                    self.img = self.imgList['purple']
                else :
                    self.img = self.imgList['green']
            elif self.tagData.tagList[0][1] == "S" :
                if self.tagData.tagList[0][3] == "J" :
                    self.img = self.imgList['blue']
                else :
                    self.img = self.imgList['yellow']  
        self.head_geometry()                 
        self.main_geometry()
    def head_geometry(self) :
        self.backBtn = Button(self.root,image=self.imgList['back'],bd=0
        ,bg=self.bgColor,activebackground=self.bgColor,
        command=lambda:self.controller.switch_frame(ProfilePage))
        self.backBtn.pack(anchor=NW)
        self.headText = Label(self.root,text="Edit Profile",font='leelawadee 20 bold',
        bg=self.bgColor,anchor=N)
        self.headText.pack(anchor=NW,padx=115,ipady=10)
    def main_geometry(self) :
        self.controller.title("BU Friends  |  Edit Profile")
        if self.nameStr is None :
            self.nameStr = StringVar()
            self.nameStr.set(self.tagData.name) 
        if self.bioStr is None :
            if self.tagData.bio is not None :
                self.bioStr = self.tagData.bio 
            else :     
                self.bioStr = "" 
        if self.searchEntryBox is not None :
            self.searchEntryBox.destroy()
        if self.mainFrame is not None :
            self.mainFrame.destroy()
        self.backBtn.config(command=lambda:self.controller.switch_frame(ProfilePage))
        self.headText.config(text="Edit Profile")
        headList = ("Username","Bio","MBTI","Interest")
        self.mainFrame = Frame(self.root,bg=self.bgColor)
        self.mainFrame.pack(anchor=W,padx=115)
        for i,data in enumerate(headList) :
            Label(self.mainFrame,text=data,fg='#868383'
            ,bg=self.bgColor).grid(row=i,column=0,pady=25,sticky=W)
        entryBox = Label(self.mainFrame,image=self.imgList['entry'],bg=self.bgColor)
        entryBox.grid(row=0,column=1,sticky=N,pady=10,padx=115)
        entryBox.propagate(0)
        entry = Entry(entryBox,font='leelawadee 15',width=38,bd=0,textvariable=self.nameStr,fg='#868383')
        entry.pack(expand=1)
    
        entryBox2 = Label(self.mainFrame,image=self.imgList['entry2'],bg=self.bgColor)
        entryBox2.grid(row=1,column=1,sticky=N,pady=10,padx=115)
        entryBox2.propagate(0)

        self.bioEntry = Text(entryBox2,font='leelawadee 15',
        bg=self.bgColor,width=38,height=3,bd=0,fg='#868383')

        self.bioEntry.insert(END,self.bioStr)     
        self.bioEntry.pack(expand=1)
        self.tag_geometry()
        self.end_geometry()   
    def tag_geometry(self) :
        self.addWidget = None
        self.mbtiTag = None
        self.mbtiBtn = None
        self.vars = [StringVar() for i in range(len(self.tagData.tagList))]
        self.tagWidgetList = []
        if self.tagData.tagList[0] is not None :
            self.mbtiTag = Label(self.mainFrame,text=self.tagData.tagList[0],image=self.img,bg=self.bgColor,
            compound=CENTER,fg='white')
            self.mbtiTag.grid(row=2,column=1,sticky=W,padx=115)            
            self.mbtiBtn = Button(self.mainFrame,text="Redo the test?",command=lambda: self.controller.switch_frame(Mbti),bg=self.bgColor,fg='#23B7F4',bd=0,
            activebackground=self.bgColor,activeforeground='#23B7F4')
            self.mbtiBtn.grid(row=2,column=1)
        else :
            self.mbtiBtn = Button(self.mainFrame,text="Do the test?",command=lambda: self.controller.switch_frame(Mbti),bg=self.bgColor,fg='#23B7F4',bd=0,
            activebackground=self.bgColor,activeforeground='#23B7F4')
            self.mbtiBtn.grid(row=2,column=1,sticky=W,padx=115)
        if self.mbtiTag is not None :
            self.mbtiTag.bind('<Button-1>',lambda e: self.delete_mbti(e))
        row = 3
        top = Frame(self.mainFrame,bg=self.bgColor)
        top.grid(row=row,column=1,sticky=W,padx=115)
        frame = top
        for i in range(len(self.tagData.tagList)+1) :
            if i > 0 and i < len(self.tagData.tagList):
                self.vars[i].set(self.tagData.tagList[i])
                if len(self.tagData.tagList[i]) <= 9 :
                    tag = Label(frame,image=self.imgList['tag'],bg=self.bgColor)
                    tag.pack(anchor=W)
                    tag.propagate(0)
                    lb = Label(tag,text=self.tagData.tagList[i],fg='white',bg='#88A3F3',width=8,textvariable=self.vars[i])
                    lb.pack(expand=1,anchor=W,padx=10)

                else:
                    tag = Label(frame,image=self.imgList['longtag'],bg=self.bgColor)
                    tag.pack(anchor=W)
                    tag.propagate(0)
                    lb = Label(tag,text=self.tagData.tagList[i],fg='white',bg='#88A3F3',width=12,textvariable=self.vars[i])
                    lb.pack(expand=1,anchor=W,padx=12)
                tag.bind('<Button-1>',lambda e,c=i: self.delete_tag(e,c))
                self.tagWidgetList.append(tag)
                if i%2 == 0 :
                    row+=1
                    newframe = Frame(self.mainFrame,bg=self.bgColor)
                    newframe.grid(row=row,column=1,sticky=W,padx=115)
                    frame = newframe
                else :
                    tag.pack(side=LEFT)
            elif i > 0 and i >= len(self.tagData.tagList):
                if len(self.tagData.tagList) <= 4 :
                    self.addWidget = Label(frame,image=self.imgList['add'],bg=self.bgColor)
                    self.addWidget.pack(anchor=W)
                    self.addWidget.bind('<Button-1>',lambda e,c=i: self.addtag_page(e))
    def end_geometry(self) :
            self.endFrame = Frame(self.root,bg=self.bgColor)
            self.endFrame.pack(pady=20)
            Button(self.endFrame,image=self.imgList['button'],text="Save Change",bd=0,compound=CENTER,
            bg=self.bgColor,fg='white',activebackground=self.bgColor,activeforeground='white',
            command=lambda : self.save_change()).pack(side=LEFT,padx=20)

            Button(self.endFrame,image=self.imgList['cancel'],text="Cancel",bd=0,
            bg=self.bgColor,fg='white',activebackground=self.bgColor,compound=CENTER,
            activeforeground='white',command=lambda:self.controller.switch_frame(ProfilePage)).pack(side=LEFT)

    def delete_tag(self,event,index) :
        self.tagData.tagList.pop(index)
        if self.addWidget is not None :
            self.addWidget.destroy()
        if self.mbtiTag is not None :
            self.mbtiTag.destroy()
        self.mbtiBtn.destroy()
        for i in range(len(self.tagWidgetList)) :
            self.tagWidgetList[i].destroy()
        self.tag_geometry()

    def addtag_page(self,event) :
        self.controller.title("BU Friends  |  Add Interest")
        self.bioStr = self.bioEntry.get(1.0,'end-1c')
        print(len(self.bioStr))
        self.mainFrame.destroy()
        self.endFrame.destroy()
        self.backBtn.config(command=lambda:self.main_geometry())
        self.headText.config(text="Add Interest")
        self.searchEntryBox = Label(self.root,image=self.imgList['longentry'],bg=self.bgColor)
        self.searchEntryBox.pack(pady=10)
        self.searchEntryBox.propagate(0)
        self.searchEntry = Entry(self.searchEntryBox,bd=0,font='leelawadee 16',fg='#868383',width=62)
        self.searchEntry.pack(expand=1,anchor=W,padx=10,side=LEFT)
        self.searchEntry.insert(END,"Search")
        self.searchEntry.focus_force()
        self.searchEntry.select_range(0,END)
        Button(self.searchEntryBox,image=self.imgList['search'],bg=self.bgColor,bd=0,
        activebackground=self.bgColor,command=lambda : self.search_event()).pack(anchor=E,expand=1,padx=10,side=LEFT)
        self.mainFrame = Frame(self.root,bg=self.bgColor)
        self.mainFrame.pack()
        self.get_alltag()
        self.show_tags(self.allTags)
        for i,data in enumerate(self.tagData.tagList) :
            print(data)
            self.select_tag(data,1)
        self.searchEntry.bind('<Return>', lambda e : self.search_event())
    def search_event(self) :
        searchList = []
        self.mainFrame.destroy()
        self.mainFrame = Frame(self.root,bg=self.bgColor)
        self.mainFrame.pack()
        for i,data in enumerate(self.allTags) :
            if self.searchEntry.get().lower() in data['tagName'].lower():
                searchList.append({'tagName':data['tagName']})
        print(searchList)
        self.show_tags(searchList)
        for i,data in enumerate(self.tagData.tagList) :
            print(data)
            self.select_tag(data)
    def get_alltag(self) :
        self.allTags = []
        conn = self.controller.create_connection()
        conn.row_factory = sqlite3.Row
        sql = """SELECT Tid,TagName FROM Tags"""
        if conn is not None:
            c = self.controller.execute_sql(sql)
            data = c.fetchone()
            while data :
                self.allTags.append({'tid':data['Tid'],'tagName':data['TagName']})
                data = c.fetchone()
            conn.close()
    def select_tag(self,name,check=None) :
        for i,data in enumerate(self.tagWidgets) :
            if data['name'] == name :
                data['widget'].config(image=self.imgList['selectBox'],compound=CENTER)
                if data['status'] == 0 :
                    if len(self.tagData.tagList) < 5 :
                        print(name)
                        data['status'] = 1
                        if data['name'] not in self.tagData.tagList :
                            self.tagData.tagList.append(data['name'])
                    else :
                        if check is not None :
                            messagebox.showwarning("BU Friends  |  Warning","You can select tag at most 4 tags")
                            data['widget'].config(image=self.imgList['box'],compound=CENTER)
                elif data['status'] == 1:
                    data['widget'].config(image=self.imgList['box'],compound=CENTER)
                    print(name)
                    data['status'] = 0
                    if data['name'] in self.tagData.tagList :
                        self.tagData.tagList.remove(data['name'])
                break
        print(self.tagData.tagList)
    def show_tags(self,showList) :
        print(self.tagData.tagList)
        row = 0
        column = 0
        self.tagWidgets = []
        for i,data in enumerate(showList) :
            lb = Button(self.mainFrame,image=self.imgList['box'],text=data['tagName'],bd=0,
            compound=CENTER,font='leelawadee 15 bold',bg=self.bgColor,fg='white',
            activeforeground='white',activebackground='white',command=lambda name=data['tagName']: self.select_tag(name,1))
            lb.propagate(0)
            self.tagWidgets.append({'name':data['tagName'],'widget':lb,'status':0})
            lb.grid(row=row,column=column,padx=20,pady=10)
            column+=1
            if i%3 == 2 :
                column=0
                row+=1 

    def delete_mbti(self,event) :
        self.tagData.tagList[0] = None
        self.mbtiBtn.destroy()
        self.mbtiTag.destroy()
        self.tag_geometry()

    def save_change(self) :
        print("tag =",self.tagData.tagList)
        self.bioStr = self.bioEntry.get(1.0,'end-1c')
        if self.bioStr.isspace() :
            self.bioStr = None
        if self.nameStr.get() == "" or self.nameStr.get().isspace():
            messagebox.showwarning("BU Friends  |  Warning","Your name cannot be empty")
            return
        if len(self.nameStr.get()) > 32 :
            messagebox.showwarning("BU Friends  |  Warning","Your display name cannot be longer than 32 characters")
            return
        if len(self.bioStr) > 100 :
            messagebox.showwarning("BU Friends  |  Warning","Your bio cannot be longer than 100 characters")
            return
        values = [None for i in range(5)]
        values[0] = self.tagData.tagList[0]
        print("here")
        self.get_alltag()
        conn = self.controller.create_connection()
        sql = """UPDATE Users SET DisplayName=?,Bio=? WHERE Uid=?"""
        if conn is not None:
            c = self.controller.execute_sql(sql,[self.nameStr.get(),self.bioStr,self.controller.uid])
            conn.close()
            valuesIndex = 1
            for i,data in enumerate(self.allTags) :
                if data['tagName'] in self.tagData.tagList :
                    values[valuesIndex] = data['tid']
                    valuesIndex+=1
            conn = self.controller.create_connection()
            sql = """UPDATE Userstag SET UserType=?,Tid1=?,Tid2=?,Tid3=?,Tid4=? WHERE Uid=?"""
            c = self.controller.execute_sql(sql,[values[0],values[1],values[2],values[3],values[4],self.controller.uid])
            conn.close()
            messagebox.showinfo("BU Friends  |  Successful","Profile has been successfully edited")
            self.controller.switch_frame(ProfilePage)

class MyAccountPage(Frame):
    def __init__(self,controller):
        Frame.__init__(self,controller)
        self.bgColor = 'white'
        self.controller = controller
        self.controller.title("BU Friends  |  My Account")
        Frame.configure(self,bg=self.bgColor)
        scroll = ScrollFrame(self)
        self.root = scroll.interior
        fontTag = Font(family='leelawadee',size=13,weight='bold')
        self.option_add('*font',fontTag)
        self.imgList = {}
        imgPathList = [
            {'name':'back','path':'./assets/icons/goback.png','x':50,'y':50},
            {'name':'pwd','path':'./assets/buttons/my_account.png','x':660,'y':55},
            {'name':'delete','path':'./assets/buttons/deactivate.png','x':660,'y':55},
            {'name':'background','path':'./assets/images/myaccount.png','x':800,'y':332}]
        for i,data in enumerate(imgPathList) :
            img = self.controller.get_image(data['path'],data['x'],data['y'])
            self.imgList[data['name']] = img
        self.my_account()

    def my_account(self) :
        Button(self.root,image=self.imgList['back'],bd=0
        ,bg=self.bgColor,activebackground=self.bgColor,
        command=lambda:self.controller.switch_frame(ProfilePage)).pack(anchor=NW)

        Label(self.root,text="My Account",font='leelawadee 20 bold',
        bg=self.bgColor,anchor=N).pack(anchor=NW,padx=115,ipady=10)

        Button(self.root,text="Change Password",image=self.imgList['pwd'],bd=0
        ,bg=self.bgColor,activebackground=self.bgColor,compound=CENTER,
        command=lambda:self.controller.switch_frame(ChangePasswordPage)).pack(pady=5)

        Button(self.root,text="Deactivate Account",image=self.imgList['delete'],bd=0
        ,bg=self.bgColor,activebackground=self.bgColor,compound=CENTER,
        command=lambda:self.controller.switch_frame(DeactivatePage)).pack(pady=5)

        Label(self.root,image=self.imgList['background'],bg=self.bgColor,anchor=S,bd=0).pack(ipady=10)
class ChangePasswordPage(Frame):
    def __init__(self,controller):
        Frame.__init__(self,controller)
        self.bgColor = 'white'
        self.controller = controller
        self.controller.title("BU Friends  |  Change Password")
        Frame.configure(self,bg=self.bgColor)
        scroll = ScrollFrame(self)
        self.root = scroll.interior
        fontHead = Font(family='leelawadee',size=13,weight='bold')
        self.option_add('*font',fontHead)
        self.pwdEntryList = []
        self.imgList = {}
        imgPathList = [
            {'name':'back','path':'./assets/icons/goback.png','x':50,'y':50},
            {'name':'button','path':'./assets/buttons/buttonRaw.png','x':277,'y':76}]
        for i,data in enumerate(imgPathList) :
            img = self.controller.get_image(data['path'],data['x'],data['y'])
            self.imgList[data['name']] = img
        self.page_geometry()
    def page_geometry(self) :
        textList = ("Current Password","New Password","Confirm Password")

        canvas = Canvas(self.root,highlightthickness=0,bg=self.bgColor)
        canvas.pack(fill=BOTH, expand=1)
        Button(canvas,image=self.imgList['back'],bd=0,
        bg=self.bgColor,activebackground=self.bgColor,
        command=lambda:self.controller.switch_frame(MyAccountPage)).pack(anchor=NW)

        Label(canvas,text="Change Password",font='leelawadee 20 bold',
        bg=self.bgColor,anchor=N).pack(anchor=NW,padx=115,ipady=10)
        y = 186
        for i,data in enumerate(textList) :
            Label(canvas,text=data,bg=self.bgColor,fg='#868383',
            anchor=N).pack(padx=140,anchor=NW,ipady=3)
            self.pwdEntryList.append(Entry(canvas,font="leelawadee 13",bd=0,fg='#868383', show="*"))
            self.pwdEntryList[i].pack(padx=140,pady=20,anchor=W,fill=X)
            canvas.create_line(140, y, 760, y,fill='#868383')
            y+=94
        self.pwdEntryList[0].focus_force()
        Button(canvas,text="Update Password",image=self.imgList['button'],bd=0,bg=self.bgColor,
        activebackground=self.bgColor,compound=CENTER,fg='white',activeforeground='white',
        command=self.password_validation).pack(pady=30)
        self.pwdEntryList[2].bind('<Return>',lambda e : self.password_validation())

    def password_validation(self) :
        self.pwds = []
        for i in range(len(self.pwdEntryList)) :
            self.pwds.append(self.pwdEntryList[i].get())
        if len(self.pwds[0]) > 0 :
            print("have data")
            if len(self.pwds[1]) > 7 and any(c.isdigit() == True for c in self.pwds[1]) and any(c.isalpha() == True for c in self.pwds[1]):
                print("allowed password")
                if self.pwds[1] == self.pwds[2] :
                    print("match password")
                    self.change_password()
                else :
                    messagebox.showerror("BU Friends  |  Incomplete","Password do not matching")
                    self.pwdEntryList[2].focus_force()
                    self.pwdEntryList[2].select_range(0,END)
            else :
                messagebox.showerror("BU Friends  |  Incomplete","Invalid password!!!\n[ Required ] At least 8 characters \n[ Required ] A mix of letters and number")
                self.pwdEntryList[1].focus_force()
                self.pwdEntryList[1].select_range(0,END)
        else:
            messagebox.showerror("BU Friends  |  Warning","Please enter current password")
            self.pwdEntryList[0].focus_force()
    
    def change_password(self) :
        conn = self.controller.create_connection()
        conn.row_factory = sqlite3.Row
        sql = """SELECT PassHash,PassSalt FROM Users WHERE Uid=?"""
        if conn is not None:
            c = self.controller.execute_sql(sql,[self.controller.uid])
            data = c.fetchone()
            passHash = data['passHash']
            passSalt = data['passSalt']
            passkey = self.controller.password_encryptioncheck(self.pwds[0],passSalt)
            if passkey == passHash :
                print("same password")
                newSalt = os.urandom(32)
                newpass = self.controller.password_encryptioncheck(self.pwds[1],newSalt)
                sql2 = """UPDATE Users SET PassHash = ?,PassSalt = ? WHERE uid = ?"""
                c2 = self.controller.execute_sql(sql2, (newpass,newSalt,self.controller.uid))
                conn.close()
                messagebox.showinfo("BU Friends  |  Successful","Password has been successfully changed")
                self.controller.switch_frame(MyAccountPage)
            else :
                messagebox.showerror("BU Friends  |  Incomplete","Incorrect current password!")
                self.pwdEntryList[0].focus_force()
                self.pwdEntryList[0].select_range(0,END)
class DeactivatePage(Frame):
    def __init__(self,controller):
        Frame.__init__(self,controller)
        self.bgColor = 'white'
        self.controller = controller
        self.data = ProfilePage(self.controller).profile
        self.controller.title("BU Friends  |  Deactivate Account")
        Frame.configure(self,bg=self.bgColor)
        scroll = ScrollFrame(self)
        self.root = scroll.interior
        fontHead = Font(family='leelawadee',size=20,weight='bold')
        self.fontBody = Font(family='leelawadee',size=15,weight='bold')
        self.option_add('*font',fontHead)
        self.imgList = {}
        imgPathList = [
            {'name':'back','path':'./assets/icons/goback.png','x':50,'y':50},
            {'name':'profile','path':'./assets/icons/profileSm.png','x':80,'y':80},
            {'name':'box','path':'./assets/images/box.png','x':620,'y':250},
            {'name':'entry','path':'./assets/entrys/entry2rz.png','x':400,'y':50},
            {'name':'button','path':'./assets/buttons/buttonPurplerz.png','x':200,'y':65}]
        for i,data in enumerate(imgPathList) :
            img = self.controller.get_image(data['path'],data['x'],data['y'])
            self.imgList[data['name']] = img
        self.page_geometry()
    def page_geometry(self) :
        canvas = Canvas(self.root,highlightthickness=0,bg=self.bgColor)
        canvas.pack(fill=BOTH, expand=1)

        Button(canvas,image=self.imgList['back'],bd=0,
        bg=self.bgColor,activebackground=self.bgColor,
        command=lambda:self.controller.switch_frame(MyAccountPage)).pack(anchor=NW)
        Label(canvas,text="Deactivate Account",
        bg=self.bgColor,anchor=N).pack(anchor=NW,padx=115,ipady=10)
        self.topFrame = Frame(canvas,bg=self.bgColor)
        self.topFrame.pack(anchor=W,padx=115,pady=15)
        Label(self.topFrame,image=self.imgList['profile'],
        bg=self.bgColor).pack(side=LEFT)
        Label(self.topFrame,text=self.data.name,bg=self.bgColor).pack(pady=5,anchor=W,padx=20)
        Label(self.topFrame,text=self.data.email,font=self.fontBody,bg=self.bgColor,
        fg='#868383').pack(anchor=W,padx=20)
        canvas.create_line(140, 225, 760, 225,fill='#868383')
        box = Label(canvas,image=self.imgList['box'],bg=self.bgColor)
        box.pack(pady=60)
        box.propagate(0)
        Label(box,text="Please enter password to deactivate your account.",
        font=self.fontBody,bg='#D0EEFF',fg='#4D3ED6').pack(pady=30)
        entryBox = Label(box,image=self.imgList['entry'],bg='#D0EEFF')
        entryBox.pack()
        entryBox.propagate(0)
        self.password = Entry(entryBox,font='leelawadee 15',width=35,bd=0,show="*")
        self.password.pack(expand=1)
        self.password.focus_force()
        Button(box,text="Deactivate",image=self.imgList['button'],bd=0,bg='#D0EEFF',
        activebackground='#D0EEFF',compound=CENTER,fg='white',
        activeforeground='white',font='leelawadee 13 bold',
        command=self.deactivate).pack(pady=30)
        self.password.bind('<Return>',lambda e : self.deactivate())
    def deactivate(self) :
        print(self.password.get())
        if self.password.get() == "" :
            messagebox.showwarning("BU Friends  |  Warning","Please enter your password")
            self.password.focus_force()
            return
        conn = self.controller.create_connection()
        conn.row_factory = sqlite3.Row
        sql = """SELECT PassHash,PassSalt FROM Users WHERE Uid=?"""
        sqlDelete = []
        sqlDelete.append("""DELETE FROM Blacklists WHERE Uid=?""")
        sqlDelete.append("""DELETE FROM Postings WHERE Uid=?""")
        sqlDelete.append("""DELETE FROM Reports WHERE ReporterUid=?""")
        sqlDelete.append("""DELETE FROM Reports WHERE ReportedUid=?""")
        sqlDelete.append("""DELETE FROM UsersTag WHERE Uid=?""")
        sqlDelete.append("""DELETE FROM Users WHERE Uid=?""")
        if conn is not None:
            c = self.controller.execute_sql(sql,[self.controller.uid])
            data = c.fetchone()
            passHash = data['passHash']
            passSalt = data['passSalt']
            passkey = self.controller.password_encryptioncheck(self.password.get(),passSalt)
            if passkey == passHash :
                print("same password ")
                ms = messagebox.askquestion("BU Friends  |  Notification","Are you sure you want to deactivate account?")
                if ms == "yes" :
                    for i,data in enumerate(sqlDelete):
                        c = self.controller.execute_sql(data,[self.controller.uid])
                    print("deactivate account")
                    self.controller.uid = 0
                    self.controller.set_sessions()
                    messagebox.showinfo("BU Friends  |  Successful","Your account has been deactivated\nHave a nice time and GOOD BYE ...")
                    self.controller.destroy()
            else :
                messagebox.showerror("BU Friends  |  Incomplete","Incorrect password! Please try again")
                self.password.focus_force()
                self.password.select_range(0,END)
        conn.close()
class InfoOnProfile() :
    def __init__(self, root, bgcolor,controller,parent,uid):
        self.root = root
        self.bgColor = bgcolor
        self.controller=controller
        self.optionFrame = None
        self.parent = parent
        self.uid = uid
        self.tagList = []
        self.mbtiTag = None
        self.get_profile()
        self.profile_frame()
        self.tag_frame()    
    def get_profile(self) :
        conn = self.controller.create_connection()
        sql = """SELECT DisplayName,Bio,Email FROM Users WHERE Uid=?"""
        sql2 = """SELECT UserType FROM UsersTag WHERE Uid=?"""
        sql3 = """SELECT TagName FROM Tags LEFT JOIN UsersTag 
        ON Tags.Tid=UsersTag.Tid1 OR Tags.Tid=UsersTag.Tid2 
        OR Tags.Tid=UsersTag.Tid3 OR Tags.Tid=UsersTag.Tid4 WHERE Uid=?"""
        if conn is not None:
            c = self.controller.execute_sql(sql,[self.uid])
            userData = c.fetchone()
            self.name = userData[0]
            self.bio = userData[1]
            self.email = userData[2]
            c = self.controller.execute_sql(sql2,[self.uid])
            self.tagList.append(c.fetchone()[0])
            c = self.controller.execute_sql(sql3,[self.uid])
            tagData = c.fetchall()
            for i,data in enumerate(tagData) :
                self.tagList.append(data[0])
        else:
            print("Error! cannot create the database connection.")
        conn.close()
        
    def request_delete(self) :
        sql = """INSERT INTO PermanentBanned(Email) SELECT Email FROM Users WHERE Users.Uid = ?"""
        sqlDelete = []
        sqlDelete.append("""DELETE FROM Blacklists WHERE Uid=?""")
        sqlDelete.append("""DELETE FROM Postings WHERE Uid=?""")
        sqlDelete.append("""DELETE FROM Reports WHERE ReporterUid=?""")
        sqlDelete.append("""DELETE FROM Reports WHERE ReportedUid=?""")
        sqlDelete.append("""DELETE FROM UsersTag WHERE Uid=?""")
        sqlDelete.append("""DELETE FROM Users WHERE Uid=?""")
        conn = self.controller.create_connection()
        if conn is not None:
            c = self.controller.execute_sql(sql,[self.controller.requestReport])
            for i,data in enumerate(sqlDelete):
                c = self.controller.execute_sql(data,[self.controller.requestReport])
            conn.close()
            messagebox.showinfo("BU Friends  |  Successful","This account has been deactivated")
            self.controller.requestReport = None
            self.controller.ridSelect = None
            self.controller.switch_frame(Administration)
            
    def request_blacklist(self) :
        conn = self.controller.create_connection()
        conn.row_factory = sqlite3.Row
        print(self.controller.requestReport)
        sql = """SELECT * FROM Blacklists WHERE Uid=?"""
        if conn is not None:
            c = self.controller.execute_sql(sql,[self.controller.requestReport])
            data = c.fetchone()
            if data is None :
                sql = """INSERT INTO Blacklists (Uid) SELECT Uid FROM Users WHERE Users.Uid = ?"""
                c = self.controller.execute_sql(sql,[self.controller.requestReport])
                sql = """UPDATE Blacklists SET EndDate = datetime(StartDate, '+7 days') WHERE Uid = ?"""
                c = self.controller.execute_sql(sql,[self.controller.requestReport])
                sql = """UPDATE Reports SET Status = 1 WHERE ReportedUid = ?"""
                c = self.controller.execute_sql(sql,[self.controller.requestReport])
                messagebox.showinfo("BU Friends  |  Successful","This account has been banned")
                self.controller.requestReport = None
                self.controller.ridSelect = None
                self.controller.switch_frame(Administration)
            else :
                sql = """SELECT Status,Amount FROM Blacklists WHERE Uid=?"""
                c = self.controller.execute_sql(sql,[self.controller.requestReport])
                data = c.fetchone()
                if data['Amount'] >= 3 :
                    ms = messagebox.askquestion("BU Friends  |  Warning","This account has been banned 3 times\nIf you continue, this account will be deactivted")
                    if ms == "yes" :
                        self.request_delete()
                        return
                    else: 
                        return
                if data['Status'] == 1 :
                    messagebox.showwarning("BU Friends  |  Incomplete","""This account has already banned\n***Policies***\n[minor offense] Reject the report\n[major offense] Deactivate this account""")
                else :
                    sql = """UPDATE Blacklists SET Amount=Amount+1, Status=1, StartDate=datetime('now'), EndDate=datetime('now','+7 days') WHERE Uid = ?"""
                    c = self.controller.execute_sql(sql,[self.controller.requestReport])
                    sql = """UPDATE Reports SET Status = 1 WHERE ReportedUid = ?"""
                    c = self.controller.execute_sql(sql,[self.controller.requestReport])
                    self.controller.requestReport = None
                    self.controller.ridSelect = None
                    self.controller.switch_frame(Administration)
                # update data
            conn.close()
    
    class ReportUser:
        def __init__(self, root, controllerFrame, oldframe):
            self.bgColor = "#333333"
            self.root = root
            self.controller = controllerFrame
            self.controller.title("BU Friends  |  Report-User")
            self.oldFrame = oldframe
            self.disable_allframe(oldframe)
            self.w,self.h = 700, 410
            self.x = (self.controller.width//2) - (self.w//2)
            self.y = (self.controller.height//2-10) - (self.h//2)
            self.reportFrame = Frame(self.controller, width=self.w, height=self.h,bg="#eeeeee",bd=1,relief=SOLID)
            self.reportFrame.propagate(0)
            self.reportFrame.place(x=self.x, y=self.y)
            self.top_geometry()
            self.content_geometry()
            self.reportFrame.grab_set()
            
        def top_geometry(self):
            bg = "#bbbbbb"
            hFrame = Frame(self.reportFrame, height=50, bg=bg, bd=0,relief=SOLID)
            hFrame.propagate(0)
            hFrame.pack(side=TOP,fill=X,pady=0)
            Label(hFrame, text="Report User", fg="#555555",font="leelawadee 16 bold",bg=bg).pack(side=LEFT,padx=18,pady=10)
            closeImg = self.controller.get_image(r'./assets/icons/Close.png')
            closeBtn = Button(hFrame, image=closeImg, command=lambda:self.report_closeto(self.oldFrame), width=70, bd=0, bg=bg,activebackground=bg)
            closeBtn.image = closeImg
            closeBtn.pack(side=RIGHT)

        def content_geometry(self):
            bg, fgHead,fg = "#eeeeee", "#555555","#222222"
            fontHead = "leelawadee 14 bold"
            mainFrame = Frame(self.reportFrame,height=self.h ,bg=bg, bd=0)
            mainFrame.pack(fill=BOTH)
            mainFrame.option_add('*font',self.controller.fontBody)
            canvas = Canvas(mainFrame, bg=bg,highlightthickness=0,height=self.h)
            canvas.pack(fill=BOTH)
            canvas.create_line(10,50,self.w-10,50, fill="#bbbbbb")
            canvas.create_line(10,100,self.w-10,100, fill="#bbbbbb")
            userReportedFrame = Frame(canvas,width=self.w, height=50,bg=bg, bd=0)
            canvas.create_window(20,10,anchor=NW,window=userReportedFrame)
            Label(userReportedFrame, text="Report", font=fontHead,fg=fgHead).pack(side=LEFT)
            self.userReported = self.get_udname_reported()
            Label(userReportedFrame, text=f"@{self.userReported['DisplayName']}",font=fontHead,fg="#B20600").pack(side=LEFT,padx=20)
            subjectFrame = Frame(canvas,width=self.w, height=50,bg=bg, bd=0)
            Label(subjectFrame, text="Subject", font=fontHead,fg=fgHead).pack(side=LEFT)
            subjectReportLst = ["Violence", "Hate Speech or Harassment",
                                "Nudity or Sexual content","Fake Account",
                                "False Information or Scams", "Intellectual Property"]
            self.sjCombo = ttk.Combobox(subjectFrame, values=subjectReportLst, width=49,state="readonly")
            self.sjCombo.set(subjectReportLst[0])
            self.sjCombo.pack(side=LEFT,padx=20)
            canvas.create_window(20,60,anchor=NW,window=subjectFrame)
            dFrame = Frame(canvas, bg=bg, width=650)
            canvas.create_window(20,110,anchor=NW,window=dFrame)
            Label(dFrame, text="Details",font=fontHead, fg=fgHead).pack(anchor=W)
            self.detailReport = Text(dFrame,bg="#fafafa",height=5,width=59,relief=SOLID)
            self.detailReport.pack(side=TOP,pady=5)
            self.detailReport.bind('<KeyPress>',lambda e: self.update_textlimit(e))
            self.detailReport.bind('<KeyRelease>',lambda e: self.update_textlimit(e))
            btnImg = self.controller.get_image(r'./assets/buttons/buttonRaw.png',240,66)
            self.sendReport = Button(canvas, command=lambda:self.report_commit(),text="Send Report!",image=btnImg,
                                     font=fontHead,fg=bg,bd=0,activebackground=bg,compound=CENTER)
            self.sendReport.image = btnImg
            limit = 256
            self.detailLenNow = Label(canvas, text=f"0/{limit}",font="leelawadee 12",justify=RIGHT,fg="#666666")
            self.controller.update_text_limit(self.detailReport, self.detailLenNow, limit, "Report Details")
            canvas.create_window((self.w//2)-120,280,anchor=NW, window=self.sendReport)
            canvas.create_window((self.w//2)+256,115, anchor=NW, window=self.detailLenNow)
        
        def report_closeto(self, frame):
            for i in range(len(frame)):
                for child in frame[i].winfo_children():
                    child.config(state=NORMAL)
            self.reportFrame.destroy()
            self.controller.title("BU Friends  |  Profile Review")
        def disable_allframe(self, frame):
            for i in range(len(frame)):
                for child in frame[i].winfo_children():
                    child.config(state=DISABLED)
            
        def get_udname_reported(self):
            print(self.controller.uidSelect)
            conn = self.controller.create_connection()
            if conn is None:
                print("No connection")
                return
            conn.row_factory = sqlite3.Row
            sqlwho = """SELECT DisplayName FROM Users WHERE Uid = ?;"""
            userReported = self.controller.execute_sql(sqlwho, [self.controller.uidSelect]).fetchone()
            conn.close()
            return userReported
           
        def report_commit(self):
            conn = self.controller.create_connection()
            if conn is None:
                print("Connection Failed")
                return
            sqlReport = """INSERT INTO Reports (ReporterUid, ReportedUid, Header, Detail) VALUES(?,?,?,?);"""
            reportDataLst = [self.controller.uid, self.controller.uidSelect, self.sjCombo.get(), self.detailReport.get(1.0,"end-1c")]
            print(reportDataLst)
            report = self.controller.execute_sql(sqlReport, reportDataLst)
            conn.commit()
            comitted = report.rowcount
            if comitted > 0:
                messagebox.showinfo("BU Friends  |  Successful",f"[ {self.userReported['DisplayName']} ] has been reported\nThank for information")
                self.report_closeto(self.oldFrame)
                return
            else:
                messagebox.showwarning("BU Friends  |  Incomplete","Cannot report this time\nPlease try again")
                return
        
    def option_click(self) :
        def next_page(index) :
            if pageList[index] is not None :
                print(self.controller.uidSelect)
                if pageList[index] == self.ReportUser:
                    self.optionFrame.destroy()
                    self.optionFrame = None
                    self.ReportUser(self.root, self.controller, [self.topFrame])
                    return
                self.controller.switch_frame(pageList[index])
            elif self.parent == 2 and index == 2 :
                ms = messagebox.askquestion("BU Friends  |  Notification","Are you sure you want to log out?")
                if ms == "yes" :
                    self.controller.uid = 0
                    self.controller.set_sessions()
                    self.controller.switch_frame(SignIn)
            elif self.parent == 3 :
                if index == 0 :
                    ms = messagebox.askquestion("BU Friends  |  Warning","Are you sure you want to ban this account?")
                    if ms == "yes" :
                        self.request_blacklist()
                else:
                    ms = messagebox.askquestion("BU Friends  |  Warning","Are you sure you want to deactivate this account?")
                    if ms == "yes" :
                        self.request_delete()
        bgColor = '#686DE0'
        if self.parent == 1 :
            optionList = ["Report"]
            imgOptionList = [None]
            pageList = [self.ReportUser]
        elif self.parent == 2 :
            optionList = ["Edit Profile","My account","Log out"]
            imgOptionList = [
                ('./assets/icons/edit.png',20,20),
                ('./assets/icons/userWhite.png',25,25),
                ('./assets/icons/signOut.png',25,25)]
            pageList = [EditPage,MyAccountPage,None]
        else :
            optionList = ["Blacklist","Delete account"]
            imgOptionList = [
                ('./assets/icons/blacklist.png',25,25),
                ('./assets/icons/delete.png',25,25)]
            pageList = [None,None]
        self.imgOption = []
        for i in range(len(optionList)) :
            if imgOptionList[i] is not None :
                self.imgOption.append(self.controller.get_image(imgOptionList[i][0],imgOptionList[i][1],imgOptionList[i][2]))
            else :
                self.imgOption.append(None)
        if self.optionFrame is None :
            self.optionFrame = Frame(self.root)
            for i,data in enumerate(optionList) :
                Button(self.optionFrame,text=data,bd=0,bg=bgColor,activebackground=bgColor,anchor=W
                ,padx=10,fg='white',activeforeground='white',font='leelawadee 13 bold',width=175
                ,image=self.imgOption[i],compound=LEFT
                ,command=lambda c=i : next_page(c)).pack(ipady=10)
            self.optionFrame.place(x=704,y=45)
        else :
            self.optionFrame.destroy()
            self.optionFrame = None

    def profile_frame(self) :
        self.topFrame = Frame(self.root,bg=self.bgColor)
        bottomFrame = Frame(self.root,bg=self.bgColor)
        imgPathList = ( ('./assets/icons/goback.png',50,50),
                        ('./assets/icons/hamberger.png',25,25),
                        ('./assets/icons/profile.png',180,180))
        profilePathLst = [r'./assets/images/avt0.png', 
                          r'./assets/images/avt1.png',
                          r'./assets/images/avt2.png', 
                          r'./assets/images/avt3.png',
                          r'./assets/images/avt4.png', 
                          r'./assets/images/avt5.png',]
        fontTag = Font(family='leelawadee',size=13)
        bottomFrame.option_add('*font',fontTag)
        self.imgList = []
        self.profileImgLst = []
        for i,data in enumerate(imgPathList) :
            img = self.controller.get_image(data[0],data[1],data[2])
            self.imgList.append(img)
        for i,data in enumerate(profilePathLst):
            img = self.controller.get_image(data,180,180)
            self.profileImgLst.append(img)
        if self.parent == 3 :
            Button(self.topFrame,image=self.imgList[0],bd=0,bg=self.bgColor,
            command=lambda:self.controller.switch_frame(Administration),
            activebackground=self.bgColor).pack(side=LEFT)
        else :
            Button(self.topFrame,image=self.imgList[0],bd=0,bg=self.bgColor,
            command=lambda:self.controller.switch_frame(Matching),
            activebackground=self.bgColor).pack(side=LEFT)
        self.optionBtn = Button(self.topFrame,image=self.imgList[1],bd=0,bg=self.bgColor,
        activebackground=self.bgColor,command=lambda:self.option_click())
        self.optionBtn.pack(side=RIGHT,padx=20)
        Label(bottomFrame,image=self.profileImgLst[self.uid%6],bg=self.bgColor).pack()
        Label(bottomFrame,text=self.name,font="leelawadee 22 bold",bg=self.bgColor).pack(pady=15)
        if self.bio is not None :
            bioWidget = Text(bottomFrame,bg=self.bgColor,width=40,bd=0)
            bioWidget.insert(END,self.bio)     
            bioWidget.tag_configure("center",justify=CENTER)
            bioWidget.tag_add("center",1.0,END)
            line = float(bioWidget.index(END)) - 1
            bioWidget.config(height=line,state=DISABLED)
            bioWidget.pack()
        self.topFrame.pack(fill=X)
        bottomFrame.pack(fill=X,pady=20)

    def tag_frame(self) :
        outerFrame = Frame(self.root,bg=self.bgColor,highlightthickness=2)
        outerFrame.pack(fill=X)
        fontTag = Font(family='leelawadee',size=13,weight='bold')
        outerFrame.option_add('*font',fontTag)
        imgPathList = ( ('./assets/buttons/mbtiPurple.png',130,45),
                        ('./assets/buttons/mbtiGreen.png',130,45),
                        ('./assets/buttons/mbtiCyan.png',130,45),
                        ('./assets/buttons/mbtiYellow.png',130,45))   
        if self.tagList[0] is not None :
            if self.tagList[0][1] == "N" :
                if self.tagList[0][2] == "T" :
                    self.img = self.controller.get_image(imgPathList[0][0],imgPathList[0][1],imgPathList[0][2])
                else :
                    self.img = self.controller.get_image(imgPathList[1][0],imgPathList[1][1],imgPathList[1][2])
            elif self.tagList[0][1] == "S" :
                if self.tagList[0][3] == "J" :
                    self.img = self.controller.get_image(imgPathList[2][0],imgPathList[2][1],imgPathList[2][2])
                else :
                    self.img = self.controller.get_image(imgPathList[3][0],imgPathList[3][1],imgPathList[3][2])     

        self.img2 = self.controller.get_image('./assets/buttons/tagButton.png',130,45)
        frame = Frame(outerFrame,bg=self.bgColor)
        frame.pack(pady=30)            
        for i,data in enumerate(self.tagList) :
            if data is not None :
                if i == 0 :
                    self.mbtiTag = Label(frame,text=data,image=self.img,compound=CENTER,bg=self.bgColor,fg='white')
                    self.mbtiTag.pack(side=LEFT)
                else :
                    Label(frame,text=data,image=self.img2,compound=CENTER,bg=self.bgColor,fg='white').pack(side=LEFT)
        if self.mbtiTag :
            self.mbtiTag.bind('<Button-1>',lambda e : self.mbti_info())
    def mbti_info(self) :
        for child in self.topFrame.winfo_children():
            child.config(state=DISABLED)
        print(self.tagList[0])
        if self.tagList[0] is not None :
            if self.tagList[0][1] == "N" :
                if self.tagList[0][2] == "T" :
                    mbtiColor = '#AF86E3'
                else :
                    mbtiColor = '#99D575'
            elif self.tagList[0][1] == "S" :
                if self.tagList[0][3] == "J" :
                    mbtiColor = '#83D8EF'
                else :
                    mbtiColor = '#D2C75D'
        self.closeImg = self.controller.get_image('./assets/icons/Close.png',30,30)
        bgFrame = Frame(self.controller,highlightthickness=2,highlightbackground=mbtiColor)
        fontTag = Font(family='leelawadee',size=15,weight='bold')
        bgFrame.option_add('*font',fontTag)
        data = mbtiData.get_mbti_info()[self.tagList[0]]
        lines = data.split("\n")
        des = ""
        for i in range(1,len(lines)):
            des += lines[i]
            if i < len(lines) - 1 :
                des += "\n"
        topFrame = Frame(bgFrame,bg=mbtiColor)
        topFrame.pack(fill=X)
        endFrame = Frame(bgFrame,bg='#F0F0F0')
        endFrame.pack(fill=BOTH)
        def mbtiinfo_close():
            bgFrame.destroy()
            for child in self.topFrame.winfo_children():
                child.config(state=NORMAL)
        Label(topFrame,text=lines[0],bg=mbtiColor,fg='white').pack(side=LEFT,padx=30,pady=15)
        Button(topFrame,image=self.closeImg,bd=0,bg=mbtiColor,
        activebackground=mbtiColor,command=lambda:mbtiinfo_close()).pack(side=RIGHT,padx=15)
        Label(endFrame,text=des,bg='#F0F0F0',font='leelawadee 13',justify=LEFT).pack(padx=30,pady=20)   
        bgFrame.place(relx=0.5, rely=0.5, anchor=CENTER)
        bgFrame.grab_set()
class PostOnProfile() :
    def __init__(self,root,bgColor,controller,uid):
        self.root = root
        self.bgColor = bgColor
        self.controller = controller
        self.frame = Frame(self.root,bg='#E6EEFD')
        self.postList = []
        self.uid = uid
        self.frame.pack(side=BOTTOM, fill=BOTH, expand=1)
        fontTag = Font(family='leelawadee',size=13)
        self.frame.option_add('*font',fontTag)
        self.get_post()
        self.post()
    def get_post(self) :
        conn = self.controller.create_connection()
        sql = """SELECT Detail FROM Postings WHERE Uid=?"""
        sql2 = """SELECT DisplayName FROM Users WHERE Uid=?"""
        if conn is not None:
                c = self.controller.execute_sql(sql,[self.uid])
                c2 = self.controller.execute_sql(sql2,[self.uid])
                userData = c.fetchall()
                self.name = c2.fetchone()[0]
                for i,data in enumerate(userData) :
                    self.postList.append(data[0])        
        else:
            print("Error! cannot create the database connection.")
        conn.close()
        Label(self.frame,text="Post",font="leelawadee 20 bold",bg='#E6EEFD').pack(anchor=W,padx=20,pady=5)
        print("post in profile =",len(self.postList))

    def post(self):
        limitPostlen = 300
        for i in range(1,len(self.postList)+1):
            innerFrame = LabelFrame(self.frame,bg=self.bgColor,relief=RIDGE,bd=1,width=815)
            Label(innerFrame,text=self.name,font="leelawadee 18 bold",bg=self.bgColor).pack(anchor=W,padx=15,pady=4)
            textPost = Text(innerFrame,width=90,relief=SUNKEN,bd=0)
            textPost.insert(END,self.postList[-i])
            textPost.tag_configure("center")
            textPost.tag_add("center",1.0,END)
            line = float(textPost.index(END)) - 1
            textPost.config(height=line,state=DISABLED)
            textPost.pack(pady=5)
            innerFrame.pack(ipadx=20,pady=10)

class Administration(Frame):
    def __init__(self,controller):
        Frame.__init__(self,controller)
        self.bgColor = '#181B23'
        self.controller = controller
        self.controller.title("BU Friends  |  Administration")
        Frame.config(self,bg=self.bgColor)
        scroll = ScrollFrame(self,self.bgColor)
        self.root = scroll.interior
        self.typeVar = IntVar()
        self.typeVar.set(1)
        self.allReports = []
        self.allBlacklists = []
        self.line = []
        self.searchBox = None
        self.imgList = {}
        imgPathList = [
            {'name':'logout','path':'./assets/icons/signOut.png','x':40,'y':40},
            {'name':'blacklist','path':'./assets/icons/BlacklistlDefault.png','x':30,'y':30},
            {'name':'blacklist2','path':'./assets/icons/BlacklistClicked.png','x':30,'y':30},
            {'name':'report','path':'./assets/icons/MailDefault.png','x':30,'y':30},
            {'name':'report2','path':'./assets/icons/MailClicked.png','x':30,'y':30},
            {'name':'longentry','path':'./assets/entrys/searchtabrz.png','x':760,'y':50}]
        for i,data in enumerate(imgPathList) :
            img = self.controller.get_image(data['path'],data['x'],data['y'])
            self.imgList[data['name']] = img
        if self.controller.ridSelect is None :
            self.page_geometry()
        else :
            self.page_geometry()
            self.RequestReport(self,self.controller,self.controller.ridSelect)
    def page_geometry(self) :
        def call_function() :
            if self.typeVar.get() == 1 :
                self.get_report()
            elif self.typeVar.get() == 2 :
                self.get_blacklist()
        def log_out() :
            ms = messagebox.askquestion("BU Friends  |  Notification","Are you sure you want to log out?")
            if ms == "yes" :
                self.controller.set_sessions()
                self.controller.switch_frame(SignIn)
        def on_entry_click() :
            if self.searchEntry.get() == 'Search':
                self.searchEntry.delete(0, END)
                self.searchEntry.insert(0, '')
        self.topFrame = Frame(self.root,bg=self.bgColor)
        self.topFrame.pack()
        self.searchEntryBox = Label(self.topFrame,image=self.imgList['longentry'],bg=self.bgColor)
        self.searchEntryBox.pack(pady=10,padx=20,side=LEFT)
        self.searchEntryBox.propagate(0)
        self.searchEntry = Entry(self.searchEntryBox,bd=0,font='leelawadee 15',fg='#B7B7B7',
        width=67,bg=self.bgColor,insertbackground='#B7B7B7')
        self.searchEntry.pack(expand=1,anchor=W,padx=10,side=LEFT)
        self.searchEntry.insert(END,"Search")
        self.searchEntry.bind('<FocusIn>', lambda e:on_entry_click())
        self.searchEntry.bind('<Return>', lambda e:self.get_search())
        Button(self.topFrame,image=self.imgList['logout'],bd=0,
        bg=self.bgColor,activebackground=self.bgColor,command=lambda:log_out()).pack(anchor=E,pady=15,padx=10)
        fontTag = Font(family='leelawadee',size=13,weight='bold')
        self.option_add('*font',fontTag)
        self.mainFrame = Frame(self.root,bg='#282D39',width=800,height=60)
        self.mainFrame.pack()
        self.mainFrame.propagate(0)
        self.reportRadioBtn = Radiobutton(self.mainFrame,text="New Report",bg='#282D39',
        fg='#B7B7B7',indicatoron=0,bd=0,width=400,height=60,anchor=W,variable=self.typeVar,
        value=1,selectcolor='#282D39',activeforeground='#7167A0',activebackground='#282D39',
        image=self.imgList['report'],selectimage=self.imgList['report2'],
        compound=LEFT,command=call_function,padx=20)
        self.reportRadioBtn.pack(side=LEFT,anchor=NW)

        self.blacklistRadioBtn = Radiobutton(self.mainFrame,text="Blacklist",bg='#282D39',
        fg='#B7B7B7',indicatoron=0,bd=0,width=400,height=60,anchor=W,variable=self.typeVar,
        value=2,selectcolor='#282D39',activeforeground='#7167A0',activebackground='#282D39',
        image=self.imgList['blacklist'],selectimage=self.imgList['blacklist2'],
        compound=LEFT,command=call_function,padx=20)
        self.blacklistRadioBtn.pack(anchor=W)

        bottomFrame = Frame(self.root,bg='#282D39',width=800,height=440)
        bottomFrame.pack()
        bottomFrame.propagate(0)
        self.scroll = ScrollFrame(bottomFrame,'#282D39')
        self.container = self.scroll.interior
        self.innerCanvas = Canvas(self.container, bg='#282D39',highlightthickness=0)
        self.innerCanvas.pack(side=LEFT, fill=BOTH, expand=1)
        self.innerCanvas.create_line(20, 0, 780, 0,fill='#868383')
        self.get_report()
    def get_report(self) :
        self.allReports.clear()
        self.blacklistRadioBtn.config(fg='#B7B7B7')
        self.reportRadioBtn.config(fg='#7167A0')
        conn = self.controller.create_connection()
        conn.row_factory = sqlite3.Row
        sql = """SELECT Rid,Header FROM Reports WHERE Status=0"""
        if conn is not None:
            c = self.controller.execute_sql(sql)
            data = c.fetchall()
            for i,report in enumerate(data) :
                self.allReports.append({'rid':report['Rid'],'header':report['Header']})
            for i,report in enumerate(self.allReports) :
                sql = """
                SELECT DisplayName FROM Users LEFT JOIN Reports 
                ON Users.Uid=Reports.ReportedUid WHERE Rid=?;"""
                c = self.controller.execute_sql(sql,[report['rid']])
                data = c.fetchone()
                self.allReports[i].update({'reportedName': data['displayName']})
        self.report_geometry()
    
    def get_blacklist(self) :
        self.allBlacklists.clear()
        self.reportRadioBtn.config(fg='#B7B7B7')
        self.blacklistRadioBtn.config(fg='#7167A0')
        conn = self.controller.create_connection()
        conn.row_factory = sqlite3.Row
        sql = """SELECT Uid,Amount FROM Blacklists WHERE Status=1"""
        if conn is not None:
            c = self.controller.execute_sql(sql)
            data = c.fetchall()
            for i,blacklist in enumerate(data) :
                self.allBlacklists.append({'uid':blacklist['Uid'],'amount':blacklist['Amount']})
            for i,blacklist in enumerate(self.allBlacklists) :
                sql = """
                SELECT DisplayName FROM Users LEFT JOIN Blacklists 
                ON Users.Uid=Blacklists.Uid WHERE Blacklists.Uid=?;"""
                c = self.controller.execute_sql(sql,[blacklist['uid']])
                data = c.fetchone()
                self.allBlacklists[i].update({'name': data['displayName']})
        self.blacklist_geometry()
    def get_search(self) :
        if self.searchBox :
            self.searchBox.destroy()
        self.mouse_pos = "out"
        def enter_event() :
            self.mouse_pos = "in"
        def leave_event() :
            self.mouse_pos = "out"
        def click_event() :
            if self.mouse_pos == "out" :
                self.searchBox.destroy()
        conn = self.controller.create_connection()
        conn.row_factory = sqlite3.Row
        sql = """
        SELECT Users.Uid,DisplayName,Email 
        FROM Users LEFT JOIN UsersTag ON UsersTag.Uid=Users.Uid 
        WHERE UsersTag.UserType != 'ADMIN' AND (DisplayName LIKE ? OR Email LIKE ?)"""
        if conn is not None:
            c = self.controller.execute_sql(sql,['%'+self.searchEntry.get()+'%','%'+self.searchEntry.get()+'%'])
            data = c.fetchall()
            conn.close()
            if data :
                self.searchBox = self.SearchUser(self.controller,data)
                self.searchBox.place(x=43,y=62)
                self.searchBox.bind("<Enter>", lambda e: enter_event())
                self.searchBox.bind("<Leave>", lambda e: leave_event())
                self.bind_all("<Button-1>", lambda e: click_event())
    
    def report_geometry(self) :
        for i,line in enumerate(self.line) :
            self.innerCanvas.delete(line)
        for child in self.innerCanvas.winfo_children():
            child.destroy()
        self.scroll.canvas.xview_moveto(0)
        self.scroll.canvas.yview_moveto(0)
        y = 65
        row_ = 0
        def request_rid(requestRid) :
            print("request_rid")
            print(f"Rid is {requestRid}")
            self.RequestReport(self,self.controller,requestRid)
        for i,report in enumerate(self.allReports) :
            Button(self.innerCanvas,text=report['reportedName'],bg='#282D39',fg='#B7B7B7',
            bd=0,activebackground='#282D39',activeforeground='#B7B7B7',anchor=W,
            width=15,height=2,command=lambda rid=report['rid'] : request_rid(rid)).grid(row=row_,column=0,sticky=W,pady=7,padx=20)
            Label(self.innerCanvas,text=report['header'],bg='#282D39',fg='#B7B7B7',
            font='leelawadee 13').grid(row=row_,column=1,sticky=W)
            self.line.append(self.innerCanvas.create_line(20, y, 780, y,fill='#868383'))
            y+=65
            row_+=1

    def blacklist_geometry(self) :
        for i,line in enumerate(self.line) :
            self.innerCanvas.delete(line)
        for child in self.innerCanvas.winfo_children():
            child.destroy()
        self.scroll.canvas.xview_moveto(0)
        self.scroll.canvas.yview_moveto(0)
        y = 65
        row_ = 0
        for i,blacklist in enumerate(self.allBlacklists) :
            Button(self.innerCanvas,text=blacklist['name'],bg='#282D39',fg='#B7B7B7',
            bd=0,activebackground='#282D39',activeforeground='#B7B7B7',anchor=W,
            width=15,height=2).grid(row=row_,column=0,sticky=W,pady=7,padx=20)
            msg = f"This account has been banned {blacklist['amount']} times"
            Label(self.innerCanvas,text=msg,bg='#282D39',fg='#B7B7B7',
            font='leelawadee 13').grid(row=row_,column=1,sticky=W)
            self.line.append(self.innerCanvas.create_line(20, y, 780, y,fill='#868383'))
            y+=65
            row_+=1
            
    class SearchUser(Frame):
        def __init__(self, controllerFrame, user):
            Frame.__init__(self, controllerFrame)
            Frame.config(self,bg='white')
            self.controller = controllerFrame
            self.user = user
            self.allSearch = []
            self.layout()
        def layout(self) :
            for row_, record in enumerate(self.user):
                Button(self,text=record['DisplayName'],bd=0,anchor=W,bg='white',activebackground='white',
                width=15,height=1,command=lambda uid=record['Uid'] : self.select_event(uid)).grid(row=row_,column=0,sticky=W,pady=7,padx=20)
                Label(self,text=record['Email'],bg='white',fg='#868383',
                font='leelawadee 13',anchor=W).grid(row=row_,column=1,sticky=W,ipadx=160)
                if row_>= 4: break
        def select_event(self,uid) :
            self.controller.uidSelect = uid
            self.controller.requestReport = uid
            self.controller.switch_frame(AdminReviewPage)
            
    class RequestReport:
        def __init__(self, root, controllerFrame,requestRid):
            self.root = root
            self.controller = controllerFrame
            self.controller.title("BU Friends  |  Report Request")
            self.bgColor = '#282D39'
            self.rid = requestRid
            self.report = None
            self.imgList = {}
            imgPathList = [
                {'name':'close','path':'./assets/icons/Close.png','x':30,'y':30},
                {'name':'button','path':'./assets/buttons/buttonGreyrz.png','x':120,'y':45}]
            for i,data in enumerate(imgPathList) :
                img = self.controller.get_image(data['path'],data['x'],data['y'])
                self.imgList[data['name']] = img
            self.get_request_report()
            self.page_geometry()
        def get_request_report(self) :
            conn = self.controller.create_connection()
            conn.row_factory = sqlite3.Row
            sql = """SELECT * FROM Reports WHERE Rid=?"""
            if conn is not None:
                c = self.controller.execute_sql(sql,[self.rid])
                data = c.fetchone()
                self.report = {
                    'reporter':data['ReporterUid'],'reported':data['ReportedUid'],
                    'header':data['Header'],'detail':data['Detail']
                }
                sql = """SELECT displayName FROM Users WHERE Uid=?"""
                c = self.controller.execute_sql(sql,[self.report['reporter']])
                data = c.fetchone()
                self.report.update({'reporterName':data['displayName']})

                sql = """SELECT displayName FROM Users WHERE Uid=?"""
                c = self.controller.execute_sql(sql,[self.report['reported']])
                data = c.fetchone()
                self.report.update({'reportedName':data['displayName']})
            print(self.report)
        def remember_rid(self):
            self.controller.ridSelect = self.rid
            self.controller.requestReport = self.report['reported']
            print("self.root.ridSelect",self.controller.ridSelect)
            self.controller.uidSelect = self.report['reported']
            self.controller.switch_frame(AdminReviewPage)
        def page_geometry(self) :
            mainFrame = Frame(self.controller,width=900,height=700,bg=self.bgColor)
            mainFrame.place(x=0,y=0)
            mainFrame.propagate(0)
            self.topFrame = Frame(mainFrame,bg='#181B23')
            self.topFrame.pack(fill=X)
            Label(self.topFrame,text=f"Sent by",bg='#181B23',fg='#B7B7B7').pack(padx=18,pady=15,anchor=W,side=LEFT)
            Label(self.topFrame,text=f"@{self.report['reporterName']}",bg='#181B23',fg='#A7f875').pack(padx=0,pady=15,anchor=W,side=LEFT)
            Button(self.topFrame,image=self.imgList['close'],bd=0,bg='#181B23',
            activebackground='#181B23',command=lambda:self.close_report(mainFrame)).pack(side=RIGHT,padx=20)
            canvas = Canvas(mainFrame, bg=self.bgColor,highlightthickness=0)
            canvas.pack(side=LEFT, fill=BOTH, expand=1)
            canvas.propagate(0)
            frameInCanvas = Frame(canvas,bg=self.bgColor)
            frameInCanvas.pack(fill=X,padx=20,pady=15)
            Label(frameInCanvas,text="Report",bg=self.bgColor,fg='#B7B7B7').grid(sticky=W,row=0,column=0)
            Button(frameInCanvas,text=f"@{self.report['reportedName']}",bg=self.bgColor,
            fg='#ff4646',bd=0,activebackground=self.bgColor,activeforeground='salmon',
            command=self.remember_rid).grid(sticky=W,row=0,column=1,padx=20)
            canvas.create_line(0, 55, 900, 55,fill='#868383')
            frameInCanvas2 = Frame(canvas,bg=self.bgColor)
            frameInCanvas2.pack(fill=X,padx=20,pady=10)
            Label(frameInCanvas2,text="Subject",bg=self.bgColor,fg='#B7B7B7').grid(sticky=W,row=1,column=0)
            Label(frameInCanvas2,text=f"{self.report['header']}",bg=self.bgColor,fg='white',
            font='leelawadee 13').grid(sticky=W,row=1,column=1,padx=20)
            canvas.create_line(0, 110, 900, 110,fill='#868383')
            detail = Text(canvas,relief=FLAT,height=15,bg=self.bgColor,fg='white')
            if self.report['detail'] :
                detail.insert(INSERT,self.report['detail'])
            detail.tag_configure('heading',font='leelawadee 13')
            detail.tag_add('heading',1.0,END)
            detail.config(state=DISABLED)
            detail.pack(padx=20,pady=15,anchor=W)     
            Button(canvas,text="Reject",image=self.imgList['button'],bd=0
            ,bg=self.bgColor,activebackground=self.bgColor,compound=CENTER,
            command=self.reject_report).pack(pady=10)
        def reject_report(self) :
            conn = self.controller.create_connection()
            sql = """UPDATE Reports SET Status=1 WHERE Rid=?"""
            if conn is not None:
                c = self.controller.execute_sql(sql,[self.rid])
                affected_rows = c.rowcount
                if affected_rows > 0 :
                    self.controller.requestReport = None
                    self.controller.ridSelect = None
                    self.controller.switch_frame(Administration)
        def close_report(self, mainFrame):
            mainFrame.destroy()
            self.controller.title("BU Friends  |  Administration")

if __name__ == '__main__':
    BUFriends().mainloop() 