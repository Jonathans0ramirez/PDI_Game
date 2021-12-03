import cv2
import time
import HandTracking.HandTrackingModule as Htm

wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

detector = Htm.HandDetector(max_hands=1)

while cap.isOpened():

    success, image = cap.read()

    if not success:
        print("Ignoring empty camera frame.")
        # If loading a video, use 'break' instead of 'continue'.
        continue

    start = time.time()

    image = detector.find_hands(image)
    landmark_list, bbox = detector.find_position(image, draw=True)

    if len(landmark_list) != 0:
        fingers = detector.fingers_up()
        print(fingers)
        area = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1]) // 100

        if 150 < area < 1080:
            distance, image, line_info = detector.find_distance(4, 8, image)
            if distance > 70:
                cv2.circle(image, (line_info[4], line_info[5]), 8, (0, 255, 160), cv2.FILLED)
            elif distance > 40:
                cv2.circle(image, (line_info[4], line_info[5]), 8, (0, 160, 255), cv2.FILLED)
            else:
                cv2.circle(image, (line_info[4], line_info[5]), 8, (255, 160, 0), cv2.FILLED)
                # time.sleep(0.10)

    end = time.time()
    totalTime = end - start

    fps = 1 / totalTime

    cv2.putText(image, str(int(fps)), (10, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 166))

    cv2.imshow("MediaPipe Hands", image)

    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
