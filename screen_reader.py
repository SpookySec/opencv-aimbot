import cv2 as cv
import mss
import utils
import numpy as np
import pyautogui as ag
import win32api, win32con
from time import sleep

needle = cv.imread('./images/needle3.png', cv.IMREAD_GRAYSCALE)
monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}
sct = mss.mss()
threshold = 0.65
scale = 0.7
w, h = 50, 60
x_off, y_off = 20, 50
screen_center = (960, 540)

while True:

    # Take a screen shot to draw on later
    screenshot = np.array(sct.grab(monitor))

    # Current screen (GRAY)
    haystack = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)

    # Results from template matching
    result = cv.matchTemplate(haystack, needle, cv.TM_CCOEFF_NORMED)

    yloc, xloc = np.where(result >= threshold)
    heads = []

    for (x, y) in zip(xloc, yloc):
        x -= x_off
        y += y_off
        heads.append([int(x), int(y), int(w), int(h)])
        heads.append([int(x), int(y), int(w), int(h)])

    heads, _ = cv.groupRectangles(heads, 1, 0.2)

    if len(heads) < 1:
        print("[!] No heads found :(")

    else:
        print(f"\r[+] Found {len(heads)} heads\n", end="")

        closest = heads[0]

        entity_center = (closest[0] + w // 2, closest[1] + h // 2)

        print(entity_center)
        rect = cv.rectangle(screenshot, (closest[0], closest[1]), (closest[0] + w, closest[1] + h), (0, 255, 0), 2)
        line = cv.line(rect, screen_center, entity_center, (255, 255, 255), 2)


        # cv.imshow("Best matches", utils.resize_img(line, 75))

        # utils.move_to(x, y)

        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, int((entity_center[0] - screen_center[0]) * scale), int((entity_center[1] - screen_center[1]) * scale), 0, 0 )
        shoot_x, shoot_y = int((entity_center[0] - screen_center[0]) * scale), int((entity_center[1] - screen_center[1]) * scale)
        utils.shoot(shoot_x, shoot_y)
    sleep(1)
        # Press "q" to quit
    # if cv.waitKey(1) & 0xFF == ord("q"):
    #     cv.destroyAllWindows()
    #     break
