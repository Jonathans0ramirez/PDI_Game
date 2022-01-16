import pygame


class Start(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('resources/Images/start_button.png'), (240, 90))
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]
