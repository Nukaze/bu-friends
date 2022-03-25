'''
    Nukaze BU Friends
'''
from tkinter import *
from tkinter import ttk,messagebox
from tkinter import font
from tkinter.font import Font
from PIL import Image, ImageTk
from sqlite3 import Error
import sqlite3
import os
import hashlib
from datetime import *
import time
import random
import assets.mbti.mbtiData as qz


def BUFriends_Time():
    timeFull = datetime.now()
    timeNow = timeFull.strftime("%d-%b-%Y",) + " " + timeFull.strftime("( %H:%M:%S )")
    #print("[{}]\n[{}]".format(timeFull,timeNow))
    return timeNow


class BUFriends(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.frame = None
        self.uid = 0
        self.uidSelect = 0
        self.mbtiCode = ""
        self.timeNow = BUFriends_Time()
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
        with open(r'./database/sessions.txt','r')as ss:
            self.ssid = int(ss.read())
            print(self.ssid)
        if self.ssid == 0:
            self.switch_frame(SignIn)
        else:
            self.uid = self.ssid
            #self.switch_frame(Mbti)
            self.switch_frame(Matching)
            messagebox.showinfo('BU Friends',"{}Welcome back !{}".format(" "*10," "*10))

    def switch_frame(self, frame_class):
        print("switching to {} \n==|with uid = {}".format(frame_class, self.uid))
        new_frame = frame_class(self)
        if self.frame is not None:
            self.frame.destroy()
        self.frame = new_frame
        self.config(bg=self.frame.bgColor)
        self.frame.pack(side=BOTTOM, fill=BOTH, expand=TRUE)
        
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
    def __init__(self,root,scrollable):
        # creating
        self.root = root
        self.scrollable = scrollable
        self.scrollbar = Scrollbar(self.root, orient=VERTICAL,width=0)
        #self.scrollbar.pack(fill=Y, side=RIGHT, expand=0)
        self.canvas = Canvas(self.root, bg=self.root.bgColor,highlightthickness=0, yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=1)
        self.scrollbar.config(command=self.canvas.yview)
        # reset the view
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)
        # create a frame inside the canvas which will be scrolled with it
        self.interior = Frame(self.canvas,bg=self.root.bgColor)
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
        '''
            print(size)
        '''
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
            self.canvas.yview_scroll(int(-1*(event.delta/100)), "units")
        else :
            self.canvas.yview_scroll(0, "units")
            
    def _bind_to_mousewheel(self, event):
        self.root.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_from_mousewheel(self, event):
        self.root.unbind_all("<MouseWheel>")
        

class SignIn(Frame):
    def __init__(self, controllerFrame):
        Frame.__init__(self, controllerFrame)
        self.bgColor,self.fg = "#B6E0F7","#cc07e6"
        Frame.config(self, bg=self.bgColor)
        self.pack()
        self.root = ScrollFrame(self, False).interior
        self.SignInContent(self.root, controllerFrame)

    class SignInContent:
        def __init__(self, root, controllerFrame):
            self.bg,self.bgentry,self.fghead,self.fg,self.fgHolder = "#B6E0F7","#ffffff","#000000","#333333","#999999"
            self.controller = controllerFrame
            self.controller.uid = 0
            self.controller.title("BU Friends  |  Sign-In")
            print("uidcheck", self.controller.uid)
            self.root = root
            self.loginDict = {"usermail":"",
                              "userpass":""
                              }
            #BannerCanva
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
                            self.userEntryLst[index][0].config(show="*")
                        self.userEntryLst[index][0].delete(0,END)
                        self.userEntryLst[index][0].config(fg=self.fg)
                    def key_event(index):
                        if index == 1:
                            self.userEntryLst[index][0].config(show="*")
                        self.userEntryLst[index][0].config(fg=self.fg)
                    def access_event(index):
                        if index == 1:
                            self.login_req()
                    def entry_binding(index):
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
                self.loginBtn = Button(self.frameBtn, text="Sign-In", command=self.login_query
                                       , image=self.imgBtn, foreground="white", bg=self.bg,activebackground=self.bg
                                       , activeforeground="white",bd=0,compound="center")
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
        
        def login_query(self):
            sqlQuery = """SELECT Uid, PassHash, PassSalt, DisplayName FROM Users WHERE Email = ?;"""
            self.loginDict['usermail'] = (self.userName.get())
            conn = self.controller.create_connection()
            if conn is None:
                print("DB Can't Connect!")
                return
            else:
                #q = conn.cursor().execute(sqlQuery, [self.userName.get()])
                q = self.controller.execute_sql(sqlQuery, [self.userName.get()])
                rowExist = q.fetchall()
                print("checkfetch = ",len(rowExist))
                if rowExist == []:
                    messagebox.showwarning('Sign-in Incomplete', "Sorry [ {} ] Doesn't Exist \nPlease Check BU-Mail Carefully and Try Again.".format(self.userName.get()))
                    self.controller.switch_frame(SignIn)
                else:
                    self.row = rowExist[0]
                    self.login_validation()
            
        def login_validation(self):
            logPasskey = self.controller.password_encryptioncheck(self.userPass.get(), self.row[2])
            print("loghash {}\ndbhash  {}".format(logPasskey, self.row[1]))
            print(type(logPasskey), type(self.row[1]))
            self.loginDict['userpass'] = logPasskey
            if self.loginDict['userpass'] == self.row[1]:
                messagebox.showinfo('Sign-In Complete!',"Welcome Back [ {} ] \nHave a great time in BU Friends.".format(self.row[3]))
                self.controller.uid = self.row[0]
                self.login_submit()
            else:
                messagebox.showwarning('Sign-in Incomplete', "Sorry Your Password Did not Match \nPlease Check Your Password Carefully and Try Again.")
                self.userPass.focus_force()
                self.userPass.select_range(0,END)
        
        def login_submit(self):
            self.controller.switch_frame(Matching)
        
            
class SignUp(Frame):
    def __init__(self, controllerFrame):
        Frame.__init__(self, controllerFrame)
        self.bgColor = "#ccefff"
        Frame.config(self,bg=self.bgColor)
        self.pack()
        self.controller = controllerFrame
        self.controller.uid = 0
        self.root = ScrollFrame(self,False).interior
        self.SignUpContent(self.root, controllerFrame)

    class SignUpContent:
        def __init__(self, root, controllerFrame):
            self.controller = controllerFrame
            print("uidcheck",self.controller.uid)
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
                        self.entryLst[index].delete(0,END)
                        self.entryLst[index].config(fg=self.fg)
                    def key_event(index):
                        if index == 1 or index == 2:
                            self.entryLst[index].config(show="*")
                        self.entryLst[index].config(fg=self.fg)
                    def entry_binding(index):
                        self.entryLst[index].bind('<Button-1>',lambda e, index=index:clear_event(index))
                        self.entryLst[index].bind('<Key>', lambda e, index=index:key_event(index))
                    for i in range(len(self.entryLst)):
                        entry_binding(i)
                events()        
            def zone_buttons():
                self.imgBtn = self.controller.get_image(r'./assets/buttons/signup_newrz.png')
                self.imgBtn2 = self.controller.get_image(r'./assets/buttons/back_newrz.png')
                self.signupBtn = Button(root, text="Sign Up", command=self.signup_reqvalidation, image=self.imgBtn,fg="#ffffff"
                                   ,bg="#ffffff",bd=-10,compound="center",activebackground="#ffffff")
                self.backBtn = Button(root, text="Cancel", command=lambda:self.controller.switch_frame(SignIn), image=self.imgBtn2
                                    ,bg="#ffffff", foreground="white",bd=-10,compound="center",activebackground="#ffffff")
                self.canvasFrame.create_window(250,430,anchor="nw",window=self.signupBtn)
                self.canvasFrame.create_window(455,430,anchor="nw",window=self.backBtn)
            zone_widgets()
            zone_buttons() 
        # class method
        def signup_form(self,_root, _index):
            entry = Entry(_root, justify="left",relief="flat",fg=self.fgHolder,width=32)
            entry.insert(0,self.regisInfoLst[_index])
            return entry
        
        def register_error(self,errorFormat="Unknow error, Please Contact Moderater"):
            print("[SignUp Validator Reject]")
            messagebox.showinfo('Sign Up Incomplete', '{}\nPlease Sign Up Form Again'.format(errorFormat))

                    
        def signup_reqvalidation(self):
            print("check entry var")
            try:
                for i,data in enumerate(self.entryLst):
                    print(data.get())
                    if data.get() == "" or data.get().isspace() or " " in self.entryLst[0].get():
                        self.register_error("Sign Up Form Information do not Blank or Space")
                        self.entryLst[i].focus_force()
                        self.entryLst[i].select_range(0,END)
                        break
                if "@bumail.net" not in self.entryLst[0].get():
                    self.register_error("BU Friends Exclusive for Bangkok University\nStudent Mail  [ bumail.net ]  only")
                    self.entryLst[0].focus_force()
                    self.entryLst[0].select_range(0,END)
                    return
                elif self.entryLst[1].get() != self.entryLst[2].get():
                    self.register_error("Sign Up Password do not Matching")
                    self.entryLst[1].focus_force()
                    self.entryLst[1].select_range(0,END)
                    self.entryLst[2].delete(0,END)
                    return
                elif not len(self.entryLst[1].get()) > 7:
                    self.register_error(
                        "Sign Up Password Again\n[ Required ] At Least 8 Characters \n[ Required ] Alphabet and Number Password\n[ Optional ] Special Characters\nYour Password Have {} Characters".format(len(self.entryLst[1].get())))
                elif not self.check_alnumpass(self.entryLst[1].get()):
                    print("check alnum")
                    print(self.check_alnumpass(self.entryLst[1].get()))
                    self.register_error("Sign Up Password Again\n[ Required ] Alphabet and Number Password\n[ Optional ] Special Characters")
                else:
                    self.regisSubmitDict['bumail']=self.entryLst[0].get()
                    self.regisSubmitDict['displayname']=self.entryLst[3].get()
                    self.regisSubmitDict['bio']= ""
                    print(self.regisSubmitDict)
                    def database_validator(self):
                        conn = self.controller.create_connection()
                        if conn is None: print("DB Can't Create Connection in db validator.");return
                        else:
                            try:
                                print("query bumail..")   
                                sqlquery = """SELECT * FROM Users WHERE Email=?;"""
                                bumail = self.regisSubmitDict['bumail'] 
                                cur = self.controller.execute_sql(sqlquery, [bumail])
                                rowbumail = cur.fetchall()
                                print("rowbumail = ",rowbumail)
                                if rowbumail != []: self.register_error("Sorry This [ {} ] Already Existed".format(self.regisSubmitDict['bumail']))
                                else: self.password_encryption();conn.close()
                            except sqlite3.Error as e :print("catch!!! {}".format(e))
                    database_validator(self)
            except ValueError as ve: print(ve)
            
        def check_alnumpass(self,_pass):
            return any(c.isdigit() == True for c in _pass) and any(c.isalpha() == True for c in _pass)
        
        def password_encryption(self):
            print("password enc")
            stdhash = 'sha256'
            stdencode = 'utf-8'
            salt = os.urandom(32)
            password = self.entryLst[1].get()
            passkey = hashlib.pbkdf2_hmac(stdhash, password.encode(stdencode), salt, 161803)
            self.regisSubmitDict['passhash'], self.regisSubmitDict['salt'] = passkey, salt
            print("bumail = ", self.regisSubmitDict.get('bumail'))
            print("Displayname = ", self.regisSubmitDict.get('displayname'))
            print("Passhash = ", self.regisSubmitDict.get('passhash'))
            print("salt = ", self.regisSubmitDict.get('salt'))
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
                messagebox.showerror("Database Problem","Can't SignUp ")
            else:
                try:
                    self.controller.execute_sql(sqlRegis, userinfoValues)
                    self.controller.execute_sql(sqlAddUserTag)
                    cur = self.controller.execute_sql(sqlGetuid, [sqlMail])
                    getUid = (cur.fetchall())[0]
                    print(getUid)
                    self.controller.uid = getUid[0]
                    print("user id = [ {} ]".format(self.controller.uid))
                    messagebox.showinfo('Sign Up Successfully'
                                        ,"Welcome to BU Friends [ {} ] \nHave a Great Time in BU Friends".format(self.regisSubmitDict['displayname']))
                    conn.close()
                    self.signup_complete()
                except Error as e :print("catch!!! {}".format(e))

        def signup_complete(self):
            print(self.controller.uid)
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
            redirectLst = [lambda:self.controller.switch_frame(Mbti), lambda:self.controller.switch_frame(SignIn)]
            imgPathLst = [r'./assets/buttons/rectangleGreen.png',r'./assets/buttons/rectangleWhite.png']
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
        self.root = ScrollFrame(self, True).interior
        self.MbtiContent(self.root, controllerFrame)
        
    class MbtiContent:
        def __init__(self, root, controllerFrame):
            self.root = root
            self.controller = controllerFrame
            self.controller.title("BU Friends  |  MBTi Test")
            print("Checkuid",self.controller.uid)
            bg = "#ffffff"
            fontQuiz = Font(family="leelawadee",size=22,weight="bold")
            font = Font(family="leelawadee",size=14,weight="bold")
            self.mbtiFrame = Canvas(self.root,width=900,bd=0,highlightthickness=0,bg=bg)
            self.mbtiFrame.option_add("*font",font)
            self.mbtiFrame.pack(expand=1,fill=BOTH)
            self.bannerFrame = Frame(self.root)
            self.bannerMbti = self.controller.get_image(r'./assets/mbti/banner.png')
            Label(self.mbtiFrame, image=self.bannerMbti,bd=0).pack(side=TOP,expand=1,fill=X)
            self.mbtiFrame.image = self.bannerMbti
            self.backImg =  self.controller.get_image(r'./assets/icons/goback.png')
            self.back = Button(self.mbtiFrame,command=lambda:self.controller.switch_frame(SignIn), image=self.backImg, relief="flat",bd=0)
            self.back.place(x=20,y=10 ,anchor="nw")
            """if from regis page:
                self.back.config(command=lambda:self.controller.switch_frame(Matching))
            else:
                self.back.config(commnad=lambda:self.controller.switch_frame(EditProfile))
            """
            self.mbtiProgress = {'ie':[],
                                 'ns':[],
                                 'ft':[],
                                 'pj':[]
                                 }
            self.mbtiCodeLst = []
            self.quizLst = qz.get_MbtiQuizTH()
            self.answLst = qz.get_MbtiAnsTH()
            self.answVar = [StringVar() for i in range(len(self.quizLst))]
            self.answSubmitLst = []
            self.randLst = random.sample(range(len(self.quizLst)), len(self.quizLst))
            def request_quiz(_i):
                r = self.randLst[_i]
                bg = "#d0eeff"
                bgbtn = "#2E3033"
                btnfg = "#486edf"
                self.mainFrame = Frame(self.mbtiFrame,bg="pink")
                self.mainFrame.pack(expand=1,fill=BOTH)
                Label(self.mainFrame ,text="[{}] {}".format(i+1, self.quizLst[r][1]),font=fontQuiz,bg=bg,fg="#000000")\
                    .pack(expand=1,fill=X,ipady=200)
                self.subFrame = Frame(self.mainFrame,height=155)
                self.subFrame.propagate(0)
                self.subFrame.pack(expand=1,fill=X)
                self.a1 = Radiobutton(self.subFrame ,variable=self.answVar[r],value=self.answLst[r][0],text="{} {}".format("A :", self.answLst[r][2])\
                    ,bg=bgbtn,fg=btnfg,font=font,indicatoron=0,activebackground=btnfg,width=40)
                self.a1.pack(side=LEFT,expand=1,fill=Y,ipady=60)
                self.a2 = Radiobutton(self.subFrame ,variable=self.answVar[r],value=self.answLst[r][1],text="{} {}".format("B :", self.answLst[r][3])\
                    ,bg=bgbtn,fg=btnfg,font=font,indicatoron=0,activebackground=btnfg,width=40)
                self.a2.pack(side=LEFT,expand=1,fill=Y,ipady=60)
            print("RandomSample =",self.randLst)
            for i in range(len(self.quizLst)):
                request_quiz(i)
                pass
            self.btnImg = self.controller.get_image(r'./assets/buttons/buttonRaw.png')
            self.mbtiBtn = Button(self.mbtiFrame, text="Submit!", command=self.mbti_calculator, image=self.btnImg, compound="center",
                                  bd=0,activebackground=bg,bg=bg,fg=bg)
            self.mbtiBtn.image = self.btnImg
            self.mbtiBtn.pack(expand=1,pady=30)
    
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
            print(len(self.answVar))
            for i,data in enumerate(self.answVar):
                print(data.get(), end=", ")
                if "I" in data.get():self.mbtiProgress["ie"].append(0)
                elif "E" in data.get():self.mbtiProgress["ie"].append(1)
                elif "N" in data.get():self.mbtiProgress["ns"].append(0)
                elif "S" in data.get():self.mbtiProgress["ns"].append(1)
                elif "F" in data.get():self.mbtiProgress["ft"].append(0)
                elif "T" in data.get():self.mbtiProgress["ft"].append(1)
                elif "P" in data.get():self.mbtiProgress["pj"].append(0)
                elif "J" in data.get():self.mbtiProgress["pj"].append(1)
                else:
                    print("out of mbti range")
            self.mindLst = self.mbtiProgress.get('ie')
            self.energyLst = self.mbtiProgress.get('ns')
            self.natureLst = self.mbtiProgress.get('ft')
            self.tacticLst = self.mbtiProgress.get('pj')
            print("\n  Mind{}".format(self.mindLst))
            print("Energy{}".format(self.energyLst))
            print("Nature{}".format(self.natureLst))
            print("Tactic{}".format(self.tacticLst))
            try:
                if len(self.mindLst) != 7 or len(self.energyLst) != 7 or len(self.natureLst) != 7 or len(self.tacticLst) != 7:
                    self.reset_values()
                    messagebox.showwarning("MBTi Quiz Incomplete","Sorry Please Answer MBTi Quiz Completely.")
                    print("please answer quiz complete")
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
                    print("{} ".format(self.controller.mbtiCode))
                    self.mindLst.clear()
                    self.energyLst.clear()
                    self.natureLst.clear()
                    self.tacticLst.clear()
                    self.mbti_commit()
                    
            except: print("mbti calculator catch!!!")   
        
        def mbti_commit(self):
            print("checkuid b4 mbti commited",self.controller.uid)
            sqlMbti = """UPDATE UsersTag SET UserType = ? WHERE Uid = ? ;"""
            if self.controller.conn is None:
                print("DB Cannot Connect!")
            else:
                try:
                    self.controller.execute_sql(sqlMbti, (self.controller.mbtiCode, self.controller.uid))
                    print("mbti commited !")
                except Error as e:
                    print(e)
            self.controller.switch_frame(MbtiSuccess)
    
class MbtiSuccess(Frame):
    def __init__(self, controllerFrame):
        Frame.__init__(self, controllerFrame)
        self.bgColor = "#d0eeff"
        Frame.config(self,bg=self.bgColor)
        self.pack(expand=1,fill=BOTH)
        self.root = ScrollFrame(self, False).interior
        self.controller = controllerFrame
        bg = "#d0eeff"
        self.frame = Frame(self.root, width=900, height=600)
        self.frame.option_add('*font',self.controller.fontBody)
        self.frame.pack(expand=1,fill=BOTH)
        Label(self.frame, text=self.controller.mbtiCode, font=self.controller.fontHeading).pack(expand=1)
        self.controller.title("BUFriends  |  MBTi Test Successfully!")
        Button(self.frame,text="Go to Matching",command=lambda:self.controller.switch_frame(Matching)).pack(expand=1)
        Button(self.frame,text="Go to Edit Profile",command=lambda:self.controller.switch_frame(EditPage)).pack(expand=1)
        #get mbti code 
        #get mbti image
        #update mbti tag
        #wait designer Mbti Charecters
        pass


class Matching(Frame):
    def __init__(self, controllerFrame):
        Frame.__init__(self, controllerFrame)
        self.bgColor = "#FFFFFF"
        Frame.config(self,bg=self.bgColor)
        self.pack(expand=1,fill=BOTH)
        self.controller = controllerFrame
        print("matching id = ",self.controller.uid)
        with open(r'./database/sessions.txt','w')as ss:
            ss.write("{}".format(self.controller.uid))
        self.root = ScrollFrame(self, True).interior
        self.MatchingContent(self.root, self.controller)
        
    class MatchingContent:
        def __init__(self, root, controllerFrame):
            self.root = root
            self.controller = controllerFrame
            self.controller.title("BU Friends  |  Matching")
            print("checkuid =",self.controller.uid)
            self.bgCanva = "#FFFFFF"
            self.canvasMain = Canvas(self.root, width=900, height=6000 ,bg=self.bgCanva,bd=0, highlightthickness=0)
            self.canvasMain.pack(expand=1,fill=BOTH)
            print("reqwidth =",self.root.winfo_reqwidth())
            print("reqheight",self.root.winfo_reqheight())
            # widgetzone 
            self.filterframe = None
            self.headBgImg = self.controller.get_image(r'./assets/images/banner.png')
            self.headingBg = Label(self.canvasMain,image=self.headBgImg,compound=CENTER, bg=self.bgCanva,width=900,height=20)
            self.headingBg.pack(side=TOP,pady=30)
            self.searchBarImg = self.controller.get_image(r'./assets/darktheme/searchtabrz.png')
            self.searchBar = Button(self.canvasMain, text="#Hashtags Filter", command=lambda: self.filter_tags(), image=self.searchBarImg,
                              font="leelawadee 18 bold",bg=self.bgCanva,bd=0,activebackground=self.bgCanva, compound=CENTER)
            # self.searchBar = Button(self.canvasMain, text="#Hashtags Filter", command=lambda: self.filter_tags(), image=self.searchBarImg,
            #                         font="leelawadee 18 bold",bg=self.bgCanva,bd=0,activebackground=self.bgCanva, compound=CENTER)
            self.searchBar.image = self.searchBarImg
            self.searchBar.place(x=35,y=10,anchor=NW)
            self.myImg = self.controller.get_image(r'./assets/icons/profileXs.png')
            self.myProfile = Button(self.canvasMain, image=self.myImg, command=lambda:self.goto_my_profile(),bg=self.bgCanva,bd=0,activebackground=self.bgCanva, compound=CENTER)
            self.myProfile.image = self.myImg
            self.myProfile.place(x=815,y=11,anchor=NW)
            # Display user filter result
            self.usersFrame = Frame(self.canvasMain,width=900,bg=self.bgCanva)
            self.usersFrame.pack(side=BOTTOM,expand=1)
            self.uuidLst, self.uinfoLst, self.udnameLst = [],[],[]
            self.cntLoop = 0
            self.random_user()
            print("\nRe-Loop count (Found ADMIN or Your-Self) =",self.cntLoop)
            print("\nuuidLst user to show =",self.uuidLst)
            print("dname cnt=",len(self.udnameLst))
            print("dnamelst =",self.udnameLst)
            for i,info in enumerate(self.uinfoLst):
                print(*info,end=">=> ")
            print()
            self.display_user()
            
        def get_tagname(self):
            self.tagnameLst = []
            sql = """SELECT Tid,TagName FROM Tags"""
            self.conn = self.controller.create_connection()
            self.conn.row_factory = sqlite3.Row
            if self.conn is None:
                print('self.conn is None!!')
                return
            else:
                cur = self.controller.execute_sql(sql)
                row = cur.fetchone()
                while row:
                    self.tagnameLst.append({'tid':row['Tid'],'tagName':row['TagName']})
                    row = cur.fetchone()
                print("We have {} tag in Database.".format(len(self.tagnameLst)))
                self.conn.close()
                return self.tagnameLst
            print("tag name = ",self.tagnameLst)
            pass
        
        
        # people_by_name = build_dict(lst, key="name")
        # tom_info = people_by_name.get("Tom")
        def find_dict(seq, key):
            return dict((d[key], dict(d, index=index)) for (index, d) in enumerate(seq))
        
        def filter_tags(self):
            def destroy_frame():
                self.filterframe.destroy()
                self.filterframe = None
            bg = "#ffffff"
            fg = "#444444"
            if self.filterframe:
                destroy_frame()
            else:
                self.filterFrame = LabelFrame(self.root,bg=bg,width=740,relief=GROOVE,highlightthickness=0)
                #self.filterFrame.propagate(0)
                self.filterFrame.place(x=50,y=75,anchor=NW)
                self.mbtiFrame = LabelFrame(self.filterFrame,bg=bg,width=740,height=360,relief=GROOVE)
                self.mbtiFrame.pack(side=TOP,fill=X)
                self.mbtiFrame.propagate(0)
                ttFrame = Frame(self.mbtiFrame,bg=bg,width=740)
                ttFrame.pack(side=TOP,pady=25)
                Label(self.mbtiFrame, text="MBTI",bg=bg,fg=fg).place(x=20,y=20,anchor=NW)
                content = Frame(self.mbtiFrame,bg=bg,width=740)
                content.pack(side=TOP,fill=BOTH)
                self.selectTags = []
                mbtiLst = ["INTJ","INTP","ENTJ","ENTP",
                           "INFJ","INFP","ENFJ","ENFP",
                           "ISTJ","ISFJ","ESTJ","ESFJ",
                           "ISTP","ISFP","ESTP","ESFP"]
                w,h = 140, 50
                self.mbtiWidgets = []
                def show_mbti(_i, _utype,r,c):
                    print(r,c)
                    if "N" in _utype and "T" in _utype: self.userTagImg = self.controller.get_image(r'./assets/buttons/mbtiPurple2.png', w, h)
                    elif "N" in _utype and "F" in _utype: self.userTagImg = self.controller.get_image(r'./assets/buttons/mbtiGreen2.png', w, h)
                    elif "S" in _utype and "J" in _utype: self.userTagImg = self.controller.get_image(r'./assets/buttons/mbtiCyan2.png', w, h)
                    elif "S" in _utype and "P" in _utype: self.userTagImg = self.controller.get_image(r'./assets/buttons/mbtiYellow2.png', w, h)
                    btn = Button(content,command=lambda: print(_utype),text=_utype,
                                 image=self.userTagImg,fg=fg,bg=bg,bd=0,
                                 activebackground=bg,compound=CENTER)
                    btn.image = self.userTagImg
                    btn.grid(row=r,column=c,padx=18,pady=10, sticky=NSEW)
                    self.mbtiWidgets.append({"status":0, 
                                             "widget":btn, 
                                             "userType":_utype})
                r,c = 0,0
                for i,tag in enumerate(mbtiLst):
                    show_mbti(i,tag,r,c)
                    c+=1
                    if c==4:
                        c = 0
                        r +=1
                    
                self.tagsFrame = LabelFrame(self.filterFrame,bg=bg)
                self.tagsFrame.pack(side=TOP,fill=BOTH)
                self.tagnameLst.clear()
                self.tagnameLst = self.get_tagname()
                self.tagWidgets = []
                r,c = 0,0
                self.userTagImg = self.controller.get_image(r'./assets/buttons/tagButton2.png',w,h)
                def show_tag(_i, _tag):
                    btnTag = Button(self.tagsFrame, text=_tag['tagName'],command=lambda:print(_tag['tid']),
                                 image=self.userTagImg,bd=0,bg=bg,fg=fg,font="leelawadee 12 bold",
                                 activebackground=bg, compound=CENTER)
                    btnTag.image = self.userTagImg
                    btnTag.grid(row=r,column=c,padx=18,pady=10, sticky=NSEW)
                    self.tagWidgets.append({"status":0, 
                                            "widget":btnTag,
                                            "tid":_tag['tid'], 
                                            "tagName":_tag['tagName']})
                    pass
                for i,tag in enumerate(self.tagnameLst):
                    show_tag(i, tag)
                    c+=1
                    if c==4:
                        c = 0
                        r +=1
                    pass
                pass
        
        def random_user(self):
            def reset_var():
                self.uuidLst.clear()
                self.uinfoLst.clear()
                self.udnameLst.clear()
            reset_var()
            self.conn = self.controller.create_connection()
            self.conn.row_factory = sqlite3.Row
            if self.conn is None:
                print("DB connot connect")            
            else:
                sqlLastUid = """SELECT Uid FROM UsersTag ORDER BY Uid DESC LIMIT 1;"""
                cur = self.controller.execute_sql(sqlLastUid)
                userCount = (cur.fetchone())['Uid']             #get Last User Uid in DB
                randLst = []
                randLst = random.sample(range(1,userCount),12)
                while self.controller.uid in randLst:
                    reset_var()
                    randLst = random.sample(range(1,userCount),12)
                print(randLst)
                sqlRandTag = """SELECT * FROM UsersTag WHERE Uid IN (?,?,?,?,?,?,
                                                                     ?,?,?,?,?,?);"""
                cur = self.controller.execute_sql(sqlRandTag, randLst)
                infoRows = cur.fetchall()
                print(self.controller.uid)
                print(type(self.controller.uid))
                for i, row in enumerate(infoRows):
                    if row['UserType'] is None:
                        pass
                    elif "ADMIN" in row['UserType']:
                        self.cntLoop +=1
                        print("check admin")
                        reset_var()
                        randLst.clear()
                        self.conn.close()
                        self.random_user()
                        break
                    self.uinfoLst.append(row)
                    self.uuidLst.append(infoRows[i]['Uid'])
                    
                sqlDisplayName = """SELECT DisplayName FROM Users WHERE Uid IN (?,?,?,?,?,?,
                                                                                ?,?,?,?,?,?);"""
                curr = self.controller.execute_sql(sqlDisplayName, self.uuidLst)
                dnameRows = curr.fetchall()
                self.udnameLst.clear()
                for i,row in enumerate(dnameRows):
                    self.udnameLst.append(row['DisplayName'])
            pass
                    
        def display_user(self):
            self.userTabBtnImg = self.controller.get_image(r'./assets/images/rectangle.png',820,180)
            self.idxrandLst = random.sample(range(len(self.uuidLst)), len(self.uuidLst))
            print("Display random index of uuidlst",self.idxrandLst)
            self.get_tagname()
            print(self.tagnameLst)
            for i in range(len(self.uuidLst)):
                self.get_usertab(i)
                
        def get_usertab(self,_i):
            bgRectangle = "#e6eefd"
            ir = self.idxrandLst[_i]
            self.tabFrame = Frame(self.canvasMain,bg=self.bgCanva)
            self.tabFrame.pack(pady=10)
            self.tabFrame.option_add("*font","leelawadee 15 bold")
            self.tabFrame.option_add("*foreground","#ffffff")
            self.userTabBtn = Button(self.tabFrame, command=lambda:self.goto_review_profile(self.uuidLst[ir]), 
                                     image=self.userTabBtnImg, justify=LEFT,bg=self.bgCanva, 
                                     bd=0,compound=CENTER,activebackground=self.bgCanva,
                                    relief=FLAT)
            self.userTabBtn.pack(pady=10,anchor=W)
            self.userDisname = Label(self.tabFrame, text=self.udnameLst[ir],bg=bgRectangle, font="leelawadee 20 bold",fg="#000000")
            self.userDisname.place(x=210,y=40)
            self.img = self.controller.get_image(r'./assets/images/avt{}.png'.format(self.uuidLst[ir]%6),138,144)
            self.profileImg = Label(self.tabFrame, image=self.img ,bg=bgRectangle,bd=0)
            self.profileImg.image = self.img
            self.profileImg.place(x=40,y=20,anchor=NW)
            xplace = 200
            w,h = 140,45
            for i, tag in enumerate((self.uinfoLst[ir])):
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
                        self.userTag = Label(self.tabFrame, text="{}".format(tag), image=self.userTagImg,
                                            bg=bgRectangle, compound=CENTER)
                        self.userTag.image = self.userTagImg
                        self.userTag.place(x=xplace,y=110)
                    else:pass
                elif isinstance(tag, str):
                    self.userTag = Label(self.tabFrame, text="{}".format(self.uinfoLst[ir][i]), image=self.userTagImg,
                                        bg=bgRectangle, compound=CENTER)
                    self.userTag.image = self.userTagImg
                    self.userTag.place(x=xplace,y=110)
                else:
                    tag = self.tagnameLst[(self.uinfoLst[ir][i])-1]
                    self.userTag = Label(self.tabFrame, text="{}".format(tag['tagName']), image=self.userTagImg,
                                        bg=bgRectangle, compound=CENTER)
                    self.userTag.image = self.userTagImg
                    self.userTag.place(x=xplace,y=110)
                xplace += 150
            nextIcon = self.controller.get_image(r'./assets/icons/next.png')
            self.next = Button(self.tabFrame,command=lambda:self.goto_review_profile(self.uuidLst[ir]), image=nextIcon, 
                               bd=0, bg=bgRectangle, activebackground=bgRectangle)
            self.next.image = nextIcon
            self.next.place(x=720,y=45, anchor=NW)
            pass
        
        def get_userfilter(self):
            print("get_userfilter")
            pass
        
        def goto_review_profile(self,_uidselect):
            self.controller.uidSelect = _uidselect
            print(self.controller.uidSelect)
            self.controller.option_add('*foreground',"#000000")
            self.controller.switch_frame(ProfileReviewPage)
            
        def goto_my_profile(self):
            print(self.controller.uid)
            self.controller.option_add('*foreground',"#000000")
            self.controller.switch_frame(ProfilePage)
            
            
     
class ProfileReviewPage(Frame):
    def __init__(self,controller):
        Frame.__init__(self,controller)
        self.bgColor = 'white'
        self.controller = controller
        Frame.config(self,bg=self.bgColor)
        scroll = ScrollFrame(self,TRUE)
        self.root = scroll.interior
        self.profile = InfoOnProfile(self.root,self.bgColor,self.controller,1,self.controller.uidSelect)
        PostOnProfile(self.root,self.bgColor,self.controller,self.controller.uidSelect)

class ProfilePage(Frame):
    def __init__(self,controller):
        Frame.__init__(self,controller)
        self.bgColor = 'white'
        self.controller = controller
        Frame.config(self,bg=self.bgColor)
        scroll = ScrollFrame(self,TRUE)
        self.root = scroll.interior
        self.profile = InfoOnProfile(self.root,self.bgColor,self.controller,2,self.controller.uid)
        self.create_post_frame()
        PostOnProfile(self.root,self.bgColor,self.controller,self.controller.uid)
    def post_event(self):
        txt = self.post.get(1.0,END)
        if not txt.isspace() and len(txt) <=300 :
            conn = self.controller.create_connection()
            sql = """INSERT INTO Postings(Detail,Uid) VALUES (?,?)""".format(txt,self.controller.uid)
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
        self.post = Text(frame,width=90,height=4,relief=SUNKEN)
        self.post.pack()
        Button(frame,text="Post",font='leelawadee 13 bold',fg='white',
        activeforeground='white',image=self.img3,compound=CENTER,bd=0,
        bg=self.bgColor,activebackground=self.bgColor,command=self.post_event).pack(side=RIGHT,padx=35,pady=10)
        frame.pack(fill=X)   

class EditPage(Frame):
    def __init__(self,controller):
        Frame.__init__(self,controller)
        self.bgColor = 'white'
        self.controller = controller
        self.tagData = ProfilePage(self.controller).profile
        Frame.configure(self,bg=self.bgColor)
        scroll = ScrollFrame(self,FALSE)
        self.root = scroll.interior
        fontTag = Font(family='leelawadee',size=13,weight='bold')
        self.option_add('*font',fontTag)
        self.imgList = {}
        imgPathList = [
            {'name':'back','path':'./assets/icons/goback.png','x':50,'y':50},
            {'name':'entry','path':'./assets/entrys/entry2rz.png','x':400,'y':50},
            {'name':'tag','path':'./assets/buttons/tagEdit.png','x':130,'y':45},
            {'name':'add','path':'./assets/buttons/addTag.png','x':130,'y':45},
            {'name':'yellow','path':'./assets/buttons/mbtiYellowEdit.png','x':130,'y':45},
            {'name':'blue','path':'./assets/buttons/mbtiBlueEdit.png','x':130,'y':45},
            {'name':'green','path':'./assets/buttons/mbtiGreenEdit.png','x':130,'y':45},
            {'name':'purple','path':'./assets/buttons/mbtiPurpleEdit.png','x':130,'y':45},
            {'name':'longtag','path':'./assets/buttons/tagEditLong.png','x':180,'y':45},
            {'name':'button','path':'./assets/buttons/buttonPurplerz.png','x':200,'y':65},
            {'name':'cancel','path':'./assets/buttons/back_newrz.png','x':180,'y':40}]
        if self.tagData.tagList[0] is not None :
            if self.tagData.tagList[0][1] == "N" :
                if self.tagData.tagList[0][2] == "T" :
                    self.img = self.controller.get_image(imgPathList[4]['path'],imgPathList[4]['x'],imgPathList[4]['y'])
                else :
                    self.img = self.controller.get_image(imgPathList[5]['path'],imgPathList[5]['x'],imgPathList[5]['y'])
            elif self.tagData.tagList[0][1] == "S" :
                if self.tagData.tagList[0][3] == "J" :
                    self.img = self.controller.get_image(imgPathList[6]['path'],imgPathList[6]['x'],imgPathList[6]['y'])
                else :
                    self.img = self.controller.get_image(imgPathList[7]['path'],imgPathList[7]['x'],imgPathList[7]['y'])
        for i,data in enumerate(imgPathList) :
            img = self.controller.get_image(data['path'],data['x'],data['y'])
            self.imgList[data['name']] = img        
        self.page_geometry()
        self.tag_geometry()
        self.end_geometry()
    def page_geometry(self) :
        headList = ("Username","Bio","MBTI","Interest")
        Button(self.root,image=self.imgList['back'],bd=0
        ,bg=self.bgColor,activebackground=self.bgColor,
        command=lambda:self.controller.switch_frame(ProfilePage)).pack(anchor=NW)
        Label(self.root,text="Edit Profit",font='leelawadee 20 bold',
        bg=self.bgColor,anchor=N).pack(anchor=NW,padx=115,ipady=10)
        self.mainFrame = Frame(self.root,bg=self.bgColor)
        self.mainFrame.pack(anchor=W,padx=115)
        for i,data in enumerate(headList) :
            Label(self.mainFrame,text=data,fg='#868383'
            ,bg=self.bgColor).grid(row=i,column=0,pady=25,sticky=W)
        entryBox = Label(self.mainFrame,image=self.imgList['entry'],bg=self.bgColor)
        entryBox.grid(row=0,column=1,sticky=N,pady=10,padx=115)
        entryBox.propagate(0)
        entry = Entry(entryBox,font='leelawadee 15',width=35,bd=0)
        entry.insert(0,self.tagData.name)
        entry.pack(expand=1)
    
        entryBox2 = Label(self.mainFrame,image=self.imgList['entry'],bg=self.bgColor,height=75)
        entryBox2.grid(row=1,column=1,sticky=N,pady=10,padx=115)
        entryBox2.propagate(0)
        # entry2 = Entry(entryBox2,font='leelawadee 15',width=35,bd=0)
        # entry2.insert(0,self.tagData.bio)
        # entry2.pack(expand=1)
        entry2 = Text(entryBox2,font='leelawadee 15',bg=self.bgColor,width=35,height=3)
        if self.tagData.bio is not None :
            entry2.insert(END,self.tagData.bio)     
        entry2.pack(expand=1)

        # entry2 = Text(font='leelawadee 15',width=35)
        # entry2.insert(0,self.tagData.bio)
        # entry2.grid(row=1,column=1,sticky=N,pady=10,padx=115)
        
    def tag_geometry(self) :
        self.addWidget = None
        self.mbtiTag = None
        self.bmtiBtn = None
        self.vars = [StringVar() for i in range(len(self.tagData.tagList))]
        self.tagWidgetList = []
        if self.tagData.tagList[0] is not None :
            self.mbtiTag = Label(self.mainFrame,text=self.tagData.tagList[0],image=self.img,bg=self.bgColor,
            compound=CENTER,fg='white')
            self.mbtiTag.grid(row=2,column=1,sticky=W,padx=115)            
            self.bmtiBtn = Button(self.mainFrame,text="Redo the test?",bg=self.bgColor,fg='#23B7F4',bd=0,
            activebackground=self.bgColor,activeforeground='#23B7F4')
            self.bmtiBtn.grid(row=2,column=1)
        else :
            self.bmtiBtn = Button(self.mainFrame,text="Do the test?",bg=self.bgColor,fg='#23B7F4',bd=0,
            activebackground=self.bgColor,activeforeground='#23B7F4')
            self.bmtiBtn.grid(row=2,column=1,sticky=W,padx=115)
        if self.mbtiTag is not None :
            self.mbtiTag.bind('<Button-1>',lambda e: self.delete_mbti(e))
        # tagFrame = Frame(self.mainFrame,bg=self.bgColor)
        # tagFrame.grid(row=3,column=1,sticky=W,padx=115)
        # row = 0
        # column = 0
        row = 3
        top = Frame(self.mainFrame,bg=self.bgColor)
        top.grid(row=row,column=1,sticky=W,padx=115)
        frame = top
        for i in range(len(self.tagData.tagList)+1) :
            if i > 0 and i < len(self.tagData.tagList):
                self.vars[i].set(self.tagData.tagList[i])
                if len(self.tagData.tagList[i]) <= 9 :
                    tag = Label(frame,image=self.imgList['tag'],bg=self.bgColor)
                    # tag.grid(row=row,column=column,sticky=W)
                    tag.pack(anchor=W)
                    tag.propagate(0)
                    lb = Label(tag,text=self.tagData.tagList[i],fg='white',bg='#88A3F3',width=8,textvariable=self.vars[i])
                    lb.pack(expand=1,anchor=W,padx=10)

                else:
                    tag = Label(frame,image=self.imgList['longtag'],bg=self.bgColor)
                    # tag.grid(row=row,column=column,sticky=W)
                    tag.pack(anchor=W)
                    tag.propagate(0)
                    lb = Label(tag,text=self.tagData.tagList[i],fg='white',bg='#88A3F3',width=12,textvariable=self.vars[i])
                    lb.pack(expand=1,anchor=W,padx=12)
                tag.bind('<Button-1>',lambda e,c=i: self.delete_tag(e,c))
                self.tagWidgetList.append(tag)
                # column+= 1
                if i%2 == 0 :
                    row+=1
                    newframe = Frame(self.mainFrame,bg=self.bgColor)
                    newframe.grid(row=row,column=1,sticky=W,padx=115)
                    frame = newframe
                    # column=0
                else :
                    tag.pack(side=LEFT)
            elif i > 0 and i >= len(self.tagData.tagList):
                if len(self.tagData.tagList) <= 4 :
                    # Button(frame,image=self.imgList['add'],bg=self.bgColor,
                    # bd=0,activebackground=self.bgColor).pack(anchor=W)
                    self.addWidget = Label(frame,image=self.imgList['add'],bg=self.bgColor)
                    self.addWidget.pack(anchor=W)
                    self.addWidget.bind('<Button-1>',lambda e,c=i: self.add_tag(e))
    def end_geometry(self) :
            frame = Frame(self.root,bg=self.bgColor)
            frame.pack(pady=25)
            Button(frame,image=self.imgList['button'],text="Save Change",bd=0,compound=CENTER,
            bg=self.bgColor,fg='white',activebackground=self.bgColor,activeforeground='white',
            command=lambda : self.save_change()).pack(side=LEFT,padx=20)

            Button(frame,image=self.imgList['cancel'],text="Cancel",bd=0,
            bg=self.bgColor,fg='white',activebackground=self.bgColor,compound=CENTER,
            activeforeground='white').pack(side=LEFT)
    def delete_tag(self,event,index) :
        self.tagData.tagList.pop(index)
        if self.addWidget is not None :
            self.addWidget.destroy()
        if self.mbtiTag is not None :
            self.mbtiTag.destroy()
        self.bmtiBtn.destroy()
        for i in range(len(self.tagWidgetList)) :
            self.tagWidgetList[i].destroy()
        self.tag_geometry()
    def add_tag(self,event) :
        print("add tag")
    def delete_mbti(self,event) :
        self.tagData.tagList[0] = None
        self.bmtiBtn.destroy()
        self.mbtiTag.destroy()
        self.tag_geometry()
    def save_change(self) :
        print(self.tagData.tagList)
class MyAccountPage(Frame):
    def __init__(self,controller):
        Frame.__init__(self,controller)
        self.bgColor = 'white'
        self.controller = controller
        Frame.configure(self,bg=self.bgColor)
        scroll = ScrollFrame(self,FALSE)
        self.root = scroll.interior
        fontTag = Font(family='leelawadee',size=13,weight='bold')
        self.option_add('*font',fontTag)
        self.my_account()
    def my_account(self) :
        self.imgList = {}
        imgPathList = [
            {'name':'back','path':'./assets/icons/goback.png','x':50,'y':50},
            {'name':'pwd','path':'./assets/buttons/my_account.png','x':660,'y':55},
            {'name':'delete','path':'./assets/buttons/deactivate.png','x':660,'y':55},
            {'name':'background','path':'./assets/images/myaccount.png','x':800,'y':338}]
        for i,data in enumerate(imgPathList) :
            img = self.controller.get_image(data['path'],data['x'],data['y'])
            self.imgList[data['name']] = img

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

        Label(self.root,image=self.imgList['background'],bg=self.bgColor).pack(pady=20)
class ChangePasswordPage(Frame):
    def __init__(self,controller):
        Frame.__init__(self,controller)
        self.bgColor = 'white'
        self.controller = controller
        Frame.configure(self,bg=self.bgColor)
        scroll = ScrollFrame(self,FALSE)
        self.root = scroll.interior
        fontHead = Font(family='leelawadee',size=13,weight='bold')
        self.option_add('*font',fontHead)
        self.page_geometry()
    def page_geometry(self) :
        self.pwdList = [StringVar(),StringVar(),StringVar()]
        # self.pwdList = {
        #     'current':StringVar(),
        #     'new':StringVar(),
        #     'confirm':StringVar()}
        self.imgList = {}
        imgPathList = [
            {'name':'back','path':'./assets/icons/goback.png','x':50,'y':50},
            {'name':'button','path':'./assets/buttons/buttonPurplerz.png','x':200,'y':65}]
        textList = ("Current Password","New Password","Confirm Password")
        for i,data in enumerate(imgPathList) :
            img = self.controller.get_image(data['path'],data['x'],data['y'])
            self.imgList[data['name']] = img
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
            entry = Entry(canvas,font="leelawadee 13",bd=0,fg='#868383',textvariable=self.pwdList[i])
            if i == 0 :
                entry.focus_force()
            entry.pack(padx=140,pady=20,anchor=W,fill=X)
            canvas.create_line(140, y, 760, y,fill='#868383')
            y+=96
        Button(canvas,text="Update Password",image=self.imgList['button'],bd=0,bg=self.bgColor,
        activebackground=self.bgColor,compound=CENTER,fg='white',activeforeground='white',
        command=self.password_validation).pack(pady=30)
    def password_validation(self) :
        self.pwds = []
        for i in range(len(self.pwdList)) :
            self.pwds.append(self.pwdList[i].get())
        if len(self.pwds[0]) > 0 :
            print("have data")
            if len(self.pwds[1]) > 7 and any(c.isdigit() == True for c in self.pwds[1]) and any(c.isalpha() == True for c in self.pwds[1]):
                print("allowed password")
                if self.pwds[1] == self.pwds[2] :
                    print("match password")
                    self.change_password()
                else :
                    messagebox.showerror("Change password","Password do not Matching")
            else :
                messagebox.showerror("Change password","Invalid password!!!\n[ Required ] At Least 8 Characters \n[ Required ] A mixture of letters and numbers")
        else:
            messagebox.showerror("Change password","Please enter current password")
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
                try:
                    c2 = self.controller.execute_sql(sql2, (newpass,newSalt,self.controller.uid))
                    messagebox.showinfo("Change password","Password has been successfully changed.")
                    self.controller.switch_frame(MyAccountPage)
                except Error as e:
                    print(e)
            else :
                messagebox.showerror("Change password","Incorrect current password!!!")
        conn.close()

class DeactivatePage(Frame):
    def __init__(self,controller):
        Frame.__init__(self,controller)
        self.bgColor = 'white'
        self.controller = controller
        self.data = ProfilePage(self.controller).profile
        Frame.configure(self,bg=self.bgColor)
        scroll = ScrollFrame(self,FALSE)
        self.root = scroll.interior
        fontHead = Font(family='leelawadee',size=20,weight='bold')
        self.fontBody = Font(family='leelawadee',size=15,weight='bold')
        self.option_add('*font',fontHead)
        self.page_geometry()
    def page_geometry(self) :
        self.password = StringVar()
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
        canvas = Canvas(self.root,highlightthickness=0,bg=self.bgColor)
        canvas.pack(fill=BOTH, expand=1)

        Button(canvas,image=self.imgList['back'],bd=0,
        bg=self.bgColor,activebackground=self.bgColor,
        command=lambda:self.controller.switch_frame(MyAccountPage)).pack(anchor=NW)
        Label(canvas,text="Deactivate Account",
        bg=self.bgColor,anchor=N).pack(anchor=NW,padx=115,ipady=10)
        topFrame = Frame(canvas,bg=self.bgColor)
        topFrame.pack(anchor=W,padx=115,pady=15)
        Label(topFrame,image=self.imgList['profile'],
        bg=self.bgColor).pack(side=LEFT)
        Label(topFrame,text=self.data.name,bg=self.bgColor).pack(pady=5,anchor=W,padx=20)
        Label(topFrame,text=self.data.email,font=self.fontBody,bg=self.bgColor,
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
        entry = Entry(entryBox,font='leelawadee 15',width=35,bd=0,
        textvariable=self.password,show="*")
        entry.pack(expand=1)
        entry.focus_force()
        Button(box,text="Deactivate",image=self.imgList['button'],bd=0,bg='#D0EEFF',
        activebackground='#D0EEFF',compound=CENTER,fg='white',
        activeforeground='white',font='leelawadee 13 bold',
        command=self.deactivate).pack(pady=30)
    def deactivate(self) :
        pwd = self.password.get()
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
            passkey = self.controller.password_encryptioncheck(pwd,passSalt)
            if passkey == passHash :
                print("same password")
                ms = messagebox.askquestion("Deactivate","Are you sure you want to deactivate account?")
                if ms == "yes" :
                    for i,data in enumerate(sqlDelete):
                        c = self.controller.execute_sql(data,[self.controller.uid])
                    print("deactivate account")
                    self.controller.destroy()
                else :
                    self.password.set('')
            #     # newSalt = os.urandom(32)
            #     # newpass = self.controller.password_encryptioncheck("test1234",newSalt)
            #     # sql2 = """UPDATE Users SET PassHash = ?,PassSalt = ? WHERE uid = ?"""
            #     # try:
            #     #     c = self.controller.execute_sql(sql2, (newpass,newSalt,self.controller.uid))
            #     # except Error as e:
            #     #     print(e)
            else :
                messagebox.showerror("Deactivate","Incorrect password!!!")
        conn.close()
class InfoOnProfile() :
    def __init__(self, root, bgcolor,controller,parent,uid):
        self.root = root
        self.bgColor = bgcolor
        self.controller=controller
        self.optionFrame = None
        self.parent = parent
        self.uid = uid
        conn = self.controller.create_connection()
        sql = """SELECT DisplayName,Bio,Email FROM Users WHERE Uid=?"""
        sql2 = """SELECT UserType,Tid1,Tid2,Tid3,Tid4 FROM UsersTag WHERE Uid=?"""
        if conn is not None:
            c = self.controller.execute_sql(sql,[self.uid])
            c2 = self.controller.execute_sql(sql2,[self.uid])
            tagData = c2.fetchone()
            print(tagData)
            self.tagList = []
            self.tagList.append(tagData[0])
            for i in range(1,len(tagData)):
                if tagData[i] is not None :
                    sql3 = """SELECT TagName FROM Tags WHERE Tid=?"""
                    c3 = self.controller.execute_sql(sql3,[tagData[i]])
                    self.tagList.append(c3.fetchone()[0])
            userData = c.fetchone()
            self.name = userData[0]
            self.bio = userData[1]
            self.email = userData[2]
        else:
            print("Error! cannot create the database connection.")
        conn.close()
        self.profile_frame()
        self.tag_frame()    

    def option_click(self) :
        def next_page(index) :
            if pageList[index] is not None :
                self.controller.switch_frame(pageList[index])
            elif self.parent == 2 and index == 2 :
                ms = messagebox.askquestion("log out","Are you sure you want to log out?")
                if ms == "yes" :
                    self.controller.uid = 0
                    with open(r'./database/sessions.txt','w')as ss:
                        ss.write("{}".format(0))
                    self.controller.switch_frame(SignIn)
        bgColor = '#686DE0'
        if self.parent == 2 :
            optionList = ["Edit","My account","Log out"]
            imgOptionList = [
                ('./assets/icons/edit.png',20,20),
                ('./assets/icons/userWhite.png',25,25),
                ('./assets/icons/signOut.png',25,25)]
            pageList = [EditPage,MyAccountPage,None]
        else :
            optionList = ["Report"]
            imgOptionList = [None]
            pageList = [None]
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
        topFrame = Frame(self.root,bg=self.bgColor)
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
        for i,data in enumerate(imgPathList) :
            img = self.controller.get_image(data[0],data[1],data[2])
            self.imgList.append(img)
        self.profileImgLst = []
        for i, path in enumerate(profilePathLst):
            img = self.controller.get_image(path,180,180)
            self.profileImgLst.append(img)
        Button(topFrame,image=self.imgList[0],command=lambda:self.controller.switch_frame(Matching),bd=0,bg=self.bgColor,activebackground=self.bgColor).pack(side=LEFT)
        Button(topFrame,image=self.imgList[1],bd=0,bg=self.bgColor,
        activebackground=self.bgColor,command=lambda:self.option_click()).pack(side=RIGHT,padx=20)
        Label(bottomFrame,image=self.profileImgLst[self.uid%6],bg=self.bgColor).pack()
        Label(bottomFrame,text=self.name,font="leelawadee 22 bold",bg=self.bgColor).pack(pady=15)
        if self.bio is not None :
            bioWidget = Text(bottomFrame,bg=self.bgColor,width=30,bd=0)
            bioWidget.insert(END,self.bio)     
            bioWidget.tag_configure("center",justify=CENTER)
            bioWidget.tag_add("center",1.0,END)
            line = float(bioWidget.index(END)) - 1
            bioWidget.config(height=line,state=DISABLED)
            bioWidget.pack()
        topFrame.pack(fill=X)
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
                    Label(frame,text=data,image=self.img,compound=CENTER,bg=self.bgColor,fg='white').pack(side=LEFT)
                else :
                    Label(frame,text=data,image=self.img2,compound=CENTER,bg=self.bgColor,fg='white').pack(side=LEFT)

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
        print(len(self.postList))
        self.post()

    def post(self):
        for i in range(1,len(self.postList)+1):
            innerFrame = Frame(self.frame,bg=self.bgColor)
            Label(innerFrame,text=self.name,font="leelawadee 18 bold",bg=self.bgColor).pack(anchor=W,padx=15)
            textPost = Text(innerFrame,width=90,relief=SUNKEN,bd=0)  
            textPost.insert(END,self.postList[-i])     
            textPost.tag_configure("center")
            textPost.tag_add("center",1.0,END)
            line = float(textPost.index(END)) - 1
            textPost.config(height=line,state=DISABLED)
            textPost.pack(pady=5)
            innerFrame.pack(ipadx=20,pady=10)


if __name__ == '__main__':
    BUFriends().mainloop()
    