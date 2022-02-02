import time

import cv2
import numpy as np
import pygame

from src.ColorProcessing.ColorProcessingModule import ColorProcessingModule
from src.Enums.ApplicationState import ApplicationState
from src.Enums.ColorValues import ColorValues
from src.HandTracking.HandTrackingModule import HandDetector
from src.Sprites.Menu.Logo import Logo
from src.Sprites.Menu.Start import Start
from src.Utils.CollisionUtility import collision_box_check


class Menu:
    def __init__(self, cam_width=640, cam_height=480, screen_width=600, screen_height=683, max_hands=1,
                 cursor=pygame.mouse):
        # Declare screen and cv dimensions
        self.wCam = cam_width
        self.hCam = cam_height
        self.wScreen = screen_width
        self.hScreen = screen_height
        # Margin for better interactions with hand tracking module and color processing module
        self.frame_margin = 70
        # Image from camera source
        self.image = None
        # Creating the necessary sprites
        self.logo_sprite = Logo(0, 0)
        self.start_sprite = Start(180, 530)
        # Sprite group
        self.moving_sprites = pygame.sprite.Group()
        # Create an instance of the hand tracking module
        self.detector = HandDetector(max_hands=max_hands)
        # Detector variables
        self.landmark_list = None
        self.bbox = None
        self.fingers = None
        # Game screen
        self.screen = pygame.display.set_mode((self.wScreen, self.hScreen))
        # Clock from pygame
        self.clock = pygame.time.Clock()
        # For fps information
        self.start = 0
        self.end = 0
        self.total_time = 0
        # Cursor from pygame to access the functions of it
        self.cursor = cursor
        # Variables for cursor position (Init at center of the screen)
        self.x_relative = self.wScreen / 2
        self.y_relative = self.hScreen / 2
        # Flag for pausing purposes
        self.paused = False
        self.limiter = 0
        # For breaking module
        self.running = True
        # Creating the sprites and grouped by layers to better display the images
        self.moving_sprites = pygame.sprite.Group()
        self.moving_sprites.add(self.logo_sprite, self.start_sprite)
        # Color processing module variables for each color
        self.green = ColorProcessingModule(ColorValues.LOW_GREEN.value, ColorValues.HIGH_GREEN.value)
        self.red = ColorProcessingModule(ColorValues.LOW_RED.value, ColorValues.HIGH_RED.value)
        self.yellow = ColorProcessingModule(ColorValues.LOW_YELLOW.value, ColorValues.HIGH_YELLOW.value)
        self.blue = ColorProcessingModule(ColorValues.LOW_BLUE.value, ColorValues.HIGH_BLUE.value)

    # Function to handle pauses needed by the game without the need to block the main thread
    def pause_program(self, limit=10):
        self.limiter += 1
        if self.limiter == limit:
            self.limiter = 0
            return False
        return True

    def start_menu(self, cap):
        # Grab the next frame from camera and return a boolean that returns true if the frame is available
        # and the image array vector captured
        success, self.image = cap.read()
        # Flip the image horizontally for later selfie-view display
        self.image = cv2.flip(self.image, 1)
        # Get the contours of the blue color detected in the image captured
        self.image, blue_bitwise_color, _, x_medium, y_medium = self.blue.generate_contour(self.image)
        # Get the contours of extra colors for explanation purposes
        self.image, red_bitwise_color, red_mask, _, _ = self.red.generate_contour(self.image)
        self.image, green_bitwise_color, _, _, _ = self.green.generate_contour(self.image)
        self.image, yellow_bitwise_color, _, _, _ = self.yellow.generate_contour(self.image)

        # Break program if image could not be read
        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            return ApplicationState.MUSIC_BREAK

        # Assign the values of the center of the detected blue object to the cursor making an interpolation
        # based on camera and screen size with the frame margin value
        self.x_relative = np.interp(x_medium, (self.frame_margin, self.wCam - self.frame_margin),
                                    (0, self.wScreen - 10))
        self.y_relative = np.interp(y_medium, (self.frame_margin, self.hCam - self.frame_margin),
                                    (0, self.hScreen - 10))
        self.cursor.set_pos((self.x_relative, self.y_relative))

        # Start time captured for fps information
        self.start = time.time()

        # Find and draws the lines and dots of the hand
        self.image = self.detector.find_hands(self.image, draw=True)
        # Draw dots in fingers of the detected hand and returns the bbox enclosing the hand
        self.landmark_list, self.bbox = self.detector.find_position(self.image, draw=True)
        # Refreshes the screen
        self.screen.fill((0, 0, 0))
        self.moving_sprites.draw(self.screen)

        # Recalculate paused flag
        if self.paused:
            self.paused = self.pause_program()

        # Validates that at least one hand is on screen
        if len(self.landmark_list) != 0:
            # Calculates the area of the box enclosing the hand
            area = (self.bbox[2] - self.bbox[0]) * (self.bbox[3] - self.bbox[1]) // 100

            # Draw the rectangle that limits the area in which the cursor is allowed to move
            cv2.rectangle(self.image, (self.frame_margin, self.frame_margin),
                          (self.wCam - self.frame_margin, self.hCam - self.frame_margin), (255, 0, 255), 2)

            # It is validated that the detected hand is close enough to avoid confusion
            if 150 < area < 1080:
                # Fingers up detector is initialized
                self.fingers = self.detector.fingers_up()
                # If the cursor is inside the area of the start button and the index and middle fingers are up,
                # the game starts
                if collision_box_check(self.start_sprite.rect.topleft, self.start_sprite.rect.size,
                                       (self.x_relative, self.y_relative)) and not self.paused:
                    if self.fingers[1] and self.fingers[2]:
                        # Creates a micro-pause to avoid double clicks
                        self.paused = self.pause_program()
                        # Variable to stop this screen
                        self.running = False

        # End time captured for fps information
        self.end = time.time()
        # Calculates the elapsed time
        self.total_time = self.end - self.start

        # Calculates the value of fps
        fps = 1 / self.total_time

        # Update sprites and screen display
        self.moving_sprites.update()
        pygame.display.flip()

        # Limit the runtime speed of a game (60 fps maximum)
        self.clock.tick(60)

        # Write fps value on camera frame / image
        cv2.putText(self.image, str(int(fps)), (10, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 166))

        # Show the camera image and the mask
        cv2.imshow("MediaPipe Hands", self.image)
        cv2.imshow("Mask", blue_bitwise_color + red_bitwise_color + green_bitwise_color + yellow_bitwise_color)

        # Stop the running application if esc is pressed int the cv2 frame
        if cv2.waitKey(5) & 0xFF == 27:
            return ApplicationState.STOP
        if not self.running:
            self.running = True
            return ApplicationState.MUSIC_BREAK
        return ApplicationState.RUNNING
