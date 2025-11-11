# Every color except White 

import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    
    #Every color except white
    low = np.array([0, 42, 0]) 
    high = np.array([179, 255, 255])
    
    mask = cv2.inRange(hsv_frame, low, high)
    result = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.imshow("Frame", frame) 
    cv2.imshow('Result', result)
    
    
    key = cv2.waitKey(1)
    if key ==27:
        break



