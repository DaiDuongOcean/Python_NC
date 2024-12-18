from ..config.db import connect_db
from tkinter import messagebox

def save_note(title, content):
    if not title or not content:
        messagebox.showwarning("Input Error", "Title and content cannot be empty.")
        return

    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO notes (title, content) VALUES (%s, %s)", (title, content))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Note saved successfully!")

# Load notes into the listbox
def load_notes():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, description, category, date, time, priority, image, status FROM notes")
        notes = cursor.fetchall()
        conn.close()
        return notes
    else:
        return []

# Delete selected note
def delete_note(note_id):
    if not note_id:
        return

    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM notes WHERE id = %s", (note_id,))
        conn.commit()
        conn.close()
