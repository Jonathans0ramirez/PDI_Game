import cv2
import time
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

with mp_hands.Hands(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:

    while cap.isOpened():

        success, image = cap.read()

        start = time.time()

        # Flip the image horizontally for later selfie-view display
        # Convert the BGR to RGB
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

        # To imporve performace, optionally mark the image as not writeable
        # Pass by reference
        image.flags.writeable = False

        # Process the image and find hands
        results = hands.process(image)

        # Set the image as writeable again
        image.flags.writeable = True

        # Draw the hand annotations on the image
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        multiHandLandMarks = results.multi_hand_landmarks

        if multiHandLandMarks:
            for hand_Landmarks in multiHandLandMarks:
                for id, lm in enumerate(hand_Landmarks.landmark):
                    # print(id, lm)
                    h, w, c = image.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    if id == 8:
                        cv2.circle(image, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

                mp_drawing.draw_landmarks(image, hand_Landmarks, mp_hands.HAND_CONNECTIONS)


        end = time.time()
        totalTime = end - start

        fps = 1/totalTime

        cv2.putText(image, str(int(fps)), (10,30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 166))

        cv2.imshow("MediaPipe Hands", image)

        if cv2.waitKey(5) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()