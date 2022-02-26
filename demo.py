'''
    demo BUFriends
'''
from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image,ImageTk
import os

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
        print("switching")
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
            def clear_name(e):
                self.userName.delete(0, END)
            def clear_pass(e):
                self.userPass.delete(0, END)
            Label(root,text="BU Friends  |  Log-In",font=self.fontHead,bg=self.bg,foreground=self.fg)\
                .pack(expand=1,padx=50,pady=50)
            userName, userPass = StringVar(), StringVar()
            self.userName = Entry(root, textvariable=userName,width=25, font=self.font,justify="center",relief="solid")
            self.userPass = Entry(root, textvariable=userPass,show="*",width=25, font=self.font,justify="center",relief="solid")
            self.userName.insert(0,"Enter BU-Mail")
            self.userPass.insert(0,"Enter Password")
            self.userName.bind('<Button-1>',clear_name)
            self.userPass.bind('<Button-1>',clear_pass)
            self.userName.pack(pady=5)
            self.userPass.pack(pady=5)
            self.frameBtn = Frame(root, bg=self.bg)
            self.frameBtn.pack(pady=20)
            self.loginBtn = Button(self.frameBtn,text="Log-in",command=self.login_submit,font=self.font,bg="#f8bfff"
                                   ,relief="solid",width=29)
            self.loginBtn.pack(pady=10)
            self.regisBtn = Button(self.frameBtn,text="Register",command=lambda :masterFrame.switch_page(Registration)
                                   ,bg="#edffbf",font="Kanit 12",relief="solid",width=25)
            self.regisBtn.pack(side=LEFT,pady=2)
            self.clearBtn = Button(self.frameBtn,text="Quit",command=masterFrame.destroy,font="Kanit 12",relief="solid",width=12)
            self.clearBtn.pack(side=LEFT,padx=5,pady=2)

        def login_submit(self):
            print(self.userName.get())
            print(self.userPass.get())
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
            self.bg,self.fg = "#ccefff","#cc07e6"
            self.fontHead = "Kanit 36 bold"
            self.font = "Kanit 16 "
            Label(root, text="BU Friends  |  Registration",font=self.fontHead,bg=self.bg,foreground=self.fg)\
                .pack(expand=1)
            self.frameRegis = Frame(root,width=500,height=500)
            self.frameRegis.pack(expand=1,fill=BOTH,ipadx=10,ipady=10)
            self.regisInfolst = [["BUMail"],["Display Name"],["Password"],["Confirm Password"]]
            self.regisDataSubmit = []
            for i in range(len(self.regisInfolst)):
                self.regisInfolst[i].append(StringVar())
                self.regis_form(self.regisInfolst[i][0],self.font,i,self.regisInfolst[i][1])
            print(self.regisInfolst)
            self.frameBtn = Frame(self.frameRegis)
            self.frameBtn.grid(row=4,column=0,columnspan=3)
            self.regisBtn = Button(self.frameBtn,text="Register!",command=self.regis_submit,relief="solid",width=25,height=2
                                   ,bd=2,highlightcolor="green", highlightthickness=1)
            self.regisBtn.grid(row=4,column=1,sticky="nsew",padx=2,pady=15)
            self.CancelBtn = Button(self.frameBtn,text="Cancel",command=lambda :masterFrame.switch_page(LogIn),relief="solid",width=25,height=2)
            self.CancelBtn.grid(row=4,column=2,sticky="nsew",padx=2,pady=15)

        def regis_form(self,_text,_font,_row,_entVar):
                Label(self.frameRegis, text=_text ,font=_font,anchor="w").grid(row=_row,column=0,sticky="nsew",padx=20,pady=10)
                Label(self.frameRegis, text=":", font=_font,anchor="e").grid(row=_row,column=1,sticky="nsew",pady=10)
                if _row == 2 or _row ==3:
                    Entry(self.frameRegis, textvariable=_entVar,show="*",font="Kanit 10",justify="left",width=22)\
                        .grid(row=_row,column=2,sticky="nsew",pady=10)
                else:
                    Entry(self.frameRegis, textvariable=_entVar, font="Kanit 10", justify="left",width=22)\
                        .grid(row=_row, column=2, sticky="nsew", pady=10)

        def regis_submit(self):
            self.regisDataSubmit = []
            for i,data in enumerate(self.regisInfolst):
                self.regisDataSubmit.append(data[1].get())
            messagebox.showinfo('Register Successfully'
                                ,"BUMail : {}\nDisplayName : {}\nPassword1 : {}\nPassword2 : {}".format(*self.regisDataSubmit))


if __name__ == '__main__':
    BUFriends().mainloop()
