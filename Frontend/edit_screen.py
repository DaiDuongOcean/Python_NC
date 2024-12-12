import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from PIL import Image, ImageTk
from Backend.controller.main import load_notes, save_note, delete_note, load_notes

bg_color = "#4A90E2"

class EditTodoScreen(tk.Frame):
    def __init__(self, controller):
        super().__init__(controller.root)
        self.controller = controller
        self.configure(bg="#2F2F2F")
        self.pack(fill="both", expand=True)

        # Add note form container
        add_todo_content = tk.Frame(self, bg=bg_color,  padx=20, pady=20)
        add_todo_content.place(relx=0.5, rely=0.5, anchor="center", width=400, height=600)

        # Title
        title_label = tk.Label(add_todo_content, text="Edit note", font=("Arial", 16, "bold"), bg=bg_color, fg="white")
        title_label.pack(pady=(0, 15))

        # Fields
        fields = [
            ("Name", None),
            ("Description", None),
            ("Category", ["Cate 1", "Cate 2", "Cate 3"]),
            ("Date", None),
            ("Time", None),
            ("Priority", ["Low", "Medium", "High"]),
        ]

        self.entries = {}
        for field, options in fields:
            frame = tk.Frame(add_todo_content, bg=bg_color)
            frame.pack(fill="x", pady=5)

            label = tk.Label(frame, text=field, font=("Arial", 10), bg=bg_color, fg="white")
            label.pack(side="left", padx=(0, 10))

            if options is None:
                # Text Entry
                entry = tk.Entry(frame, font=("Arial", 10), bg="#1E1E1E", fg="white", insertbackground="white")
                entry.pack(side="left", fill="x", expand=True)
                self.entries[field] = entry
            else:
                # Dropdown (Combobox)
                combo = ttk.Combobox(frame, values=options, state="readonly", font=("Arial", 10))
                combo.pack(side="left", fill="x", expand=True)
                self.entries[field] = combo

        # File Chooser
        file_frame = tk.Frame(add_todo_content, bg=bg_color)
        file_frame.pack(fill="x", pady=(10, 15))

        file_button = tk.Button(file_frame, text="Choose File", bg="#4A90E2", fg="white", font=("Arial", 10), command=self.choose_file)
        file_button.pack(side="left", padx=(0, 10))

        self.file_label = tk.Label(file_frame, text="No file chosen", font=("Arial", 10), bg=bg_color, fg="white")
        self.file_label.pack(side="left", fill="x", expand=True)

        # Image Preview
        self.image_preview = tk.Label(self, bg=bg_color)
        self.image_preview.place(relx=0.5, rely=0.85, anchor="center")

        # Buttons
        button_frame = tk.Frame(add_todo_content, bg=bg_color)
        button_frame.pack(pady=10)

        edit_button = tk.Button(button_frame, text="Add", font=("Arial", 12), bg="green", fg="white", width=10, command=self.edit_note)
        edit_button.pack(side="left", padx=10)

        cancel_button = tk.Button(button_frame, text="Cancel", font=("Arial", 12), bg="gray", fg="white", width=10, command=lambda: self.controller.show_frame("MainScreen"))
        cancel_button.pack(side="left", padx=10)

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
        note_data = {field: entry.get() for field, entry in self.entries.items()}
        note_data['File'] = self.file_label.cget("text")
        print("Note added:", note_data)
        messagebox.showinfo("Success", "Note added successfully!")
        self.controller.show_frame("MainScreen")