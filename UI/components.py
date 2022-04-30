import logging
import tkinter as tk
from enum import Enum
from tkinter.filedialog import askopenfile
from typing import List

from application_context import UserMessage

# from UI.utility_view import WindowController

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


class ComponentName(Enum):
    LOGIN_ATTEMPT = 4
    MESSAGE = 1
    SEND = 2
    LOGIN_REGISTRATION = 3
    LOGOUT = 5


class HeaderComponent(tk.Frame):
    def __init__(self, parent, width: int, height: int, username: str, bg, text_color):
        tk.Frame.__init__(
            self, parent, width=width, height=height, background=bg, name="header"
        )
        self.parent = parent
        self.username = username
        self.bg = bg
        self.text_color = text_color
        # create label welcome username
        self.label_welcome = tk.Label(
            self, text=f"Welcome: {self.username}", bg=bg, fg=text_color
        )
        self.label_welcome.grid(
            row=0, column=0, columnspan=2, sticky="w", padx=20, pady=20
        )
        # create my message button
        self.button_my_message = tk.Button(
            self, text="My Message", command=self.my_message
        )
        self.button_my_message.grid(
            row=0, column=2, columnspan=2, sticky="e", padx=20, pady=20
        )
        # create logout button
        self.button_logout = tk.Button(self, text="Logout", command=self.logout)
        self.button_logout.grid(row=0, column=4, sticky="e", padx=20, pady=20)
        self.pack(
            fill=tk.BOTH
        )

    def my_message(self):
        self.parent.switch_frame(ComponentName.MESSAGE)
        logging.info("My message button clicked")

    def logout(self):
        self.parent.switch_frame(ComponentName.LOGOUT)
        logging.info("Logout button clicked")


class SideComponent(tk.Frame):
    def __init__(
            self, parent, width: int, height: int, usernames: List[str], bg, text_color
    ):
        tk.Frame.__init__(
            self, parent, width=width, height=height, background=bg, name="side"
        )
        self.parent = parent
        self.bg = bg
        self.text_color = text_color
        # create label "send message to"
        self.label_send_message_to = tk.Label(
            self, text="Send message to:", bg=bg, fg=text_color
        )
        self.label_send_message_to.grid(row=0, column=0, sticky="w", padx=20, pady=20)
        self.usernames = [
            self._create_user_button(username, i)
            for i, username in enumerate(usernames)
        ]
        self.pack(fill=tk.BOTH, side=tk.LEFT)

    def _create_user_button(self, username, index):
        button = tk.Button(
            self, text=username, width=10, command=lambda: self._user_message(username)
        )
        button.grid(row=index + 1, column=0, sticky="w", padx=20, pady=20)
        return button

    def _user_message(self, username):
        self.parent.switch_frame(ComponentName.SEND, username=username)
        logging.info(f"User {username} clicked")


class MessageComponent(tk.Frame):
    def __init__(
            self,
            parent,
            width: int,
            height: int,
            bg,
            text_color,
            message_list: List[UserMessage],
    ):
        tk.Frame.__init__(
            self, parent, width=width, height=height, background=bg, name="message"
        )
        self.bg = bg
        self.parent = parent
        self.text_color = text_color
        self.message_list = message_list
        # create label "my messages"
        self.label_my_messages = tk.Label(
            self, text="My Messages", bg=bg, fg=text_color
        )
        self.label_my_messages.grid(
            row=0, column=0, columnspan=2, sticky="nsew", padx=20, pady=20
        )
        self.messages = [
            self._create_message_widget(message, i)
            for i, message in enumerate(message_list)
        ]
        # pack the frame
        self.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

    def _create_message_widget(self, message, i):
        from_user = tk.Label(
            self, text=f"From: {message.from_user}", bg=self.bg, fg=self.text_color
        )
        from_user.grid(row=i + 1, column=0, sticky="w", padx=10, pady=10)
        send_at = tk.Label(
            self,
            text=f"Send at: {message.send_at.strftime('%b %d %Y %H:%M:%S')}",
            bg=self.bg,
            fg=self.text_color,
        )
        send_at.grid(row=i + 1, column=1, sticky="w", padx=10, pady=10)
        # download button
        download_button = tk.Button(
            self, text="Download", command=lambda: self._download_message(message)
        )
        download_button.grid(row=i + 1, column=2, sticky="e", padx=10, pady=10)
        logging.info(f"Message {message} created")

    def _download_message(self, message: UserMessage):
        logging.info(f"Download message {message.file_uuid}")


class SendComponent(tk.Frame):
    def __init__(
            self, parent, width: int, height: int, bg: str, text_color: str, username: str
    ):
        tk.Frame.__init__(
            self, parent, width=width, height=height, background=bg, name="send"
        )
        self.parent = parent
        self.file_path = None
        self.bg = bg
        self.text_color = text_color
        self.username = username
        self.__supported_file_types = [
            ("Text Files", "*.txt"),
            ("Image Files", "*.jpeg"),
            ("PDF Files", "*.pdf"),
        ]
        # create label "send message to"
        self.label_send_message_to = tk.Label(
            self, text=f"Send message to: {username}", bg=bg, fg=text_color
        )
        self.label_send_message_to.grid(row=0, column=0, sticky="w", padx=20, pady=20)
        # upload file
        self.upload_file_label = tk.Label(
            self, text="Upload file", bg=bg, fg=text_color
        )
        self.upload_file_label.grid(row=1, column=0, sticky="w", padx=20, pady=20)
        # create button to upload file
        self.upload_file_button = tk.Button(
            self, text="Upload", command=lambda: self.open_file()
        )
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
        self.upload_label = tk.Label(
            self,
            text=f"File {self._extract_file_name(file_path.name)} selected",
            bg=self.bg,
            fg=self.text_color,
        )
        self.upload_label.grid(row=2, column=0, sticky="w", padx=20, pady=20)
        self.upload_button = tk.Button(
            self, text="Send", command=lambda: self.upload_file()
        )
        self.upload_button.grid(row=3, column=0, sticky="e", padx=20, pady=20)

    def upload_file(self):
        if self.file_path is None:
            tk.Label(
                self, text="Please select file first", bg=self.bg, fg=self.text_color
            ).grid(row=3, column=0, sticky="w", padx=20, pady=20)
            return
        self.parent.send_file(to_user=self.username,
                              file_name=self._extract_file_name(self.file_path.name),
                              file_path=self.file_path.name)
        logging.info(f"File uploaded")
        tk.Label(self, text="File uploaded", bg=self.bg, fg=self.text_color).grid(
            row=3, column=0, sticky="w", padx=20, pady=20
        )

    def _extract_file_name(self, name):
        return name.split("/")[-1]
