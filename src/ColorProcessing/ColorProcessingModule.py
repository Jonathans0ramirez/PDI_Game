import cv2
import numpy as np


class ColorProcessingModule:
    def __init__(self, low_color, high_color):
        self.x_medium = 0
        self.y_medium = 0
        self.low_color = np.array(low_color)
        self.high_color = np.array(high_color)

    def transform_color(self, image):
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        color_mask = cv2.inRange(hsv_image, self.low_color, self.high_color)
        bitwise_color = cv2.bitwise_and(image, image, mask=color_mask)
        return image, color_mask, bitwise_color

    def generate_contour(self, image):
        image, color_mask, bitwise_color = self.transform_color(image)
        contours, _ = cv2.findContours(color_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)

        for cnt in contours:
            (x, y, w, h) = cv2.boundingRect(cnt)
            self.x_medium = (x + x + w) // 2
            self.y_medium = (y + y + h) // 2
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            break

        return image, bitwise_color, color_mask, self.x_medium, self.y_medium
