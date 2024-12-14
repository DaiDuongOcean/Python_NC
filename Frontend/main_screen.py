import tkinter as tk

class MainScreen(tk.Frame):
    def __init__(self, controller):
        super().__init__(controller.root)
        self.controller = controller
        self.configure(bg="#4A90E2")
        self.pack(fill="both", expand=True)

        main_title = tk.Label(self, text="React To-Do List", font=("Arial", 18, "bold"), bg="#4A90E2", fg="white")
        main_title.pack(pady=20)

        # Navigation Buttons (dùng grid để chia đều)
        nav_frame = tk.Frame(self, bg="#4A90E2")
        nav_frame.pack(pady=10)

        # Cấu hình các cột của grid
        nav_frame.grid_columnconfigure(0, weight=1, uniform="equal")
        nav_frame.grid_columnconfigure(1, weight=1, uniform="equal")
        nav_frame.grid_columnconfigure(2, weight=1, uniform="equal")
        nav_frame.grid_columnconfigure(3, weight=1, uniform="equal")
        nav_frame.grid_columnconfigure(4, weight=2, uniform="equal")  # Tăng chiều rộng cho cột cuối

        # Add button remains the same
        add_todo_button = tk.Button(nav_frame, text="Add", font=("Arial", 10), bg="white", fg="#4A90E2",
                                    command=lambda: self.controller.show_frame("AddTodoScreen"))
        add_todo_button.grid(row=0, column=0, padx=10, pady=5, sticky="ew")  # Căn chỉnh cho nút "Add"

        # OptionMenus with smaller font size
        status_options = ["Status", "To-do", "Completed"]
        self.status_var = tk.StringVar(nav_frame)
        self.status_var.set(status_options[0])  # Set mặc định là "Status"
        status_menu = tk.OptionMenu(nav_frame, self.status_var, *status_options)
        status_menu.config(font=("Arial", 10), bg="white", fg="#4A90E2")
        status_menu.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        task_options = ["All", "Pending", "Completed"]
        self.task_var = tk.StringVar(nav_frame)
        self.task_var.set(task_options[0])  # Set mặc định là "All"
        task_menu = tk.OptionMenu(nav_frame, self.task_var, *task_options)
        task_menu.config(font=("Arial", 10), bg="white", fg="#4A90E2")
        task_menu.grid(row=0, column=2, padx=10, pady=5, sticky="ew")

        priority_options = ["Priority", "High", "Medium", "Low"]
        self.priority_var = tk.StringVar(nav_frame)
        self.priority_var.set(priority_options[0])  # Set mặc định là "Priority"
        priority_menu = tk.OptionMenu(nav_frame, self.priority_var, *priority_options)
        priority_menu.config(font=("Arial", 10), bg="white", fg="#4A90E2")
        priority_menu.grid(row=0, column=3, padx=10, pady=5, sticky="ew")

        # Tạo phần search bar chiếm nhiều không gian hơn
        search_frame = tk.Frame(nav_frame, bg="#4A90E2")
        search_frame.grid(row=0, column=4, padx=10, pady=5, sticky="ew")

        search_entry = tk.Entry(search_frame, font=("Arial", 12), width=20)
        search_entry.pack(side="left", ipadx=0, ipady=5)

        search_button = tk.Button(search_frame, text="🔍", font=("Arial", 12), bg="white", fg="#4A90E2",
                                  command=self.search_action)
        search_button.pack(side="left", padx=5)

        # Table Headers
        table_frame = tk.Frame(self, bg="white", padx=10, pady=10)
        table_frame.pack(fill="x", padx=20, pady=20)

        headers = ["Task", "Description", "Category", "When", "Priority", "Fulfillment", "Actions"]
        for i, header in enumerate(headers):
            header_label = tk.Label(table_frame, text=header, font=("Arial", 10, "bold"), bg="white", anchor="w")
            header_label.grid(row=0, column=i, sticky="w", padx=5)

        # Example Rows (Dummy Data)
        tasks = [
            ["Learn React", "Managing State, Effects", "Programming", "-", "High", "30%", ""],
            ["Shopping", "Potatoes, Onions, Eggs", "Household", "26.02.2023", "High", "0%", ""],
            ["Buy Tickets", "cheapflights.com/shanghai", "Travel", "12.01.2023 12:00", "Medium", "100%", ""],
        ]

        for row, task in enumerate(tasks, start=1):
            for col, data in enumerate(task):
                task_label = tk.Label(table_frame, text=data, font=("Arial", 10), bg="white", anchor="w")
                task_label.grid(row=row, column=col, sticky="w", padx=5)

    def search_action(self):
        # Lấy giá trị từ ô tìm kiếm và thực hiện hành động
        print("Tìm kiếm:", self.search_entry.get())
