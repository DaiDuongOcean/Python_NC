import tkinter as tk
from tkinter import ttk

class ListBoxWithButtons(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Listbox with Buttons")
        self.geometry("400x300")

        # Tạo Canvas để hỗ trợ scroll
        canvas = tk.Canvas(self)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Tạo Scrollbar
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Liên kết scrollbar với canvas
        canvas.configure(yscrollcommand=scrollbar.set)

        # Tạo Frame bên trong Canvas
        frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=frame, anchor="nw")

        # Đảm bảo canvas có thể cuộn
        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        frame.bind("<Configure>", on_frame_configure)

        # Thêm các dòng với nút vào Frame
        for i in range(20):  # Tạo 20 dòng
            row_frame = tk.Frame(frame)
            row_frame.pack(fill=tk.X, padx=5, pady=2)

            label = tk.Label(row_frame, text=f"Row {i+1}", width=20, anchor="w")
            label.pack(side=tk.LEFT)

            button1 = tk.Button(row_frame, text="Button 1", command=lambda i=i: self.button_action(i, 1))
            button1.pack(side=tk.LEFT, padx=5)

            button2 = tk.Button(row_frame, text="Button 2", command=lambda i=i: self.button_action(i, 2))
            button2.pack(side=tk.LEFT)

    def button_action(self, row, button_num):
        print(f"Button {button_num} clicked in Row {row+1}")


# Chạy ứng dụng
if __name__ == "__main__":
    app = ListBoxWithButtons()
    app.mainloop()
