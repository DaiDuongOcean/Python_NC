import os
from Backend.controller.main import load_notes
from threading import Thread
import tkinter as tk
from tkinter import messagebox
import time
from tkinter import Label, Button
from PIL import Image, ImageTk  # For handling images
from datetime import datetime
from Frontend.add_screen import imgs_folder
from Frontend.util import is_image_file_in_folder, convert_from_list_to_dict

bg_color = "#4A90E2"

def is_current_datetime_matching(date_str, time_str):
    # Parse the input strings
    target_date = datetime.strptime(date_str, "%m/%d/%y")
    target_time = datetime.strptime(time_str, "%H:%M")
    now = datetime.now()
    return now.date() == target_date.date() and now.time().hour == target_time.time().hour and now.time().minute == target_time.time().minute

def notify_when_time_matches(notes):
    def check_time():
        while True:
            for note in notes:
                dict_note = convert_from_list_to_dict(note)
                note_date = dict_note['date']
                note_time = dict_note['time']
                match_time = is_current_datetime_matching(note_date, note_time)
                if match_time:
                    create_note_box(dict_note)
            time.sleep(60)  # Check every minute to reduce CPU usage

    # Run the time-checking logic in a separate thread
    Thread(target=check_time, daemon=True).start()

def create_note_box(note):
    def close_window():
        window.destroy()

    # Create the tkinter window
    window = tk.Tk()
    window.title("Note Information")
    window.geometry("400x500")  # Adjust window size
    window.resizable(False, False)
    window.configure(bg=bg_color)

    # Display the note's name
    Label(window, bg=bg_color, fg="white", text="Name:", font=("Arial", 12, "bold")).pack(anchor="w", padx=10, pady=(10, 0))
    Label(window, bg=bg_color, fg="white", text=note["name"], font=("Arial", 12)).pack(anchor="w", padx=20)

    # Display the note's description
    Label(window, bg=bg_color, fg="white", text="Description:", font=("Arial", 12, "bold")).pack(anchor="w", padx=10, pady=(10, 0))
    Label(window, bg=bg_color, fg="white", text=note["description"], font=("Arial", 12), wraplength=350, justify="left").pack(anchor="w", padx=20)

    # Display the note's category
    Label(window, bg=bg_color, fg="white", text="Category:", font=("Arial", 12, "bold")).pack(anchor="w", padx=10, pady=(10, 0))
    Label(window, bg=bg_color, fg="white", text=note["category"], font=("Arial", 12)).pack(anchor="w", padx=20)

    # Display the note's priority
    Label(window, bg=bg_color, fg="white", text="Priority:", font=("Arial", 12, "bold")).pack(anchor="w", padx=10, pady=(10, 0))
    Label(window, bg=bg_color, fg="white", text=note["priority"], font=("Arial", 12)).pack(anchor="w", padx=20)

    # Display the note's image
    Label(window, bg=bg_color, fg="white", text="Image:", font=("Arial", 12, "bold")).pack(anchor="w", padx=10, pady=(10, 0))
    img_preview = tk.Label(window, bg=bg_color)

    try:
        available_img = is_image_file_in_folder(imgs_folder, note['image'])
        if available_img:
            input_path = os.path.join(imgs_folder, note['image'])
            print("input_path: ", input_path)
            img = Image.open(input_path)
            img = img.resize((150, 150))  # Resize the image to fit in the box
            # Convert the image to a format Tkinter can use
            tk_image = ImageTk.PhotoImage(master=window, image=img)
            img_preview.config(image=tk_image)
            img_preview.image = tk_image
            img_preview.pack(pady=5)
    except Exception as e:
        print(e)
        Label(window, text="Image not found or invalid.", font=("Arial", 12, "italic"), fg="red").pack(pady=10)

    # Close button
    Button(window, text="Close", command=close_window, bg="red", fg="white", font=("Arial", 12)).pack(pady=20)

    # Start the tkinter main loop
    window.mainloop()

def notice_time():
    notes = load_notes()
    notify_when_time_matches(notes)