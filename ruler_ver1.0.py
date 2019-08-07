# pyinstaller -F -w -i "icon.ico" ruler_ver1.0.py
# -popupwindow -screen-width 1920 -screen-height 1080
from tkinter import *
from math import sin, cos, pi

import keyboard as kb

import ctypes

class Drow(object):
    def __init__(self):
        self.root = Tk()
        self.root.overrideredirect(True)
        self.root.wm_attributes("-topmost", "true",
                                "-transparentcolor", "white")

        # Разрешение экрана
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()

        (self.GDR_W, self.GDR_h) = (user32.GetSystemMetrics(0), user32.GetSystemMetrics(1))

        # Создание и расположение холста
        self.c = Canvas(self.root,
                        width=self.GDR_W,
                        height=self.GDR_h,
                        bg='white',
                        # relief='ridge',
                        highlightthickness=0)

        self.c.create_oval(0, 0, 100, 50,
                           fill='black')

        lbl_font = ("Purisa", 18)
        self.label = self.c.create_text(11, 12,
                                        anchor='nw',
                                        text="100, 90",
                                        font=lbl_font,
                                        fill="#FFFFFE")


        self.c.pack()


        self.X0, self.Y0 = self.cursor_position()
        self.force, self.angle = 99, 180 - 72

        # центр танка
        kb.add_hotkey('b', self.center)
        # Управление параболой # в этих функциях можно дописать код
        kb.add_hotkey('t', self.more)
        kb.add_hotkey('g', self.less)
        kb.add_hotkey('f', self.left)
        kb.add_hotkey('h', self.right)

        # тестировочные хоткеи
        kb.add_hotkey('x', self.drow_parabola)
        kb.add_hotkey('c', self.delete)
        kb.add_hotkey('q', self.exit0)


    def change_Label(self):
        angle = self.angle
        if angle > 90:
            angle = 180 - angle
        self.c.itemconfig(self.label, text=str(self.force) + ', ' + str(angle))

    def center(self):
        self.X0, self.Y0 = self.cursor_position()
        # print(self.X0, self.Y0)

    # force
    def more(self):
        if (100 - self.force):
            self.force += 1
        self.changeAll()

    def less(self):
        if (self.force):
            self.force -= 1
        self.changeAll()

    # velocity
    def left(self):
        if (270 - self.angle == 0):
            self.angle = -90
        if (270 - self.angle):
            self.angle += 1
        elif (self.angle + 90):
            self.angle -= 1
        self.changeAll()

    def right(self):
        if (self.angle == -90):
            self.angle = 270
        if (self.angle + 90):
            self.angle -= 1
        elif (270 - self.angle):
            self.angle += 1
        self.changeAll()

    def changeAll(self):
        self.change_Label()
        self.drow_parabola()

    def cursor_position(self):
        x = self.root.winfo_pointerx()
        y = self.root.winfo_pointery()
        return (x, y)

    # определим параболу
    def parabola(self, t, g = 9.81, coef = 2.45, R = 8): # 1920x1080
    # def parabola(self, t, g=9.81, coef=1.79, R=8): # 1400x1050

        t = t / 20
        Xcenter, Ycenter = (R * cos(self.angle / 180 * pi),
                            R * sin(self.angle / 180 * pi))

        X, Y = (self.force * t * cos (self.angle / 180 * pi),
                -self.force * t * sin (self.angle / 180 * pi) + g * t * t / 2)

        X = (X + Xcenter) * coef + self.X0
        Y = (Y - Ycenter) * coef + self.Y0
        return (X, Y)

    def plot(self, func):
        self.c.create_line(func,
                           fill="red",
                           tag='parabola')

    # Рисуем параболу
    def drow_parabola(self):
        self.delete()

        funcParab = []
        for t in range(500):
            x, y = self.parabola(t)
            funcParab.append([x, y])
        self.plot(funcParab)

    # Удаляем параболу
    def delete(self):
        self.c.delete('parabola')

    def exit0(self):
        self.root.destroy()

if __name__ == '__main__':
    main = Drow()
    main.root.mainloop()

