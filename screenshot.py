import numpy as np
import pyautogui
import cv2

class ScreenShot(object):

    """
    image: box for save screenshot-image
    """
    def __init__(self):
        self.image = np.array([])

    """
    GetScreenhot: allow to get full screen shot
                  It returns image in Numpy.array type
    has not atributes
    """
    def GetScreenhot(self):
        # Выбираем размер
        self.image = pyautogui.screenshot(region=(0,0, 1920, 1080))

        # Переводим в читаемый вид
        self.image = cv2.cvtColor(np.array(self.image), cv2.COLOR_RGB2BGR)

        return self.image

    """
    ShowIm: show image
    name: name of window with showing image
    """
    def ShowIm(self, name = 'ImageWindow'):
        cv2.imshow(name, self.image)
        cv2.waitKey()

    """
    SaveIm: allow save image file
    It has:
     -name      name of the image
     -path      path. need add '/' in the end of the path
    """
    def SaveIm(self, name = 'image', path = ''):
        # Сохраняем изображение на диск
        cv2.imwrite(path + name + '.png', self.image)
        pass
