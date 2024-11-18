import tkinter as tk
from tkinter import messagebox, ttk
from Backend.controller.main import load_notes, save_note, delete_note, load_notes

# def handle_save_note():
#     title = title_entry.get()
#     content = content_text.get("1.0", tk.END).strip()
#     save_note(title, content)
#     title_entry.delete(0, tk.END)
#     content_text.delete("1.0", tk.END)
#     handle_load_notes()
#     messagebox.showinfo("Success", "Saved")
#
# def handle_load_notes():
#     notes_listbox.delete(0, tk.END)
#     notes = load_notes()
#     for note in notes:
#         notes_listbox.insert(tk.END, f"{note[0]} - {note[1]}")

class AddTodoScreen(tk.Frame):
    def __init__(self, controller):
        super().__init__(controller.root)
        self.controller = controller
        self.configure(bg="#4A90E2")
        self.pack(fill="both", expand=True)

        add_todo_content = tk.Frame(self, bg="white", padx=20, pady=20)
        add_todo_content.place(relx=0.5, rely=0.5, anchor="center", width=450, height=500)

        add_title_label = tk.Label(add_todo_content, text="React To-Do List", font=("Arial", 16, "bold"), bg="white",
                                   fg="#4A90E2")
        add_title_label.pack(pady=10)

        add_subtitle_label = tk.Label(add_todo_content, text="Add a new to-do:", font=("Arial", 12), bg="white",
                                      anchor="w")
        add_subtitle_label.pack(fill="x", pady=(10, 5))

        fields = [
            ("Name:", "name for the task you're going to do"),
            ("Description:", "a short description of the task - can be omitted"),
            ("Category:", "e.g. household, school, work"),
            ("Date:", "dd/mm/yyyy - can be omitted"),
            ("Time:", "hh:mm - can be omitted"),
        ]

        for label, placeholder in fields:
            frame = tk.Frame(add_todo_content, bg="white")
            frame.pack(fill="x", pady=5)

            lbl = tk.Label(frame, text=label, font=("Arial", 10), bg="white", anchor="w")
            lbl.pack(side="left", padx=(0, 10), pady=5)

            entry = tk.Entry(frame, font=("Arial", 10), width=30, fg="gray")
            entry.insert(0, placeholder)

            # Clear placeholder on focus
            def on_focus_in(event, placeholder=placeholder):
                if event.widget.get() == placeholder:
                    event.widget.delete(0, tk.END)
                    event.widget.config(fg="black")

            def on_focus_out(event, placeholder=placeholder):
                if not event.widget.get():
                    event.widget.insert(0, placeholder)
                    event.widget.config(fg="gray")

            entry.bind("<FocusIn>", on_focus_in)
            entry.bind("<FocusOut>", on_focus_out)
            entry.pack(side="left", expand=True)

        # Priority dropdown
        priority_frame = tk.Frame(add_todo_content, bg="white")
        priority_frame.pack(fill="x", pady=10)

        priority_label = tk.Label(priority_frame, text="Priority:", font=("Arial", 10), bg="white", anchor="w")
        priority_label.pack(side="left", padx=(0, 10))

        priority_combo = ttk.Combobox(priority_frame, values=["Low", "Medium", "High"], state="readonly", width=25)
        priority_combo.pack(side="left", fill="x")

        # Fulfillment slider
        fulfillment_frame = tk.Frame(add_todo_content, bg="white")
        fulfillment_frame.pack(fill="x", pady=10)

        fulfillment_label = tk.Label(fulfillment_frame, text="Fulfillment:", font=("Arial", 10), bg="white", anchor="w")
        fulfillment_label.pack(side="left", padx=(0, 10))

        slider = ttk.Scale(fulfillment_frame, from_=0, to=100, orient="horizontal")
        slider.pack(side="left", fill="x", expand=True)

        # Buttons
        button_frame = tk.Frame(add_todo_content, bg="white")
        button_frame.pack(pady=20)

        save_button = tk.Button(button_frame, text="Save", font=("Arial", 12), bg="#4A90E2", fg="white", width=10)
        save_button.pack(side="left", padx=10)

        cancel_button = tk.Button(button_frame, text="Cancel", font=("Arial", 12), bg="gray", fg="white", width=10,
                                  command=lambda: self.controller.show_frame("MainScreen"))
        cancel_button.pack(side="left", padx=10)
