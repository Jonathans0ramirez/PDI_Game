import pygame


class Score(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, title_text='Score'):
        super().__init__()
        self.title_text = title_text
        self.gameplay_font_dir = 'resources/Fonts/Gameplay.ttf'
        self.image = pygame.font.Font(self.gameplay_font_dir, 50).render(f"{self.title_text}: 0", True, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]

    def update(self, score=0, *args):
        self.image = self.image = pygame.font.Font(self.gameplay_font_dir, 50).render(
            f"{self.title_text}: {str(score)}", True, (255, 255, 255))
