from tkinter import messagebox
import mysql.connector

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',
    'database': 'notes_app'
}

# Database connection
def connect_db():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return None

def create_table(table_name):
    print("here")
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {table_name} (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    content TEXT NOT NULL
                )
            """)
            conn.commit()
        except IOError as err:
            messagebox.showerror("Database Error", f"Error creating table: {err}")
        finally:
            conn.close()

create_table("notes")