import cv2
import time
import pygame
import numpy as np
from HandTracking.HandTrackingModule import HandDetector
from GameModule.JotyModule import JotySays

# Declare screen and cv dimensions
wCam, hCam = 640, 480

# Margin for better interactions with hand tracking module
frame_margin = 70

# Configure the camera and its dimensions
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

# Set up pygame
pygame.init()
pygame.mixer.init()

# Create an instance of the hand tracking module
detector = HandDetector(max_hands=1)
joty = JotySays()

# Game Screen
pygame.display.set_icon(joty.logo)
pygame.display.set_caption("Joty says")

# Pygame startup
logo_bob = 150
waiting = True
joty.menu_music.play(-1)
joty.cursor.set_cursor(pygame.cursors.broken_x)
joty.cursor.set_pos(joty.width // 2, joty.height // 2)
title_text = joty.title_font.render('Simon', True, joty.white)

bob_direction = True  # true = down, false = up

# Menu game screen
while waiting:
    success, image = cap.read()
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    if not success:
        print("Ignoring empty camera frame.")
        # If loading a video, use 'break' instead of 'continue'.
        continue

    # Red color detector
    low_red = np.array([161, 155, 84])
    high_red = np.array([179, 255, 255])
    red_mask = cv2.inRange(hsv_image, low_red, high_red)
    contours, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)

    image = detector.find_hands(image, draw=True)
    landmark_list, bbox = detector.find_position(image, draw=True)

    if len(landmark_list) != 0:
        fingers = detector.fingers_up()
        # print(fingers)
        area = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1]) // 100

        cv2.rectangle(image, (frame_margin, frame_margin), (wCam - frame_margin, hCam - frame_margin), (255, 0, 255), 2)

        if 150 < area < 1080:
            distance, image, line_info = detector.find_distance(4, 8, image)
            x_relative = np.interp(line_info[4], (frame_margin, wCam - frame_margin), (0, joty.width - 10))
            y_relative = np.interp(line_info[5], (frame_margin, hCam - frame_margin), (0, joty.height - 10))
            joty.cursor.set_pos((x_relative, y_relative))
            if distance > 70:
                cv2.circle(image, (line_info[4], line_info[5]), 8, (0, 255, 160), cv2.FILLED)
            elif distance > 40:
                cv2.circle(image, (line_info[4], line_info[5]), 8, (0, 160, 255), cv2.FILLED)
            else:
                cv2.circle(image, (line_info[4], line_info[5]), 8, (255, 160, 0), cv2.FILLED)
                pos = joty.cursor.get_pos()
                x = pos[0]
                y = pos[1]
                if 180 <= x <= 420 and 530 <= y <= 620:
                    joty.menu_music.stop()
                    waiting = False

    # Reset pygame screen
    joty.screen.fill(joty.black)

    # Display assets
    joty.screen.blit(title_text, (220, 50))
    joty.screen.blit(joty.big_logo, (150, logo_bob))
    joty.screen.blit(joty.start_button, (180, 530))
    pygame.display.update()

    if logo_bob == 150:
        bob_direction = True
    elif logo_bob == 190:
        bob_direction = False

    if bob_direction:
        logo_bob += 0.5
    else:
        logo_bob -= 0.5

    joty.clock.tick(60)

    cv2.imshow("MediaPipe Hands", image)
    cv2.imshow("Mask", red_mask)

    if cv2.waitKey(5) & 0xFF == 27:
        joty.quit_game()
        break

# Game running
while joty.running:

    success, image = cap.read()
    cv2.imshow("MediaPipe Hands", image)

    # Generate a new pattern
    joty.new_pattern()
    # Display the pattern
    joty.show_pattern()

    turn_time = time.time()
    player_pattern = []

    joty.time_delay = 500 - 100 * int(len(joty.pattern) / 5)
    if joty.time_delay <= 100:
        joty.time_delay = 100

    while time.time() <= turn_time + 6 and len(player_pattern) < len(joty.pattern):
        success, image = cap.read()
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue

        # Red color
        low_red = np.array([161, 155, 84])
        high_red = np.array([179, 255, 255])
        red_mask = cv2.inRange(hsv_image, low_red, high_red)
        contours, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)

        image = detector.find_hands(image, draw=True)
        landmark_list, bbox = detector.find_position(image, draw=True)

        if len(landmark_list) != 0:
            fingers = detector.fingers_up()
            # print(fingers)
            area = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1]) // 100

            cv2.rectangle(image, (frame_margin, frame_margin), (wCam - frame_margin, hCam - frame_margin),
                          (255, 0, 255), 2)

            if 150 < area < 1080:
                distance, image, line_info = detector.find_distance(4, 8, image)
                x_relative = np.interp(line_info[4], (frame_margin, wCam - frame_margin), (0, joty.width - 10))
                y_relative = np.interp(line_info[5], (frame_margin, hCam - frame_margin), (0, joty.height - 10))
                joty.cursor.set_pos((x_relative, y_relative))
                if distance > 70:
                    cv2.circle(image, (line_info[4], line_info[5]), 8, (0, 255, 160), cv2.FILLED)
                elif distance > 40:
                    cv2.circle(image, (line_info[4], line_info[5]), 8, (0, 160, 255), cv2.FILLED)
                else:
                    cv2.circle(image, (line_info[4], line_info[5]), 8, (255, 160, 0), cv2.FILLED)
                    pos = joty.cursor.get_pos()
                    x = pos[0]
                    y = pos[1]
                    if 50 < x < 300 and 150 < y < 400:
                        joty.draw_screen(green_light=joty.green_light)
                        player_pattern, turn_time = joty.click_display(player_pattern, 1, joty.green_sound)
                    elif 300 < x < 550 and 150 < y < 400:
                        joty.draw_screen(red_light=joty.red_light)
                        player_pattern, turn_time = joty.click_display(player_pattern, 2, joty.red_sound)
                    elif 50 < x < 300 and 400 < y < 650:
                        joty.draw_screen(yellow_light=joty.yellow_light)
                        player_pattern, turn_time = joty.click_display(player_pattern, 3, joty.yellow_sound)
                    elif 300 < x < 550 and 400 < y < 650:
                        joty.draw_screen(blue_light=joty.blue_light)
                        player_pattern, turn_time = joty.click_display(player_pattern, 4, joty.blue_sound)
        cv2.imshow("MediaPipe Hands", image)
        cv2.imshow("Mask", red_mask)

        if cv2.waitKey(5) & 0xFF == 27:
            joty.quit_game()
            break

    image = cv2.imread("resources/Images/simon_logo.png")
    image = cv2.resize(image, (wCam, hCam))
    cv2.imshow("MediaPipe Hands", image)
    if not time.time() <= turn_time + 3:
        joty.lose_screen()

joty.quit_game()
