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
threshold = 0.75
w, h = 50, 60
x_off, y_off = 20, 40
center = (960, 540)

while True:

    # Take a screen shot to draw on later
    screenshot = np.array(sct.grab(monitor))

    # Current screen (GRAY)
    haystack = cv.cvtColor(np.array(sct.grab(monitor)), cv.COLOR_BGR2GRAY)

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
        exit(1)

    print(f"\r[+] Found {len(heads)} heads", end="")

    closest = heads[0]

    rect = cv.rectangle(screenshot, (closest[0], closest[1]), (closest[0] + w, closest[1] + h), (0, 255, 0), 2)
    line = cv.line(rect, center, (closest[0], closest[1]), (255, 255, 255), 2)


    scale = 0.7
    x = int((closest[0] - center[0]) * scale)
    y = int((closest[1] - center[1]) * scale)


    # cv.imshow("Best matches", utils.resize_img(line, 75))

    cv.imshow('Ghost Recon', utils.resize_img(screenshot, 75))
    sleep(2)
    utils.move_to(x, y)
    # utils.move_to(int(max_loc[0] - 960), int(max_loc[1] - 540))

        # Press "q" to quit
    if cv.waitKey(1) & 0xFF == ord("q"):
        cv.destroyAllWindows()
        break
