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
        self.uidSelect = 7
        self.ridSelect = None
        self.requestReport = None
        self.update_blacklist()
        self.switch_frame(ChangePasswordPage)

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
        self.frame.pack_propagate(False)
        self.frame.pack(side=BOTTOM, fill=BOTH, expand=True)

    def get_image(self, _path, _width, _height):
        origin = Image.open(_path).resize((_width,_height),Image.ANTIALIAS)
        img = ImageTk.PhotoImage(origin)
        return img
    def password_encryptioncheck(self, _password, _salt):
            stdhash = 'sha256'
            stdencode = 'utf-8'
            passkey = hashlib.pbkdf2_hmac(stdhash, _password.encode(stdencode), _salt, 161803)
            return passkey
    def update_blacklist(self) :
        sql = """
        UPDATE Blacklists SET Status=0, StartDate=NULL, EndDate=NULL 
        WHERE EndDate <= datetime('now')"""
        conn = self.create_connection()
        if conn is not None:
            c = self.execute_sql(sql)
            conn.close()
class ScrollFrame():
    def __init__(self,root,scrollable,bgColor='white'):
        # creating
        self.root = root
        self.bgColor = bgColor
        self.scrollable = scrollable
        self.canvas = Canvas(self.root, bg=self.bgColor,highlightthickness=0)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=1)
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
        if self.interior.winfo_reqheight() > self.root.winfo_reqheight():
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
        Frame.config(self,bg=self.bgColor,height=600)
        scroll = ScrollFrame(self,True)
        self.root = scroll.interior
        self.profile = InfoOnProfile(self.root,self.bgColor,self.controller,1,self.controller.uidSelect)
        PostOnProfile(self.root,self.bgColor,self.controller,self.controller.uidSelect)

class AdminReviewPage(Frame):
    def __init__(self,controller):
        Frame.__init__(self,controller)
        self.bgColor = 'white'
        self.controller = controller
        Frame.config(self,bg=self.bgColor,height=600)
        scroll = ScrollFrame(self,True)
        self.root = scroll.interior
        self.profile = InfoOnProfile(self.root,self.bgColor,self.controller,3,self.controller.uidSelect)
        PostOnProfile(self.root,self.bgColor,self.controller,self.controller.uidSelect)

class ProfilePage(Frame):
    def __init__(self,controller):
        Frame.__init__(self,controller)
        self.bgColor = 'white'
        self.controller = controller
        Frame.config(self,bg=self.bgColor)
        scroll = ScrollFrame(self,True)
        self.root = scroll.interior
        self.profile = InfoOnProfile(self.root,self.bgColor,self.controller,2,self.controller.uid)
        self.create_post_frame()
        PostOnProfile(self.root,self.bgColor,self.controller,self.controller.uid)
    def post_event(self):
        txt = self.post.get(1.0,END)
        if txt.isspace() :
            messagebox.showwarning("Posting","Your post cannot be empty.")
        elif len(txt) >300 :
            messagebox.showwarning("Posting","Your post cannot be longer than 300 characters.")
        else :
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
        self.nameStr = None
        self.bioStr = None
        self.searchEntryBox = None
        self.mainFrame = None
        self.tagData = ProfilePage(self.controller).profile
        Frame.configure(self,bg=self.bgColor)
        scroll = ScrollFrame(self,True)
        self.root = scroll.interior
        fontTag = Font(family='leelawadee',size=13,weight='bold')
        self.option_add('*font',fontTag)
        self.imgList = {}
        imgPathList = [
            {'name':'back','path':'./assets/icons/goback.png','x':50,'y':50},
            {'name':'entry','path':'./assets/entrys/entry2rz.png','x':440,'y':50},
            {'name':'longentry','path':'./assets/darktheme/searchtabrz.png','x':760,'y':50},
            {'name':'search','path':'./assets/darktheme/Search.png','x':35,'y':35},
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
        self.headText = Label(self.root,text="Edit Profit",font='leelawadee 20 bold',
        bg=self.bgColor,anchor=N)
        self.headText.pack(anchor=NW,padx=115,ipady=10)
    def main_geometry(self) :
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
        self.headText.config(text="Edit Profit")
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
            self.mbtiBtn = Button(self.mainFrame,text="Redo the test?",bg=self.bgColor,fg='#23B7F4',bd=0,
            activebackground=self.bgColor,activeforeground='#23B7F4')
            self.mbtiBtn.grid(row=2,column=1)
        else :
            self.mbtiBtn = Button(self.mainFrame,text="Do the test?",bg=self.bgColor,fg='#23B7F4',bd=0,
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

    def searchTag(self,event) : 
        if self.search.get() == "Search" : 
            self.search.set("")

    def addtag_page(self,event) :
        self.search = StringVar()
        self.search.set("Search")
        self.bioStr = self.bioEntry.get(1.0,'end-1c')
        print(len(self.bioStr))
        self.mainFrame.destroy()
        self.endFrame.destroy()
        self.backBtn.config(command=lambda:self.main_geometry())
        self.headText.config(text="Add Interest")
        self.searchEntryBox = Label(self.root,image=self.imgList['longentry'],bg=self.bgColor)
        self.searchEntryBox.pack(pady=10)
        self.searchEntryBox.propagate(0)
        searchEntry = Entry(self.searchEntryBox,bd=0,font='leelawadee 16',fg='#868383',width=62,textvariable=self.search)
        searchEntry.pack(expand=1,anchor=W,padx=10,side=LEFT)
        searchEntry.focus_force()
        searchEntry.select_range(0,END)
        searchEntry.bind('<Button-1>',lambda e :self.searchTag(e))
        Button(self.searchEntryBox,image=self.imgList['search'],bg=self.bgColor,bd=0,
        activebackground=self.bgColor,command=lambda : self.search_event()).pack(anchor=E,expand=1,padx=10,side=LEFT)
        self.mainFrame = Frame(self.root,bg=self.bgColor)
        self.mainFrame.pack()
        self.get_alltag()
        self.show_tags(self.allTags)
        for i,data in enumerate(self.tagData.tagList) :
            print(data)
            self.select_tag(data,1)
    def search_event(self) :
        searchList = []
        self.mainFrame.destroy()
        self.mainFrame = Frame(self.root,bg=self.bgColor)
        self.mainFrame.pack()
        for i,data in enumerate(self.allTags) :
            if self.search.get().lower() in data['tagName'].lower():
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
                            messagebox.showwarning("Add Interest","You can select 4 attentions.")
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
            messagebox.showwarning("Save change","Your name cannot be empty.")
            return
        if len(self.nameStr.get()) > 32 :
            messagebox.showwarning("Save change","Your name cannot be longer than 32 characters.")
            return
        if len(self.bioStr) > 100 :
            messagebox.showwarning("Save change","Your bio cannot be longer than 100 characters.")
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
            messagebox.showinfo("Edit Profile","Profile has been successfully edited.")
            self.controller.switch_frame(ProfilePage)
class MyAccountPage(Frame):
    def __init__(self,controller):
        Frame.__init__(self,controller)
        self.bgColor = 'white'
        self.controller = controller
        Frame.configure(self,bg=self.bgColor)
        scroll = ScrollFrame(self,False)
        self.root = scroll.interior
        fontTag = Font(family='leelawadee',size=13,weight='bold')
        self.option_add('*font',fontTag)
        self.imgList = {}
        imgPathList = [
            {'name':'back','path':'./assets/icons/goback.png','x':50,'y':50},
            {'name':'pwd','path':'./assets/buttons/my_account.png','x':660,'y':55},
            {'name':'delete','path':'./assets/buttons/deactivate.png','x':660,'y':55},
            {'name':'background','path':'./assets/images/myaccount.png','x':800,'y':338}]
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

        Label(self.root,image=self.imgList['background'],bg=self.bgColor).pack(pady=20)
class ChangePasswordPage(Frame):
    def __init__(self,controller):
        Frame.__init__(self,controller)
        self.bgColor = 'white'
        self.controller = controller
        Frame.configure(self,bg=self.bgColor)
        scroll = ScrollFrame(self,False)
        self.root = scroll.interior
        fontHead = Font(family='leelawadee',size=13,weight='bold')
        self.option_add('*font',fontHead)
        self.pwdList = [StringVar(),StringVar(),StringVar()]
        self.imgList = {}
        imgPathList = [
            {'name':'back','path':'./assets/icons/goback.png','x':50,'y':50},
            {'name':'button','path':'./assets/buttons/buttonPurplerz.png','x':200,'y':65}]
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
            entry = Entry(canvas,font="leelawadee 13",bd=0,fg='#868383',textvariable=self.pwdList[i])
            if i == 0 :
                entry.focus_force()
            entry.pack(padx=140,pady=20,anchor=W,fill=X)
            canvas.create_line(140, y, 760, y,fill='#868383')
            y+=94
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
                c2 = self.controller.execute_sql(sql2, (newpass,newSalt,self.controller.uid))
                conn.close()
                messagebox.showinfo("Change password","Password has been successfully changed.")
                self.controller.switch_frame(MyAccountPage)
            else :
                messagebox.showerror("Change password","Incorrect current password!!!")


class DeactivatePage(Frame):
    def __init__(self,controller):
        Frame.__init__(self,controller)
        self.bgColor = 'white'
        self.controller = controller
        self.data = ProfilePage(self.controller).profile
        Frame.configure(self,bg=self.bgColor)
        scroll = ScrollFrame(self,False)
        self.root = scroll.interior
        fontHead = Font(family='leelawadee',size=20,weight='bold')
        self.fontBody = Font(family='leelawadee',size=15,weight='bold')
        self.option_add('*font',fontHead)
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
        self.page_geometry()
    def page_geometry(self) :
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
        if self.password.get() == "" :
            messagebox.showwarning("Deactivate","Please enter your password")
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
                print("same password")
                ms = messagebox.askquestion("Deactivate","Are you sure you want to deactivate account?")
                if ms == "yes" :
                    for i,data in enumerate(sqlDelete):
                        c = self.controller.execute_sql(data,[self.controller.uid])
                    print("deactivate account")
                    self.controller.destroy()
                else :
                    self.password.set('')
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
        self.tagList = []
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
            # tagData = c.fetchone()
            # print(tagData)
            self.tagList.append(c.fetchone()[0])
            c = self.controller.execute_sql(sql3,[self.uid])
            tagData = c.fetchall()
            for i,data in enumerate(tagData) :
                self.tagList.append(data[0])
            # for i in range(1,len(tagData)):
            #     if tagData[i] is not None :
            #         sql3 = """SELECT TagName FROM Tags WHERE Tid=?"""
            #         c3 = self.controller.execute_sql(sql3,[tagData[i]])
            #         self.tagList.append(c3.fetchone()[0])
            # userData = c.fetchone()
            # self.name = userData[0]
            # self.bio = userData[1]
            # self.email = userData[2]
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
            c = self.controller.execute_sql(sql,[self.controller.requestReport['reported']])
            for i,data in enumerate(sqlDelete):
                c = self.controller.execute_sql(data,[self.controller.requestReport['reported']])
            conn.close()
            messagebox.showinfo("delete","delete successfully")
            self.controller.requestReport = None
            self.controller.ridSelect = None
            self.controller.switch_frame(Administration)
    def request_blacklist(self) :
        conn = self.controller.create_connection()
        conn.row_factory = sqlite3.Row
        print(self.controller.requestReport)
        sql = """SELECT * FROM Blacklists WHERE Uid=?"""
        if conn is not None:
            c = self.controller.execute_sql(sql,[self.controller.requestReport['reported']])
            data = c.fetchone()
            if data is None :
                sql = """INSERT INTO Blacklists (Uid,Email) SELECT Uid,Email FROM Users WHERE Users.Uid = ?"""
                c = self.controller.execute_sql(sql,[self.controller.requestReport['reported']])
                sql = """UPDATE Blacklists SET EndDate = datetime(StartDate, '+7 days') WHERE Uid = ?"""
                c = self.controller.execute_sql(sql,[self.controller.requestReport['reported']])
                sql = """UPDATE Reports SET Status = 1 WHERE ReportedUid = ?"""
                c = self.controller.execute_sql(sql,[self.controller.requestReport['reported']])
                affected_rows = c.rowcount
                if affected_rows > 0 :
                    messagebox.showinfo("Blacklist","Suspending Successfully")
                    self.controller.requestReport = None
                    self.controller.ridSelect = None
                    self.controller.switch_frame(Administration)
            else :
                sql = """SELECT Status,Amount FROM Blacklists WHERE Uid=?"""
                c = self.controller.execute_sql(sql,[self.controller.requestReport['reported']])
                data = c.fetchone()
                if data['Amount'] >= 3 :
                    ms = messagebox.askquestion("Blacklist","บัญชีโดนระงับครบ 3 ครั้ง หากดำเนินการต่อจะเป็นการลบบัญชีนี้")
                    if ms == "yes" :
                        self.request_delete()
                        return
                    else: 
                        return
                if data['Status'] == 1 :
                    messagebox.showwarning("Blacklist","""
                    This account is already suspended.\n
                    ***Policies***\n
                    -รอจนหมดเวลาระงับบัญชี\n
                    -หากรุนแรงให้ลบบัญชีนี้""")
                else :
                    sql = """UPDATE Blacklists SET Amount=Amount+1, Status=1, StartDate=datetime('now'), EndDate=datetime('now','+7 days') WHERE Uid = ?"""
                    c = self.controller.execute_sql(sql,[self.controller.requestReport['reported']])
                    sql = """UPDATE Reports SET Status = 1 WHERE ReportedUid = ?"""
                    c = self.controller.execute_sql(sql,[self.controller.requestReport['reported']])
                    affected_rows = c.rowcount
                    if affected_rows > 0 :
                        self.controller.requestReport = None
                        self.controller.ridSelect = None
                        self.controller.switch_frame(Administration)
                # update data
            conn.close()
    def option_click(self) :
        def next_page(index) :
            if pageList[index] is not None :
                self.controller.switch_frame(pageList[index])
            elif self.parent == 2 and index == 2 :
                ms = messagebox.askquestion("log out","Are you sure you want to log out?")
                if ms == "yes" :
                    self.controller.destroy()
            elif self.parent == 3 :
                if index == 0 :
                    ms = messagebox.askquestion("blacklist","Are you sure you want to suspend this account?")
                    if ms == "yes" :
                        self.request_blacklist()
                else:
                    ms = messagebox.askquestion("delete","Are you sure you want to dalete this account?")
                    if ms == "yes" :
                        self.request_delete()
        bgColor = '#686DE0'
        if self.parent == 1 :
            optionList = ["Report"]
            imgOptionList = [None]
            pageList = [None]
        elif self.parent == 2 :
            optionList = ["Edit","My account","Log out"]
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
        topFrame = Frame(self.root,bg=self.bgColor)
        bottomFrame = Frame(self.root,bg=self.bgColor)
        imgPathList = ( ('./assets/icons/goback.png',50,50),
                        ('./assets/icons/hamberger.png',25,25),
                        ('./assets/icons/profile.png',180,180))
        fontTag = Font(family='leelawadee',size=13)
        bottomFrame.option_add('*font',fontTag)
        self.imgList = []
        for i,data in enumerate(imgPathList) :
            img = self.controller.get_image(data[0],data[1],data[2])
            self.imgList.append(img)
        if self.parent == 3 :
            Button(topFrame,image=self.imgList[0],bd=0,bg=self.bgColor,
            command=lambda:self.controller.switch_frame(Administration),
            activebackground=self.bgColor).pack(side=LEFT)
        else :
            Button(topFrame,image=self.imgList[0],bd=0,bg=self.bgColor,
            activebackground=self.bgColor).pack(side=LEFT)
        Button(topFrame,image=self.imgList[1],bd=0,bg=self.bgColor,
        activebackground=self.bgColor,command=lambda:self.option_click()).pack(side=RIGHT,padx=20)
        Label(bottomFrame,image=self.imgList[2],bg=self.bgColor).pack()
        Label(bottomFrame,text=self.name,font="leelawadee 22 bold",bg=self.bgColor).pack(pady=15)
        if self.bio is not None :
            bioWidget = Text(bottomFrame,bg=self.bgColor,width=40,bd=0)
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
        print(len(self.postList))

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

class Administration(Frame):
    def __init__(self,controller):
        Frame.__init__(self,controller)
        self.bgColor = '#181B23'
        self.controller = controller
        Frame.config(self,bg=self.bgColor)
        scroll = ScrollFrame(self,False,self.bgColor)
        self.root = scroll.interior
        self.typeVar = IntVar()
        self.typeVar.set(1)
        self.allReports = []
        self.allBlacklists = []
        self.line = []
        self.imgList = {}
        imgPathList = [
            {'name':'logout','path':'./assets/icons/signOut.png','x':35,'y':35},
            {'name':'blacklist','path':'./assets/icons/BlacklistlDefault.png','x':30,'y':30},
            {'name':'blacklist2','path':'./assets/icons/BlacklistClicked.png','x':30,'y':30},
            {'name':'report','path':'./assets/icons/MailDefault.png','x':30,'y':30},
            {'name':'report2','path':'./assets/icons/MailClicked.png','x':30,'y':30}]
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
            ms = messagebox.askquestion("log out","Are you sure you want to log out?")
            if ms == "yes" :
                self.controller.destroy()
        Button(self.root,image=self.imgList['logout'],bd=0,
        bg=self.bgColor,activebackground=self.bgColor,command=lambda:log_out()).pack(anchor=NE,pady=10,padx=10)
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

        self.BottomFrame = Frame(self.root,bg='#282D39',width=800,height=440)
        self.BottomFrame.pack()
        self.BottomFrame.propagate(0)
        self.scroll = ScrollFrame(self.BottomFrame,True,'#282D39')
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
            msg = f"เคยโดยระงับบัญชีชั่วคราวทั้งหมด {blacklist['amount']} ครั้ง"
            Label(self.innerCanvas,text=msg,bg='#282D39',fg='#B7B7B7',
            font='leelawadee 13').grid(row=row_,column=1,sticky=W)
            self.line.append(self.innerCanvas.create_line(20, y, 780, y,fill='#868383'))
            y+=65
            row_+=1
    class RequestReport:
        def __init__(self, root, controllerFrame,requestRid):
            print("RequestReport")
            self.root = root
            self.controller = controllerFrame
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
            self.controller.requestReport = self.report
            print("self.root.ridSelect",self.controller.ridSelect)
            self.controller.uidSelect = self.report['reported']
            self.controller.switch_frame(AdminReviewPage)
        def page_geometry(self) :
            mainFrame = Frame(self.controller,width=900,height=700,bg=self.bgColor)
            mainFrame.place(x=0,y=0)
            mainFrame.propagate(0)
            topFrame = Frame(mainFrame,bg='#181B23')
            topFrame.pack(fill=X)
            Label(topFrame,text=f"Sent by @{self.report['reporterName']}",bg='#181B23',fg='#B7B7B7').pack(padx=20,pady=15,anchor=W,side=LEFT)
            Button(topFrame,image=self.imgList['close'],bd=0,bg='#181B23',
            activebackground='#181B23',command=lambda:mainFrame.destroy()).pack(side=RIGHT,padx=20)
            canvas = Canvas(mainFrame, bg=self.bgColor,highlightthickness=0)
            canvas.pack(side=LEFT, fill=BOTH, expand=1)
            canvas.propagate(0)
            frameInCanvas = Frame(canvas,bg=self.bgColor)
            frameInCanvas.pack(fill=X,padx=20,pady=15)
            Label(frameInCanvas,text="Report",bg=self.bgColor,fg='#B7B7B7').grid(sticky=W,row=0,column=0)
            Button(frameInCanvas,text=f"@{self.report['reportedName']}",bg=self.bgColor,
            fg='#99D575',bd=0,activebackground=self.bgColor,activeforeground='#99D575',
            command=self.remember_rid).grid(sticky=W,row=0,column=1,padx=20)
            canvas.create_line(0, 55, 900, 55,fill='#868383')
            frameInCanvas2 = Frame(canvas,bg=self.bgColor)
            frameInCanvas2.pack(fill=X,padx=20,pady=10)
            Label(frameInCanvas2,text="Subject",bg=self.bgColor,fg='#B7B7B7').grid(sticky=W,row=1,column=0)
            Label(frameInCanvas2,text=f"{self.report['header']}",bg=self.bgColor,fg='white',
            font='leelawadee 13').grid(sticky=W,row=1,column=1,padx=20)
            canvas.create_line(0, 110, 900, 110,fill='#868383')
            detail = Text(canvas,relief=FLAT,height=15,bg=self.bgColor,fg='white')
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
if __name__ == '__main__':
    app = BUFriends()
    app.mainloop()