import logging
from datetime import datetime

from UI.components import (
    HeaderComponent,
    SideComponent,
    SendComponent,
    MessageComponent,
    ComponentName,
)
from UI.utility import BLACK, WHITE
from UI.utility_view import WindowController
from application_context import UserMessage

if __name__ == "__main__":
    root = WindowController(
        frame_width=600, frame_height=600, default_frame=ComponentName.MESSAGE
    )
    root.title("Login/Registration")
    root.geometry("800x600")
    root.resizable(False, False)
    app = HeaderComponent(root, 800, 100, "John", bg=BLACK, text_color=WHITE)
    side_view = SideComponent(
        root, 200, 700, ["John", "Jane", "Jack"], bg=BLACK, text_color=WHITE
    )
    message_list = [
        UserMessage(
            "Jane", "John", datetime.now(), "Hello", "file_type", "session key"
        ),
        UserMessage(
            "Jane1", "John1", datetime.now(), "Hello1", "file_type", "session key"
        ),
        UserMessage(
            "Jane2", "John2", datetime.now(), "Hello2", "file_type", "session key"
        ),
        UserMessage(
            "Jane3", "John3", datetime.now(), "Hello3", "file_type", "session key"
        ),
    ]
    message_view = MessageComponent(
        root, 600, 700, bg=WHITE, text_color=BLACK, message_list=message_list
    )
    send_message_view = SendComponent(
        root, 600, 700, bg=WHITE, text_color=BLACK, username="John"
    )
    root.mainloop()
    logging.info("Exiting")
