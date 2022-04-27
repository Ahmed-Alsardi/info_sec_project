from tkinter import *
import tkinter.messagebox as tm
import tkinter as tk

class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(LoginFrame)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

class LoginFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        #super().__init__(master)

        self.label_username = Label(self, text="Username")
        self.label_password = Label(self, text="Password")

        self.entry_username = Entry(self)
        self.entry_password = Entry(self, show="*")

        self.label_username.grid(row=0, sticky=E)
        self.label_password.grid(row=1, sticky=E)
        self.entry_username.grid(row=0, column=1)
        self.entry_password.grid(row=1, column=1)

        self.logbtn = Button(self, text="Login", command=self._login_btn_clicked)
        self.logbtn.grid(row=2, column=0)

        self.logbtn = Button(self, text="register", command=self._register_btn_clicked)
        self.logbtn.grid(row=2, column=1)


        self.pack()

    def _login_btn_clicked(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if username == "user" and password == "password":
            tm.showinfo("Login info", "Welcome")
            tk.Button(self, text="Go to main page",
                  command=lambda: master.switch_frame(PageOne)).grid(row=0, sticky=E)
        else:
            tm.showerror("Login error", "Incorrect username")
    
    def _register_btn_clicked(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if username == "user" and password == "password":
            tm.showinfo("Login info", "Welcome")
            tk.Button(self, text="Go to main page",
                  command=lambda: master.switch_frame(PageOne)).grid(row=0, sticky=E)
        else:
            tm.showerror("Login error", "Incorrect username")

class PageOne(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="This is page one").pack(side="top", fill="x", pady=10)
        tk.Button(self, text="Return to start page",
                  command=lambda: master.switch_frame(StartPage)).pack()


root = Tk()
root.geometry('600x400')
lf = LoginFrame(root)
root.mainloop()