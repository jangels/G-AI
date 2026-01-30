import tkinter as tk
from tkinter import messagebox
import random
import os
from PIL import Image, ImageTk
import time
from datetime import datetime as dt

# 动态获取用户目录
user_home = os.path.expanduser("~")


class ImageSelectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("好友想念器")
        self.root.attributes("-alpha", 0.9)  # 设置窗口半透明
        self.root.attributes("-topmost", True)  # 窗口置顶

        # 获取屏幕尺寸并计算右上角位置
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window_width = 800  # 窗口宽度
        window_height = 300  # 窗口高度
        x = screen_width - window_width - 20  # 右边距20像素
        y = 150  # 上边距50像素
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # 人名和对应图片路径
        self.people = {
            "李传鸡": os.path.join(user_home, "Downloads/dingge/li.jpg"),
            "牛哥": os.path.join(user_home, "Downloads/dingge/niu.jpg"),
            "丁哥": os.path.join(user_home, "Downloads/dingge/dingge.jpg"),
            "阿四": os.path.join(user_home, "Downloads/dingge/qiao.jpg"),
            "小波钱": os.path.join(user_home, "Downloads/dingge/xiao.jpg"),
        }

        # 加载并调整图片大小
        self.images = []
        self.names = list(self.people.keys())
        for name in self.names:
            try:
                img = Image.open(self.people[name])
                img = img.resize((145, 145), Image.LANCZOS)
                self.images.append(ImageTk.PhotoImage(img))
            except Exception as e:
                print(f"加载图片失败: {e}")
                blank_img = Image.new("RGB", (120, 120), color="gray")
                self.images.append(ImageTk.PhotoImage(blank_img))

        # 创建UI元素
        self.create_widgets()

    def create_widgets(self):
        # 主容器
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # 图片和名字显示区域
        self.image_labels = []
        self.name_labels = []

        for i in range(5):
            # 图片容器
            person_frame = tk.Frame(main_frame, bg="#f0f0f0")
            person_frame.grid(row=0, column=i, padx=5, pady=5)

            # 图片标签
            label = tk.Label(person_frame, image=self.images[i], bg="#f0f0f0")
            label.pack()
            self.image_labels.append(label)

            # 名字标签
            name_label = tk.Label(
                person_frame, text=self.names[i], font=("Helvetica", 11), bg="#f0f0f0"
            )
            name_label.pack()
            self.name_labels.append(name_label)

        # 开始选择按钮
        self.select_btn = tk.Button(
            main_frame,
            text="开始随机想念",
            command=self.animate_selection,
            font=("Helvetica", 12),
            bg="#4CAF50",
            fg="black",
            activebackground="#45a049",
        )
        self.select_btn.grid(row=1, column=0, columnspan=5, pady=15)

    def animate_selection(self):
        self.select_btn.config(state=tk.DISABLED)

        # 动画效果：随机高亮图片
        for _ in range(15):
            idx = random.randint(0, 4)
            self.highlight_person(idx)
            self.root.update()
            time.sleep(0.1)

        # 最终选择
        selected_idx = random.randint(0, 4)
        self.highlight_person(selected_idx, permanent=True)

        # 计算随机天数（从2015年至今）
        day = random.randint(3000, (dt.now() - dt(2015, 1, 1)).days)

        # 显示macOS通知
        self.show_macos_notification(self.names[selected_idx], day)

        self.select_btn.config(state=tk.NORMAL)

    def highlight_person(self, idx, permanent=False):
        # 重置所有高亮
        for label in self.image_labels:
            label.config(borderwidth=0, highlightthickness=0)
        for label in self.name_labels:
            label.config(fg="black")

        # 高亮选中的图片和名字
        if permanent:
            # 设置红色边框（重点修改处）
            self.image_labels[idx].config(
                borderwidth=4,
                relief="solid",
                highlightbackground="red",  # 边框颜色
                highlightthickness=4,  # 边框粗细
                highlightcolor="red",  # 边框颜色（活动状态）
            )

            self.name_labels[idx].config(fg="red", font=("Helvetica", 16, "bold"))
        else:
            self.image_labels[idx].config(
                borderwidth=3, relief="solid", highlightbackground="#f44336"
            )
            self.name_labels[idx].config(fg="#f44336")

    def show_macos_notification(self, name, day):
        # 获取对应头像路径
        avatar_path = self.people[name]
        os.system(
            f'osascript -e \'display notification "想念{name}的第{day}天" with title "每日想念" sound name "Glass"\''
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageSelectorApp(root)
    root.mainloop()