from main_screen import MainScreen
from add_screen import AddTodoScreen
from edit_screen import  EditTodoScreen
#
# class Controller:
#     def __init__(self, root):
#         self.root = root
#         self.frames = {}
#
#         # Initialize frames
#         self.frames["MainScreen"] = MainScreen(self)
#         self.frames["AddTodoScreen"] = AddTodoScreen(self)
#         self.frames["EditTodoScreen"] = EditTodoScreen(self)
#
#         # Show the main screen by default
#         self.show_frame("MainScreen")
#
#         self.frames["AddTodoScreen"].set_up()
#         self.frames["EditTodoScreen"].set_up()
#
#     def show_frame(self, frame_name, data=None):
#         """Switch to the specified frame."""
#         show_frame = self.frames[frame_name]
#
#         # Hide other frames
#         for frame in self.frames.values():
#             if frame != show_frame:
#                 frame.pack_forget()
#
#         # Show the selected frame
#         show_frame.pack(fill="both", expand=True)
#
#         # Nếu có dữ liệu, truyền vào frame đang được hiển thị
#         # if data and hasattr(show_frame, "update_screen"):
#         #     show_frame.update_screen(data)
#
#         # Nếu quay lại MainScreen, cập nhật dữ liệu
#         if frame_name == "MainScreen":
#             self.frames["MainScreen"].update_screen()
#
#         # Nếu chuyển sang AddTodoScreen, reset các trường dữ liệu
#         if frame_name == "AddTodoScreen":
#             self.frames["AddTodoScreen"].reset_fields()

class Controller:
    def __init__(self, root):
        self.root = root
        self.frames = {}

        # Initialize frames
        self.frames["MainScreen"] = MainScreen(self)
        self.frames["AddTodoScreen"] = AddTodoScreen(self)
        self.frames["EditTodoScreen"] = EditTodoScreen(self)

        # Show the main screen by default
        self.show_frame("MainScreen")

        # Set up the frames
        self.frames["AddTodoScreen"].set_up()
        self.frames["EditTodoScreen"].set_up()

    def show_frame(self, frame_name, data=None):
        """Switch to the specified frame."""
        show_frame = self.frames[frame_name]

        # Hide other frames
        for frame in self.frames.values():
            if frame != show_frame:
                frame.pack_forget()

        # Show the selected frame
        show_frame.pack(fill="both", expand=True)
        # If data is provided, update the frame
        if data and hasattr(show_frame, "set_up"):
            show_frame.set_up(data)

        # Nếu quay lại MainScreen, cập nhật dữ liệu
        if frame_name == "MainScreen":
            self.frames["MainScreen"].update_screen()

        # Nếu chuyển sang AddTodoScreen, reset các trường dữ liệu
        if frame_name == "AddTodoScreen":
            self.frames["AddTodoScreen"].reset_fields()

