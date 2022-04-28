import tkinter as tk
import logging

logging.basicConfig(level=logging.INFO)


class HeaderView(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, width=800, height=100, background="#3df5e5")
        self.welcome_user = tk.Label(self, text=f"Welcome: Ahmed")
        self.my_message = tk.Button(
            self, text="My Message", command=self.show_my_message
        )

    def show_my_message(self):
        logging.info("Show my message")

    def pack_widgets(self):
        self.welcome_user.pack(side=tk.LEFT, padx=50)
        self.my_message.pack(side=tk.RIGHT, padx=50)


class SideBarView(tk.Frame):
    def __init__(self, parent, width=200, height=500):
        tk.Frame.__init__(
            self, parent, width=width, height=height, background="#303030"
        )
        self.buttons = [self.create_button(i) for i in range(1, 10)]
        # for i in range(1, 10):
        #     tk.Button(self, text=f"Button {i}", command=lambda: self.user_click()).pack(side=tk.TOP, pady=10)

    def user_click(self, i):
        logging.info(f"User clicked button {i}")

    def create_button(self, i):
        tk.Button(self, text=f"Button {i}", command=lambda: self.user_click(i)).pack(
            side=tk.TOP, pady=10
        )


if __name__ == "__main__":
    root = tk.Tk()
    root.title("HeaderView")
    root.geometry("800x600")
    header_view = HeaderView(root)
    header_view.pack_propagate(0)
    header_view.pack()
    side_bar_view = SideBarView(root, width=200, height=500)
    side_bar_view.pack(side=tk.LEFT, fill=tk.BOTH)
    header_view.pack_widgets()
    root.mainloop()
