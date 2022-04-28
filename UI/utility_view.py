import logging
import tkinter as tk
from datetime import datetime
from tkinter.filedialog import askopenfile
from typing import List

from UI.utility import BLACK, WHITE
from application_context import UserMessage

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


class SendMessageView(tk.Frame):
    def __init__(self, parent, width: int, height: int, bg: str, text_color: str, username: str):
        tk.Frame.__init__(self, parent, width=width, height=height, background=bg)
        self.file_path = None
        self.frame_width = width
        self.frame_height = height
        self.bg = bg
        self.text_color = text_color
        self.username = username
        self.__supported_file_types = [
            ("Text Files", "*.txt"),
            ("Image Files", "*.jpeg"),
            ("PDF Files", "*.pdf"),
        ]
        # create label "send message to"
        self.label_send_message_to = tk.Label(self, text=f"Send message to: {username}", bg=bg, fg=text_color)
        self.label_send_message_to.grid(row=0, column=0, sticky="w", padx=20, pady=20)
        # upload file
        self.upload_file_label = tk.Label(self, text="Upload file", bg=bg, fg=text_color)
        self.upload_file_label.grid(row=1, column=0, sticky="w", padx=20, pady=20)
        # create button to upload file
        self.upload_file_button = tk.Button(self, text="Upload", command=lambda: self.open_file())
        self.upload_file_button.grid(row=1, column=1, sticky="e", padx=20, pady=20)

        # pack the frame
        self.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

    def open_file(self):
        file_path = askopenfile(mode="r", filetypes=self.__supported_file_types)
        if file_path is None:
            return
        print(type(file_path))
        print(dir(file_path))
        print(file_path)
        logging.info(f"File {file_path.name} selected")
        self.file_path = file_path
        self.upload_label = tk.Label(self,
                                     text=f"File {self._extract_file_name(file_path.name)} selected",
                                     bg=self.bg, fg=self.text_color)
        self.upload_label.grid(row=2, column=0, sticky="w", padx=20, pady=20)
        self.upload_button = tk.Button(self, text="Send", command=lambda: self.upload_file())
        self.upload_button.grid(row=3, column=0, sticky="e", padx=20, pady=20)

    def upload_file(self):
        if self.file_path is None:
            tk.Label(self, text="Please select file first",
                     bg=self.bg, fg=self.text_color).grid(row=3, column=0, sticky="w", padx=20, pady=20)
            return
        logging.info(f"File uploaded")
        tk.Label(self, text="File uploaded",
                 bg=self.bg, fg=self.text_color).grid(row=3, column=0, sticky="w", padx=20, pady=20)

    def _extract_file_name(self, name):
        return name.split("/")[-1]


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
    # message_view = MessageView(root, 600, 700, bg=WHITE, text_color=BLACK, message_list=message_list)
    send_message_view = SendMessageView(root, 600, 700, bg=WHITE, text_color=BLACK, username="John")
    root.mainloop()
    logging.info("Exiting")
