import pygame


class Blue(pygame.sprite.Sprite):
    def __init__(self, pos_x=300, pos_y=400):
        super().__init__()
        self.blue = (0, 0, 100)
        self.blue_light = (0, 0, 255)
        self.image = pygame.Surface([250, 250])
        self.image.fill(self.blue)
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]
        self.color_animation = None

    def change_color(self, condition):
        self.color_animation = condition

    def update(self, *args):
        if self.color_animation:
            self.image.fill(self.blue_light)
        else:
            self.image.fill(self.blue)

