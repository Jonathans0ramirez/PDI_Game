import pygame


class Green(pygame.sprite.Sprite):
    def __init__(self, pos_x=50, pos_y=150):
        super().__init__()
        self.green = (0, 100, 0)
        self.green_light = (0, 255, 0)
        self.image = pygame.Surface([250, 250])
        self.image.fill(self.green)
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]
        self.color_animation = None

    def change_color(self, condition):
        self.color_animation = condition

    def update(self, *args):
        if self.color_animation:
            self.image.fill(self.green_light)
        else:
            self.image.fill(self.green)
