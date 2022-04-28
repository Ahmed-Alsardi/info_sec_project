import tkinter as tk
import logging
from UI.utility import BLACK, WHITE
from typing import List
from application_context import UserMessage
from datetime import datetime

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


class MessageView(tk.Frame):
    def __init__(self, parent, width: int, height: int, bg, text_color, message_list: List[UserMessage]):
        tk.Frame.__init__(self, parent, width=width, height=height, background=bg)
        self.frame_width = width
        self.frame_height = height
        self.bg = bg
        self.text_color = text_color
        self.message_list = message_list
        # create label "my messages"
        self.label_my_messages = tk.Label(self, text="My Messages", bg=bg, fg=text_color)
        self.label_my_messages.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=20, pady=20)
        self.messages = [self._create_message_widget(message, i) for i, message in enumerate(message_list)]
        # pack the frame
        self.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

    def _create_message_widget(self, message, i):
        from_user = tk.Label(self, text=f"From: {message.from_user}", bg=self.bg, fg=self.text_color)
        from_user.grid(row=i + 1, column=0, sticky="w", padx=10, pady=10)
        send_at = tk.Label(self, text=f"Send at: {message.send_at}", bg=self.bg, fg=self.text_color)
        send_at.grid(row=i + 1, column=1, sticky="w", padx=10, pady=10)
        # download button
        download_button = tk.Button(self, text="Download", command=lambda: self._download_message(message))
        download_button.grid(row=i + 1, column=2, sticky="e", padx=10, pady=10)
        logging.info(f"Message {message} created")

    def _download_message(self, message: UserMessage):
        logging.info(f"Download message {message.file_uuid}")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Login/Registration")
    root.geometry("800x600")
    root.resizable(False, False)
    app = HeaderView(root, 800, 100, "John", bg=BLACK, text_color=WHITE)
    side_view = SideView(root, 200, 700, ["John", "Jane", "Jack"],
                         bg=BLACK, text_color=WHITE)
    message_list = [
        UserMessage("Jane", "John", datetime.now(), "Hello", "file_type", "session key"),
        UserMessage("Jane1", "John1", datetime.now(), "Hello1", "file_type", "session key"),
        UserMessage("Jane2", "John2", datetime.now(), "Hello2", "file_type", "session key"),
        UserMessage("Jane3", "John3", datetime.now(), "Hello3", "file_type", "session key"),
    ]
    message_view = MessageView(root, 600, 700, bg=WHITE, text_color=BLACK, message_list=message_list)
    root.mainloop()
    logging.info("Exiting")
