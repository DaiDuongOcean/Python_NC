from ..config.db import connect_db
from tkinter import messagebox

def save_note(title, content):
    if not title or not content:
        return
    mydb = connect_db()
    if mydb:
        cursor = mydb.cursor()
        cursor.execute("INSERT INTO notes (title, content) VALUES (%s, %s)", (title, content))
        mydb.commit()
        mydb.close()
        messagebox.showinfo("Success", "Note saved successfully!")

def load_notes(filter_val = None, search_val = ""):
    mydb = connect_db()
    if mydb:
        cursor = mydb.cursor()
        condition_str = ""
        if filter_val != None:
            items = list(filter_val.items())
            for item_index in range(len(items)):
                item = items[item_index]
                key = item[0]
                value = item[1]
                if value != "All":
                    if len(condition_str) > 0:
                        condition_str += "and"
                    condition_str += f" {key} = '{value}' "
        if len(search_val.strip()) > 0:
            if len(condition_str) > 0:
                condition_str += " and "
            condition_str +=  f"name LIKE \'%{search_val.strip()}%\'"
        if len(condition_str) > 0:
           query = f"""
                SELECT * 
                FROM notes
                WHERE {condition_str}
            """
        else:
            query = "SELECT * FROM notes"
        cursor.execute(query)
        notes = cursor.fetchall()
        mydb.close()
        return notes
    else:
        return []

def get_note_info(note):
    id = ""
    if 'id' in note:
        id = note['id']
    name = note['name']
    des = note['description']
    category = note['category']
    date = note['date']
    time = note['time']
    priority = note['priority']
    image = note['image']
    status = note['status']
    return id, name, des, category, date, time, priority, image, status

def add_note(note):
    id, name, des, category, date, time, priority, image, status = get_note_info(note)
    mydb = connect_db()
    if mydb:
        cursor = mydb.cursor()
        query = """
                INSERT INTO notes (name, description, category, date, time, priority, image, status) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (name, des, category, date, time, priority, image, status))
        mydb.commit()
        mydb.close()

def update_note(note):
    id, name, des, category, date, time, priority, image, status = get_note_info(note)
    mydb = connect_db()
    if mydb:
        cursor = mydb.cursor()
        query = """
                UPDATE notes
                SET name=%s, description=%s, category=%s, date=%s, time=%s, priority=%s, image=%s, status=%s
                WHERE id=%s
        """
        cursor.execute(query, (name, des, category, date, time, priority, image, status, id))
        mydb.commit()
        mydb.close()

def delete_note(note_id):
    if not note_id:
        return
    mydb = connect_db()
    if mydb:
        cursor = mydb.cursor()
        cursor.execute("DELETE FROM notes WHERE id = %s", (note_id,))
        mydb.commit()
        mydb.close()


def get_note(id):
    if not id:
        return
    mydb = connect_db()
    if mydb:
        cursor = mydb.cursor()
        cursor.execute(f"SELECT * FROM notes WHERE id = {id}")
        note = cursor.fetchone()
        return note