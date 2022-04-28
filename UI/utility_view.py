import logging
import tkinter as tk

from UI.components import (
    ComponentName,
)

logging.basicConfig(
    level=logging.INFO, format=" %(asctime)s - %(levelname)s - %(message)s"
)


class WindowController(tk.Tk):
    def __init__(
            self, frame_width, frame_height, default_frame: ComponentName, *args, **kwargs
    ):
        tk.Tk.__init__(self, *args, **kwargs)
        self.current_frame: ComponentName = default_frame
        self.frame_width = frame_width
        self.frame_height = frame_height

    def switch_frame(self, new_frame: ComponentName, **kwargs):
        if new_frame is None:
            return
        self._delete_current_frame()
        if new_frame == ComponentName.MESSAGE:
            self._load_message_frame(**kwargs)
        else:
            self._load_send_frame(**kwargs)

    def _delete_current_frame(self):
        logging.info("Deleting current frame")

    def _load_message_frame(self, **kwargs):
        logging.info("Loading message frame")

    def _load_send_frame(self, **kwargs):
        logging.info("Loading send frame")
