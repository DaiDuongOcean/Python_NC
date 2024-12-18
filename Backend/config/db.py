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
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {table_name} (
                    id int auto_increment primary key,
                    name nvarchar(100) NOT NULL,
                    description nvarchar(100),
                    category nvarchar(100),
                    date nvarchar(100),
                    time nvarchar(100),
                    priority varchar(100),
                    image varchar(100),
                    status varchar(100)
                )
            """)
            conn.commit()
        except IOError as err:
            messagebox.showerror("Database Error", f"Error creating table: {err}")
        finally:
            conn.close()

create_table("notes")