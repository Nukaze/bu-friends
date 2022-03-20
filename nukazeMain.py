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
        #self.switch_frame(SignIn)
        #self.switch_frame(Mbti)
        self.switch_frame(Matching)

    def switch_frame(self, frame_class):
        print("switching to {}".format(frame_class))
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
                c = self.conn.cursor()
                c.execute(sql)
                self.conn.commit()
            except Error as e:
                print(e)
        else:
            try:
                c = self.conn.cursor()
                c.execute(sql, values)
                self.conn.commit()
            except Error as e:
                print(e)
        return c
    
    def get_image(self, _path):
        img = PhotoImage(file = _path)
        return img
    
    def get_imagerz(self, _path, _width, _height):
        origin = Image.open(_path).resize((_width,_height),Image.ANTIALIAS)
        img = ImageTk.PhotoImage(origin)
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
        
        def login_submit(self):
            self.controller.switch_frame(Mbti)
        
            
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
            self.canvasFrame.pack(expand=1,fill=BOTH)
            
            self.bgCanvaImg = self.controller.get_image(r"./assets/images/regisbg.png")
            self.canvasFrame.create_image(0,0,image=self.bgCanvaImg,anchor="nw")
            self.canvasFrame.create_text(450,90,text="Registration",font="leelawadee 36 bold", fill=self.fgHead)
            self.regisInfoLst = ["Enter your BU-Mail", "Enter Your Password", "Confirm Your Password", "Enter your Display Name"]
            self.regisVarLst = []
            self.regisSubmitDict  = {'bumail': "",
                                    'passhash':"",
                                    'salt':"",
                                    'displayname':"",
                                    'bio':""}
            def zone_widgets():
                self.entryLst = []
                self.entryimg = self.controller.get_image(r'./assets/entrys/entry2rz.png')
                for i in range(len(self.regisInfoLst)):
                    self.regisVarLst.append(StringVar())
                    self.entryLst.append(self.signup_form(self.canvasFrame, i, self.regisVarLst[i]))
                    x,y = 260,70*(i+2)
                    self.canvasFrame.create_image(x,y,image=self.entryimg,anchor="nw")
                    #self.canvasFrame.create_line(x+10,y+40,650,y+40,fill="blue",smooth=True)
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
                self.signupBtn = Button(root, text="Sign Up", command=self.signup_submitreq, image=self.imgBtn,fg="#ffffff"
                                   ,bg="#ffffff",bd=-10,compound="center",activebackground="#ffffff")
                self.backBtn = Button(root, text="Cancel", command=lambda:self.controller.switch_frame(SignIn), image=self.imgBtn2
                                    ,bg="#ffffff", foreground="white",bd=-10,compound="center",activebackground="#ffffff")
                self.canvasFrame.create_window(250,430,anchor="nw",window=self.signupBtn)
                self.canvasFrame.create_window(455,430,anchor="nw",window=self.backBtn)
            zone_widgets()
            zone_buttons() 
        # class method
        def signup_form(self,_root, _index, _entVar):
            entry = Entry(_root, textvariable=_entVar, justify="left",relief="flat",fg=self.fgHolder,width=32)
            entry.insert(0,self.regisInfoLst[_index])
            return entry
        
        def register_error(self,errorFormat="Unknow error, Please Contact Moderater"):
            print("[SignUp Validator Reject]")
            messagebox.showinfo('Sign Up Incomplete', '{}\nPlease Sign Up Form Again'.format(errorFormat))
            for var in self.regisVarLst:
                var.set("")
                print("Varget =",var.get())
            #self.regisSubmitDict.fromkeys(self.regisSubmitDict, "")    reset Submitdict values to = ""
            self.controller.switch_frame(SignUp)
                    
        def signup_submitreq(self):
            print("check regis var")
            print(self.regisSubmitDict)
            def signup_validator(self):
                try:
                    for i,data in enumerate(self.regisVarLst):
                        print(data.get())
                        if data.get() == "" or data.get().isspace() or " " in self.regisVarLst[0].get():
                            self.register_error("Sign Up Form Information do not Blank or Space")
                            break
                    if "@bumail.net" not in self.regisVarLst[0].get():
                        self.register_error("BU Friends Exclusive for Bangkok University\nStudent Mail  [ bumail.net ]  only")
                    elif self.regisVarLst[1].get() != self.regisVarLst[2].get():
                        self.register_error("Sign Up Password do not Matching")
                    elif not len(self.regisVarLst[1].get()) > 7 and (self.regisVarLst[1].get()).isalnum():
                        self.register_error("Sign Up Password Again\n[ Required ] At Least 8 Characters \n[ Required ] Alphanumeric Password\nYour Password Have {} Characters".format(len(self.regisVarLst[1].get())))
                    else:
                        print("go addict")
                        self.regisSubmitDict['bumail']=self.regisVarLst[0].get()
                        self.regisSubmitDict['displayname']=self.regisVarLst[3].get()
                        self.regisSubmitDict['bio']= ""
                        print(self.regisSubmitDict)
                        def database_validator(self):
                            conn = self.controller.create_connection()
                            if conn is None:
                                print("DB Can't Create Connection in db validator.")
                            else:
                                try:
                                    print("query bumail..")   
                                    sqlquery = """SELECT * FROM Users WHERE Email=?;"""
                                    bumail = self.regisSubmitDict['bumail'] 
                                    cur = self.controller.execute_sql(sqlquery, [bumail])
                                    rowbumail = cur.fetchall()
                                    print("rowbumail = ",rowbumail)
                                    if rowbumail != []: self.register_error("Sorry This [ {} ] Already Existed".format(self.regisSubmitDict['bumail']))
                                    else: self.password_encryption()
                                except sqlite3.Error as e :print("catch!!! {}".format(e))
                        database_validator(self)
                except ValueError as ve:
                    print(ve)
            signup_validator(self)
        
        def password_encryption(self):
            print("password enc")
            stdhash = 'sha256'
            stdencode = 'utf-8'
            salt = os.urandom(32)
            password = self.regisVarLst[1].get()
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
                            self.regisSubmitDict['displayname']
                            )
            
            sqlGetuid = """SELECT Uid FROM Users WHERE Email = ?;"""
            sqlMail = (self.regisSubmitDict['bumail'])          
            
            sqlAddUserTag = """INSERT INTO UsersTag VALUES(NULL,NULL,NULL,NULL,NULL,NULL);"""

            print(type(self.regisSubmitDict['passhash']))
            print(type(self.regisSubmitDict['salt']))
            if self.controller.conn is None:
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
            """if from regis page:
                self.back.config(command=lambda:self.controller.switch_frame(Matching))
            else:
                self.back.config(commnad=lambda:self.controller.switch_frame(EditProfile))
            """
            self.back.place(x=20,y=10 ,anchor="nw")
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
        self.root = ScrollFrame(self, True).interior
        self.MatchingContent(self.root, self.controller)
        
    class MatchingContent:
        def __init__(self, root, controllerFrame):
            self.root = root
            self.controller = controllerFrame
            self.controller.title("BU Friends  |  Matching")
            print("checkuid =",self.controller.uid)
            self.bgCanva = "#FFFFFF"
            self.canvasMain = Canvas(self.root, width=900, bg=self.bgCanva,bd=0, highlightthickness=0)
            self.canvasMain.pack(expand=1,fill=BOTH)
            print("reqwidth =",self.root.winfo_reqwidth())
            print("reqheight",self.root.winfo_reqheight())
            self.widgetFrame = Frame(self.root)
            self.widgetFrame.pack(side=TOP)
            self.searchBarImg = self.controller.get_image(r'./assets/darktheme/searchtabrz.png')
            self.searchBar = Button(self.widgetFrame, text="#Hashtags Filter", image=self.searchBarImg,bg=self.bgCanva, width=810,bd=0,activebackground=self.bgCanva, compound=CENTER)
            self.searchBar.image = self.searchBarImg
            self.searchBar.pack(side=LEFT,expand=1)
            self.profileImg = self.controller.get_image(r'./assets/icons/profileXs.png')
            self.profile = Button(self.widgetFrame, image=self.profileImg, bg=self.bgCanva, bd=0, activebackground=self.bgCanva,compound=CENTER)
            self.profile.image = self.profileImg
            self.profile.pack(side=LEFT,expand=1)

            #self.searchTab = 
            
            
                


if __name__ == '__main__':
    sqlnewtable = """ CREATE TABLE IF NOT EXISTS tableName(
                                    id integer(20) PRIMARY KEY,
                                    bumail text(50) NOT NULL,
                                    passwordx password NOT NULL,
                                    displayname varchar(50) NOT NULL
                                    );"""
    
    sqlselect = """ SELECT * FROM Users WHERE Uid = {}""".format(1)
                # (next step) # rows = 
                                        
    sqlinto = """INSERT INTO tableName (email, passhash, passsalt, displayname)
                                    VALUES("{}","{}","{}","{}");""".format("hehe%@bumail","12345","12345","Woohoo~")
   
    sqldel = """DELETE FROM Users"""#.format() 
    
    sqldrop = """ DROP TABLE tableName;"""

        
    #BUFriends_Time()
    BUFriends().mainloop()
    