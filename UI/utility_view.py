import logging
import tkinter as tk

from UI.components import (
    ComponentName, MessageComponent, HeaderComponent, SideComponent, SendComponent,
)
from UI.utility import WHITE, BLACK
from application_context import ApplicationContext

logging.basicConfig(
    level=logging.INFO, format=" %(asctime)s - %(levelname)s - %(message)s"
)


class WindowController(tk.Tk):
    def __init__(
            self, frame_width, frame_height,
            default_frame: ComponentName,
            application_context: ApplicationContext, *args, **kwargs
    ):
        tk.Tk.__init__(self, *args, **kwargs)
        self.current_frame: ComponentName = default_frame
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.__application_context = application_context
        self._load_default_frames()  # default frame

    def switch_frame(self, new_frame: ComponentName, **kwargs):
        if new_frame is None:
            return
        self._delete_current_main_frame()
        if new_frame == ComponentName.MESSAGE:
            self._load_message_frame(**kwargs)
        else:
            self._load_send_frame(**kwargs)

    def _delete_current_main_frame(self):
        for frame in self.winfo_children():
            if str(frame) == ".message" or str(frame) == ".send":
                frame.destroy()
        logging.info("Deleting current frame")

    def _load_message_frame(self, **kwargs):

        logging.info("Loading message frame")
        message_frame = MessageComponent(self,
                                         width=self.frame_width,
                                         height=self.frame_height,
                                         bg=WHITE, text_color=BLACK,
                                         message_list=self.__application_context.get_messages(),
                                         )
        message_frame.pack(fill=tk.BOTH, expand=True)

    def _load_send_frame(self, **kwargs):
        assert "username" in kwargs
        logging.info("Loading send frame")
        username = kwargs["username"]
        send_frame = SendComponent(self, width=self.frame_width, height=self.frame_height,
                                   bg=WHITE, text_color=BLACK, username=username)
        send_frame.pack(fill=tk.BOTH, expand=True)

    def _load_default_frames(self):
        header_frame = HeaderComponent(self, width=800, height=100,
                                       username=self.__application_context.username,
                                       bg=BLACK, text_color=WHITE)
        header_frame.pack(fill=tk.BOTH)
        side_frame = SideComponent(self, width=200, height=500,
                                   bg=BLACK, text_color=WHITE,
                                   usernames=self.__application_context.get_users())
        side_frame.pack(fill=tk.BOTH)
        self._load_message_frame()
