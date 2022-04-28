import tkinter as tk
import logging
from UI.utility import BLACK, WHITE
from typing import List

logging.basicConfig(level=logging.INFO, format=' %(asctime)s - %(levelname)s - %(message)s')


class HeaderView(tk.Frame):
    def __init__(self, parent, width: int, height: int, username: str, bg, text_color):
        tk.Frame.__init__(self, parent, width=width, height=height, background=bg)
        self.frame_width = width
        self.frame_height = height
        self.username = username
        self.bg = bg
        self.text_color = text_color
        # create label welcome username
        self.label_welcome = tk.Label(self, text=f"Welcome: {self.username}", bg=bg, fg=text_color)
        self.label_welcome.grid(row=0, column=0, columnspan=2, sticky="w", padx=20, pady=20)
        # create my message button
        self.button_my_message = tk.Button(self, text="My Message",
                                           command=self.my_message)
        self.button_my_message.grid(row=0, column=2, columnspan=2, sticky="e", padx=20, pady=20)
        self.pack(fill=tk.BOTH, )

    def my_message(self):
        logging.info("My message button clicked")


class SideView(tk.Frame):
    def __init__(self, parent, width: int, height: int, usernames: List[str], bg, text_color):
        tk.Frame.__init__(self, parent, width=width, height=height, background=bg)
        self.frame_width = width
        self.frame_height = height
        self.bg = bg
        self.text_color = text_color
        # create label "send message to"
        self.label_send_message_to = tk.Label(self, text="Send message to:", bg=bg, fg=text_color)
        self.label_send_message_to.grid(row=0, column=0, sticky="w", padx=20, pady=20)
        self.usernames = [self._create_user_button(username, i) for i, username in enumerate(usernames)]
        self.pack(fill=tk.BOTH, side=tk.LEFT)

    def _create_user_button(self, username, index):
        button = tk.Button(self, text=username, width=10,
                           command=lambda: self._user_message(username))
        button.grid(row=index + 1, column=0, sticky="w", padx=20, pady=20)
        return button

    def _user_message(self, username):
        logging.info(f"User {username} clicked")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Login/Registration")
    root.geometry("800x600")
    root.resizable(False, False)
    app = HeaderView(root, 800, 100, "John", bg=BLACK, text_color=WHITE)
    side_view = SideView(root, 200, 700, ["John", "Jane", "Jack"],
                         bg=BLACK, text_color=WHITE)
    root.mainloop()
    logging.info("Exiting")
