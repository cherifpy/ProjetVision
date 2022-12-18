import cv2 as cv

def drawBox(frame, rectangle):
 
    x,y,w,h = int(rectangle[0]), int(rectangle[1]), int(rectangle[2]), int(rectangle[3])
    cv.rectangle(frame, (x,y),((x+w), (y+h)), (0,0,255),1,1)
    cv.putText(frame, "Tracking", (40, 80), cv.FONT_HERSHEY_COMPLEX,0.6,(0,255,0),1)
    return x+w/2, y+h/2
    

cap = cv.VideoCapture(0)
cap.set(cv.CAP_PROP_FPS, 1200)


#tracker = cv.legacy.TrackerMOSSE_create()
tracker = cv.TrackerCSRT_create()
ret, frame = cap.read()
cv.flip(frame,1,frame)
rectangle = cv.selectROI("Tracking", frame, False)
tracker.init(frame, rectangle)


while True:
    ret, frame = cap.read()
    cv.resize(frame, (800,600))
    cv.flip(frame,1,frame)
    ret, rectangle = tracker.update(frame)

    if ret:
        x,y = drawBox(frame, rectangle)
        cv.circle(frame, (int(x), int(y)), 3, (0,255,0), 2,1)
        #affichage des coordonée
        cv.putText(frame, "X = ",(0,30), cv.FONT_HERSHEY_COMPLEX, 0.7,(0,255,0),1)
        cv.putText(frame, str(int(x)),(40,30), cv.FONT_HERSHEY_COMPLEX, 0.7,(0,255,0),1)
        cv.putText(frame, "Y = ",(100,30), cv.FONT_HERSHEY_COMPLEX, 0.7,(0,255,0),1)
        cv.putText(frame, str(int(y)),(140,30), cv.FONT_HERSHEY_COMPLEX, 0.7,(0,255,0),1)       
    else:
        cv.putText(frame, "Lost Tracking",(50,80), cv.FONT_HERSHEY_COMPLEX, 0.7,(0,255,0),1)

    cv.imshow("Tracking", frame)
    
    car = cv.waitKey(1)&0xFF
    if car == ord("0") :
        break
cap.release()
cv.destroyAllWindows()

