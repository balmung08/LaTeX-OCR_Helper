import time
import matplotlib
import optimize
from pix2tex import cli
import cv2
from ultralytics import YOLO
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog
import tkinter.messagebox
from PIL import Image,ImageTk,ImageGrab
import webbrowser
import threading
import ctypes
from time import sleep
import tkinter
import ctypes
import os
import matplotlib
matplotlib.use('TkAgg')
from matplotlib import mathtext
global prc_state,single_doing,multi_doing,error,rt_solve


prc_state = False
single_doing = False
multi_doing = False
update = False
error = False
rt_solve = False
def init():
    try:
        os.remove("result.png")
    except FileNotFoundError as e:
        print(e)
    try:
        os.remove("result.txt")
    except FileNotFoundError as e:
        print(e)
    try:
        os.remove("crop.jpg")
    except FileNotFoundError as e:
        print(e)
    try:
        os.remove("tmp.png")
    except FileNotFoundError as e:
        print(e)
    try:
        os.remove("prtsc.jpg")
    except FileNotFoundError as e:
        print(e)
class CTkPrScrn():
    def __init__(self):
        self.__start_x, self.__start_y = 0, 0
        self.__scale = 1

        self.__win = tkinter.Tk()
        self.__win.attributes("-alpha", 0.1)  # 设置窗口半透明
        self.__win.attributes("-fullscreen", True)  # 设置全屏
        self.__win.attributes("-topmost", True)  # 设置窗口在最上层

        self.__width, self.__height = self.__win.winfo_screenwidth(), self.__win.winfo_screenheight()

        # 创建画布
        self.__canvas = tkinter.Canvas(self.__win, width=self.__width, height=self.__height, bg="gray")

        self.__win.bind('<Button-1>', self.xFunc1)  # 绑定鼠标左键点击事件
        self.__win.bind('<ButtonRelease-1>', self.xFunc1)  # 绑定鼠标左键点击释放事件
        self.__win.bind('<B1-Motion>', self.xFunc2)  # 绑定鼠标左键点击移动事件
        self.__win.bind('<Escape>', lambda e: self.__win.destroy())  # 绑定Esc按键退出事件

        user32 = ctypes.windll.user32
        gdi32 = ctypes.windll.gdi32
        dc = user32.GetDC(None)
        widthScale = gdi32.GetDeviceCaps(dc, 8)  # 分辨率缩放后的宽度
        heightScale = gdi32.GetDeviceCaps(dc, 10)  # 分辨率缩放后的高度
        width = gdi32.GetDeviceCaps(dc, 118)  # 原始分辨率的宽度
        height = gdi32.GetDeviceCaps(dc, 117)  # 原始分辨率的高度
        self.__scale = width / widthScale
        print(self.__width, self.__height, widthScale, heightScale, width, height, self.__scale)

        #self.__win.mainloop()  # 窗口持久化

    def xFunc1(self, event):
        global prc_state,multi_doing,rt_solve,update
        # print(f"鼠标左键点击了一次坐标是:x={g_scale * event.x}, y={g_scale * event.y}")
        if event.state == 0 or event.state == 8:  # 鼠标左键按下
            self.__start_x, self.__start_y = event.x, event.y
        elif event.state == 256 or  event.state == 264:  # 鼠标左键释放
            if event.x == self.__start_x or event.y == self.__start_y:
                return
            im = ImageGrab.grab((self.__scale * self.__start_x, self.__scale * self.__start_y,
                                 self.__scale * event.x, self.__scale * event.y))
            imgName = 'tmp.png'
            im.save(imgName)

            print('保存成功')
            self.__win.update()
            sleep(0.5)
            self.__win.destroy()

            if prc_state == True:
                show_prtsc("tmp.png")
                show_latex_formula()
                prc_state = False
                multi_doing = False
                if rt_solve == True:
                    update = True
                    rt_solve = False



    def xFunc2(self, event):
        # print(f"鼠标左键点击了一次坐标是:x={self.__scale * event.x}, y={self.__scale * event.y}")
        if event.x == self.__start_x or event.y == self.__start_y:
            return
        self.__canvas.delete("prscrn")
        self.__canvas.create_rectangle(self.__start_x, self.__start_y, event.x, event.y,
                                       fill='white', outline='red', tag="prscrn")
        # 包装画布
        self.__canvas.pack()

def ui():
    global t, status, canvas
    # 窗体初始化
    window = tk.Tk()
    window.title('LATEX公式助手')
    window.geometry('800x500')
    window.resizable(False, False)
    canvas = tk.Canvas(window, width=800, height=600, bg="#F5F5F5")
    menubar = tk.Menu(window)
    helpmenu1 = tk.Menu(menubar, tearoff=0)
    helpmenu2 = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label='关于', menu=helpmenu1)
    menubar.add_cascade(label='说明', menu=helpmenu2)
    def show_rule():
        webbrowser.open("docs\\note.html")

    helpmenu1.add_command(label='文档', command=show_rule)
    def show_md():
        webbrowser.open("docs\\README.html")
    helpmenu2.add_command(label='文档', command=show_md)
    window.config(menu=menubar)
    canvas.create_rectangle(250, 10, 790, 490, outline='black')
    canvas.create_line(0, 45, 160, 45)
    canvas.create_line(0, 300, 160, 300)
    canvas.create_line(250, 200, 790, 200)
    canvas.create_line(250, 350, 790, 350)
    canvas.create_line(160, 5, 160, 590,dash=(4, 4))
    canvas.create_oval(112, 275, 132, 295, fill='black')
    canvas.create_oval(112, 225, 132, 245, fill='black')
    image = Image.open("docs\\logo1.png")
    image = image.convert('RGBA')
    image = image.resize((160, 202))  # 规定图片大小
    img = ImageTk.PhotoImage(image)
    pic = canvas.create_image(2, 305, anchor='nw', image=img)
    #pic = tkinter.Label(image=img, anchor='nw').place(x=10, y=327)
    w1 = tk.Label(canvas, text="公式位置:", background="#F5F5F5", font=('', 11))
    w1.place(x=170, y=10)
    w2 = tk.Label(canvas, text="公式输出:", background="#F5F5F5", font=('', 11))
    w2.place(x=170, y=250)
    w3 = tk.Label(canvas, text="渲染预览:", background="#F5F5F5", font=('', 11))
    w3.place(x=170, y=350)
    w4 = tk.Label(canvas, text="渲染指示:", background="#F5F5F5", font=('', 11))
    w4.place(x=25, y=224)
    w5 = tk.Label(canvas, text="语法检查:", background="#F5F5F5", font=('', 11))
    w5.place(x=25, y=274)
    w6 = tk.Label(canvas, text="Latex公式助手", background="#F5F5F5", font=('', 11))
    w6.place(x=25, y=16)
    canvas.place(x=0, y=0)

    global ti
    ti = tk.scrolledtext.ScrolledText(canvas, width=73, height=11)
    ti.place(x=252, y=202)
    tk.Button(canvas, text="定位", command=lambda: show_prtsc("tmp.png")).place(x=12, y=52, width=59, height=30)
    tk.Button(canvas, text="识别", command=show_latex_formula).place(x=12, y=102, width=59, height=30)
    tk.Button(canvas, text="渲染", command=show_latex_result).place(x=12, y=152, width=59, height=30)
    tk.Button(canvas, text="截图", command=fin).place(x=90, y=152, width=59, height=30)
    tk.Button(canvas, text="一键", command=one_shot).place(x=90, y=102, width=59, height=30)
    tk.Button(canvas, text="更新", command=change_mode).place(x=90, y=52, width=59, height=30)
    window.mainloop()

def change_mode():
    global update
    update = not update

def show_prtsc(path):
    try:
        global img0,single_doing
        single_doing = True
        model = YOLO("best_update.pt")  # build a YOLOv8n model from scratch
        model.info()  # display model information
        results = model(path, conf=0.6, iou=0.3)  # 对图像进行预测
        res_plotted = results[0].plot()
        res_box = results[0].boxes
        x1 = res_box.xyxy[0][0].item()
        y1 = res_box.xyxy[0][1].item()
        x2 = res_box.xyxy[0][2].item()
        y2 = res_box.xyxy[0][3].item()
        box = (int(x1), int(y1), int(x2), int(y2))

        img = Image.open(path)
        region = img.crop(box)
        region = region.convert('RGB')
        region.save('crop.jpg')
        cv2.imwrite("prtsc.jpg", res_plotted)

        image = Image.open("prtsc.jpg")
        shape = image.size
        sf_state = 182/shape[1]
        #print(sf_state)
        length = int(shape[0]*sf_state)
        if length>530:
            length=530
        image = image.resize((length, 182))  # 规定图片大小
        img0 = ImageTk.PhotoImage(image)
        pic = tkinter.Label(image=img0, anchor='nw').place(x=252, y=12)
        single_doing = False
    except IndexError as e:
        tk.messagebox.showinfo('出现错误！', '似乎并没有找到公式！\n' + str(e))




def show_latex_formula():
    global single_doing
    single_doing = True
    ti.delete(1.0, tk.END)
    img = Image.open("crop.jpg")
    model = cli.LatexOCR()
    prediction = model(img)
    prediction = optimize.post_post_process_latex(prediction)
    #print(prediction)
    ti.insert("insert", prediction)
    ti.yview_moveto(1.0)
    single_doing = False


def show_latex_result():
    global img1,error
    try:
        result = str(ti.get("1.0", "end")).strip()
        #os.system("start pythonw draw.py")
        mathtext.math_to_image((r'$'+result+r'$').strip(), r'result.png', dpi = 144)
        image = Image.open("result.png")
        shape = image.size
        sf_state = 152/shape[1]
        #print(sf_state)
        length = int(shape[0]*sf_state)
        if length>530:
            length=530
        image = image.resize((length, 132))  # 规定图片大小
        img1 = ImageTk.PhotoImage(image)
        pic = tkinter.Label(image=img1, anchor='nw').place(x=252, y=352)
        error = False
    except ValueError as e:
        global update
        if update == False:
            tk.messagebox.showinfo('出现错误！', 'matplotlib对latex的支持有限，请检查是否出现了高级标签！\n'+str(e))
        if update == True:
            error = True
            pass
    except SystemError as e:
        pass


def fin():
    global multi_doing
    multi_doing = True
    CTkPrScrn()

def one_shot():
    global prc_state,multi_doing,update,rt_solve
    multi_doing = True
    prc_state = True
    if update == True:
        update = False
        rt_solve = True

    a = CTkPrScrn()


def compare_result():
    global update
    first = True
    try:
        while True:
            time.sleep(0.5)
            if update == False:
                canvas.create_oval(112, 225, 132, 245, fill='black')
                error = False
            if update == True:
                canvas.create_oval(112, 225, 132, 245, fill='green')
                result = str(ti.get("1.0", "end")).strip()
                if first == True:
                    result_old = result

                    tk.messagebox.showinfo('注意！', '在开启更新模式以后，渲染不会实时报错！仅以指示灯表示是否出错\n')
                    first = False

                if result_old != result:
                    if single_doing == False and multi_doing == False:
                        show_latex_result()
                result_old = result
    except Exception as e:
        print(e)
        pass

def error_state():
    global error
    while True:
        time.sleep(0.1)
        if update == True:
            if error == True:
                canvas.create_oval(112, 275, 132, 295, fill='red')
                canvas.update()
            if error == False:
                canvas.create_oval(112, 275, 132, 295, fill='black')
                canvas.update()
        else:
            canvas.create_oval(112, 275, 132, 295, fill='black')
            canvas.update()




# 区分线程来使得ui和刷新异步
class myThread(threading.Thread):
    def __init__(self, threadID, name, function):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.function = function
        # self.lock = threading.RLock()

    def run(self):
        # self.lock.acquire()
        self.function()
        # self.lock.acquire()

thread1 = myThread(1, "Thread-1", ui)
thread2 = myThread(2, "Thread-2", compare_result)
thread3 = myThread(3, "Thread-3", error_state)
def t1_go():
    thread1.start()
def t2_go():
    thread2.daemon = True
    thread2.start()
def t3_go():
    thread3.daemon = True
    thread3.start()
if __name__  == '__main__':
    init()
    t1_go()
    time.sleep(0.1)
    t3_go()
    compare_result()
















