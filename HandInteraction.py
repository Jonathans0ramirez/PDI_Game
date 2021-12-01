import cv2
import math
import time
import numpy as np
import HandTracking.HandTrackingModule as Htm

wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

detector = Htm.HandDetector(detection_confidence=0.7)

while cap.isOpened():

    _, image = cap.read()

    start = time.time()

    image = detector.find_hands(image)
    lmList = detector.find_position(image, draw=False)

    if len(lmList) != 0:
        # print(lmList)

        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        cv2.circle(image, (x1, y1), 8, (255, 0, 255), cv2.FILLED)
        cv2.circle(image, (x2, y2), 8, (255, 0, 255), cv2.FILLED)
        cv2.line(image, (x1, y1), (x2, y2), (255, 0, 255), 3, cv2.LINE_AA)
        cv2.circle(image, (cx, cy), 8, (255, 0, 255), cv2.FILLED)

        distance = math.hypot(x2 - x1, y2 - y1)

        if distance > 50:
            print(distance)

    end = time.time()
    totalTime = end - start

    fps = 1 / totalTime

    cv2.putText(image, str(int(fps)), (10, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 166))

    cv2.imshow("MediaPipe Hands", image)

    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
