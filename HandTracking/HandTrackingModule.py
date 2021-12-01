import cv2
import time
import mediapipe as mp


class HandDetector:
    def __init__(self, mode=False, max_hands=2, detection_confidence=0.5, tracking_confidence=0.5):
        self.multiHandLandMarks = None
        self.mode = mode
        self.maxHands = max_hands
        self.detectionCon = detection_confidence
        self.trackCon = tracking_confidence

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(static_image_mode=self.mode, max_num_hands=self.maxHands,
                                         min_detection_confidence=self.detectionCon,
                                         min_tracking_confidence=self.trackCon)
        self.mp_drawing = mp.solutions.drawing_utils

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

        self.multiHandLandMarks = results.multi_hand_landmarks

        if self.multiHandLandMarks:
            for hand_Landmarks in self.multiHandLandMarks:
                if draw:
                    self.mp_drawing.draw_landmarks(image, hand_Landmarks, self.mp_hands.HAND_CONNECTIONS,
                                                   self.mp_drawing.DrawingSpec(color=(0, 220, 255), thickness=4,
                                                                               circle_radius=3),
                                                   self.mp_drawing.DrawingSpec(color=(255, 220, 0), thickness=2,
                                                                               circle_radius=5))

        return image

    def find_position(self, image, hand_number=0, draw=True):
        landmark_list = []

        if self.multiHandLandMarks:
            hand_landmarks = self.multiHandLandMarks[hand_number]
            for index, lm in enumerate(hand_landmarks.landmark):
                # print(id, lm)
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                landmark_list.append([index, cx, cy])
                if draw:
                    if index in [4, 8, 12, 16, 20]:
                        cv2.circle(image, (cx, cy), 6, (255, 0, 255), cv2.FILLED)

        return landmark_list


def main():
    cap = cv2.VideoCapture(0)
    detector = HandDetector()
    while cap.isOpened():

        _, image = cap.read()

        start = time.time()

        image = detector.find_hands(image)
        detector.find_position(image)

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
