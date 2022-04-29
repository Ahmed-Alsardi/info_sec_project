import logging
import tkinter as tk

from UI.components import (
    ComponentName,
    MessageComponent,
    HeaderComponent,
    SideComponent,
    SendComponent,
)
from UI.log_reg_view import LoginRegistrationComponent
from UI.utility import WHITE, BLACK
from application_context import ApplicationContext

logging.basicConfig(
    level=logging.INFO, format=" %(asctime)s - %(levelname)s - %(message)s"
)


class WindowController(tk.Tk):
    def __init__(
            self,
            frame_width,
            frame_height,
            default_frame: ComponentName,
            application_context: ApplicationContext,
            *args,
            **kwargs
    ):
        tk.Tk.__init__(self, *args, **kwargs)
        self.current_frame: ComponentName = default_frame
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.__application_context = application_context
        if application_context.username is None:
            self._load_login_frame()
        else:
            self._load_dashboard_frames()  # default frame

    def switch_frame(self, new_frame: ComponentName, **kwargs):
        if new_frame is None:
            return
        self._delete_frames()
        if new_frame == ComponentName.MESSAGE:
            self._load_message_frame(**kwargs)
        elif new_frame == ComponentName.SEND:
            self._load_send_frame(**kwargs)
        elif new_frame == ComponentName.LOGIN_REGISTRATION:
            self._load_login_frame()
        elif new_frame == ComponentName.DASHBOARD:
            self._login_attempt(**kwargs)

    def send_file(self, to_user, file_name, file_path):
        logging.info(f"Sending file {file_path} to {to_user}")
        with open(file_path, "rb") as f:
            file_data = f.read()
            self.__application_context.send_message(to_user=to_user, file=file_data, file_type=file_name)

    def _delete_frames(self, all=False):
        for frame in self.winfo_children():
            if all:
                frame.destroy()
                continue
            if str(frame) == ".message" or str(frame) == ".send":
                frame.destroy()
        logging.info("Deleting current frame")

    def _load_message_frame(self, **kwargs):
        if self.current_frame == ComponentName.LOGIN_REGISTRATION or self.current_frame == ComponentName.DASHBOARD:
            self._layout_frames()
        logging.info("Loading message frame")
        message_frame = MessageComponent(
            self,
            width=self.frame_width,
            height=self.frame_height,
            bg=WHITE,
            text_color=BLACK,
            message_list=self.__application_context.get_messages(),
        )
        message_frame.pack(fill=tk.BOTH, expand=True)
        self.current_frame = ComponentName.MESSAGE

    def _load_send_frame(self, **kwargs):
        if self.current_frame == ComponentName.LOGIN_REGISTRATION:
            self._layout_frames()
        assert "username" in kwargs
        logging.info("Loading send frame")
        username = kwargs["username"]
        send_frame = SendComponent(
            self,
            width=self.frame_width,
            height=self.frame_height,
            bg=WHITE,
            text_color=BLACK,
            username=username,
        )
        send_frame.pack(fill=tk.BOTH, expand=True)
        self.current_frame = ComponentName.SEND

    def _load_dashboard_frames(self, **kwargs):
        self._delete_frames(all=True)
        self._layout_frames()
        self._load_message_frame()

    def _layout_frames(self):
        self._delete_frames(all=True)
        header_frame = HeaderComponent(
            self,
            width=800,
            height=100,
            username=self.__application_context.username,
            bg=BLACK,
            text_color=WHITE,
        )
        header_frame.pack(fill=tk.BOTH)
        side_frame = SideComponent(
            self,
            width=200,
            height=500,
            bg=BLACK,
            text_color=WHITE,
            usernames=self.__application_context.get_users(),
        )
        side_frame.pack(fill=tk.BOTH)

    def _load_login_frame(self):
        self._delete_frames(all=True)
        login_frame = LoginRegistrationComponent(self, width=800, height=600, bg=WHITE, text_color=BLACK)
        login_frame.pack(expand=True, anchor=tk.CENTER)
        self.current_frame = ComponentName.LOGIN_REGISTRATION

    def _login_attempt(self, **kwargs):
        assert "username" in kwargs
        assert "password" in kwargs
        assert "new_user" in kwargs
        logging.info("Attempting login")
        username = kwargs["username"]
        password = kwargs["password"]
        new_user = kwargs["new_user"]
        if new_user:
            if self.__application_context.register(username=username, password=password):
                logging.info("Successfully registered")
                self.switch_frame(ComponentName.MESSAGE)
            else:
                tk.Label(self, text="Username already exists", bg=WHITE, fg=BLACK).pack()
        else:
            if self.__application_context.login(username=username, password=password):
                logging.info("Successfully logged in")
                self.switch_frame(ComponentName.MESSAGE)
            else:
                tk.Label(self, text="Incorrect username or password", bg=WHITE, fg=BLACK).pack()
