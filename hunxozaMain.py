import sqlite3
from sqlite3 import Error
from tkinter import *
from tkinter.font import Font
from PIL import Image, ImageTk

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

    def execute_sql(conn, sql):
        try:
            c = conn.cursor()
            c.execute(sql)
            conn.commit()
        except Error as e:
            print(e)
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
        self.switch_frame(ProfilePage)
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
class ScrollFrame():
    def __init__(self,root,scrollable):
        # creating
        self.root = root
        self.scrollable = scrollable
        self.scrollbar = Scrollbar(self.root, orient=VERTICAL,width=0)
        self.scrollbar.pack(fill=Y, side=RIGHT, expand=0)
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
class ProfilePage(Frame):
    def __init__(self,controller):
        Frame.__init__(self,controller)
        self.bgColor = 'white'
        self.controller = controller
        Frame.configure(self,bg=self.bgColor)
        scroll = ScrollFrame(self,TRUE)
        self.root = scroll.interior
        self.profileFrame()
        self.tagFrame()
        self.postFrame()

    def profileFrame(self) :
        topFrame = Frame(self.root,bg=self.bgColor)
        bottomFrame = Frame(self.root,bg=self.bgColor)
        imgPathList = ( ('./assets/icons/goback.png',50,50),
                        ('./assets/icons/hamberger.png',25,25),
                        ('./assets/icons/profile.png',180,180))
        bioText = """HEllo \nID LINE:Dekuloveallmight"""
        fontTag = Font(family='leelawadee',size=13)
        bottomFrame.option_add('*font',fontTag)
        self.imgList = []
        for i,data in enumerate(imgPathList) :
            img = self.controller.get_imagerz(data[0],data[1],data[2])
            self.imgList.append(img)
        Button(topFrame,image=self.imgList[0],bd=0,bg=self.bgColor,activebackground=self.bgColor).pack(side=LEFT)
        Button(topFrame,image=self.imgList[1],bd=0,bg=self.bgColor,activebackground=self.bgColor).pack(side=RIGHT,padx=20)
        Label(bottomFrame,image=self.imgList[2],bg=self.bgColor).pack()
        Label(bottomFrame,text="Midoriya Izuku",font="leelawadee 22 bold",bg=self.bgColor).pack(pady=15)
        bioWidget = Text(bottomFrame,bg=self.bgColor,width=30,bd=0)  
        bioWidget.insert(END,bioText)     
        bioWidget.tag_configure("center",justify=CENTER)
        bioWidget.tag_add("center",1.0,END)
        line = float(bioWidget.index(END)) - 1
        bioWidget.config(height=line,state=DISABLED)
        bioWidget.pack()
        topFrame.pack(fill=X)
        bottomFrame.pack(fill=X)
    def tagFrame(self) :
        outerFrame = Frame(self.root,bg=self.bgColor,highlightthickness=2)
        outerFrame.pack(fill=X,pady=20)
        fontTag = Font(family='leelawadee',size=13,weight='bold')
        outerFrame.option_add('*font',fontTag)
        imgPathList = ( ('./assets/buttons/mbtiCyan.png',120,40),
                        ('./assets/buttons/mbtiGreen.png',120,40),
                        ('./assets/buttons/mbtiPurple.png',120,40),
                        ('./assets/buttons/mbtiYellow.png',120,40))   
        tagList = ("INFJ","ITI","game","travel","sport")
        if tagList[0][1:3] == "NT" :
            self.img = self.controller.get_imagerz(imgPathList[0][0],imgPathList[0][1],imgPathList[0][2])
        elif tagList[0][1:3] == "NF" :
            self.img = self.controller.get_imagerz(imgPathList[1][0],imgPathList[1][1],imgPathList[1][2])
        elif tagList[0][1:3] == "ST" :
            self.img = self.controller.get_imagerz(imgPathList[2][0],imgPathList[2][1],imgPathList[2][2])
        elif tagList[0][1:3] == "SF" :
            self.img = self.controller.get_imagerz(imgPathList[3][0],imgPathList[3][1],imgPathList[3][2])
        self.img2 = self.controller.get_imagerz('./assets/buttons/tagButton.png',120,40)
        # for i,data in enumerate(imgPathList) :
        #     img = self.controller.get_imagerz(data[0],data[1],data[2])
        #     self.imgList.append(img)    
        frame = Frame(outerFrame,bg=self.bgColor)
        frame.pack(pady=30)            
        # print(tagList[0][1:3])
        for i,data in enumerate(tagList) :
            if i == 0 :
                Label(frame,text=data,image=self.img,compound=CENTER,bg=self.bgColor).pack(side=LEFT)
            else :
                Label(frame,text=data,image=self.img2,compound=CENTER,bg=self.bgColor).pack(side=LEFT)
    def postFrame(self) :
        self.img3 = self.controller.get_imagerz('./assets/buttons/buttonPurplerz.png',200,65)
        var = StringVar()
        var.set("Hi")
        frame = Frame(self.root,bg=self.bgColor)
        fontTag = Font(family='leelawadee',size=13)
        frame.option_add('*font',fontTag)
        
        Label(frame,text="Create Post",font="leelawadee 20 bold",bg=self.bgColor).pack(anchor=W,padx=35)
        Text(frame,width=90,height=4,relief=SUNKEN).pack()
        Button(frame,text="Post",font='leelawadee 13 bold',fg='white',activeforeground='white',image=self.img3,compound=CENTER,bd=0,bg=self.bgColor,activebackground=self.bgColor).pack(side=RIGHT,padx=35)
        frame.pack(fill=X)   



if __name__ == '__main__':
    app = BUFriends()
    # conn = DBController.create_connection()
    # sql = """INSERT INTO test(score) VALUES ("8")"""
    # if conn is not None:
    #         DBController.execute_sql(conn, sql)
    # else:
    #     print("Error! cannot create the database connection.")
    app.mainloop()