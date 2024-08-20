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
        self.is_resizing = False
        self.drag_data = {"x": 0, "y": 0, "item": None}

        # 设置窗口透明度并移除装饰
        self.root.attributes("-alpha", 0.3)
        self.root.overrideredirect(True)

        # 绑定鼠标事件
        self.root.bind("<Button-1>", self.on_button_press)
        self.root.bind("<B1-Motion>", self.on_mouse_drag)
        self.root.bind("<ButtonRelease-1>", self.on_button_release)

    def on_button_press(self, event):
        # 判断是否点击在已有的矩形内，如果是，则进入调整模式
        if self.rect and self.canvas.coords(self.rect):
            x1, y1, x2, y2 = self.canvas.coords(self.rect)
            if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                self.is_resizing = True
                self.drag_data["item"] = self.rect
                self.drag_data["x"] = event.x
                self.drag_data["y"] = event.y
                return

        # 开始新的矩形选区
        self.start_x = event.x
        self.start_y = event.y
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="red", width=2)
        self.is_resizing = False

    def on_mouse_drag(self, event):
        if self.is_resizing and self.rect:
            # 调整已有的矩形选区
            x1, y1, x2, y2 = self.canvas.coords(self.rect)
            self.canvas.coords(self.rect, min(event.x, x2), min(event.y, y2), max(event.x, x2), max(event.y, y2))
        else:
            # 更新选区大小
            cur_x = event.x
            cur_y = event.y
            self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)

    def on_button_release(self, event):
        cur_x = event.x
        cur_y = event.y
        self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)
        # 松开鼠标后截屏
        if not self.is_resizing and self.start_x and self.start_y:
            self.capture_screen()

    def capture_screen(self):
        x1, y1, x2, y2 = self.canvas.coords(self.rect)

        # 确保宽度和高度大于0
        if x2 == x1:
            x2 += 1
        if y2 == y1:
            y2 += 1

        # 将画布坐标转换为屏幕坐标
        x1 = int(self.root.winfo_rootx() + x1)
        y1 = int(self.root.winfo_rooty() + y1)
        x2 = int(self.root.winfo_rootx() + x2)
        y2 = int(self.root.winfo_rooty() + y2)

        # 保持当前窗口可见并截取窗口区域
        self.root.attributes("-alpha", 0)  # 将窗口设为完全透明
        img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        img.save('screenshot.png')
        print("截图已保存。")

        # 恢复窗口透明度并退出程序
        self.root.attributes("-alpha", 1)
        self.root.quit()

def screenshot():
    root = tk.Tk()
    root.title("选择截图区域")
    root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")
    ScreenshotTool(root)
    root.mainloop()

# 运行截图工具
screenshot()
