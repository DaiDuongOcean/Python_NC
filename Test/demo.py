import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
from pymongo import MongoClient
from PIL import Image, ImageTk
import datetime
import threading
import time
import os
from bson.objectid import ObjectId

# Kết nối MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["note_app"]
notes_collection = db["notes"]

# Biến toàn cục để lưu đường dẫn ảnh
image_path = None


# Hàm chọn ảnh
def attach_image():
    global image_path
    image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg")])
    if image_path:
        messagebox.showinfo("Thông báo", "Đã đính kèm hình ảnh.")


# Hàm tạo ghi chú mới với đính kèm hình ảnh và thời gian nhắc nhở
def create_note():
    global image_path
    title = title_entry.get()
    content = content_text.get("1.0", tk.END).strip()
    category = category_var.get()
    priority = priority_var.get()
    reminder_time = reminder_entry.get()

    if title and content:
        note = {
            "title": title,
            "content": content,
            "category": category,
            "priority": priority,
            "date_created": datetime.datetime.now(),
            "image_path": image_path,
            "reminder_time": reminder_time
        }
        notes_collection.insert_one(note)
        messagebox.showinfo("Thông báo", "Ghi chú đã được tạo thành công!")

        # Khởi động lời nhắc nếu có thời gian nhắc nhở
        if reminder_time:
            threading.Thread(target=set_reminder, args=(title, content, image_path, reminder_time)).start()

        clear_fields()
        load_notes()
    else:
        messagebox.showwarning("Cảnh báo", "Vui lòng nhập tiêu đề và nội dung.")


# Hàm xóa ghi chú
def delete_note():
    selected_item = notes_list.selection()
    if not selected_item:
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn ghi chú cần xóa.")
        return

    note_id = notes_list.item(selected_item, "values")[0]
    notes_collection.delete_one({"_id": ObjectId(note_id)})
    messagebox.showinfo("Thông báo", "Ghi chú đã được xóa.")
    load_notes()


# Hàm thiết lập lời nhắc nhở
def set_reminder(title, content, image_path, reminder_time):
    try:
        reminder_datetime = datetime.datetime.strptime(reminder_time, "%Y-%m-%d %H:%M")
        while datetime.datetime.now() < reminder_datetime:
            time.sleep(10)

        # Hiển thị thông báo với nội dung và hình ảnh
        reminder_popup = tk.Toplevel(app)
        reminder_popup.title("Lời nhắc")

        tk.Label(reminder_popup, text=title, font=("Arial", 16, "bold")).pack(pady=5)
        tk.Label(reminder_popup, text=content, wraplength=300).pack(pady=5)

        if image_path and os.path.exists(image_path):
            image = Image.open(image_path)
            image.thumbnail((200, 200))
            img_display = ImageTk.PhotoImage(image)
            img_label = tk.Label(reminder_popup, image=img_display)
            img_label.image = img_display  # Giữ tham chiếu để hiển thị ảnh
            img_label.pack(pady=10)

        tk.Button(reminder_popup, text="Đóng", command=reminder_popup.destroy).pack(pady=10)
    except ValueError:
        messagebox.showerror("Lỗi", "Định dạng thời gian nhắc nhở không hợp lệ (Đúng: YYYY-MM-DD HH:MM)")


# Hàm tải và hiển thị danh sách ghi chú
def load_notes():
    notes = notes_collection.find()
    update_notes_list(notes)


# Hàm cập nhật danh sách ghi chú trong Treeview
def update_notes_list(notes):
    notes_list.delete(*notes_list.get_children())
    for note in notes:
        notes_list.insert("", "end", values=(
            note["_id"], note["title"], note["category"], note["priority"], note["date_created"].strftime("%Y-%m-%d"),
            note.get("reminder_time", "")))


# Hàm xóa các trường nhập
def clear_fields():
    global image_path
    title_entry.delete(0, tk.END)
    content_text.delete("1.0", tk.END)
    category_var.set("")
    priority_var.set("")
    reminder_entry.delete(0, tk.END)
    image_path = None


# Hàm cập nhật các trường khi chọn một ghi chú trong Treeview
def on_note_select(event):
    selected_item = notes_list.selection()
    if selected_item:
        note_id = notes_list.item(selected_item, "values")[0]
        note = notes_collection.find_one({"_id": ObjectId(note_id)})

        # Cập nhật các trường nhập liệu
        title_entry.delete(0, tk.END)
        title_entry.insert(0, note["title"])

        content_text.delete("1.0", tk.END)
        content_text.insert("1.0", note["content"])

        category_var.set(note["category"])
        priority_var.set(note["priority"])
        reminder_entry.delete(0, tk.END)
        reminder_entry.insert(0, note["reminder_time"])

        # Lưu lại đường dẫn ảnh để có thể sử dụng khi cần thiết
        global image_path
        image_path = note.get("image_path", None)


# Tạo giao diện Tkinter
app = tk.Tk()
app.title("Ứng dụng Ghi Chú Cá Nhân")
app.geometry("950x700")

# Tiêu đề ghi chú
tk.Label(app, text="Tiêu đề:").grid(row=0, column=0, padx=10, pady=5)
title_entry = tk.Entry(app, width=50)
title_entry.grid(row=0, column=1, columnspan=3, padx=10, pady=5)

# Nội dung ghi chú
tk.Label(app, text="Nội dung:").grid(row=1, column=0, padx=10, pady=5, sticky="N")
content_text = tk.Text(app, height=10, width=50)
content_text.grid(row=1, column=1, columnspan=3, padx=10, pady=5)

# Phân loại ghi chú
tk.Label(app, text="Chủ đề:").grid(row=2, column=0, padx=10, pady=5)
category_var = tk.StringVar()
category_entry = ttk.Combobox(app, textvariable=category_var, values=["Công việc", "Cá nhân", "Học tập"])
category_entry.grid(row=2, column=1, padx=10, pady=5)

# Mức độ ưu tiên
tk.Label(app, text="Mức độ ưu tiên:").grid(row=2, column=2, padx=10, pady=5)
priority_var = tk.StringVar()
priority_entry = ttk.Combobox(app, textvariable=priority_var, values=["Cao", "Trung bình", "Thấp"])
priority_entry.grid(row=2, column=3, padx=10, pady=5)

# Đính kèm ảnh
tk.Button(app, text="Đính kèm hình ảnh", command=attach_image).grid(row=3, column=1, padx=10, pady=5)

# Thời gian nhắc nhở
tk.Label(app, text="Thời gian nhắc nhở (YYYY-MM-DD HH:MM):").grid(row=4, column=0, padx=10, pady=5)
reminder_entry = tk.Entry(app, width=30)
reminder_entry.grid(row=4, column=1, padx=10, pady=5)

# Nút chức năng
tk.Button(app, text="Tạo Ghi Chú", command=create_note).grid(row=5, column=1, padx=10, pady=10)
tk.Button(app, text="Xóa Ghi Chú", command=delete_note).grid(row=5, column=2, padx=10, pady=10)

# Hiển thị danh sách ghi chú
columns = ("_id", "title", "category", "priority", "date_created", "reminder_time")
notes_list = ttk.Treeview(app, columns=columns, show="headings")
for col in columns:
    notes_list.heading(col, text=col)
    notes_list.column(col, width=120)
notes_list.grid(row=6, column=0, columnspan=4, padx=10, pady=10)

# Thêm sự kiện khi chọn một ghi chú trong Treeview
notes_list.bind("<<TreeviewSelect>>", on_note_select)

# Tải ghi chú khi khởi động
load_notes()

app.mainloop()
