import cv2 as cv
import numpy as np

video = cv.VideoCapture(0)

if video.isOpened() :
    fps = 60
    wait_msec = int(1/fps*1000)

    fourcc = cv.VideoWriter_fourcc(*'XVID')
    rec = cv.VideoWriter()
    rec.open('record.avi', fourcc, fps, (640, 480))
    recording = False
    reverse = False
    while 1 :
        valid, img = video.read()
        if not valid :
            break
        
        if recording :
            cv.circle(img, (10,10), radius = 5, color = (0,0,255), thickness = -1)
            rec.write(img)
            
        if reverse :
            img = img[:,::-1,:]
        
        cv.imshow('recorder', img)
        key = cv.waitKey(wait_msec)
        if key == 27 :
            break
        elif key == 32 :
            recording = not recording
        elif key == ord('r') :
            reverse = not reverse
            
            
    # Release everything if job is finished
    video.release()
    rec.release()
    cv.destroyAllWindows()