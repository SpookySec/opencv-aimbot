import cv2 as cv
import numpy as np
import pyautogui as pag

def display(image):
    cv.imshow('reader', image)
    cv.waitKey(0)

def move_to(x, y):
    pag.dragTo(x, y, duration=2)

def resize_img(img, scale):
    scale_percent = 60 # percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    return cv.resize(img, dim)