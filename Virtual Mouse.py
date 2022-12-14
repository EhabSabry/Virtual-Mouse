import numpy as np
import cv2
import HandTracking as htm
import time
import autopy






smoothening = 7

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 360)
plocX, plocY = 0, 0
clocX, clocY = 0, 0

pTime = 0

detector = htm.handDetector(detectionCon=1, maxHands=1)
wSrc , hSrc = autopy.screen.size()
#print(wSrc,hSrc)
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = detector.findHands(img)
    lmlist , bbox = detector.findPosition(img)



    if len(lmlist)!=0 :
        x1 , y1 = lmlist[8][1:]
        x2, y2 = lmlist[12][1:]

        #print(x1,y1,x2,y2)

        fingers = detector.fingersUp()
       # print(fingers)


        if fingers[1] ==1 and fingers[2] == 0:
            cv2.rectangle(img,(100,100),(640-100,360-100),(255,0,255),2)
            x3 = np.interp(x1,(100,640-100),(0,wSrc))
            y3 = np.interp(y1, (100, 480-100), (0, hSrc))
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening
            autopy.mouse.move(x3,y3)
            cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED)
            plocX, plocY = clocX, clocY


        if fingers[1] == 1 and fingers[2] == 1:
           length , img , lineInfo = detector.findDistance(8,12,img)
           print(length)
           if length < 40:
               cv2.circle(img, (lineInfo[4], lineInfo[5]),
                          15, (0, 255, 0), cv2.FILLED)
               autopy.mouse.click()










    cTime = time.time()
    fps =  1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img,str(int(fps)),(20,50),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)


