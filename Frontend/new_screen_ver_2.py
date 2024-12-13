import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests
from io import BytesIO

# Hàm xử lý khi nhấn nút "Thao tác"
def thao_tac(id):
    print(f"Thao tác với ID: {id}")

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Bảng Dữ Liệu với Nút Thao Tác")

# Tạo Treeview
columns = ("id", "link", "name", "thao_tac")
tree = ttk.Treeview(root, columns=columns, show="headings", height=10)

# Cấu hình cột
tree.heading("id", text="ID")
tree.heading("link", text="Link Ảnh")
tree.heading("name", text="Tên Ảnh")
tree.heading("thao_tac", text="Thao tác")

tree.column("id", width=50, anchor="center")
tree.column("link", width=200)
tree.column("name", width=150)
tree.column("thao_tac", width=150, anchor="center")

tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

# Hàm để tải và hiển thị ảnh từ URL
def load_image(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    img = img.resize((50, 50))  # Thay đổi kích thước ảnh cho phù hợp
    return ImageTk.PhotoImage(img)

# Thêm dữ liệu mẫu
data = [
    (1, "https://photo-resize-zmp3.zadn.vn/w600_r1x1_jpeg/cover/5/d/a/7/5da7072eaf8a8cf3350ee91fb2544221.jpg", "Ảnh 1"),
    (2, "https://photo-resize-zmp3.zadn.vn/w600_r1x1_jpeg/cover/5/d/a/7/5da7072eaf8a8cf3350ee91fb2544221.jpg", "Ảnh 2"),
    (3, "https://photo-resize-zmp3.zadn.vn/w600_r1x1_jpeg/cover/5/d/a/7/5da7072eaf8a8cf3350ee91fb2544221.jpg", "Ảnh 3"),
]

# Hàm tạo nút "Thao tác" cho từng hàng và hiển thị ảnh
def add_thao_tac_button(item, id, url):
    # Tạo Frame cho mỗi hàng để chứa nút và ảnh
    frame = tk.Frame(root)
    thao_tac_btn = tk.Button(frame, text="Thao tác", command=lambda: thao_tac(id), width=10)
    thao_tac_btn.pack(padx=5, pady=5)

    # Hiển thị ảnh trong cột "Link"
    img = load_image(url)
    label = tk.Label(frame, image=img)
    label.image = img  # Giữ tham chiếu đến ảnh để tránh bị xóa
    label.pack(side="left")

    # Gắn nút và ảnh vào cột "Thao tác"
    tree.set(item, "thao_tac", "")
    tree.item(item, tags=(id,))
    frame.pack(side="left")

# Thêm dữ liệu vào bảng và nút "Thao tác" cho mỗi hàng
for row in data:
    item = tree.insert("", "end", values=row[:3])
    add_thao_tac_button(item, row[0], row[1])

root.mainloop()
