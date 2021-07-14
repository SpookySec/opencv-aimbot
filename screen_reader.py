import cv2 as cv
import mss
import utils
import numpy as np
import pyautogui as ag
import win32api, win32con

needle = cv.imread('./images/needle3.png', cv.IMREAD_GRAYSCALE)
with mss.mss() as sct:
    monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}
    while True:
        screenshot = np.array(sct.grab(monitor))

        haystack = np.array(sct.grab(monitor))
        # haystack = cv.imread('./images/haystack.png')

        haystack = cv.cvtColor(haystack, cv.COLOR_BGR2GRAY)
        result = cv.matchTemplate(haystack, needle, cv.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
        utils.move_to(int(max_loc[0] - 960), int(max_loc[1] - 540))
        found = cv.circle(screenshot, (max_loc[0] + 11, max_loc[1] + 13), 17, (0, 0, 255), 2)
        scaled_found = utils.resize_img(found, 70)
        scaled_result = utils.resize_img(result, 70)
        
        cv.imshow("Best matches", scaled_found)
            # Press "q" to quit
        if cv.waitKey(30) & 0xFF == ord("q"):
            cv.destroyAllWindows()
            break
