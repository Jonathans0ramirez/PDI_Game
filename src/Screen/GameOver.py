import time

import cv2
import numpy as np
import pygame

from src.ColorProcessing.ColorProcessingModule import ColorProcessingModule
from src.Enums.ColorValues import ColorValues
from src.HandTracking.HandTrackingModule import HandDetector
from src.Enums.ApplicationState import ApplicationState
from src.Sprites.GameOver.Again import Again
from src.Sprites.GameOver.Score import Score
from src.Sprites.GameOver.Title import Title
from src.Sprites.GameOver.Exit import Exit
from src.Utils.CollisionUtility import collision_box_check


class GameOver:
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
        # Font file loading and size
        self.gameplay_font_dir = 'resources/Fonts/Gameplay.ttf'
        self.title_font = pygame.font.Font(self.gameplay_font_dir, 50)
        # Creating the necessary sprites
        self.title_sprite = Title(161.5, 50)
        self.score_sprite = Score(600, 120)
        self.again_sprite = Again(180, 300)
        self.exit_sprite = Exit(180, 450)
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
        # Variables for cursor position (Init at center of the screen)n
        self.x_relative = self.wScreen / 2
        self.y_relative = self.hScreen / 2
        # Flag for pausing purposes
        self.paused = False
        self.limiter = 0
        # For breaking module
        self.running = True
        # Creating the sprites and grouped by layers to better display the images
        self.moving_sprites = pygame.sprite.Group()
        self.moving_sprites.add(self.title_sprite, self.score_sprite, self.again_sprite, self.exit_sprite)
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

    def lose_screen(self, cap, score):
        success, self.image = cap.read()
        # Flip the image horizontally for later selfie-view display
        self.image = cv2.flip(self.image, 1)
        self.image, bitwise_color, _, x_medium, y_medium = self.blue.generate_contour(self.image)

        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            return ApplicationState.MUSIC_BREAK

        self.x_relative = np.interp(x_medium, (self.frame_margin, self.wCam - self.frame_margin),
                                    (0, self.wScreen - 10))
        self.y_relative = np.interp(y_medium, (self.frame_margin, self.hCam - self.frame_margin),
                                    (0, self.hScreen - 10))
        self.cursor.set_pos((self.x_relative, self.y_relative))


        self.start = time.time()

        self.image = self.detector.find_hands(self.image, draw=True)
        self.landmark_list, self.bbox = self.detector.find_position(self.image, draw=True)
        self.screen.fill((0, 0, 0))
        self.score_sprite.rect.topleft = [((600 - self.title_font.size('Score: ' + str(score))[0]) / 2), 120]
        self.moving_sprites.draw(self.screen)
        if self.paused:
            self.paused = self.pause_program()

        if len(self.landmark_list) != 0:
            area = (self.bbox[2] - self.bbox[0]) * (self.bbox[3] - self.bbox[1]) // 100

            cv2.rectangle(self.image, (self.frame_margin, self.frame_margin),
                          (self.wCam - self.frame_margin, self.hCam - self.frame_margin), (255, 0, 255), 2)

            if 150 < area < 1080:
                self.fingers = self.detector.fingers_up()
                if self.fingers[1] and self.fingers[2]:
                    if collision_box_check(self.again_sprite.rect.topleft, self.again_sprite.rect.size,
                                           (self.x_relative, self.y_relative)) and not self.paused:
                        print("AGAIN")
                        self.paused = self.pause_program()
                        return ApplicationState.RESTART
                    if collision_box_check(self.exit_sprite.rect.topleft, self.exit_sprite.rect.size,
                                           (self.x_relative, self.y_relative)) and not self.paused:
                        print("EXIT")
                        self.paused = self.pause_program()
                        self.running = False

                    # print(f"x_relative: {x_relative}; y_relative: {y_relative}")

        self.end = time.time()
        self.total_time = self.end - self.start

        fps = 1 / self.total_time
        self.moving_sprites.update(score)
        pygame.display.flip()
        self.clock.tick(60)

        cv2.putText(self.image, str(int(fps)), (10, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 166))

        cv2.imshow("MediaPipe Hands", self.image)
        cv2.imshow("Mask", bitwise_color)

        if cv2.waitKey(5) & 0xFF == 27:
            return ApplicationState.STOP
        if not self.running:
            return ApplicationState.MUSIC_BREAK
        return ApplicationState.RUNNING
