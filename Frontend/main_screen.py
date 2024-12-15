import tkinter as tk
from tkinter import ttk

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

        # Empty columns for spacing
        # empty_label_1 = tk.Label(nav_frame, bg="#4A90E2")
        # empty_label_1.grid(row=0, column=1)

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

        self.tree = ttk.Treeview(table_frame, columns=("Task", "Description", "Category", "When", "Priority", "Fulfillment", "Actions"), show="headings")
        self.tree.heading("Task", text="Task")
        self.tree.heading("Description", text="Description")
        self.tree.heading("Category", text="Category")
        self.tree.heading("When", text="When")
        self.tree.heading("Priority", text="Priority")
        self.tree.heading("Fulfillment", text="Fulfillment")
        self.tree.heading("Actions", text="Actions")

        # Column Widths
        self.tree.column("Task", width=120, anchor="w")
        self.tree.column("Description", width=200, anchor="w")
        self.tree.column("Category", width=100, anchor="w")
        self.tree.column("When", width=100, anchor="w")
        self.tree.column("Priority", width=100, anchor="w")
        self.tree.column("Fulfillment", width=100, anchor="w")
        self.tree.column("Actions", width=150, anchor="center")

        tasks = [
            ["Learn React", "Managing State, Effects", "Programming", "-", "High", "30%", ""],
            ["Shopping", "Potatoes, Onions, Eggs", "Household", "26.02.2023", "High", "0%", ""],
            ["Buy Tickets", "cheapflights.com/shanghai", "Travel", "12.01.2023 12:00", "Medium", "100%", ""],
        ]

        for task in tasks:
            self.tree.insert("", "end", values=task[:-1])

        self.tree.pack(fill="both", expand=True)

        # Action buttons
        action_buttons_frame = tk.Frame(self, bg="#4A90E2", pady=10)
        action_buttons_frame.pack()

        edit_button = tk.Button(action_buttons_frame, text="Edit", font=("sans 12 bold"), bg="white", fg="#4A90E2", width=12, command=self.edit_task, bd=5)
        delete_button = tk.Button(action_buttons_frame, text="Delete", font=("sans 12 bold"), bg="white", fg="#4A90E2", width=12, command=self.delete_task, bd=5)

        edit_button.pack(side="left", padx=10)
        delete_button.pack(side="left", padx=10)

    def edit_task(self):
        print("Edit Task")

    def delete_task(self):
        print("Delete Task")

    def search_action(self):
        print("Search action executed")
