import pygame
import random

class GrassGenerator(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(GrassGenerator, self).__init__()
        self.surf = pygame.Surface((25, 25))
        self.surf.fill((100, 0, 255))
        self.rect = self.surf.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.progress = 0

    def update(self, screen):
        self.surf.fill((100,0,225))

        self.progress = self.progress + .1
        pygame.draw.circle(screen, (0,255,0), self.rect.center, 50)


        font = pygame.font.SysFont(None, 16)
        self.img = font.render(str(int(self.progress)), True, (0, 0, 0))
        self.surf.blit(self.img, (0, 5))

        screen.blit(self.surf, self.rect)