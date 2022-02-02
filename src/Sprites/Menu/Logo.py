import pygame


class Logo(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.picture = pygame.image.load('resources/Images/the_game_logo.png')
        self.logo = self.picture.subsurface((40, 50, 520, 470))
        self.image = self.picture

        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rect = self.image.get_rect()
        self.pause = 0
        self.logo_light = False
        self.rect.topleft = [self.pos_x, self.pos_y]

    def update(self, *args):
        if self.pause:
            self.pause -= 1
        else:
            self.pause = 15
            self.logo_light = False if self.logo_light else True

        if self.logo_light:
            self.image = pygame.image.load('resources/Images/the_game_logo_light.png')
        else:
            self.image = pygame.image.load('resources/Images/the_game_logo.png')
