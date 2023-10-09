import cv2
import os
from PIL import Image
import numpy as np
import easyocr
import matplotlib.pyplot as plt

thresold=0.45
yellow=[0,255,255]

def get_limits(color):
    c= np.uint8([[color]])
    hsvC=cv2.cvtColor(c,cv2.COLOR_BGR2HSV)
     
    lower_limit=hsvC[0][0][0]-10,100,100
    upper_limit=hsvC[0][0][0]+10,255,255
    
    lower_limit=np.array(lower_limit,dtype=np.uint8)
    upper_limit=np.array(upper_limit,dtype=np.uint8)

    return lower_limit,upper_limit

obj = cv2.VideoCapture(0)
while True:
    ret, frame = obj.read()
    if(ret):
        hsvimg = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        lowerlim,upperlim=get_limits(yellow)
        mask=cv2.inRange(hsvimg,lowerlim,upperlim) 
        newmask=Image.fromarray(mask)
        bbox=newmask.getbbox()
        if bbox is not None:
            x1,y1,x2,y2=bbox
            frame=cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),5)
            frame=cv2.putText(frame,'YELLOW',(x1,y1),cv2.FONT_HERSHEY_DUPLEX,2,(0,255,255),4)
        if cv2.waitKey(1) & 0xFF==ord('q'):
            break
        cv2.imshow('frame',frame)
obj.release()
cv2.destroyAllWindows()