import tkinter as tk
from tkinter import Canvas
from PIL import ImageGrab


class ScreenshotTool:
    def __init__(self, root):
        self.root = root
        self.canvas = Canvas(root, cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.start_x = None
        self.start_y = None
        self.rect = None
        # 设置为全屏
        self.root.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}+0+0")
        self.root.bind("<Button-1>", self.on_button_press)
        self.root.bind("<B1-Motion>", self.on_mouse_drag)
        self.root.bind("<ButtonRelease-1>", self.on_button_release)
        self.root.attributes("-fullscreen", True)  # 设置窗口全屏

    def on_button_press(self, event):
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="red",
                                                 width=2)

    def on_mouse_drag(self, event):
        cur_x = self.canvas.canvasx(event.x)
        cur_y = self.canvas.canvasy(event.y)
        self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)

    def on_button_release(self, event):
        end_x = self.canvas.canvasx(event.x)
        end_y = self.canvas.canvasy(event.y)
        if self.start_x and self.start_y:
            self.capture_screen(self.start_x, self.start_y, end_x, end_y)

    def capture_screen(self, left, top, right, bottom):
        # 截取当前窗口的选定区域
        x1 = int(self.root.winfo_rootx() + left)
        y1 = int(self.root.winfo_rooty() + top)
        x2 = int(self.root.winfo_rootx() + right)
        y2 = int(self.root.winfo_rooty() + bottom)
        self.root.withdraw()  # 隐藏窗口以避免捕获
        ImageGrab.grab(bbox=(x1, y1, x2, y2)).save('screenshot.png')
        print("Screenshot saved.")
        self.root.quit()


def screenshot():
    root = tk.Tk()
    root.title("Select Screenshot Area")
    root.overrideredirect(True)  # 移除窗口装饰
    ScreenshotTool(root)
    root.mainloop()


# 运行截图工具
screenshot()