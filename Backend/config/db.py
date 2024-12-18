from tkinter import messagebox
import mysql.connector

cloud_db_config = {
    'host': "sql12.freesqldatabase.com",
    'user': "sql12752868",
    'password': "xd9WGbmFRg",
    'database': "sql12752868",
    'port': 3306
}
# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',
}

# Database connection
def connect_db():
    try:
        mydb = mysql.connector.connect(**db_config)
        create_database(mydb)
        print("Connected to database")
        return mydb
    except mysql.connector.Error as err:
        return None

def create_database(mydb):
    try:
        cursor = mydb.cursor()
        query = """
            CREATE DATABASE IF NOT EXISTS notes_app
        """
        cursor.execute(query)
        cursor.execute("use notes_app")
    except mysql.connector.Error as err:
        return None

def create_table(table_name):
    mydb = connect_db()
    if mydb:
        try:
            cursor = mydb.cursor()
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
            mydb.commit()
        except IOError as err:
            messagebox.showerror("Database Error", f"Error creating table: {err}")
        finally:
            mydb.close()

create_table("notes")