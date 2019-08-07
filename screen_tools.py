import imutils
import cv2
import numpy as np
import screenshot as ss

class screen_tools(object):
    def __init__(self):
        self.screen = ss.ScreenShot()

        self.image = np.array([])
        self.digits = np.array([])

        self.tank = np.array([])
        self.tankForSide = np.array([])

    def GetDigits(self, x = 100, y = 100): # x, y - center of the tank
        self.image = self.screen.GetScreenhot()
        self.digits = self.image[y + 30:y + 70, x - 45: x + 45]
        # self.ShowIm(image = self.digits)

    def GetCenterTank(self, x = 100, y = 100): # x, y - center of the tank
        self.image = self.screen.GetScreenhot()
        self.tank = self.image[y - 10:y + 75, x - 48: x + 48]
        # self.ShowIm(image = self.tank)

    def GetTankSide(self, x = 100, y = 100): # x, y - center of the tank
        self.image = self.screen.GetScreenhot()
        self.tankForSide = self.image[y - 30:y + 30, x - 30: x + 30]
        # self.ShowIm(image = self.tankForSide)

    def LoadIm(self, PATH_name = '',size = 500):
        self.image = cv2.imread(PATH_name, 1)
        self.image = imutils.resize(self.image, height=size)

    def ShowIm(self, name='ImageWindow', image = np.array([])):
        if image == np.array([]):
            image = self.image
        cv2.imshow(name, image)
        cv2.waitKey()

    def GreenFilter(self, size = 600):
        digits = imutils.resize(self.tankForSide, height=size)
        hsv = cv2.cvtColor(self.tankForSide, cv2.COLOR_BGR2HSV)

        # define range of blue color in HSV
        hsv_min = np.array((0, 220, 0), np.uint8)
        hsv_max = np.array((60, 255, 0), np.uint8)

        # Threshold the HSV image to get only blue colors
        mask = cv2.inRange(hsv, hsv_min, hsv_max)
        return mask

    def DigitsFilter(self, showDig = 0, size = 500):
        digits = imutils.resize(self.digits, height=size)
        gray = cv2.cvtColor(digits, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray, 254, 255, cv2.THRESH_BINARY_INV)

        if showDig:
            cv2.imshow('Digits', thresh)
            cv2.waitKey()

        coordX = [i for i in self.SplitImgX(thresh)]
        coordY = [i for i in self.SplitImgY(thresh)]

        threshCut = dict()
        for i in range(int(len(coordX) / 2)):
            threshCut[i] = thresh[coordY[0]:coordY[-1],coordX[2 * i]:coordX[2 * i + 1]]

        return threshCut

    def CenterTankFilter(self, size = 850, showDig = 0):
        digits = imutils.resize(self.tank, height=size)
        gray = cv2.cvtColor(digits, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray, 254, 255, cv2.THRESH_BINARY_INV)

        if showDig:
            cv2.imshow('Digits', thresh)
            cv2.waitKey()

        coordX = [i for i in self.SplitImgX(thresh)]
        coordY = [i for i in self.SplitImgY(thresh)]

        if coordY != [] and coordX != []:
            return (coordY[0] // 10 - 10 - 41, (coordX[0] + coordX[-1]) // 20 - 48)
        else:
            return (0, 0)

    def TankSideFilter(self, size = 600, showDig = 0):
        tank = imutils.resize(self.tankForSide, height=size)
        # tank = self.tankForSide
        # mask = cv2.inRange(tank, (50,210,50), (140, 255, 200))
        gray = cv2.cvtColor(tank, cv2.COLOR_BGR2GRAY)
        contours1, _ = cv2.findContours(gray,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
        contours1 = contours1[0].reshape(-1, 2)
        img1 = tank.copy()

        for (x, y) in contours1:
            cv2.circle(img1, (x, y), 1, (255, 0, 0), 3)

        # cv2.drawContours(tank, contours1, -1, (0, 255, 0), 3)

        # gray = cv2.cvtColor(tank, cv2.COLOR_BGR2GRAY)
        # ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV)

        # ret, thresh1 = cv2.threshold(blurred, 230, 255, cv2.THRESH_BINARY_INV)

        # mask = self.GreenFilter()
        if showDig:
            cv2.imshow('Digits', tank)
            cv2.waitKey()

        # coord = [i for i in self.SplitImgP(thresh1)]
        # # print(coord)
        # if len(coord) > 1:
        #     center = (coord[0] + coord[1]) // 20 - 30
        #     if center < 0:
        #         return 'left'
        #     else:
        #         return 'right'
        # else:
        #     return 'right'

    def SplitImgP(self, thresh1):
        maxY, maxX = thresh1.shape
        x = -1
        # X
        for i in range(x + 1, maxX):
            if 0 in thresh1[::, i]:
                x = i
                yield i
                break
        for i in range(x + 1, maxX):
            if 0 not in thresh1[::, i]:
                x = i
                yield i
                break


    def SplitImgY(self, thresh):
        maxY, maxX = thresh.shape

        # trigger for black/white pixels
        # trigger = False - white pixel
        # trigger = True  - black pixel
        if 0 not in thresh[0]:
            trigger = False
        else:
            trigger = True
            yield 0

        for i in range(maxY):
            if 0 in thresh[i] and not trigger:
                trigger = True
                yield i

            if 0 not in thresh[i] and trigger:
                trigger = False
                yield i

            if i == maxY - 1 and trigger:
                yield i

    def SplitImgX(self, thresh):
        maxY, maxX = thresh.shape

        # trigger for black/white pixels
        # trigger = False - white pixel
        # trigger = True  - black pixel
        if 0 not in thresh[::, 0]:
            trigger = False
        else:
            trigger = True
            yield 0

        for i in range(maxX):
            if 0 in thresh[::, i] and not trigger:
                trigger = True
                yield i

            if 0 not in thresh[::, i] and trigger:
                trigger = False
                yield i

            if i == maxX - 1 and trigger:
                yield i


    def SaveIm(self, path = 'C:/Users/Nikita/.PyCharmCE2019.1/config/scratches/test/', threshCut = dict()):
        pass
        # cv2.imwrite(os.path.join(path, str(i) + '.png'), threshCut)
        # cv2.imshow(str(i + 1), threshCut)