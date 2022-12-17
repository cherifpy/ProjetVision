import cv2
import numpy as np



capteur = cv2.VideoCapture(0)
fps = 10




def detect_inrange(image, surfaceMin, surfaceMax,):
    a = 0
    b = 0
    c = 255

    lo = np.array([95,100,50])
    hi = np.array([120,255,200])
    points=[]
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    image = cv2.blur(image, (5,5))
    
    mask = cv2.inRange(image, lo, hi)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=3)
    
    elements = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

    elements = sorted(elements, key=lambda x:cv2.contourArea(x), reverse = True)
    
    for element in elements:
        #print(cv2.contourArea(element))
        if surfaceMax>cv2.contourArea(element)>surfaceMin:
            ((x,y), rayon) = cv2.minEnclosingCircle(element)
            points.append(np.array([(int(x), int(y)), int(rayon)], dtype =object))
        else:
            break
    
    
    return image, mask, points



while(True):

    ret, frame = capteur.read()
    
    #frame = cv2.resize(frame,(600,600))
    cv2.flip(frame, 1, frame)
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    cv2.circle(frame, (150,150), 20, (0,255,0), 5)
    img, mask, points = detect_inrange(frame, 1500, 4000)
    #print(img[100,100])
    for point in points[0:1]:
        cv2.circle(frame, point[0], point[1], (0,0,255), 3)
        print(point[0])
    cv2.imshow("mask", mask)
    cv2.imshow("bgr img", frame)
    #cv2.imshow("hsv mask", output_hsv)

    car = cv2.waitKey(10)
    if car == ord("0"):
        break

def ColorTraking(capteur):
    ret, frame = capteur.read()
    
    frame = cv2.resize(frame,(600,600))
    cv2.flip(frame, 1, frame)
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    cv2.circle(frame, (150,150), 20, (0,255,0), 5)
    img, mask, points = detect_inrange(frame, 1500, 4000)
    #print(img[100,100])
    for point in points[0:1]:
        cv2.circle(frame, point[0], point[1], (0,0,255), 3)
        print(point[0])
    cv2.imshow("mask", mask)
    cv2.imshow("bgr img", frame)
    #cv2.imshow("hsv mask", output_hsv)

        