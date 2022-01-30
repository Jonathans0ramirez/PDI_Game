import pygame


class Title(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, title_text='You Lose'):
        super().__init__()
        self.gameplay_font_dir = 'resources/Fonts/Gameplay.ttf'
        self.image = pygame.font.Font(self.gameplay_font_dir, 50).render(title_text, True, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]
