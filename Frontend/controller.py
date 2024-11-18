from main_screen import MainScreen
from add_screen import AddTodoScreen

class Controller:
    def __init__(self, root):
        self.root = root
        self.frames = {}

        # Initialize frames
        self.frames["MainScreen"] = MainScreen(self)
        self.frames["AddTodoScreen"] = AddTodoScreen(self)

        # Show the main screen by default
        self.show_frame("MainScreen")

    def show_frame(self, frame_name):
        """Switch to the specified frame."""
        frame = self.frames[frame_name]
        if(frame_name == "MainScreen"):
            self.frames["AddTodoScreen"].pack_forget()
        else:
            self.frames["MainScreen"].pack_forget()
        frame.pack(fill="both", expand=True)
