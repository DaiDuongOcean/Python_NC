import tkinter as tk
class MainScreen(tk.Frame):
    def __init__(self, controller):
        super().__init__(controller.root)
        self.controller = controller
        self.configure(bg="#4A90E2")
        self.pack(fill="both", expand=True)
        main_title = tk.Label(self, text="React To-Do List", font=("Arial", 18, "bold"), bg="#4A90E2", fg="white")
        main_title.pack(pady=20)

        # Navigation Buttons
        nav_frame = tk.Frame(self, bg="#4A90E2")
        nav_frame.pack(pady=10)

        add_todo_button = tk.Button(nav_frame, text="Add a new to-do", font=("Arial", 12), bg="white", fg="#4A90E2",
                                    command=lambda: self.controller.show_frame("AddTodoScreen"))
        add_todo_button.pack(side="left", padx=10)

        edit_todo_button = tk.Button(nav_frame, text="Edit a new to-do", font=("Arial", 12), bg="white", fg="#4A90E2",
                                    command=lambda: self.controller.show_frame("EditTodoScreen"))
        edit_todo_button.pack(side="left", padx=10)

        all_button = tk.Button(nav_frame, text="All", font=("Arial", 12), bg="#4A90E2", fg="white", width=8)
        all_button.pack(side="left", padx=10)

        todo_button = tk.Button(nav_frame, text="To-do", font=("Arial", 12), bg="#4A90E2", fg="white", width=8)
        todo_button.pack(side="left", padx=10)

        completed_button = tk.Button(nav_frame, text="Completed", font=("Arial", 12), bg="#4A90E2", fg="white", width=8)
        completed_button.pack(side="left", padx=10)

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
