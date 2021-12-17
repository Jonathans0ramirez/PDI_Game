import time

import cv2
import numpy as np
import pygame

from src.HandTracking.HandTrackingModule import HandDetector
from src.Sprites.Menu.Logo import Logo
from src.Sprites.Menu.Start import Start
from src.Sprites.Menu.Title import Title


class Menu:
    def __init__(self, cam_width=640, cam_height=480, screen_width=1024, screen_height=683, max_hands=1,
                 cursor=pygame.mouse):
        # Declare screen and cv dimensions
        self.wCam = cam_width
        self.hCam = cam_height
        self.wScreen = screen_width
        self.hScreen = screen_height
        # Margin for better interactions with hand tracking module
        self.frame_margin = 70
        # Image from camera source
        self.image = None
        # Creating the sprites
        self.title_sprite = Title(220, 50)
        self.logo_sprite = Logo(150, 150)
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
        # Flag for pausing purposes
        self.paused = False
        self.limiter = 0
        # For breaking module
        self.running = True
        # Creating the sprites and groups
        self.moving_sprites = pygame.sprite.Group()
        self.moving_sprites.add(self.title_sprite, self.logo_sprite, self.start_sprite)
        print("INIT")

    def pause_program(self, limit=10):
        self.limiter += 1
        if self.limiter == limit:
            self.limiter = 0
            return False
        return True

    def start_menu(self, cap):
        success, self.image = cap.read()

        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            return True

        self.start = time.time()

        self.image = self.detector.find_hands(self.image, draw=True)
        self.landmark_list, self.bbox = self.detector.find_position(self.image, draw=True)
        self.screen.fill((0, 0, 0))
        self.moving_sprites.draw(self.screen)
        if self.paused:
            self.paused = self.pause_program()

        if len(self.landmark_list) != 0:
            self.fingers = self.detector.fingers_up()
            # print(self.fingers)
            area = (self.bbox[2] - self.bbox[0]) * (self.bbox[3] - self.bbox[1]) // 100

            cv2.rectangle(self.image, (self.frame_margin, self.frame_margin),
                          (self.wCam - self.frame_margin, self.hCam - self.frame_margin), (255, 0, 255), 2)

            if 150 < area < 1080:
                distance, self.image, line_info = self.detector.find_distance(4, 8, self.image)
                x_relative = np.interp(line_info[4], (self.frame_margin, self.wCam - self.frame_margin),
                                       (0, self.wScreen - 10))
                y_relative = np.interp(line_info[5], (self.frame_margin, self.hCam - self.frame_margin),
                                       (0, self.hScreen - 10))
                self.cursor.set_pos((x_relative, y_relative))
                if distance > 70:
                    cv2.circle(self.image, (line_info[4], line_info[5]), 8, (0, 255, 160), cv2.FILLED)
                elif distance > 40:
                    cv2.circle(self.image, (line_info[4], line_info[5]), 8, (0, 160, 255), cv2.FILLED)
                else:
                    cv2.circle(self.image, (line_info[4], line_info[5]), 8, (255, 160, 0), cv2.FILLED)
                    if 180 <= x_relative <= 420 and 530 <= y_relative <= 620 and not self.paused:
                        self.paused = self.pause_program()
                        self.running = False

                    # print(f"x_relative: {x_relative}; y_relative: {y_relative}")

        self.end = time.time()
        self.total_time = self.end - self.start

        fps = 1 / self.total_time
        self.moving_sprites.update(0.25)
        pygame.display.flip()
        self.clock.tick(60)

        cv2.putText(self.image, str(int(fps)), (10, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 166))

        cv2.imshow("MediaPipe Hands", self.image)

        if cv2.waitKey(5) & 0xFF == 27:
            return False
        if not self.running:
            return False
        return True
