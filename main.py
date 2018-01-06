import os
import PIL, numpy, math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time, random

need_update = True
def get_screen_image():
    # 获取手机实时截图
    os.system('adb shell screencap -p /sdcard/screen.png')
    # # 将截图拉取到工程目录下
    os.system('adb pull /sdcard/screen.png')

    return numpy.array(PIL.Image.open('screen.png'))

def jump_to_next(point1, point2):
    x1, y1 = point1; x2, y2 = point2
#     使用勾股定理计算距离
    distance = ((x1 - x2)**2 + (y1- y2)**2)**0.5
    # 点击位置， 保证每一次按压的位置不同，避免反刷机制
    press_x = random.randint(0, 500) + 1
    press_y = random.randint(0, 500) + 1
    release_x = press_x
    release_y = press_y
    print('x: ' + str(press_x) + '----' + 'y: ' + str(press_y))
    os.system('adb shell input swipe {0} {1} {2} {3} {4}'.format(press_x, press_y, release_x, release_y, int(distance*1.35)))


def on_click(event, coor = []):
    # 计算距离, event为点击事件的坐标位置(x1,y1)/(x2,y2)
    global need_update
    coor.append((event.xdata, event.ydata))
    if len(coor) == 2:
        jump_to_next(coor.pop(), coor.pop())
        need_update = True

def update_screen(frame):
#     更新截图, 必须在跳完之后才能调用
    global need_update
    if need_update:
        time.sleep(0.8)
        axes_image.set_array(get_screen_image())
        need_update = False
    return axes_image,


# 创建一个空白图片
figure = plt.figure()
axes_image = plt.imshow(get_screen_image(), animated=True)

# 将获取的图片画在坐标抽上| 将事件与函数绑定
figure.canvas.mpl_connect('button_press_event', on_click)
init = FuncAnimation(figure, update_screen, interval=50, blit=True)
plt.show()
