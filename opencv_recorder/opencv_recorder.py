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

        img_rec = contrast * img + bright
        img_rec[img_rec < 0] = 0
        img_rec[img_rec > 255] = 255
        img_rec = img_rec.astype(np.uint8)
        if not valid :
            break
        
        if reverse :
            img_rec = cv.flip(img_rec,1)

        img_scr = img_rec.copy()
        
        if recording :
            cv.circle(img_scr, (15,15), radius = 10, color = (0,0,255), thickness = -1)
            rec.write(img_rec)
            
        cv.imshow('recorder', img_scr)
        key = cv.waitKey(wait_msec)
        if key == 27 :
            break
        elif key == 32 :
            recording = not recording
        elif key == ord('r') :
            reverse = not reverse
        elif key == ord('1'):
                contrast -= 0.1
                if contrast < 0 : contrast = 0
        elif key == ord('2'):
                contrast += 0.1
        elif key == ord('3') :
                bright -= 1
                if bright < 0 :
                    bright = 0
        elif key == ord('4') :
            bright += 1
    video.release()
    rec.release()
    cv.destroyAllWindows()