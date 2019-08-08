# pyinstaller -F -w -i "icon.ico" ruler_ver1.1.py # -popupwindow -screen-width 1920 -screen-height 1080
from tkinter import *
from math import sin, cos, pi
from numpy import arange
import numpy as np

from pynput.keyboard import Key, Controller

import keyboard as kb
import time
import ctypes

# import screen_tools as ps
import screen_tools as st
import cv2
import digitsCNN as dc
# from pynput.mouse import Button, Controller
from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController

class Drow(object):
    def __init__(self):
        self.root = Tk()
        self.root.overrideredirect(True)
        self.root.wm_attributes("-topmost", "true",
                                "-transparentcolor", "white")
        self.keyboard = KeyboardController()
        self.m = MouseController()
        # Разрешение экрана
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()

        (self.GDR_W, self.GDR_h) = (user32.GetSystemMetrics(0), user32.GetSystemMetrics(1))

        # Создание и расположение холста
        self.c = Canvas(self.root,
                        width=self.GDR_W - 1,
                        height=self.GDR_h - 1,
                        bg='white',
                        # relief='ridge',
                        highlightthickness=0)

        self.X0, self.Y0 = self.cursor_position()
        self.curAngle, self.curForce = 90, 100
        self.force, self.angle = 100, 90
        self.nnAngle, self.nnForce = 0, 0
        self.gravity = 9.81
        self.mycentered = False

        self.ScTl = st.screen_tools()
        self.ImDigits = np.array([])
        self.digits = dict()
        self.nnDelay = 0.1

        self.radius = 340
        self.part = 1 # 1,2,3,4 четверти круга


        self.c.create_oval(35, 935, 235, 1080,
                           outline='red',
                           fill='black')

        lbl_font = ("Purisa", 20)
        self.label = self.c.create_text(135, 1045,
                                        anchor='center',
                                        activefill='red',
                                        text='100, 90',
                                        font=lbl_font,
                                        fill="#FFFFFE")
        self.labelnn = self.c.create_text(135, 1000,
                                        anchor='center',
                                        activefill='red',
                                        text='100, 90',
                                        font=lbl_font,
                                        fill="#FFFFFE")

        self.c.pack()

        # центр танка
        kb.add_hotkey('b', self.center)
        # Управление параболой
        kb.add_hotkey('t', self.more)
        kb.add_hotkey('g', self.less)
        kb.add_hotkey('f', self.left)
        kb.add_hotkey('h', self.right)

        # тестовые хоткеи
        kb.add_hotkey('i', self.ChangeSide)
        kb.add_hotkey('x', self.drow_parabola)
        kb.add_hotkey('v', self.change_gravitation)
        kb.add_hotkey('z', self.change_centred)
        kb.add_hotkey('r', self.refresh)
        kb.add_hotkey('n', self.NN)
        kb.add_hotkey('m', self.MyShot2)
        kb.add_hotkey('c', self.delete)
        kb.add_hotkey('q', self.exit0)

    def change_gravitation(self):
        self.gravity = -self.gravity
        self.drow_parabola()

    def change_centred(self):
        self.mycentered = not self.mycentered
        self.drow_parabola()

    def change_Label(self):
        anglE = self.angle
        if 90 < self.angle < 270:
            anglE = 180 - self.angle
        elif self.angle >= 270:
              anglE = self.angle - 360
        self.c.itemconfig(self.label, text=str(self.force) + ', ' + str(anglE))

    def change_Labelnn(self):
        self.curAngle, self.curForce = self.nnAngle, self.nnForce
        self.c.itemconfig(self.labelnn, text=str(self.nnForce) + ', ' + str(self.nnAngle))

    def ChangeSide(self):
        if self.side == 'right':
            self.side = 'left'
        else:
            self.side = 'right'
        self.c.itemconfig(self.labelside, text=self.side)

    def center(self):
        self.delete()
        self.X0, self.Y0 = self.cursor_position()
        self.TrueCenter()
        self.NN()

        # self.CurAngleChange()

        self.changeAll()
        # print(self.X0, self.Y0)

    def CurAngleChange(self):
        if self.side == 'left':
            self.curAngle = self.nnAngle % 360
        else:
            self.curAngle = 180 - self.nnAngle


    def TrueCenter(self):
        pass
        self.ScTl.GetCenterTank(self.X0, self.Y0)
        Y1, X1 = self.ScTl.CenterTankFilter()
        # # print(X1, Y1)
        self.X0 = self.X0 + X1
        self.Y0 = self.Y0 + Y1

    def NN(self):
        self.delete()
        time.sleep(self.nnDelay)
        self.findDigits()
        self.markDigit()
        self.change_Labelnn()
        self.drow_parabola()

    def findDigits(self):
        self.ScTl.GetDigits(x = self.X0, y = self.Y0)
        self.digits = self.ScTl.DigitsFilter(showDig=0)

    def markDigit(self):
        defDigit = dc.DefineDidgit()

        signs = ''
        for key, value in self.digits.items():
            sign = defDigit.Digit(value)
            if sign == 'comma':
                try:
                    self.nnForce = int(signs)
                except:
                    self.nnForce = 0
                signs = ''
            else:
                if sign == 'minus':
                    sign = '-'
                signs += sign
        try:
            self.nnAngle = int(signs)
        except:
            self.nnAngle = 0

        # print(self.nnForce, self.nnAngle)

    def refresh(self):
        self.curAngle, self.curForce = 90, 100
        self.force, self.angle = 100, 90
        self.changeAll()

    # force
    def more(self):
        if (100 - self.force):
            self.force += 1
        self.changeAll()

    def less(self):
        if (self.force):
            self.force -= 1
        self.changeAll()

    # angle
    def left(self):
        self.angle = (self.angle + 1) % 360
        self.changeAll()

    def right(self):
        self.angle = (self.angle - 1) % 360
        self.changeAll()

    def changeAll(self):
        self.change_Label()
        self.change_Labelnn()
        self.drow_parabola()

    def cursor_position(self):
        x = self.root.winfo_pointerx()
        y = self.root.winfo_pointery()
        return (x, y)

    # определим параболу
    def parabola(self, t, coef = 2.45, R = 8): # 1920x1080
    # def parabola(self, t, g=9.81, coef=1.79, R=8): # 1400x1050
        g = self.gravity
        t = t / 20
        Xcenter, Ycenter = (R * cos(self.angle / 180 * pi),
                            R * sin(self.angle / 180 * pi))

        X, Y = (self.force * t * cos (self.angle / 180 * pi),
                -self.force * t * sin (self.angle / 180 * pi) + g * t * t / 2)

        X = (X + Xcenter) * coef + self.X0
        Y = (Y - Ycenter) * coef + self.Y0
        return X, Y

    def pcenter(self):
        g = self.gravity
        Xm, Ym = self.parabola(20 * self.force * sin (self.angle / 180 * pi) / g)
        Xs = []
        Ys = []
        for t in range(-10000, 10000, 1000):
            Xs.append([(Xm, t)])
            Ys.append([(t, Ym)])
        return Xs,Ys

    def plot1(self, func):
        self.c.create_line(func,
                           fill="yellow",
                           tag='parabola',
                           dash=(100, 100),
                           width=2
                           )

    def plot2(self, func):
        self.c.create_line(func,
                           fill="red",
                           tag='parabola',
                           dash=(100, 100),
                           width=2
                           )
    def plot3(self, func):
        self.c.create_line(func,
                           fill="green",
                           tag='parabola',
                           dash=(100, 100),
                           width=2
                           )

    # Рисуем параболу
    def drow_parabola(self):
        self.delete()

        funcParabf = []
        funcParabb = []
        for t in arange(0, 500, 11.5):
            (x, y) = self.parabola(t)
            funcParabf.append([(x, y)])
        if self.mycentered:
            for t in arange(-500, 0, 11.5):
                (x, y) = self.parabola(t)
                funcParabb.append([(x, y)])
            self.plot2(funcParabb)
            mg, mv = self.pcenter()
            self.plot3(mg)
            self.plot3(mv)
        self.plot1(funcParabf)

    def MyShot2(self):
        self.delete()
        time.sleep(self.nnDelay)
        self.m.position = (int(self.X0), int(self.Y0))
        x, y = self.X_Y()
        # self.m.click(Button.left, 1)
        time.sleep(self.nnDelay)
        self.m.press(Button.left)
        time.sleep(self.nnDelay)
        self.m.move(x, -y)

        time.sleep(self.nnDelay)

        self.m.release(Button.left)
        
        self.myshot(x, y)

    def X_Y(self, R = 0):
        alpha = self.angle * pi / 180
        x = R * cos(alpha) + self.force / 100 * self.radius * cos(alpha)
        y = R * sin(alpha) + self.force / 100 * self.radius * sin(alpha)
        return (x, y)

    def Part(self, x, y):
        if x >= 0 and y >= 0:
            self.part = 1
        if x >= 0 and y < 0:
            self.part = 4
            self.curAngle = self.nnAngle % 360
        if x < 0 and y >= 0:
            self.part = 2
            self.curAngle = 180 - self.nnAngle
        if x < 0 and y < 0:
            self.part = 3
            self.curAngle = 180 - self.nnAngle

    def myshot(self, xMouse, yMouse):
        self.NN()
        self.Part(xMouse, yMouse)
        time.sleep(self.nnDelay)
        # print(self.curAngle, self.angle)
        i = 0
        while i != 4:
            epsilon = 0.0
            ca, cf = self.curAngle, self.curForce
            f, a = self.force, self.angle
            print(cf, ca, f, a)
            df = f - cf
            if a < ca:
                da = 360 + a - ca
            else:
                da = a - ca
            if da > 180:
                da = da - 360
            if da < 0:
                ma = Key.right
            elif da > 0:
                ma = Key.left
            else:
                ma = Key.delete
            if df < 0:
                mf = Key.down
            elif df > 0:
                mf = Key.up
            else:
                mf = Key.delete
            tf = (abs(df)-1)*(0.04+epsilon) + 0.16
            ta = (abs(da)-1)*(0.04+epsilon) + 0.16

            if tf > ta:
                self.keyboard.press(ma)
                self.keyboard.press(mf)
                time.sleep(ta)
                self.keyboard.release(ma)
                time.sleep(tf - ta)
                self.keyboard.release(mf)
            else:
                # print(ta, tf)
                self.keyboard.press(mf)
                self.keyboard.press(ma)
                time.sleep(tf)
                self.keyboard.release(mf)
                time.sleep(ta - tf)
                self.keyboard.release(ma)
            i += 1
            if self.CheckTrace(xMouse, yMouse):
                break

        self.keyboard.press(Key.space)
        self.keyboard.release(Key.space)

        # self.curAngle, self.curForce = self.angle, self.force

        self.drow_parabola()

    def CheckTrace(self, xMouse, yMouse):
        self.NN()
        self.Part(xMouse, yMouse)
        # print('CNN', self.nnAngle,self.nnForce, self.curAngle, self.curForce)
        return (self.curAngle,self.curForce) == (self.angle, self.force)

    # Удаляем параболу
    def delete(self):
        self.c.delete('parabola')

    def exit0(self):
        self.root.destroy()

if __name__ == '__main__':
    main = Drow()
    main.root.mainloop()

