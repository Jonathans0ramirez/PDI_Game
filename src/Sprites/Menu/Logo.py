import pygame


class Logo(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.logo = pygame.image.load('resources/Images/simon_logo.png')
        self.image = pygame.transform.scale(self.logo, (300, 300))

        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rect = self.image.get_rect()
        self.speed = 0.5
        self.pause = 0
        self.blob_direction = True
        self.start_position = 150
        self.end_position = 190
        self.rect.topleft = [self.pos_x, self.pos_y]

    def update(self, *args):
        if self.pause:
            self.blob_direction = True if self.pos_y < self.start_position else False \
                if self.blob_direction else \
                False if self.pos_y < self.start_position else True

        if self.pos_y == 150 and not self.pause:
            self.pos_y += self.speed
            self.pause = 20
        elif self.pos_y == 190 and not self.pause:
            self.pos_y -= self.speed
            self.pause = 20

        if self.pos_y < self.end_position and self.blob_direction:
            if not self.pause:
                self.pos_y += self.speed
            else:
                self.pause -= 1
        else:
            if not self.pause:
                self.pos_y -= self.speed
            else:
                self.pause -= 1
        self.rect.topleft = [self.pos_x, self.pos_y]
