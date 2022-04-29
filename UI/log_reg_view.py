import logging
import tkinter as tk

from UI.components import ComponentName

logging.basicConfig(
    level=logging.INFO, format=" %(asctime)s - %(levelname)s - %(message)s"
)


class LoginRegistrationComponent(tk.Frame):
    def __init__(self, parent, width, height, bg, text_color):
        tk.Frame.__init__(self, master=parent, width=width, height=height, bg=bg)
        self.parent = parent
        self.frame_width = width
        self.frame_height = height

        # Create username label and entry boxes
        self.username_label = tk.Label(self, text="Username:", bg=bg, fg=text_color)
        self.username_label.grid(row=0, column=0, sticky=tk.W)
        self.username_entry = tk.Entry(self, bg=bg, fg=text_color)
        self.username_entry.grid(row=0, column=1, sticky=tk.W)
        # create password label and entry boxes
        self.password_label = tk.Label(self, text="Password:", bg=bg, fg=text_color)
        self.password_label.grid(row=1, column=0, sticky=tk.W)
        self.password_entry = tk.Entry(self, bg=bg, fg=text_color)
        self.password_entry.grid(row=1, column=1, sticky=tk.W)
        # create login button
        self.login_button = tk.Button(self, text="Login", command=self.login, width=15)
        self.login_button.grid(row=2, column=0, columnspan=2, sticky=tk.W)
        self.register_button = tk.Button(
            self, text="Register", command=self.register, width=15
        )
        self.register_button.grid(row=2, column=1, columnspan=2, sticky=tk.E)

    def login(self, **kwargs):
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.parent.switch_frame(ComponentName.DASHBOARD,
                                 username=username,
                                 password=password,
                                 new_user=False)
        logging.info(f"Login button clicked for {username}, {password}")

    def register(self, **kwargs):
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.parent.switch_frame(ComponentName.DASHBOARD,
                                 username=username,
                                 password=password,
                                 new_user=True)
        logging.info(f"Login button clicked for {username}, {password}")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Login/Registration")
    root.geometry("800x600")
    root.resizable(False, False)
    app = LoginRegistrationComponent(root, 200, 200)
    root.mainloop()
    logging.info("Exiting")
