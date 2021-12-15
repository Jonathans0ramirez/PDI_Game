import cv2
import sys
import time
import pygame
import random
import numpy as np
from Sprites.Player import Player
from Sprites.Menu.Title import Title
from Sprites.Menu.Logo import Logo
from Sprites.Menu.Start import Start
from Sprites.Game.Blue import Blue
from Sprites.Game.Red import Red
from HandTracking.HandTrackingModule import HandDetector

# Declare screen and cv dimensions
wCam, hCam = 640, 480
wScreen, hScreen = 1024, 683

# Margin for better interactions with hand tracking module
frame_margin = 70

# Configure the camera and its dimensions
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

# Set up pygame
pygame.init()
pygame.mixer.init()

# Music
pygame.mixer.music.load('resources/Audio/artblock.ogg')

# Creating the sprites and groups
moving_sprites = pygame.sprite.Group()
moving_sprites_SAPO = pygame.sprite.Group()
player = Player(100, 100)
title = Title(220, 50)
logo = Logo(150, 150)
start = Start(180, 530)
blue = Blue()
red = Red()
moving_sprites.add(title, logo, start)
moving_sprites_SAPO.add(player)
copy_spr = moving_sprites.copy()

# Create an instance of the hand tracking module
detector = HandDetector(max_hands=1)

# Game Screen
screen = pygame.display.set_mode((wScreen, hScreen))
clock = pygame.time.Clock()
cursor = pygame.mouse
cursor.set_cursor(pygame.cursors.broken_x)
pygame.display.set_icon(logo.logo)
pygame.display.set_caption("Joty says")

# Start music
pygame.mixer.music.play()
channel_blue = pygame.mixer.Channel(2)
channel_green = pygame.mixer.Channel(3)
channel_red = pygame.mixer.Channel(4)
channel_yellow = pygame.mixer.Channel(5)
sound_blue = pygame.mixer.Sound("resources/Audio/blue.wav")
sound_green = pygame.mixer.Sound("resources/Audio/green.wav")
sound_red = pygame.mixer.Sound("resources/Audio/red.wav")
sound_yellow = pygame.mixer.Sound("resources/Audio/yellow.wav")

# Game info
user_checked = False
score = 0
pattern = [random.randint(1, 4)]
player_pattern = []
for_pausing = 0
paused = False


def pause_program(limit, limiter):
    limiter += 1
    if limiter == limit:
        limiter = 0
        return limiter, False
    return limiter, True


# Run while camera is streaming
while cap.isOpened():

    success, image = cap.read()

    if not success:
        print("Ignoring empty camera frame.")
        # If loading a video, use 'break' instead of 'continue'.
        continue

    start = time.time()

    image = detector.find_hands(image, draw=True)
    landmark_list, bbox = detector.find_position(image, draw=True)
    screen.fill((0, 0, 0))
    moving_sprites.draw(screen)

    if paused:
        for_pausing, paused = pause_program(10, for_pausing)
    else:
        blue.change_color(False)
        red.change_color(False)
        if channel_blue.get_busy():
            channel_blue.stop()
        if channel_red.get_busy():
            channel_red.stop()

    if len(landmark_list) != 0:
        fingers = detector.fingers_up()
        # print(fingers)
        area = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1]) // 100

        cv2.rectangle(image, (frame_margin, frame_margin), (wCam - frame_margin, hCam - frame_margin), (255, 0, 255), 2)

        if 150 < area < 1080:
            distance, image, line_info = detector.find_distance(4, 8, image)
            x_relative = np.interp(line_info[4], (frame_margin, wCam - frame_margin), (0, wScreen - 10))
            y_relative = np.interp(line_info[5], (frame_margin, hCam - frame_margin), (0, hScreen - 10))
            cursor.set_pos((x_relative, y_relative))
            if distance > 70:
                cv2.circle(image, (line_info[4], line_info[5]), 8, (0, 255, 160), cv2.FILLED)
            elif distance > 40:
                cv2.circle(image, (line_info[4], line_info[5]), 8, (0, 160, 255), cv2.FILLED)
            else:
                cv2.circle(image, (line_info[4], line_info[5]), 8, (255, 160, 0), cv2.FILLED)
                if len(player_pattern) == len(pattern) and user_checked:
                    score = len(pattern)
                    pattern.append(random.randint(1, 4))
                    user_checked = False
                if 180 <= x_relative <= 420 and 530 <= y_relative <= 620 and not paused:
                    for_pausing, paused = pause_program(10, for_pausing)
                    moving_sprites.add(blue, red)
                    blue.change_color(True)
                    red.change_color(True)
                    player.attack()
                    if not channel_blue.get_busy():
                        channel_blue.play(sound_blue)
                    if not channel_red.get_busy():
                        channel_red.play(sound_red)
                    player_pattern.append(random.randint(1, 4))
                    print("On bounds")
                    if player_pattern == pattern[:len(player_pattern)]:
                        print("Increíble")
                        user_checked = True
                    else:
                        print(f"Perdiste. {player_pattern}")
                        player_pattern.pop()

                # print(f"x_relative: {x_relative}; y_relative: {y_relative}")

    end = time.time()
    totalTime = end - start

    fps = 1 / totalTime
    moving_sprites.update(0.25)
    pygame.display.flip()
    clock.tick(60)

    cv2.putText(image, str(int(fps)), (10, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 166))

    cv2.imshow("MediaPipe Hands", image)

    if cv2.waitKey(5) & 0xFF == 27:
        break

pygame.quit()
cap.release()
cv2.destroyAllWindows()
