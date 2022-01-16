import random
import time

import cv2
import numpy as np
import pygame

from src.Enums.ApplicationState import ApplicationState
from src.HandTracking.HandTrackingModule import HandDetector
from src.Sprites.Game.Blue import Blue
from src.Sprites.Game.Green import Green
from src.Sprites.Game.Red import Red
from src.Sprites.Game.Yellow import Yellow

from src.Utils.CollisionUtility import collision_box_check


class Game:
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
        # Channel audio for colors
        self.channel_blue = pygame.mixer.Channel(2)
        self.channel_green = pygame.mixer.Channel(3)
        self.channel_red = pygame.mixer.Channel(4)
        self.channel_yellow = pygame.mixer.Channel(5)
        self.sound_blue = pygame.mixer.Sound("resources/Audio/blue.ogg")
        self.sound_green = pygame.mixer.Sound("resources/Audio/green.ogg")
        self.sound_red = pygame.mixer.Sound("resources/Audio/red.ogg")
        self.sound_yellow = pygame.mixer.Sound("resources/Audio/yellow.ogg")
        self.sound_lose = pygame.mixer.Sound("resources/Audio/lose_sfx.wav")
        # Font
        self.gameplay_font_dir = 'resources/Fonts/Gameplay.ttf'
        self.font = pygame.font.Font(self.gameplay_font_dir, 20)
        # Creating the sprites
        self.blue = Blue()
        self.red = Red()
        self.green = Green()
        self.yellow = Yellow()
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
        # Cursor from pygame to access the functions of it
        self.cursor = cursor
        # For fps information
        self.start = 0
        self.end = 0
        self.total_time = 0
        # Flag for pausing purposes
        self.paused = False
        self.limiter = 0
        self.limit = 20
        # Creating the sprites and groups
        self.moving_sprites = pygame.sprite.Group()
        self.moving_sprites.add(self.blue, self.red, self.green, self.yellow)
        # Variable to create and show a new pattern
        self.pattern = []
        self.pattern_copy = []
        self.player_pattern = []
        self.score = 0
        self.player_pattern_is_good = True
        self.playing_pattern = False
        self.add_new_pattern = True
        self.show_new_pattern = True

    def check_pattern(self):
        if self.player_pattern != self.pattern[:len(self.player_pattern)]:
            return False
        return True

    def pause_program(self):
        self.limiter += 1
        if self.limiter == self.limit:
            self.limiter = 0
            return False
        return True

    def start_game(self, cap):
        success, self.image = cap.read()

        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            return ApplicationState.BREAK

        self.start = time.time()

        self.image = self.detector.find_hands(self.image, draw=True)
        self.landmark_list, self.bbox = self.detector.find_position(self.image, draw=True)
        self.screen.fill((0, 0, 0))
        self.moving_sprites.draw(self.screen)
        score_text = self.font.render('Score: ' + str(self.score), True, (255, 255, 255))
        text_width, _ = score_text.get_size()
        self.screen.blit(score_text, (((self.wScreen // 2) - (text_width // 2)), 50))

        # Recalculate paused flag
        if self.paused:
            self.paused = self.pause_program()

        # Clean channels and color blocks
        if not self.channel_blue.get_busy():
            self.blue.change_color(False)
            self.channel_blue.stop()
        if not self.channel_red.get_busy():
            self.red.change_color(False)
            self.channel_red.stop()
        if not self.channel_green.get_busy():
            self.green.change_color(False)
            self.channel_green.stop()
        if not self.channel_yellow.get_busy():
            self.yellow.change_color(False)
            self.channel_yellow.stop()

        # Restart variables for new pattern and flag for losing screen
        if not self.paused and not self.player_pattern_is_good:
            print("You've failed")
            return ApplicationState.BREAK
        elif len(self.pattern) == len(self.player_pattern):
            self.player_pattern = []
            self.add_new_pattern = True

        # Generate a new color for the pattern
        if self.add_new_pattern and len(self.pattern_copy) == 0 and not self.paused:
            self.score = len(self.pattern)
            self.pattern.append(random.randint(1, 4))
            print(self.pattern)
            self.pattern_copy = self.pattern.copy()
            self.add_new_pattern = False
            self.show_new_pattern = False if self.paused else True

        # Color and sound blocks
        if self.show_new_pattern and len(
                self.pattern_copy) != 0 and not self.paused:  # len of player and patter are different
            number_color = self.pattern_copy[0]
            # Set a limit for the pause_program based on the pattern length
            self.limit = 20 - 1 * int(len(self.pattern) / 4)
            if self.limit <= 10:
                self.limit = 10
            # Clear channels and sprites of buttons
            self.blue.change_color(False)
            self.channel_blue.stop()
            self.red.change_color(False)
            self.channel_red.stop()
            self.green.change_color(False)
            self.channel_green.stop()
            self.yellow.change_color(False)
            self.channel_yellow.stop()
            self.paused = self.pause_program()
            # Start the sequence show
            if number_color == 1:
                self.green.change_color(True)
                # if not self.channel_green.get_busy():
                self.channel_green.play(self.sound_green)
            if number_color == 2:
                self.red.change_color(True)
                # if not self.channel_red.get_busy():
                self.channel_red.play(self.sound_red)
            if number_color == 3:
                self.yellow.change_color(True)
                # if not self.channel_yellow.get_busy():
                self.channel_yellow.play(self.sound_yellow)
            if number_color == 4:
                self.blue.change_color(True)
                # if not self.channel_blue.get_busy():
                self.channel_blue.play(self.sound_blue)

            self.pattern_copy.pop(0)
            if len(self.pattern_copy) == 0:
                self.limiter = 0
                self.limit = 15
                self.paused = self.pause_program()
                self.show_new_pattern = False

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
                elif not self.paused:
                    cv2.circle(self.image, (line_info[4], line_info[5]), 8, (255, 160, 0), cv2.FILLED)

                    #     GREEN
                    if collision_box_check(self.green.rect.topleft, self.green.rect.size, (x_relative, y_relative)):
                        self.limit = 20
                        self.paused = self.pause_program()
                        self.green.change_color(True)
                        self.player_pattern.append(1)
                        self.player_pattern_is_good = self.check_pattern()
                        if self.player_pattern_is_good:
                            if not self.channel_green.get_busy():
                                self.channel_green.play(self.sound_green)
                        else:
                            if not self.channel_green.get_busy():
                                self.channel_green.play(self.sound_lose)

                    #     RED
                    elif collision_box_check(self.red.rect.topleft, self.red.rect.size, (x_relative, y_relative)):
                        self.limit = 20
                        self.paused = self.pause_program()
                        self.red.change_color(True)
                        self.player_pattern.append(2)
                        self.player_pattern_is_good = self.check_pattern()
                        if self.player_pattern_is_good:
                            if not self.channel_red.get_busy():
                                self.channel_red.play(self.sound_red)
                        else:
                            if not self.channel_red.get_busy():
                                self.channel_red.play(self.sound_lose)

                    #     YELLOW
                    elif collision_box_check(self.yellow.rect.topleft, self.yellow.rect.size, (x_relative, y_relative)):
                        self.limit = 20
                        self.paused = self.pause_program()
                        self.yellow.change_color(True)
                        self.player_pattern.append(3)
                        self.player_pattern_is_good = self.check_pattern()
                        if self.player_pattern_is_good:
                            if not self.channel_yellow.get_busy():
                                self.channel_yellow.play(self.sound_yellow)
                        else:
                            if not self.channel_yellow.get_busy():
                                self.channel_yellow.play(self.sound_lose)

                    #     BLUE
                    elif collision_box_check(self.blue.rect.topleft, self.blue.rect.size, (x_relative, y_relative)):
                        self.limit = 20
                        self.paused = self.pause_program()
                        self.blue.change_color(True)
                        self.player_pattern.append(4)
                        self.player_pattern_is_good = self.check_pattern()
                        if self.player_pattern_is_good:
                            if not self.channel_blue.get_busy():
                                self.channel_blue.play(self.sound_blue)
                        else:
                            if not self.channel_blue.get_busy():
                                self.channel_blue.play(self.sound_lose)

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
            return ApplicationState.STOP
        return ApplicationState.RUNNING
