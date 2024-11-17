import tkinter as tk
from tkinter import messagebox
from Backend.controller.main import load_notes, save_note, delete_note, load_notes

root = tk.Tk()
root.title("Note Application")

def handle_save_note():
    title = title_entry.get()
    content = content_text.get("1.0", tk.END).strip()
    save_note(title, content)
    title_entry.delete(0, tk.END)
    content_text.delete("1.0", tk.END)
    handle_load_notes()
    messagebox.showinfo("Success", "Saved")

def handle_load_notes():
    notes_listbox.delete(0, tk.END)
    notes = load_notes()
    for note in notes:
        notes_listbox.insert(tk.END, f"{note[0]} - {note[1]}")

# Widgets
tk.Label(root, text="Title").grid(row=0, column=0, padx=10, pady=5)
title_entry = tk.Entry(root, width=40)
title_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Content").grid(row=1, column=0, padx=10, pady=5, sticky=tk.N)
content_text = tk.Text(root, width=40, height=10)
content_text.grid(row=1, column=1, padx=10, pady=5)

tk.Button(root, text="Save Note", command=handle_save_note).grid(row=2, column=0, padx=10, pady=5)
tk.Button(root, text="Delete Note", command=delete_note).grid(row=2, column=1, padx=10, pady=5, sticky=tk.E)

tk.Label(root, text="Notes List").grid(row=3, column=0, padx=10, pady=5)
notes_listbox = tk.Listbox(root, width=40, height=10)
notes_listbox.grid(row=3, column=1, padx=10, pady=5)

# Load notes on startup
handle_load_notes()

# Run the app
root.mainloop()