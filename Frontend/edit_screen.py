from tkinter import messagebox, ttk, filedialog
import tkinter as tk
from tkcalendar import DateEntry
from PIL import Image, ImageTk
import mysql.connector
import os

from Backend.controller.main import get_note, update_note
from Frontend.add_screen import imgs_folder
from Frontend.util import get_col_index_by_name, is_image_file_in_folder

bg_color = "#4A90E2"

class EditTodoScreen(tk.Frame):
    def __init__(self, controller):
        super().__init__(controller.root)
        self.controller = controller
        self.configure(bg="#2F2F2F")
        self.pack(fill="both", expand=True)

        self.data = None  # Placeholder for task data
        self.popup_set_time = None

    def set_up(self, data=None):
        self.data = data  # Receive the task data to edit
        self.clear_screen()  # Clear the screen before setting up new data

        # Add note form container
        add_todo_content = tk.Frame(self, bg=bg_color, padx=20, pady=20)
        add_todo_content.place(relx=0.5, rely=0.5, anchor="center", width=450, height=600)

        # Title
        title_label = tk.Label(add_todo_content, text="Edit Note", font=("Arial", 16, "bold"), bg=bg_color, fg="white")
        title_label.grid(row=0, column=0, columnspan=2, pady=(15, 15))

        # Fields for task details
        fields = [
            ("Name", None),
            ("Description", None),
            ("Category", ["Cate 1", "Cate 2", "Cate 3"]),
            ("Date", None),
            ("Time", None),
            ("Priority", ["Low", "Medium", "High"]),
        ]

        self.entries = {}
        for i, (field, options) in enumerate(fields):
            label = tk.Label(add_todo_content, text=field, font=("Arial", 10), bg=bg_color, fg="white")
            label.grid(row=i + 1, column=0, sticky="w", padx=10, pady=5)

            if options is None:
                if field == "Date":
                    entry = DateEntry(add_todo_content, font=("Arial", 10), background="darkblue", foreground="white",
                                      borderwidth=2)
                elif field == "Time":
                    entry = tk.Entry(add_todo_content, font=("Arial", 10), bg="white", fg="black",
                                     insertbackground="black")
                    entry.bind("<Button-1>", self.open_time_picker)
                else:
                    entry = tk.Entry(add_todo_content, font=("Arial", 10), bg="white", fg="black",
                                     insertbackground="black")
                entry.grid(row=i + 1, column=1, sticky="ew", padx=10, pady=5)
                self.entries[field] = entry
            else:
                combo = ttk.Combobox(add_todo_content, values=options, font=("Arial", 10))
                combo.grid(row=i + 1, column=1, sticky="ew", padx=10, pady=5)
                self.entries[field] = combo

        add_todo_content.columnconfigure(1, weight=1)

        # File Chooser
        file_label = tk.Label(add_todo_content, text="Attachment", font=("Arial", 10), bg=bg_color, fg="white")
        file_label.grid(row=len(fields) + 1, column=0, sticky="w", padx=10, pady=5)

        file_button = tk.Button(add_todo_content, text="Choose File", bg="#4A90E2", fg="white", font=("Arial", 10),
                                command=self.choose_file)
        file_button.grid(row=len(fields) + 1, column=1, sticky="w", padx=10, pady=5)

        self.file_label = tk.Label(add_todo_content, text="No file chosen", font=("Arial", 10), bg=bg_color, fg="white")
        self.file_label.grid(row=len(fields) + 2, column=0, columnspan=2, sticky="w", padx=10, pady=5)

        # Image Preview
        self.image_preview = tk.Label(self, bg=bg_color)
        self.image_preview.place(relx=0.5, rely=0.85, anchor="center")

        # Buttons
        button_frame = tk.Frame(add_todo_content, bg=bg_color)
        button_frame.grid(row=len(fields) + 3, column=0, columnspan=2, pady=10)

        add_button = tk.Button(button_frame, text="Save", font=("Arial", 12), bg="green", fg="white", width=10,
                               command=self.edit_note)
        add_button.pack(side="left", padx=10)

        cancel_button = tk.Button(button_frame, text="Cancel", font=("Arial", 12), bg="gray", fg="white", width=10,
                                  command=lambda: self.controller.show_frame("MainScreen"))
        cancel_button.pack(side="left", padx=10)

        # Fill in fields with existing data
        self.fill_fields_with_data()

    def clear_screen(self):
        """Clear specific fields or reset data for new entries."""
        if self.data:  # Nếu có dữ liệu
            for field, value in self.data.items():
                if field in self.entries:
                    entry = self.entries[field]
                    if isinstance(entry, tk.Entry) or isinstance(entry, DateEntry):
                        entry.delete(0, tk.END)  # Xóa nội dung của Entry
                    elif isinstance(entry, ttk.Combobox):
                        entry.set('')  # Reset Combobox nếu cần

    def fill_fields_with_data(self):
        """Populate the fields with data for editing"""
        if self.data:
            for field, value in self.data.items():
                normalized_field = field.capitalize()  # Example: 'name' to 'Name'

                if normalized_field in self.entries:
                    entry = self.entries[normalized_field]

                    if isinstance(entry, tk.Entry) or isinstance(entry, DateEntry):
                        entry.delete(0, tk.END)
                        entry.insert(0, value)

                    elif isinstance(entry, ttk.Combobox):
                        entry.set(value)

            item = get_note(self.data['id'])
            img_index = get_col_index_by_name("Image")
            img_name = item[img_index]
            available_img = is_image_file_in_folder(imgs_folder, img_name)
            if available_img:
                self.file_label.config(text=img_name)
                input_path = os.path.join(imgs_folder, img_name)
                image = Image.open(input_path)
                image = image.resize((150, 150))
                photo = ImageTk.PhotoImage(image)
                self.image_preview.config(image=photo)
                self.image_preview.image = photo


    def open_time_picker(self, event):
        if self.popup_set_time != None:
            self.popup_set_time.destroy()
        popup = tk.Toplevel(self)
        self.popup_set_time = popup
        popup.title("Select Time")
        popup.geometry("150x150")
        popup.configure(bg="#2F2F2F")

        # Hour label and Spinbox
        tk.Label(popup, text="Hour:", font=("Arial", 10), bg="#2F2F2F", fg="white").grid(row=0, column=0, padx=10,
                                                                                         pady=5)
        hour_var = tk.StringVar(value="00")
        hour_spinbox = ttk.Spinbox(
            popup, from_=0, to=23, wrap=True, textvariable=hour_var, font=("Arial", 10), width=5, validate="key"
        )
        hour_spinbox.grid(row=0, column=1, padx=10, pady=5)

        # Minute label and Spinbox
        tk.Label(popup, text="Minute:", font=("Arial", 10), bg="#2F2F2F", fg="white").grid(row=1, column=0, padx=10,
                                                                                           pady=5)
        minute_var = tk.StringVar(value="00")
        minute_spinbox = ttk.Spinbox(
            popup, from_=0, to=59, wrap=True, textvariable=minute_var, font=("Arial", 10), width=5, validate="key"
        )
        minute_spinbox.grid(row=1, column=1, padx=10, pady=5)

        # Function to validate and set time
        def set_time():
            try:
                hour = int(hour_var.get())
                minute = int(minute_var.get())

                # Ensure hour is within 0-23 and minute is within 0-59
                if 0 <= hour <= 23 and 0 <= minute <= 59:
                    time_value = f"{hour:02d}:{minute:02d}"  # Format as HH:MM
                    self.entries["Time"].delete(0, tk.END)
                    self.entries["Time"].insert(0, time_value)

                else:
                    tk.messagebox.showerror("Invalid Time", "Please enter a valid time (HH:MM).")

                popup.destroy()
            except ValueError:
                tk.messagebox.showerror("Invalid Input", "Please enter numbers only.")

        # Set button
        set_button = tk.Button(popup, text="Set", font=("Arial", 10), bg="green", fg="white", command=set_time)
        set_button.grid(row=2, column=0, columnspan=2, pady=10)

    def choose_file(self):
        filename = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif")])
        if filename:
            self.file_label.config(text=filename.split('/')[-1])
            try:
                image = Image.open(filename)
                image = image.resize((150, 150))
                photo = ImageTk.PhotoImage(image)
                self.image_preview.config(image=photo)
                self.image_preview.image = photo
            except Exception as e:
                messagebox.showerror("Error", f"Cannot load image: {e}")

    def edit_note(self):
        # Show confirmation popup
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to save this note?")
        if confirm:
            id = self.data['id']
            name = self.entries["Name"].get()
            description = self.entries["Description"].get()
            category = self.entries["Category"].get()
            date = self.entries["Date"].get()
            time = self.entries["Time"].get()
            priority = self.entries["Priority"].get()
            image = self.file_label.cget("text") if self.file_label.cget("text") != "No file chosen" else None
            status = self.data['status']

            if not name or not description or not category or not date or not time or not priority:
                messagebox.showerror("Error", "All fields except attachment are required.")
                return

            # Kết nối cơ sở dữ liệu
            try:
                note_info = {
                    'id': id,
                    'name': name,
                    'description': description,
                    'category': category,
                    'date': date,
                    'time': time,
                    'priority': priority,
                    'image': image,
                    'status': status
                }
                update_note(note_info)
                # Thông báo thành công
                messagebox.showinfo("Success", "Note edited successfully!")

                # Chuyển về màn hình chính
                self.controller.show_frame("MainScreen")
            except Exception as e:
                messagebox.showerror("Database Error", f"An error occurred: {e}")
        else:
            # If the user cancels, do nothing
            return

