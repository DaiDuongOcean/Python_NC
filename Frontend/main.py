import tkinter as tk
from controller import Controller

def main():
    root = tk.Tk()
    root.title("To-Do List")
    root.geometry("900x550")
    root.configure(bg="#4A90E2")

    app = Controller(root)  # Pass the root window to the controller
    root.mainloop()

if __name__ == "__main__":
    main()
