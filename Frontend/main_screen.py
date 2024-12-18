import tkinter as tk
from tkinter import ttk
import mysql.connector

class MainScreen(tk.Frame):
    def __init__(self, controller):
        super().__init__(controller.root)
        self.controller = controller
        self.configure(bg="#4A90E2")
        self.pack(fill="both", expand=True)

        main_title = tk.Label(self, text="Note List", font=("sans 18 bold"), bg="#4A90E2", fg="white")
        main_title.pack(pady=20)

        # Navigation Buttons
        nav_frame = tk.Frame(self, bg="#4A90E2")
        nav_frame.pack(fill="x", pady=20)

        # Column configuration for equal width and spacing
        for i in range(6):  # 7 columns (1 for "Add" button, 3 for OptionMenus, 1 for empty space, and 2 for search area)
            nav_frame.grid_columnconfigure(i, weight=1)

        # Button Add To-Do (made larger and more prominent)
        add_todo_button = tk.Button(nav_frame, text="Add", font=("sans 12 bold"), bg="white", fg="#4A90E2", bd=5,
                                    command=lambda: self.controller.show_frame("AddTodoScreen"))
        add_todo_button.grid(row=0, column=0, padx=(20, 40), pady=5, sticky="ew")

        # Option Menus (Equal size)
        status_options = ["Uncomplete", "Completed"]
        self.status_var = tk.StringVar(nav_frame)
        self.status_var.set("Status")
        status_menu = tk.OptionMenu(nav_frame, self.status_var, *status_options)
        status_menu.config(font=("sans 10"), bg="white", fg="#4A90E2")
        status_menu.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        task_options = ["Cate 1", "Cate 2"]
        self.task_var = tk.StringVar(nav_frame)
        self.task_var.set("Category")
        task_menu = tk.OptionMenu(nav_frame, self.task_var, *task_options)
        task_menu.config(font=("sans 10"), bg="white", fg="#4A90E2")
        task_menu.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        priority_options = ["High", "Medium", "Low"]
        self.priority_var = tk.StringVar(nav_frame)
        self.priority_var.set("Priority")
        priority_menu = tk.OptionMenu(nav_frame, self.priority_var, *priority_options)
        priority_menu.config(font=("sans 10"), bg="white", fg="#4A90E2")
        priority_menu.grid(row=0, column=4, padx=5, pady=5, sticky="ew")

        # Empty columns for spacing
        empty_label_2 = tk.Label(nav_frame, bg="#4A90E2")
        empty_label_2.grid(row=0, column=5)

        # Search section (pushed to the right)
        search_frame = tk.Frame(nav_frame, bg="#4A90E2")
        search_frame.grid(row=0, column=6, padx=(20, 20), pady=5, sticky="ew")

        search_entry = tk.Entry(search_frame, font=("sans 12 bold"), width=30)
        search_entry.pack(side="left", ipady=5, padx=5)

        search_button = tk.Button(search_frame, text="🔍", font=("sans 12 bold"), bg="white", fg="#4A90E2",
                                  command=self.search_action)
        search_button.pack(side="right")

        # Table Headers and Treeview
        table_frame = tk.Frame(self, bg="white", padx=10, pady=10)
        table_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.tree = ttk.Treeview(table_frame, columns=("Task", "Description", "Category", "When","Time" , "Priority", "Status", "Image"), show="headings")
        self.tree.heading("Task", text="Name")
        self.tree.heading("Description", text="Description")
        self.tree.heading("Category", text="Category")
        self.tree.heading("When", text="Date")
        self.tree.heading("Time", text="Time")
        self.tree.heading("Priority", text="Priority")
        self.tree.heading("Status", text="Status")
        self.tree.heading("Image", text="Image")

        # Column Widths
        self.tree.column("Task", width=120, anchor="w")
        self.tree.column("Description", width=200, anchor="w")
        self.tree.column("Category", width=100, anchor="w")
        self.tree.column("When", width=100, anchor="w")
        self.tree.column("Time", width=100, anchor="w")
        self.tree.column("Priority", width=100, anchor="w")
        self.tree.column("Image", width=100, anchor="w")

        # for task in tasks:
        #     self.tree.insert("", "end", values=task)

        self.tree.pack(fill="both", expand=True)

        # Action buttons
        action_buttons_frame = tk.Frame(self, bg="#4A90E2", pady=10)
        action_buttons_frame.pack()

        edit_button = tk.Button(action_buttons_frame, text="Edit", font=("sans 12 bold"), bg="white", fg="#4A90E2", width=12, command=self.edit_task, bd=5)
        delete_button = tk.Button(action_buttons_frame, text="Delete", font=("sans 12 bold"), bg="white", fg="#4A90E2", width=12, command=self.delete_task, bd=5)

        edit_button.pack(side="left", padx=10)
        delete_button.pack(side="left", padx=10)

    def update_screen(self, target_screen=None):
        """Cập nhật dữ liệu khi màn hình được hiển thị."""
        # Chỉ reset dữ liệu khi chuyển sang AddTodoScreen
        #if target_screen == "AddTodoScreen":
        self.load_data()

    def load_data(self):
        # Kết nối cơ sở dữ liệu và lấy dữ liệu
        db = mysql.connector.connect(
            host="127.0.0.1",
            username="admin",
            password="Ocean123"
        )
        cursor = db.cursor()
        cursor.execute("use BTL_PythonNC")
        cursor.execute("SELECT name, description, category, date, time, priority, status, image FROM NOTE")  # Câu SQL
        rows = cursor.fetchall()
        db.close()

        # Xóa dữ liệu cũ trong Treeview
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Thêm dữ liệu mới vào Treeview
        for row in rows:
            self.tree.insert("", "end", values=row)

    def edit_task(self):
        selected_item = self.tree.selection()  # Lấy phần tử được chọn
        if not selected_item:
            print("No item selected!")
            return

        # Lấy giá trị từ phần tử được chọn
        selected_values = self.tree.item(selected_item, "values")
        task_data = {
            "name": selected_values[0],
            "description": selected_values[1],
            "category": selected_values[2],
            "date": selected_values[3],
            "time": selected_values[4],
            "priority": selected_values[5],
            "status": selected_values[6],
        }
        print(task_data)
        # Gửi dữ liệu tới EditScreen
        self.controller.show_frame("EditTodoScreen", data=task_data)

    def delete_task(self):
        print("Delete Task")

    def search_action(self):
        print("Search action executed")
