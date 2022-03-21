import sqlite3
from sqlite3 import Error
from tkinter import *
from tkinter.font import Font
from PIL import Image, ImageTk
from tkinter import ttk,messagebox
import hashlib
import os

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
        self.iconbitmap("assets/icons/bufriends.ico")
        self.resizable(0,0)
        self.fontHeaing = Font(family="leelawadee",size=36,weight="bold")
        self.fontBody = Font(family="leelawadee",size=16)
        self.option_add('*font',self.fontBody)
        self.uid = 3
        self.switch_frame(ProfilePage)

    def create_connection(self):
        try:
            self.conn = sqlite3.connect(r"./database/BUFriends.db")
            self.conn.execute("PRAGMA foreign_keys = 1")
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
# switch page event
    def switch_frame(self, frameClass):
        new_frame = frameClass(self)
        if self.frame is not None:
            self.frame.destroy()
        self.frame = new_frame
        self.configure(bg = self.frame.bgColor)
        self.frame.pack(side=BOTTOM, fill=BOTH, expand=TRUE)

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
        self.canvas = Canvas(self.root, bg=self.root.bgColor,highlightthickness=0)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=1)
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

class ProfileReviewPage(Frame):
    def __init__(self,controller):
        Frame.__init__(self,controller)
        self.bgColor = 'white'
        self.controller = controller
        Frame.config(self,bg=self.bgColor)
        scroll = ScrollFrame(self,TRUE)
        self.root = scroll.interior
        self.profile = InfoOnProfile(self.root,self.bgColor,self.controller,1)
        PostOnProfile(self.root,self.bgColor,self.controller)

class ProfilePage(Frame):
    def __init__(self,controller):
        Frame.__init__(self,controller)
        self.bgColor = 'white'
        self.controller = controller
        Frame.config(self,bg=self.bgColor)
        scroll = ScrollFrame(self,TRUE)
        self.root = scroll.interior
        self.profile = InfoOnProfile(self.root,self.bgColor,self.controller,2)
        self.create_post_frame()
        PostOnProfile(self.root,self.bgColor,self.controller)
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
        self.img3 = self.controller.get_imagerz('./assets/buttons/buttonPurplerz.png',200,65)
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
            {'name':'longtag','path':'./assets/buttons/tagEditLong.png','x':180,'y':45},
            {'name':'button','path':'./assets/buttons/buttonPurplerz.png','x':200,'y':65},
            {'name':'cancel','path':'./assets/buttons/back_newrz.png','x':180,'y':40}]
        for i,data in enumerate(imgPathList) :
            img = self.controller.get_imagerz(data['path'],data['x'],data['y'])
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
        entry.pack(expand=1)
    
        entryBox2 = Label(self.mainFrame,image=self.imgList['entry'],bg=self.bgColor)
        entryBox2.grid(row=1,column=1,sticky=N,pady=10,padx=115)
        entryBox2.propagate(0)
        entry2 = Entry(entryBox2,font='leelawadee 15',width=35,bd=0)
        entry2.pack(expand=1)
    def tag_geometry(self) :
        if self.tagData.tagList[0] is not None :
            Label(self.mainFrame,text=self.tagData.tagList[0],image=self.tagData.img,bg=self.bgColor,
            compound=CENTER,fg='white').grid(row=2,column=1,sticky=W,padx=115)            
            Button(self.mainFrame,text="Redo the test?",bg=self.bgColor,fg='#23B7F4',bd=0,
            activebackground=self.bgColor,activeforeground='#23B7F4').grid(row=2,column=1)
        else :
            Button(self.mainFrame,text="Do the test?",bg=self.bgColor,fg='#23B7F4',bd=0,
            activebackground=self.bgColor,activeforeground='#23B7F4').grid(row=2,column=1,sticky=W,padx=115)
        # tagFrame = Frame(self.mainFrame,bg=self.bgColor)
        # tagFrame.grid(row=3,column=1,sticky=W,padx=115)
        # row = 0
        # column = 0
        row = 3
        top = Frame(self.mainFrame,bg=self.bgColor)
        top.grid(row=row,column=1,sticky=W,padx=115)
        frame = top
        self.tagData.tagList.pop(4)
        for i in range(len(self.tagData.tagList)+1) :
            if i > 0 and i < len(self.tagData.tagList):
                if len(self.tagData.tagList[i]) <= 9 :
                    tag = Label(frame,image=self.imgList['tag'],bg=self.bgColor)
                    # tag.grid(row=row,column=column,sticky=W)
                    tag.pack(anchor=W)
                    tag.propagate(0)
                    lb = Label(tag,text=self.tagData.tagList[i],fg='white',bg='#88A3F3',width=8)
                    lb.pack(expand=1,anchor=W,padx=10)
                else:
                    tag = Label(frame,image=self.imgList['longtag'],bg=self.bgColor)
                    # tag.grid(row=row,column=column,sticky=W)
                    tag.pack(anchor=W)
                    tag.propagate(0)
                    lb = Label(tag,text=self.tagData.tagList[i],fg='white',bg='#88A3F3',width=12)
                    lb.pack(expand=1,anchor=W,padx=12)
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
                    Label(frame,image=self.imgList['add'],bg=self.bgColor).pack(anchor=W)
    def end_geometry(self) :
            frame = Frame(self.root,bg=self.bgColor)
            frame.pack(pady=25)
            Button(frame,image=self.imgList['button'],text="Save Change",bd=0,
            bg=self.bgColor,fg='white',activebackground=self.bgColor,compound=CENTER,
            activeforeground='white').pack(side=LEFT,padx=20)

            Button(frame,image=self.imgList['cancel'],text="Cancel",bd=0,
            bg=self.bgColor,fg='white',activebackground=self.bgColor,compound=CENTER,
            activeforeground='white').pack(side=LEFT)
                
        #         if i == 0 :
        #             Label(frame,text=data,image=self.img,compound=CENTER,bg=self.bgColor,fg='white').pack(side=LEFT)
        #         else :
        #             Label(frame,text=data,image=self.img2,compound=CENTER,bg=self.bgColor,fg='white').pack(side=LEFT)
        # Label(self.root,text="Username",fg='#868383'
        # ,bg=self.bgColor,anchor=N).pack(anchor=NW,padx=115,ipady=25)
        
        
        # Label(self.root,text="Bio",fg='#868383'
        # ,bg=self.bgColor,anchor=N).pack(anchor=NW,padx=115,ipady=25)

        # Label(self.root,text="MBTI",fg='#868383'
        # ,bg=self.bgColor,anchor=N).pack(anchor=NW,padx=115,ipady=25)

        # Label(self.root,text="Interest",fg='#868383'
        # ,bg=self.bgColor,anchor=N).pack(anchor=NW,padx=115,ipady=25)
        # self.change_password()
    # def change_password(self) :
    #     print("Start")
    #     sql = """SELECT PassHash,PassSalt FROM Users WHERE Uid={}""".format(self.controller.uid)
    #     if self.controller.conn is not None:
    #             c = self.controller.execute_sql(sql)
    #             data = c.fetchone()
    #             passHash = data[0]
    #             passSalt = data[1]
    #     passkey = self.controller.password_encryptioncheck("test1234",passSalt)
    #     if passkey == passHash :
    #         print("same password")
    #     #     newSalt = os.urandom(32)
    #     #     newpass = self.controller.password_encryptioncheck("test1234",newSalt)
    #     #     sql2 = """UPDATE Users SET PassHash = ?,PassSalt = ? WHERE uid = ?"""
    #     #     try:
    #     #         c = self.controller.execute_sql(sql2, (newpass,newSalt,self.controller.uid))
    #     #     except Error as e:
    #     #         print(e)
    #     # else :
    #     #     print("do not same password")
    #     #     print("password can not change.")

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
            img = self.controller.get_imagerz(data['path'],data['x'],data['y'])
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
            img = self.controller.get_imagerz(data['path'],data['x'],data['y'])
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
        command=self.change_password).pack(pady=30)
    def change_password(self) :
        pwds = []
        for i in range(len(self.pwdList)) :
            pwds.append(self.pwdList[i].get())
        if len(pwds[0]) > 0 and not " " in pwds[0]:
            print("have data")
            if len(pwds[1]) > 7 and any(c.isdigit() == True for c in pwds[1]) and any(c.isalpha() == True for c in pwds[1]):
                print("allowed password")
        else:
            messagebox.showerror("Change password","Please enter current password")
        conn = self.controller.create_connection()
        conn.row_factory = sqlite3.Row
        # sql = """SELECT PassHash,PassSalt FROM Users WHERE Uid=?"""
        # if conn is not None:
        #     c = self.controller.execute_sql(sql,[self.controller.uid])
        #     data = c.fetchone()
        #     passHash = data['passHash']
        #     passSalt = data['passSalt']
        #     passkey = self.controller.password_encryptioncheck(pwd,passSalt)
        #     if passkey == passHash :
        #         print("same password")
        #         ms = messagebox.askquestion("Deactivate","Are you sure you want to deactivate account?")
        #         if ms == "yes" :
        #             for i,data in enumerate(sqlDelete):
        #                 c = self.controller.execute_sql(data,[self.controller.uid])
        #             print("deactivate account")
        #             self.controller.destroy()
        #         else :
        #             self.password.set('')
        #     #     # newSalt = os.urandom(32)
        #     #     # newpass = self.controller.password_encryptioncheck("test1234",newSalt)
        #     #     # sql2 = """UPDATE Users SET PassHash = ?,PassSalt = ? WHERE uid = ?"""
        #     #     # try:
        #     #     #     c = self.controller.execute_sql(sql2, (newpass,newSalt,self.controller.uid))
        #     #     # except Error as e:
        #     #     #     print(e)
        #     else :
        #         messagebox.showerror("Deactivate","Incorrect password!!!")
        # conn.close()

class DeactivatePage(Frame):
    def __init__(self,controller):
        Frame.__init__(self,controller)
        self.bgColor = 'white'
        self.controller = controller
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
            img = self.controller.get_imagerz(data['path'],data['x'],data['y'])
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
        Label(topFrame,text="Username",bg=self.bgColor).pack(pady=5,anchor=W,padx=20)
        Label(topFrame,text="Username@bumail.net",font=self.fontBody,bg=self.bgColor,
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
    def __init__(self, root, bgcolor,controller,parent):
        self.root = root
        self.bgColor = bgcolor
        self.controller=controller
        self.optionFrame = None
        self.parent = parent
        conn = self.controller.create_connection()
        sql = """SELECT DisplayName,Bio FROM Users WHERE Uid=?"""
        sql2 = """SELECT UserType,Tid1,Tid2,Tid3,Tid4 FROM UsersTag WHERE Uid=?"""
        if conn is not None:
            c = self.controller.execute_sql(sql,[self.controller.uid])
            c2 = self.controller.execute_sql(sql2,[self.controller.uid])
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
                    self.controller.destroy()
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
            
        self.imgOption = []
        for i in range(len(optionList)) :
            if imgOptionList[i] is not None :
                self.imgOption.append(self.controller.get_imagerz(imgOptionList[i][0],imgOptionList[i][1],imgOptionList[i][2]))
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
        fontTag = Font(family='leelawadee',size=13)
        bottomFrame.option_add('*font',fontTag)
        self.imgList = []
        for i,data in enumerate(imgPathList) :
            img = self.controller.get_imagerz(data[0],data[1],data[2])
            self.imgList.append(img)
        Button(topFrame,image=self.imgList[0],bd=0,bg=self.bgColor,activebackground=self.bgColor).pack(side=LEFT)
        Button(topFrame,image=self.imgList[1],bd=0,bg=self.bgColor,
        activebackground=self.bgColor,command=lambda:self.option_click()).pack(side=RIGHT,padx=20)
        Label(bottomFrame,image=self.imgList[2],bg=self.bgColor).pack()
        Label(bottomFrame,text=self.name,font="leelawadee 22 bold",bg=self.bgColor).pack(pady=15)
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
                    self.img = self.controller.get_imagerz(imgPathList[0][0],imgPathList[0][1],imgPathList[0][2])
                else :
                    self.img = self.controller.get_imagerz(imgPathList[1][0],imgPathList[1][1],imgPathList[1][2])
            elif self.tagList[0][1] == "S" :
                if self.tagList[0][3] == "J" :
                    self.img = self.controller.get_imagerz(imgPathList[2][0],imgPathList[2][1],imgPathList[2][2])
                else :
                    self.img = self.controller.get_imagerz(imgPathList[3][0],imgPathList[3][1],imgPathList[3][2])     

        self.img2 = self.controller.get_imagerz('./assets/buttons/tagButton.png',130,45)
        frame = Frame(outerFrame,bg=self.bgColor)
        frame.pack(pady=30)            
        for i,data in enumerate(self.tagList) :
            if data is not None :
                if i == 0 :
                    Label(frame,text=data,image=self.img,compound=CENTER,bg=self.bgColor,fg='white').pack(side=LEFT)
                else :
                    Label(frame,text=data,image=self.img2,compound=CENTER,bg=self.bgColor,fg='white').pack(side=LEFT)

class PostOnProfile() :
    def __init__(self,root,bgColor,controller):
        self.root = root
        self.bgColor = bgColor
        self.controller = controller
        self.frame = Frame(self.root,bg='#E6EEFD')
        self.postList = []
        self.frame.pack(side=BOTTOM, fill=BOTH, expand=1)
        fontTag = Font(family='leelawadee',size=13)
        self.frame.option_add('*font',fontTag)
        conn = self.controller.create_connection()
        sql = """SELECT Detail FROM Postings WHERE Uid=?"""
        sql2 = """SELECT DisplayName FROM Users WHERE Uid=?"""
        if conn is not None:
                c = self.controller.execute_sql(sql,[self.controller.uid])
                c2 = self.controller.execute_sql(sql2,[self.controller.uid])
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
    app = BUFriends()
    app.mainloop()