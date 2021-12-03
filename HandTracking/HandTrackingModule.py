import cv2
import math
import time
import mediapipe as mp


class HandDetector:
    def __init__(self, mode=False, max_hands=2, detection_confidence=0.5, tracking_confidence=0.5):
        self.landmark_list = None
        self.multi_hand_landmarks = None
        self.mode = mode
        self.max_hands = max_hands
        self.detection_confidence = detection_confidence
        self.tracking_confidence = tracking_confidence

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(static_image_mode=self.mode, max_num_hands=self.max_hands,
                                         min_detection_confidence=self.detection_confidence,
                                         min_tracking_confidence=self.tracking_confidence)
        self.mp_drawing = mp.solutions.drawing_utils
        self.tip_index = [4, 8, 12, 16, 20]

    def find_hands(self, image, draw=True):
        # Flip the image horizontally for later selfie-view display
        # Convert the BGR to RGB
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

        # To improve performance, optionally mark the image as not writeable
        # Pass by reference
        image.flags.writeable = False

        # Process the image and find hands
        results = self.hands.process(image)

        # Set the image as writeable again
        image.flags.writeable = True

        # Draw the hand annotations on the image
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        self.multi_hand_landmarks = results.multi_hand_landmarks

        if self.multi_hand_landmarks:
            for hand_Landmarks in self.multi_hand_landmarks:
                if draw:
                    self.mp_drawing.draw_landmarks(image, hand_Landmarks, self.mp_hands.HAND_CONNECTIONS,
                                                   self.mp_drawing.DrawingSpec(color=(0, 220, 255), thickness=4,
                                                                               circle_radius=3),
                                                   self.mp_drawing.DrawingSpec(color=(255, 220, 0), thickness=2,
                                                                               circle_radius=5))

        return image

    def find_position(self, image, hand_number=0, draw=True):
        x_list = []
        y_list = []
        bbox = []

        self.landmark_list = []
        if self.multi_hand_landmarks:
            hand_landmarks = self.multi_hand_landmarks[hand_number]
            for index, lm in enumerate(hand_landmarks.landmark):
                # print(id, lm)
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                x_list.append(cx)
                y_list.append(cy)
                # print(id, cx, cy)
                self.landmark_list.append([index, cx, cy])
                if draw:
                    if index in [4, 8, 12, 16, 20]:
                        cv2.circle(image, (cx, cy), 7, (133, 21, 199), cv2.FILLED)

            x_minimum, x_maximum = min(x_list), max(x_list)
            y_minimum, y_maximum = min(y_list), max(y_list)
            bbox = x_minimum, y_minimum, x_maximum, y_maximum

            if draw:
                cv2.rectangle(image, (x_minimum - 20, y_minimum - 20), (x_maximum + 20, y_maximum + 20),
                              (140, 180, 210), 2)

        return self.landmark_list, bbox

    def fingers_up(self):
        finger_list = []
        # Thumb
        if self.landmark_list[self.tip_index[0][1]] > self.landmark_list[self.tip_index[0] - 1][1]:
            finger_list.append(1)
        else:
            finger_list.append(0)

        # Fingers
        for index in range(1, 5):
            if self.landmark_list[self.tip_index[index]][2] < self.landmark_list[self.tip_index[index] - 2][2]:
                finger_list.append(1)
            else:
                finger_list.append(0)

        # total_fingers = finger_list.count(1)

        return finger_list

    def find_distance(self, p1, p2, image, draw=True, radius=8, thickness=3):
        x1, y1 = self.landmark_list[p1][1:]
        x2, y2 = self.landmark_list[p2][1:]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        if draw:
            cv2.line(image, (x1, y1), (x2, y2), (255, 0, 255), thickness, cv2.LINE_AA)
            cv2.circle(image, (x1, y1), radius, (255, 0, 255), cv2.FILLED)
            cv2.circle(image, (x2, y2), radius, (255, 0, 255), cv2.FILLED)
            cv2.circle(image, (cx, cy), radius, (255, 0, 255), cv2.FILLED)
        distance = math.hypot(x2 - x1, y2 - y1)

        return distance, image, [x1, x2, x2, y2, cx, cy]


def main():
    cap = cv2.VideoCapture(0)
    detector = HandDetector()
    while cap.isOpened():

        _, image = cap.read()

        start = time.time()

        image = detector.find_hands(image)
        landmark_list, bbox = detector.find_position(image)
        if len(landmark_list) != 0:
            print(landmark_list[4])

        end = time.time()
        totalTime = end - start

        fps = 1 / totalTime

        cv2.putText(image, str(int(fps)), (10, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 166))

        cv2.imshow("MediaPipe Hands", image)

        if cv2.waitKey(5) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
