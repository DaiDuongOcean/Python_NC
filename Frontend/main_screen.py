import tkinter as tk
from tkinter import ttk
from tkinter import  messagebox
from functools import partial
from Backend.controller.main import load_notes, update_note, delete_note
from Frontend.util import CATEGORIES, PRIORITY, STATUS, get_cols, get_col_index_by_name, convert_from_list_to_dict, \
    is_image_file_in_folder
from PIL import Image, ImageTk

class MainScreen(tk.Frame):
    def __init__(self, controller):
        super().__init__(controller.root)
        self.controller = controller
        self.configure(bg="#4A90E2")
        self.pack(fill="both", expand=True)
        self.filter = {
            'status': "All",
            'category': "All",
            'priority': "All"
        }

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
        status_options = ["All", *STATUS]
        self.status_var = tk.StringVar(nav_frame)
        self.status_var.set("Status")
        status_menu = tk.OptionMenu(nav_frame, self.status_var, *status_options, command=partial(
            self.on_select_option_menu, 'status'))
        status_menu.config(font=("sans 10"), bg="white", fg="#4A90E2")
        status_menu.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        task_options = ["All", *CATEGORIES]
        self.task_var = tk.StringVar(nav_frame)
        self.task_var.set("Category")
        task_menu = tk.OptionMenu(nav_frame, self.task_var, *task_options, command=partial(self.on_select_option_menu, 'category'))
        task_menu.config(font=("sans 10"), bg="white", fg="#4A90E2")
        task_menu.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        priority_options = ["All", *PRIORITY]
        self.priority_var = tk.StringVar(nav_frame)
        self.priority_var.set("Priority")
        priority_menu = tk.OptionMenu(nav_frame, self.priority_var, *priority_options, command=partial(
            self.on_select_option_menu, 'priority'))
        priority_menu.config(font=("sans 10"), bg="white", fg="#4A90E2")
        priority_menu.grid(row=0, column=4, padx=5, pady=5, sticky="ew")

        # Empty columns for spacing
        empty_label_2 = tk.Label(nav_frame, bg="#4A90E2")
        empty_label_2.grid(row=0, column=5)

        # Search section (pushed to the right)
        search_frame = tk.Frame(nav_frame, bg="#4A90E2")
        search_frame.grid(row=0, column=6, padx=(20, 20), pady=5, sticky="ew")

        self.search_entry = tk.Entry(search_frame, font=("sans 12 bold"), width=30)
        self.search_entry.pack(side="left", ipady=5, padx=5)

        search_button = tk.Button(search_frame, text="🔍", font=("sans 12 bold"), bg="white", fg="#4A90E2",
                                  command=self.search_action)
        search_button.pack(side="right")

        # Table Headers and Treeview
        table_frame = tk.Frame(self, bg="white", padx=10, pady=10)
        table_frame.pack(fill="both", expand=True, padx=20, pady=20)

        cols = get_cols()
        cols_name = [col['name'] for col in cols]
        self.tree = ttk.Treeview(table_frame, columns=cols_name, show="headings")
        for col in cols_name:
            self.tree.heading(col, text=col)
        # Column Widths
        for col in cols:
            self.tree.column(col['name'], width=col['width'], anchor="w")

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
        self.tree.bind("<Button-1>", lambda event: self.on_click(event))

    def toggle_checkbox(self, item_id):
        self.tree.selection_set(item_id)
        selected_item = self.tree.selection()
        if selected_item:
            row_values = list(self.tree.item(selected_item, "values"))
            col_index = get_col_index_by_name("Status")
            current_value = self.tree.item(item_id, "values")[col_index]
            if current_value == STATUS["Uncomplete"]:
                new_value = STATUS["Completed"]
            else:
                new_value = STATUS["Uncomplete"]
            row_values[col_index] = new_value
            self.tree.item(item_id, values=row_values)
            note_info = convert_from_list_to_dict(row_values)
            update_note(note_info)
            messagebox.showinfo(title="Success", message="Update status successfully")

    def on_click(self, event):
        """Handle clicks on the Treeview to toggle checkboxes."""
        region = self.tree.identify("region", event.x, event.y)
        if region == "cell":  # Check if the click is inside a cell
            column = self.tree.identify_column(event.x)
            status_col = get_col_index_by_name("Status")
            img_col = get_col_index_by_name("Image")
            if column == f"#{status_col + 1}":
                row_id = self.tree.identify_row(event.y)
                if row_id:  # Ensure a valid row is clicked
                    self.toggle_checkbox(row_id)
            elif column == f"#{img_col + 1}":
                row_id = self.tree.identify_row(event.y)
                if row_id:  # Ensure a valid row is clicked
                    self.show_image_popup(row_id)

    def on_select_option_menu(self, attribute, value):
        self.filter[f"{attribute}"] = value
        self.update_screen()

    def update_screen(self, target_screen=None):
        """Cập nhật dữ liệu khi màn hình được hiển thị."""
        # Chỉ reset dữ liệu khi chuyển sang AddTodoScreen
        #if target_screen == "AddTodoScreen":
        self.load_data()

    def load_data(self):
        filter_val = self.filter
        search_val = self.search_entry.get()
        rows = load_notes(filter_val, search_val)

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
        task_data = convert_from_list_to_dict(selected_values)

        # Gửi dữ liệu tới EditScreen
        self.controller.show_frame("EditTodoScreen", data=task_data)

    def delete_task(self):
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this note?")
        selected_item = self.tree.selection()  # Lấy phần tử được chọn
        if not selected_item or not confirm:
            print("No item selected!")
            return

        # Lấy giá trị từ phần tử được chọn
        selected_values = self.tree.item(selected_item, "values")
        task_data = convert_from_list_to_dict(selected_values)
        delete_note(task_data['id'])
        self.update_screen()

    def search_action(self):
        self.update_screen()

    def show_image_popup(self, item_id):
        imgs_folder = "../Img"
        self.tree.selection_set(item_id)
        selected_item = self.tree.selection()
        if selected_item:
            row_values = list(self.tree.item(selected_item, "values"))
            col_index = get_col_index_by_name("Image")
            img_name = row_values[col_index]
            # Create a new Toplevel window
            available_img = is_image_file_in_folder(imgs_folder, img_name)
            if available_img:
                img_absolute_path = imgs_folder + f"\\{img_name}"
                popup = tk.Toplevel()
                popup.title("Image Popup")
                # Load the image using Pillow
                image = Image.open(img_absolute_path)
                # Resize the image if needed
                image = image.resize((300, 300))
                # Convert the image to a PhotoImage object
                photo = ImageTk.PhotoImage(image)
                # Create a label to display the image
                label = tk.Label(popup, image=photo)
                label.image = photo  # Keep a reference to the image to prevent garbage collection
                label.pack()
                # Add a close button
                close_button = tk.Button(popup, text="Close", command=popup.destroy)
                close_button.pack()


