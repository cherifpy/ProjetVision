import cv2 as cv
import numpy as np


def detect_inrange(image, surfaceMin, surfaceMax,):

    points=[]
    image = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    image = cv.blur(image, (5,5))
    
    mask = cv.inRange(image, lo, hi)
    mask = cv.erode(mask, None, iterations=2)
    mask = cv.dilate(mask, None, iterations=3)
    
    elements = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[-2]

    elements = sorted(elements, key=lambda x:cv.contourArea(x), reverse = True)
    
    #for element in elements:
        #print(cv2.contourArea(element))
    if len(elements)>0:
        if surfaceMax>cv.contourArea(elements[0])>surfaceMin:
            ((x,y), rayon) = cv.minEnclosingCircle(elements[0])
            points.append(np.array([(int(x), int(y)), int(rayon)], dtype =object))
        
    
    
    return image, mask, points

capteur = cv.VideoCapture(0)


a = 0
b = 0
c = 255

lo = np.array([95,100,50])
hi = np.array([120,255,200])

perdu = 100

while True:

    ret, frame = capteur.read()

    cv.flip(frame, 1, frame)
    hsv_frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    img, mask, points = detect_inrange(frame, 1500, 4000)
    #print(img[100,100])
    if len(points)>0:
        cv.circle(frame, points[0][0], points[0][1], (0,0,255), 3)
        #affichage des coordonée
        cv.putText(frame, "X = ",(0,30), cv.FONT_HERSHEY_COMPLEX, 0.7,(0,255,0),1)
        cv.putText(frame, str(int(points[0][0][0])),(40,30), cv.FONT_HERSHEY_COMPLEX, 0.7,(0,255,0),1)
        cv.putText(frame, "Y = ",(100,30), cv.FONT_HERSHEY_COMPLEX, 0.7,(0,255,0),1)
        cv.putText(frame, str(int(points[0][0][1])),(140,30), cv.FONT_HERSHEY_COMPLEX, 0.7,(0,255,0),1)  
        #print(points[0][0])
    cv.imshow("mask", mask)
    cv.imshow("bgr img", frame)
    #cv2.imshow("hsv mask", output_hsv)

    car = cv.waitKey(10)
    if car == ord("0"):
        break

        