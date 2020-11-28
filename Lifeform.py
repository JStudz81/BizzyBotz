import math

import pygame
import random

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

from Bed import Bed
from Food import Food

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Lifeform(pygame.sprite.Sprite):
    def __init__(self, enemy=False):
        super(Lifeform, self).__init__()
        self.surf = pygame.Surface((25, 25))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
        self.rect.x = random.randint(0,775)
        self.rect.y = random.randint(0,575)
        self.enemy = enemy

        self.health = 100
        self.hunger = 0
        self.tired = 0

        self.busy = False

        self.attacking = None

        if enemy:
            self.surf.fill((255, 0, 0))

    def moveTo(self, x, y):
        if self.rect.x != x and self.rect.y != y:
            distance = (self.rect.x - x, self.rect.y - y)

            norm = math.sqrt(distance[0] ** 2 + distance[1] ** 2)
            direction = (distance[0] / norm, distance[1] / norm)

            self.rect.move_ip(direction[0] * -5, direction[1] * -5)

    def update(self, nearest_food: Food, nearest_bed: Bed, nearest_enemy=None, nearest_scrap=None):
        if nearest_enemy is not None and self.attacking is None:
            self.attacking = nearest_enemy
            self.busy = True
            self.moveTo(nearest_enemy.rect.x, nearest_enemy.rect.y)
        elif self.attacking is not None and nearest_enemy is not None:
            self.busy = True
            self.moveTo(nearest_enemy.rect.x, nearest_enemy.rect.y)
        else:
            self.busy = False
        if not self.busy and not self.enemy:
            if self.hunger > 50:
                self.moveTo(nearest_food.rect.x, nearest_food.rect.y)
            elif self.tired > 90:
                self.moveTo(nearest_bed.rect.x, nearest_bed.rect.y)
            elif nearest_scrap is not None:
                self.moveTo(nearest_scrap.rect.x, nearest_scrap.rect.y)
            elif random.randint(0,10) > 9:
                self.rect.move_ip(random.randint(-5,5), random.randint(-5,5))

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


    def tick(self):
        self.surf.fill((255, 255, 255))
        if self.enemy:
            self.surf.fill((255, 0, 0))
        font = pygame.font.SysFont(None, 16)
        self.img = font.render(str(int(self.health)), True, (0, 0, 0))
        self.surf.blit(self.img, (0, 5))

        if self.hunger < 100:
            self.hunger = self.hunger + .1
        if self.hunger > 75:
            self.health = self.health - .1
        if self.hunger < 25 and self.health < 100:
            self.health = self.health + .1
        if self.tired < 100:
            self.tired = self.tired + .05

        if self.health <= 0:
            self.kill()





