import pygame
import random

class Food(pygame.sprite.Sprite):
    def __init__(self):
        super(Food, self).__init__()
        self.surf = pygame.Surface((25, 25))
        self.surf.fill((0, 255, 255))
        self.rect = self.surf.get_rect()
        self.rect.x = random.randint(0,775)
        self.rect.y = random.randint(0,575)

