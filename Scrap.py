import pygame


class Scrap(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Scrap, self).__init__()
        self.surf = pygame.Surface((25, 25))
        self.surf.fill((100, 100, 100))
        self.rect = self.surf.get_rect()
        self.rect.x = x
        self.rect.y = y