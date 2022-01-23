import sys
import time
import pygame
import random


class JotySays:
    def __init__(self, width=1024, height=683, display=0, v_sync=32):
        self.screen = pygame.display.set_mode((width, height), display, v_sync)
        self.width = width
        self.height = height
        self.cursor = pygame.mouse
        self.clock = pygame.time.Clock()
        self.red = (100, 0, 0)
        self.red_light = (255, 0, 0)
        self.green = (0, 100, 0)
        self.green_light = (0, 255, 0)
        self.yellow = (100, 100, 0)
        self.yellow_light = (255, 255, 0)
        self.blue = (0, 0, 100)
        self.blue_light = (0, 0, 255)
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.logo = pygame.image.load('resources/Images/simon_logo.png')
        self.big_logo = pygame.transform.scale(self.logo, (300, 300))
        self.start_button = pygame.image.load('resources/Images/start_button.png')
        self.start_button = pygame.transform.scale(self.start_button, (240, 90))
        self.again_button = pygame.image.load('resources/Images/again_button.png')
        self.again_button = pygame.transform.scale(self.again_button, (240, 90))
        self.exit_button = pygame.image.load('resources/Images/exit_button.png')
        self.exit_button = pygame.transform.scale(self.exit_button, (240, 90))
        self.green_sound = pygame.mixer.Sound('resources/Audio/green.wav')
        self.red_sound = pygame.mixer.Sound('resources/Audio/red.wav')
        self.yellow_sound = pygame.mixer.Sound('resources/Audio/yellow.wav')
        self.blue_sound = pygame.mixer.Sound('resources/Audio/blue.wav')
        self.lose_sound = pygame.mixer.Sound('resources/Audio/lose_sfx.wav')
        self.menu_music = pygame.mixer.Sound('resources/Audio/artblock.ogg')
        self.gameplay_font_dir = 'resources/Fonts/Gameplay.ttf'
        self.font = pygame.font.Font(self.gameplay_font_dir, 20)
        self.title_font = pygame.font.Font(self.gameplay_font_dir, 50)
        self.score = 0
        self.pattern = []
        self.time_delay = 500
        self.running = True

    #############
    # FUNCTIONS #
    #############

    def draw_screen(self, red_light=None, green_light=None, blue_light=None, yellow_light=None):
        # refresh display
        self.screen.fill(self.black)

        # draw elements
        score_text = self.font.render('Score: ' + str(self.score), True, self.white)
        self.screen.blit(score_text, (450, 50))

        pygame.draw.rect(self.screen, green_light if green_light else self.green, pygame.Rect(50, 150, 250, 250))
        pygame.draw.rect(self.screen, red_light if red_light else self.red, pygame.Rect(300, 150, 250, 250))
        pygame.draw.rect(self.screen, yellow_light if yellow_light else self.yellow, pygame.Rect(50, 400, 250, 250))
        pygame.draw.rect(self.screen, blue_light if blue_light else self.blue, pygame.Rect(300, 400, 250, 250))

        pygame.display.update()

    def show_pattern(self):
        # 1 = GREEN
        # 2 = RED
        # 3 = YELLOW
        # 4 = BLUE

        self.time_delay = 500 - 100 * int(len(self.pattern) / 5)
        if self.time_delay <= 100:
            self.time_delay = 100

        self.draw_screen()
        pygame.time.delay(1000)

        for x in self.pattern:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()

            if x == 1:
                # GREEN
                self.draw_screen(green_light=self.green_light)
                self.green_sound.play()
                pygame.time.delay(self.time_delay)
                self.draw_screen()
                self.green_sound.stop()
            elif x == 2:
                # RED
                self.draw_screen(red_light=self.red_light)
                self.red_sound.play()
                pygame.time.delay(self.time_delay)
                self.draw_screen()
                self.red_sound.stop()
            elif x == 3:
                # YELLOW
                self.draw_screen(yellow_light=self.yellow_light)
                self.yellow_sound.play()
                pygame.time.delay(self.time_delay)
                self.draw_screen()
                self.yellow_sound.stop()
            elif x == 4:
                # BLUE
                self.draw_screen(blue_light=self.blue_light)
                self.blue_sound.play()
                pygame.time.delay(self.time_delay)
                self.draw_screen()
                self.blue_sound.stop()

            pygame.time.delay(self.time_delay)

    def new_pattern(self):
        self.score = len(self.pattern)
        self.pattern.append(random.randint(1, 4))

    def check_pattern(self, player_pattern):
        if player_pattern != self.pattern[:len(player_pattern)]:
            self.lose_screen()

    def click_listen(self):
        turn_time = time.time()
        player_pattern = []

        self.time_delay = 500 - 100 * int(len(self.pattern) / 5)
        if self.time_delay <= 100:
            self.time_delay = 100

        while time.time() <= turn_time + 3 and len(player_pattern) < len(self.pattern):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    pos = self.cursor.get_pos()
                    x = pos[0]
                    y = pos[1]

                    if 50 < x < 300 and 150 < y < 400:
                        self.draw_screen(green_light=self.green_light)
                        self.green_sound.play()
                        pygame.time.delay(self.time_delay)
                        self.green_sound.stop()
                        self.draw_screen()
                        player_pattern.append(1)
                        self.check_pattern(player_pattern)
                        turn_time = time.time()
                    elif 300 < x < 550 and 150 < y < 400:
                        self.draw_screen(red_light=self.red_light)
                        self.red_sound.play()
                        pygame.time.delay(self.time_delay)
                        self.red_sound.stop()
                        self.draw_screen()
                        player_pattern.append(2)
                        self.check_pattern(player_pattern)
                        turn_time = time.time()
                    elif 50 < x < 300 and 400 < y < 650:
                        self.draw_screen(yellow_light=self.yellow_light)
                        self.yellow_sound.play()
                        pygame.time.delay(self.time_delay)
                        self.yellow_sound.stop()
                        self.draw_screen()
                        player_pattern.append(3)
                        self.check_pattern(player_pattern)
                        turn_time = time.time()
                    elif 300 < x < 550 and 400 < y < 650:
                        self.draw_screen(blue_light=self.blue_light)
                        self.blue_sound.play()
                        pygame.time.delay(self.time_delay)
                        self.blue_sound.stop()
                        self.draw_screen()
                        player_pattern.append(4)
                        self.check_pattern(player_pattern)
                        turn_time = time.time()

        if not time.time() <= turn_time + 3:
            self.lose_screen()

    def click_display(self, player_pattern, appended_number, color_sound):
        color_sound.play()
        pygame.time.delay(self.time_delay)
        color_sound.stop()
        self.draw_screen()
        player_pattern.append(appended_number)
        self.check_pattern(player_pattern)
        turn_time = time.time()
        return player_pattern, turn_time

    def quit_game(self):
        self.running = False
        pygame.display.quit()
        pygame.quit()
        sys.exit()

    def lose_screen(self):
        self.lose_sound.play()

        # display lose screen
        self.screen.fill(self.black)
        lose_text = self.title_font.render('You Lose', True, self.white)
        score_text = self.title_font.render('Score: ' + str(self.score), True, self.white)
        self.screen.blit(lose_text, (161.5, 50))
        self.screen.blit(score_text, (((600 - self.title_font.size('Score: ' + str(self.score))[0]) / 2), 120))
        self.screen.blit(self.again_button, (180, 300))
        self.screen.blit(self.exit_button, (180, 450))

        pygame.display.update()

        # Reset variables
        self.score = 0
        self.pattern = []
        self.time_delay = 500
        self.running = True

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    pos = self.cursor.get_pos()
                    x = pos[0]
                    y = pos[1]

                    if 180 <= x <= 420 and 300 <= y <= 390:
                        self.start_menu()
                    elif 180 <= x <= 420 and 450 <= y <= 540:
                        self.quit_game()

    def start_menu(self, cursor=pygame.cursors.broken_x):
        waiting = True
        self.menu_music.play(-1)
        logo_bob = 150
        title_text = self.title_font.render('Simon', True, self.white)
        self.cursor.set_cursor(cursor)
        self.cursor.set_pos(self.width // 2, self.height // 2)

        bob_direction = True  # true = down, false = up
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    pos = self.cursor.get_pos()
                    x = pos[0]
                    y = pos[1]

                    if 180 <= x <= 420 and 530 <= y <= 620:
                        self.menu_music.stop()
                        waiting = False

            # reset screen
            self.screen.fill(self.black)

            # display assets
            self.screen.blit(title_text, (220, 50))
            self.screen.blit(self.big_logo, (150, logo_bob))
            self.screen.blit(self.start_button, (180, 530))
            pygame.display.update()

            if logo_bob == 150:
                pygame.time.delay(300)
                bob_direction = True
            elif logo_bob == 190:
                pygame.time.delay(300)
                bob_direction = False

            if bob_direction:
                logo_bob += 0.5
            else:
                logo_bob -= 0.5

            self.clock.tick(60)

        while self.running:
            self.new_pattern()
            self.show_pattern()
            self.click_listen()
