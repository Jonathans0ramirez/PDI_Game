import cv2
import numpy as np
import time

pTime = 0
cTime = 0

def mouseRGB(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN: #checks mouse left button down condition
        colorsB = frame[y,x,0]
        colorsG = frame[y,x,1]
        colorsR = frame[y,x,2]
        colors = frame[y,x]
        print("Red: ", colorsR)
        print("Green: ", colorsG)
        print("Blue: ", colorsB)
        print("BGR Format: ", colors)
        print("Coordinates of pixel: X: ", x, "Y: " ,y)


cv2.namedWindow('Camera')
cv2.setMouseCallback('Camera',mouseRGB)

cap = cv2.VideoCapture(1) # 640W, 480H, 30fps
_, frame = cap.read()
rows, cols, _ = frame.shape

x_medium = int(cols / 2)
y_medium = int(rows / 2)
center = (x_medium, y_medium)
position = 90 # Degrees

while True:
    _, frame = cap.read()
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Red color
    low_red = np.array([161, 155, 84])
    high_red = np.array([179, 255, 255])
    red_mask = cv2.inRange(hsv_frame, low_red, high_red)
    contours, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)

    for cnt in contours:
        (x, y, w, h) = cv2.boundingRect(cnt)
        x_medium = int((x + x + w) / 2)
        y_medium = int((y + y + h) / 2)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        break
    
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(frame, str(int(fps)), (10,30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 166), 2)

    cv2.line(frame, (x_medium, 0), (x_medium, 480), (0,255, 0), 2)
    cv2.line(frame, (0, y_medium), (640, y_medium), (0,0, 255), 2)

    cv2.imshow("Camera", frame)
    # cv2.imshow("Mask", red_mask)

    key = cv2.waitKey(1)

    if key == 27:
        break

    # Move to center

cap.release()
cv2.destroyAllWindows()
