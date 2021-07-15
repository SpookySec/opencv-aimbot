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

while True:

    # Take a screen shot to draw on later
    screenshot = np.array(sct.grab(monitor))

    # Current screen (GRAY)
    haystack = cv.cvtColor(np.array(sct.grab(monitor)), cv.COLOR_BGR2GRAY)

    # Results from template matching
    result = cv.matchTemplate(haystack, needle, cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

    # Finally drawing a circle
    if max_val > .8:
        circle = cv.circle(screenshot, (max_loc[0] + 11, max_loc[1] + 13), 17, (0, 0, 255), 2)
        line = cv.line(circle, (960, 540), max_loc, (255, 255, 255), 2)
        cv.imshow("Best matches", line)
    else:
        cv.imshow("Best matches", screenshot)

    # utils.move_to(int(max_loc[0] - 960), int(max_loc[1] - 540))

        # Press "q" to quit
    if cv.waitKey(30) & 0xFF == ord("q"):
        cv.destroyAllWindows()
        break
