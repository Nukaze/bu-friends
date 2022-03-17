import sqlite3
from sqlite3 import Error
from tkinter import *
from tkinter.font import Font
from PIL import Image, ImageTk
import hashlib
import os

# connecting to database
# class DBController() :
#     def create_connection():
#         conn = None
#         try:
#             conn = sqlite3.connect(r"./database/BUFriends.db")
#             conn.execute("PRAGMA foreign_keys = 1")
#             print(sqlite3.version)
#         except Error as e:
#             print(e)
#         return conn

#     def execute_sql(conn, sql):
#         try:
#             c = conn.cursor()
#             c.execute(sql)
#             conn.commit()
#         except Error as e:
#             print(e)
#         return c

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
        self.create_connection()
        self.switch_frame(EditPage)

    def create_connection(self):
        try:
            self.conn = sqlite3.connect(r"./database/BUFriends.db")
            self.conn.execute("PRAGMA foreign_keys = 1")
            print(sqlite3.version)
        except Error as e:
            print(e)

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
            # conn = DBController.create_connection()
            sql = """INSERT INTO Postings(Detail,Uid) VALUES (?,?)""".format(txt,self.controller.uid)
            if self.controller.conn is not None:
                    c = self.controller.execute_sql(sql,[txt,self.controller.uid])
                    self.controller.switch_frame(ProfilePage)
            else:
                print("Error! cannot create the database connection.")
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
        self.bgColor = 'lightpink'
        self.controller = controller
        Frame.configure(self,bg=self.bgColor)
        scroll = ScrollFrame(self,FALSE)
        master = scroll.interior
        # self.widget(master)
        self.change_password()
    def change_password(self) :
        print("Start")
        sql = """SELECT PassHash,PassSalt FROM Users WHERE Uid={}""".format(self.controller.uid)
        if self.controller.conn is not None:
                c = self.controller.execute_sql(sql)
                data = c.fetchone()
                passHash = data[0]
                passSalt = data[1]
        passkey = self.controller.password_encryptioncheck("test1234",passSalt)
        if passkey == passHash :
            print("same password")
        #     newSalt = os.urandom(32)
        #     newpass = self.controller.password_encryptioncheck("test1234",newSalt)
        #     sql2 = """UPDATE Users SET PassHash = ?,PassSalt = ? WHERE uid = ?"""
        #     try:
        #         c = self.controller.execute_sql(sql2, (newpass,newSalt,self.controller.uid))
        #     except Error as e:
        #         print(e)
        # else :
        #     print("do not same password")
        #     print("password can not change.")
    def widget(self,root) :
        Label(root, text="Edit", font=self.controller.fontHeaing).pack(side="top", pady=5)
        Button(root, text="Processing",command=self.change_password).pack() 

class MyAccountPage(Frame):
    def __init__(self,controller):
        Frame.__init__(self,controller)
        self.bgColor = 'lightpink'
        self.controller = controller
        Frame.configure(self,bg=self.bgColor)
        scroll = ScrollFrame(self,FALSE)
        master = scroll.interior
        self.widget(master)

    def widget(self,root) :
        Label(root, text="My Account", font=self.controller.fontHeaing).pack(side="top", pady=5)
        Button(root, text="Go back"
        ,command=lambda: self.controller.switch_frame(ProfilePage)).pack() 

class InfoOnProfile() :
    def __init__(self, root, bgcolor,controller,parent):
        self.root = root
        self.bgColor = bgcolor
        self.controller=controller
        self.optionFrame = None
        self.parent = parent
        # conn = DBController.create_connection()
        sql = """SELECT DisplayName,Bio FROM Users WHERE Uid=?"""
        sql2 = """SELECT UserType,Tid1,Tid2,Tid3,Tid4 FROM UsersTag WHERE Uid=?"""
        if self.controller.conn is not None:
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
        self.profile_frame()
        self.tag_frame()    

    def option_click(self) :
        bgColor = '#686DE0'
        if self.parent == 2 :
            optionList = ["Edit","My account","Log out"]
            imgOptionList = ['./assets/icons/edit.png','./assets/icons/user.png','./assets/icons/signOut.png']
        else :
            optionList = ["Report"]
            imgOptionList = [None]
        self.imgOption = []
        for i in range(len(optionList)) :
            if imgOptionList[i] is not None :
                self.imgOption.append(self.controller.get_imagerz(imgOptionList[i],20,20))
            else :
                self.imgOption.append(None)
        pageList = [EditPage,MyAccountPage]
        if self.optionFrame is None :
            self.optionFrame = Frame(self.root)
            for i,data in enumerate(optionList) :
                Button(self.optionFrame,text=data,bd=0,bg=bgColor,activebackground=bgColor,anchor=W
                ,padx=10,fg='white',activeforeground='white',font='leelawadee 13 bold',width=175
                ,image=self.imgOption[i],compound=LEFT
                ,command=lambda c=i : self.controller.switch_frame(pageList[c])).pack(ipady=10)
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
        btn = Button(topFrame,image=self.imgList[1],bd=0,bg=self.bgColor,activebackground=self.bgColor)
        btn.pack(side=RIGHT,padx=20)
        btn.config(command=lambda:self.option_click())
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
        imgPathList = ( ('./assets/buttons/mbtiPurple.png',120,40),
                        ('./assets/buttons/mbtiGreen.png',120,40),
                        ('./assets/buttons/mbtiCyan.png',120,40),
                        ('./assets/buttons/mbtiYellow.png',120,40))   
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

        self.img2 = self.controller.get_imagerz('./assets/buttons/tagButton.png',120,40)  
        frame = Frame(outerFrame,bg=self.bgColor)
        frame.pack(pady=30)            
        for i,data in enumerate(self.tagList) :
            if data is not None :
                if i == 0 :
                    Label(frame,text=data,image=self.img,compound=CENTER,bg=self.bgColor).pack(side=LEFT)
                else :
                    Label(frame,text=data,image=self.img2,compound=CENTER,bg=self.bgColor).pack(side=LEFT)

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
        # conn = DBController.create_connection()
        sql = """SELECT Detail FROM Postings WHERE Uid=?"""
        sql2 = """SELECT DisplayName FROM Users WHERE Uid=?"""
        if self.controller.conn is not None:
                c = self.controller.execute_sql(sql,[self.controller.uid])
                c2 = self.controller.execute_sql(sql2,[self.controller.uid])
                userData = c.fetchall()
                self.name = c2.fetchone()[0]
                for i,data in enumerate(userData) :
                    self.postList.append(data[0])        
        else:
            print("Error! cannot create the database connection.")
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