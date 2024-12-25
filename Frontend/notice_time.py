import os
from Backend.controller.main import load_notes
from threading import Thread
import tkinter as tk
from tkinter import Label, Button
from PIL import Image, ImageTk
from datetime import datetime
from Frontend.add_screen import imgs_folder
from Frontend.util import is_image_file_in_folder, convert_from_list_to_dict
from pygame import mixer  # Thư viện để phát âm thanh
import time

# Màu nền giao diện
bg_color = "#4A90E2"

# Hàm kiểm tra thời gian hiện tại có khớp với thời gian được chỉ định không
def is_current_datetime_matching(date_str, time_str):
    target_date = datetime.strptime(date_str, "%m/%d/%y")
    target_time = datetime.strptime(time_str, "%H:%M")
    now = datetime.now()
    return now.date() == target_date.date() and now.time().hour == target_time.time().hour and now.time().minute == target_time.time().minute

# Hàm kiểm tra và thông báo khi đến giờ chỉ định
def notify_when_time_matches():
    def check_time():
        while True:
            notes = load_notes()
            for note in notes:
                dict_note = convert_from_list_to_dict(note)
                note_date = dict_note['date']
                note_time = dict_note['time']
                match_time = is_current_datetime_matching(note_date, note_time)
                if match_time:
                    create_note_box(dict_note)
            time.sleep(60)  # Giảm tải CPU bằng cách kiểm tra mỗi phút

    # Chạy kiểm tra thời gian trong một luồng riêng
    Thread(target=check_time, daemon=True).start()

# Hàm tạo giao diện thông báo
def create_note_box(note):
    def close_window():
        window.destroy()
        mixer.music.stop()  # Dừng phát nhạc khi đóng cửa sổ

    # Khởi tạo âm thanh
    try:
        mixer.init()
        audio_file_path = "jingle-bells-278637.mp3"  # Đường dẫn đến file nhạc Giáng sinh
        mixer.music.load(audio_file_path)
        mixer.music.play(-1)  # Phát nhạc lặp vô hạn
    except Exception as e:
        print(f"Lỗi phát âm thanh: {e}")

    # Tạo cửa sổ giao diện
    window = tk.Tk()
    window.title("Note Information")
    window.geometry("400x500")  # Kích thước cửa sổ
    window.resizable(False, False)
    window.configure(bg=bg_color)

    # Hiển thị tên ghi chú
    Label(window, bg=bg_color, fg="white", text="Name:", font=("Arial", 12, "bold")).pack(anchor="w", padx=10, pady=(10, 0))
    Label(window, bg=bg_color, fg="white", text=note["name"], font=("Arial", 12)).pack(anchor="w", padx=20)

    # Hiển thị mô tả
    Label(window, bg=bg_color, fg="white", text="Description:", font=("Arial", 12, "bold")).pack(anchor="w", padx=10, pady=(10, 0))
    Label(window, bg=bg_color, fg="white", text=note["description"], font=("Arial", 12), wraplength=350, justify="left").pack(anchor="w", padx=20)

    # Hiển thị danh mục
    Label(window, bg=bg_color, fg="white", text="Category:", font=("Arial", 12, "bold")).pack(anchor="w", padx=10, pady=(10, 0))
    Label(window, bg=bg_color, fg="white", text=note["category"], font=("Arial", 12)).pack(anchor="w", padx=20)

    # Hiển thị mức độ ưu tiên
    Label(window, bg=bg_color, fg="white", text="Priority:", font=("Arial", 12, "bold")).pack(anchor="w", padx=10, pady=(10, 0))
    Label(window, bg=bg_color, fg="white", text=note["priority"], font=("Arial", 12)).pack(anchor="w", padx=20)

    # Hiển thị hình ảnh
    Label(window, bg=bg_color, fg="white", text="Image:", font=("Arial", 12, "bold")).pack(anchor="w", padx=10, pady=(10, 0))
    img_preview = tk.Label(window, bg=bg_color)

    try:
        available_img = is_image_file_in_folder(imgs_folder, note['image'])
        if available_img:
            input_path = os.path.join(imgs_folder, note['image'])
            img = Image.open(input_path)
            img = img.resize((150, 150))  # Resize ảnh để phù hợp với giao diện
            tk_image = ImageTk.PhotoImage(master=window, image=img)
            img_preview.config(image=tk_image)
            img_preview.image = tk_image
            img_preview.pack(pady=5)
    except Exception as e:
        print(e)
        Label(window, text="Image not found or invalid.", font=("Arial", 12, "italic"), fg="red").pack(pady=10)

    # Nút đóng cửa sổ
    Button(window, text="Close", command=close_window, bg="red", fg="white", font=("Arial", 12)).pack(pady=20)

    # Bắt đầu vòng lặp giao diện
    window.mainloop()

# Hàm khởi chạy thông báo
def notice_time():
    notify_when_time_matches()
