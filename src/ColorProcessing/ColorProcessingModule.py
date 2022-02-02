import cv2
import numpy as np


class ColorProcessingModule:
    def __init__(self, low_color, high_color):
        # Declare the variables x_medium and y_medium, which will be the center of the contour found next
        self.x_medium = 0
        self.y_medium = 0
        # Create numpy arrays based on the HSV colors parameters
        self.low_color = np.array(low_color)
        self.high_color = np.array(high_color)

    def transform_color(self, image):
        # Convert the camera image from BGR color space to HSV color space
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        # Create a mask to detect the object based on HSV Range Values
        color_mask = cv2.inRange(hsv_image, self.low_color, self.high_color)
        # Mask applied to the camera image
        bitwise_color = cv2.bitwise_and(image, image, mask=color_mask)
        return image, color_mask, bitwise_color

    def generate_contour(self, image):
        image, color_mask, bitwise_color = self.transform_color(image)
        # Get the contours in the mask of the color detected
        contours, _ = cv2.findContours(color_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        #  Sort the contours descending to get the biggest contour in the next step
        contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)

        # Take and draw the biggest one
        for cnt in contours:
            # Get all the dimensions from the contour
            (x, y, w, h) = cv2.boundingRect(cnt)
            # Calculate the center of the rectangle contour
            self.x_medium = (x + x + w) // 2
            self.y_medium = (y + y + h) // 2
            # Draw rectangle with the dimensions of the contour
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            break

        return image, bitwise_color, color_mask, self.x_medium, self.y_medium
