import cv2 as cv
import numpy as np
import pyautogui as pag
import win32api, win32con

def display(image):
    cv.imshow('reader', image)
    cv.waitKey(0)

def log(value):

    print(f"""
     
     ================
     VALUE: {value}
     =================
     """)
     
def apply_threshold(val, confidence):

    if val > confidence:
        return True
    return False

def move_to(x, y):
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, x, y, 0, 0)

def resize_img(img, scale):
    width = int(img.shape[1] * scale / 100)
    height = int(img.shape[0] * scale / 100)
    dim = (width, height)
    return cv.resize(img, dim);