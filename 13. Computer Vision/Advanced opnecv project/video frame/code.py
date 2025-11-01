# Detect the objects  


import cv2

import numpy as np

cap = cv2.VideoCapture(r"C:\Users\shali\Desktop\DS_Road_Map\13. Computer Vission\Advanced opnecv project\video frame\los_angeles.mp4")

_, frame = cap.read()

cv2.imshow("Frame", frame)
cv2.waitKey(0)


#-----------------------------------

# video is nothing 1 image after another image
# if i press key then it keep goes to the next frame.

import cv2

import numpy as np

cap = cv2.VideoCapture(r'C:\Users\shali\Desktop\DS_Road_Map\13. Computer Vission\Advanced opnecv project\video frame\los_angeles.mp4')

while True:
    _, frame = cap.read()
    cv2.imshow("Frame", frame)
    cv2.waitKey(0)

#--------------------------------------
    
# it will display the complete video

import cv2

import numpy as np

cap = cv2.VideoCapture(r'C:\Users\shali\Desktop\DS_Road_Map\13. Computer Vission\Advanced opnecv project\video frame\los_angeles.mp4')

while True:
    _, frame = cap.read()
    
    cv2.imshow("Frame", frame)
    
    key = cv2.waitKey(1)
    if key == 27:
        break
    
cap.release()
cv2.destroyAllWindows()
