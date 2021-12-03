import cv2
import time
import HandTracking.HandTrackingModule as Htm

wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

detector = Htm.HandDetector(detection_confidence=0.7)

while cap.isOpened():

    success, image = cap.read()

    if not success:
        print("Ignoring empty camera frame.")
        # If loading a video, use 'break' instead of 'continue'.
        continue

    start = time.time()

    image = detector.find_hands(image)
    landmark_list, bbox = detector.find_position(image, draw=False)

    if len(landmark_list) != 0:
        # print(landmark_list)
        area = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1]) // 100
        print(area)

        if 150 < area < 1080:
            distance, image, line_info = detector.find_distance(4, 8, image)

            cv2.rectangle(image, (bbox[0] - 20, bbox[1] - 20), (bbox[2] + 20, bbox[3] + 20), (140, 180, 210), 2)

            if distance > 50:
                # print(distance)
                cv2.circle(image, (line_info[4], line_info[5]), 8, (0, 160, 255), cv2.FILLED)

    end = time.time()
    totalTime = end - start

    fps = 1 / totalTime

    cv2.putText(image, str(int(fps)), (10, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 166))

    cv2.imshow("MediaPipe Hands", image)

    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
