import cv2
import easyocr
# import matplotlib.pyplot as plt
# import os

obj=cv2.VideoCapture(0)
text_reader=easyocr.Reader(['en'])
while True:
    det,img=obj.read()
    # cv2.imwrite('test.png',img)
    # img=cv2.imread('test.png')
    text_data=text_reader.readtext(img)
    thresold = 0.45
    for t in text_data:
        gbox,_text,val=t
    #     print(gbox)
        # if val>thresold:
        img = cv2.rectangle(img,(int(gbox[0][0]),int(gbox[0][1])),(int(gbox[2][0]),int(gbox[2][1])),(0,255,0),thickness=6)
        img = cv2.putText(img, _text, (int(gbox[0][0]),int(gbox[0][1])) ,  cv2.FONT_HERSHEY_DUPLEX, 3 , (0,0,0), 4 )
    cv2.imshow('img',img)
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break
obj.release()