import pygame


class Blue(pygame.sprite.Sprite):
    def __init__(self, pos_x=0, pos_y=0, layer=1):
        super().__init__()
        self._layer = layer
        self.relative_pos = (4, 348)
        self.size = (289, 289)
        self.image = pygame.image.load('resources/Images/blue.png')

        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]
        self.color_animation = None

    def change_color(self, condition):
        self.color_animation = condition

    def update(self, *args):
        if self.color_animation:
            self.image = pygame.image.load('resources/Images/blue_light.png')
            self._layer = 2
        else:
            self.image = pygame.image.load('resources/Images/blue.png')
            self._layer = 1

