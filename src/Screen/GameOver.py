import pygame


class GameOver:
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

