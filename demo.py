'''
    demo BUFriends
'''
from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image,ImageTk
import os
import hashlib

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
        self.iconbitmap('assets/icon/BUF.ico')
        self.switch_page(LogIn)

    def switch_page(self, frameClass):
        print("switching to {}".format(frameClass))
        newFrame = frameClass(self)
        if self.frame is not None:
            self.frame.destroy()
        self.frame = newFrame
        self.configure(bg=self.frame.bg)
        self.frame.pack()


class LogIn(Frame):

    def __init__(self, masterFrame):
        Frame.__init__(self, masterFrame)
        self.bg = "#ccefff"
        Frame.configure(self,bg=self.bg)
        self.pack()
        self.LogInContent(self,masterFrame)

    class LogInContent:
        def __init__(self, root, masterFrame):
            self.bg,self.fg = "#ccefff","#cc07e6"
            self.fontHead = "Kanit 36 bold"
            self.font = "Kanit 16 "
            Label(root,text="BU Friends  |  Log-In",font=self.fontHead,bg=self.bg,foreground=self.fg,justify="left")\
                .pack(side=TOP,expand=1,padx=50,pady=40)
            userName, userPass = StringVar(), StringVar()
            self.userName = Entry(root, textvariable=userName,width=25, font=self.font,justify="center",relief="solid")
            self.userPass = Entry(root, textvariable=userPass,show="*",width=25, font=self.font,justify="center",relief="solid")
            self.userName.insert(0,"Enter BU-Mail")
            self.userPass.insert(0,"Enter Password")
            self.userName.bind('<Button-1>',self.clear_name)
            self.userPass.bind('<Button-1>',self.clear_pass)
            self.userName.pack(pady=6,ipadx=1,ipady=5)
            self.userPass.pack(pady=6,ipadx=1,ipady=5)
            self.frameBtn = Frame(root, bg=self.bg)
            self.frameBtn.pack(side=TOP, pady=20, expand=1)
            self.loginBtn = Button(self.frameBtn, text="Log-in", command=lambda :self.login_submit(masterFrame)
                                   , font=self.font, bg="#f8bfff", relief="solid", width=29)
            self.regisBtn = Button(self.frameBtn, text="Register", command=lambda :masterFrame.switch_page(Registration)
                                    , bg="#edffbf", font="Kanit 12", relief="solid", width=25)
            self.clearBtn = Button(self.frameBtn, text="Quit", command=masterFrame.destroy, font="Kanit 12", relief="solid", width=15)
            self.loginBtn.pack(side=TOP,pady=10,ipady=5,fill=BOTH,padx=3)
            self.regisBtn.pack(side=LEFT,padx=3)
            self.clearBtn.pack(side=LEFT,padx=3)

        def clear_name(self,e):
            self.userName.delete(0, END)
        def clear_pass(self,e):
            self.userPass.delete(0, END)

        def login_submit(self,masterFrame):
            print(self.userName.get())
            print(self.userPass.get())
            masterFrame.switch_page(DashBoard)

            #userPass


class Registration(Frame):

    def __init__(self, masterFrame):
        Frame.__init__(self, masterFrame)
        self.bg = "#ccefff"
        Frame.configure(self,bg=self.bg)
        self.pack()
        self.RegisterContent(self, masterFrame)

    class RegisterContent:

        def __init__(self, root, masterFrame):
            self.masterFrame = masterFrame
            self.bg,self.fg = "#ccefff","#cc07e6"
            self.fontHead = "Kanit 36 bold"
            self.font = "Kanit 16 "
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
            self.CancelBtn = Button(self.frameBtn,text="Cancel",command=lambda :masterFrame.switch_page(LogIn),relief="solid",width=20,height=2)
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

            def register_error(errorFormat):
                #self.regisVarData.clear()
                self.regisDataSubmit.clear()
                messagebox.showinfo('Register Error', '{}\nPlease Register Form Again'.format(errorFormat))
                self.masterFrame.switch_page(Registration)

            def register_validate(self):
                dbUserDataLst = []
                with open('database/user.txt',buffering=1)as db:
                    while True:
                        dbdata = db.readline().split()
                        if dbdata == []:break
                        else:dbUserDataLst.append(dbdata)
                        dbUserDataLst[1]
                    print(dbUserDataLst)
                    for linedata in dbUserDataLst:
                        if self.regisVarData[0].get() == linedata[0]:
                            register_error("{} is Existed".format(self.regisVarData[0].get()))
                            print("end")
                            break
                for i,data in enumerate(self.regisVarData):
                    if data.get() == "" or data.get().isspace():
                        self.regisVarData.clear()
                        register_error("Register Form Information not Complete")
                        break
                    if "@bumail.net" not in self.regisVarData[0].get():
                        self.regisVarData.clear()
                        register_error("BU Friends Exclusive for BU Mail only")
                        break
                    if self.regisVarData[2].get() != self.regisVarData[3].get():
                        register_error("Password is not Matching")
                        break
                    else:
                        self.regisDataSubmit.append(data.get())
                if len(self.regisVarData) == len(self.regisVarData):
                    with open('database/user.txt', 'a+')as db:
                        db.writelines("{} {} {} {}\n".format(*self.regisDataSubmit))
                        messagebox.showinfo('Register Successfully'
                                            ,"BUMail : {} DisplayName : {}\nPassword1 : {}\nPassword2 : {}".format(*self.regisDataSubmit))
                else:
                    register_error("dunno u forgot")
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
            self.fontHead = "Kanit 48 bold"
            self.font = "Kanit 16"
            Label(root, text="Dashboard",font=self.fontHead).pack()

        def ehe(self):
            print("ehe nun dayo")



if __name__ == '__main__':
    BUFriends().mainloop()
