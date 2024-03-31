import cv2 as cv
import numpy as np

video = cv.VideoCapture(0)

if video.isOpened() :
    fps = 30
    wait_msec = int(1/fps*1000)

    fourcc = cv.VideoWriter_fourcc(*'XVID')
    rec = cv.VideoWriter()
    rec.open('record.avi', fourcc, fps, (640, 480))
    recording = False
    reverse = False
    contrast = 1
    bright = 0
    
    while 1 :
        valid, img = video.read()
        if not valid :
            break
        img_scr = img.copy()
        if recording :
            cv.circle(img_scr, (15,15), radius = 10, color = (0,0,255), thickness = -1)
            rec.write(img)
            
        cv.imshow('recorder', img_scr)
        key = cv.waitKey(wait_msec)
        if key == 27 :
            break
        elif key == 32 :
            recording = not recording
    video.release()
    rec.release()
    cv.destroyAllWindows()