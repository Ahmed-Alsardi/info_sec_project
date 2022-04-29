import logging

from UI.components import (
    ComponentName,
)
from UI.utility_view import WindowController
from application_context import ApplicationContext

if __name__ == "__main__":
    app_context = ApplicationContext()
    app_context.login("test", "test")
    root = WindowController(
        frame_width=600,
        frame_height=600,
        default_frame=ComponentName.MESSAGE,
        application_context=app_context,
    )
    root.title("Login/Registration")
    root.geometry("800x600")
    root.resizable(False, False)
    # message_list = [
    #     UserMessage(
    #         "Jane", "John", datetime.now(), "Hello", "file_type", "session key"
    #     ),
    #     UserMessage(
    #         "Jane1", "John1", datetime.now(), "Hello1", "file_type", "session key"
    #     ),
    #     UserMessage(
    #         "Jane2", "John2", datetime.now(), "Hello2", "file_type", "session key"
    #     ),
    #     UserMessage(
    #         "Jane3", "John3", datetime.now(), "Hello3", "file_type", "session key"
    #     ),
    # ]
    root.mainloop()
    logging.info("Exiting")
