import math

import pygame

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import *

# Initialize pygame
from Bed import Bed
from Food import Food
from GrassGenerator import GrassGenerator
from Lifeform import Lifeform
from Scrap import Scrap

pygame.init()

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Define a Player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'


# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


# Instantiate player. Right now, this is just a rectangle.

food = Food()

bed = Bed()
lifeforms_group = pygame.sprite.Group()

lifeforms = []

enemies_group = pygame.sprite.Group()
scraps = pygame.sprite.Group()
grass_gens = pygame.sprite.Group()

enemies = []

scrap_amount = 0

for i in range(0, 10):
    player = Lifeform()
    lifeforms_group.add(player)
    lifeforms.append(player)

# Variable to keep the main loop running
running = True

clock = pygame.time.Clock()

# Main loop
while running:
    # Look at every event in the queue
    for event in pygame.event.get():
        if event.type == MOUSEBUTTONDOWN:
            mouse_click = pygame.mouse.get_pressed(3)
            if mouse_click[0] and scrap_amount > 0:
                pos = pygame.mouse.get_pos()
                new_life = Lifeform()
                new_life.rect.x = pos[0]
                new_life.rect.y = pos[1]
                lifeforms.append(new_life)
                lifeforms_group.add(new_life)
                scrap_amount = scrap_amount - 1
            if mouse_click[2] and scrap_amount >= 5:
                pos = pygame.mouse.get_pos()
                grass_gen = GrassGenerator(pos[0], pos[1])
                grass_gens.add(grass_gen)
                scrap_amount = scrap_amount - 5
        # Did the user hit a key?
        elif event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop.
            if event.key == K_SPACE:
                enemy = Lifeform(True)
                lifeforms.append(enemy)
                lifeforms_group.add(enemy)
                enemies.append(enemy)
                enemies_group.add(enemy)
            if event.key == K_ESCAPE:
                running = False

        # Did the user click the window close button? If so, stop the loop.
        elif event.type == QUIT:
            running = False

    screen.fill((0, 0, 0))


    for g in grass_gens:
        g.update(screen)
        if g.progress >= 100:
            g.progress = 0
            new_life = Lifeform()
            new_life.rect.x = g.rect.x
            new_life.rect.y = g.rect.y
            lifeforms.append(new_life)
            lifeforms_group.add(new_life)
    screen.blit(food.surf, food.rect)
    screen.blit(bed.surf, bed.rect)
    for scrap in scraps:
        screen.blit(scrap.surf, scrap.rect)

    font = pygame.font.SysFont(None, 24)
    img = font.render('Scrap: ' + str(scrap_amount), True, (255, 255, 255))
    screen.blit(img, (0, 0))

    dead = []
    # Update the lifeforms
    for lifeform in lifeforms[:]:
        if len(enemies) > 0 and not lifeform.enemy:
            distances = []
            for enemy in enemies:
                distances.append(math.hypot(enemy.rect.x - lifeform.rect.x, enemy.rect.y - lifeform.rect.y))
            closest = enemies[distances.index(min(distances))]
            lifeform.update(food, bed, nearest_enemy=closest)
        elif len(scraps) > 0 and not lifeform.enemy:
            distances = []
            for scrap in scraps:
                distances.append(math.hypot(scrap.rect.x - lifeform.rect.x, scrap.rect.y - lifeform.rect.y))
            closest = scraps.sprites()[distances.index(min(distances))]

            lifeform.update(food, bed, nearest_scrap=closest)
        elif len(grass_gens) > 0 and not lifeform.enemy:
            distances = []
            for g in grass_gens:
                distances.append(math.hypot(g.rect.x - lifeform.rect.x, g.rect.y - lifeform.rect.y))
            closest = grass_gens.sprites()[distances.index(min(distances))]

            lifeform.update(food, bed, nearest_gen=closest)
        else:
            lifeform.update(food, bed)

        lifeform.tick()

        if not lifeform.busy and not lifeform.enemy:
            if pygame.sprite.collide_rect(food, lifeform):
                food = Food()
                lifeform.hunger = 0

            if pygame.sprite.collide_rect(bed, lifeform):
                lifeform.tired = 0

            scrap_pickup = pygame.sprite.spritecollideany(lifeform,scraps)
            if scrap_pickup is not None:
                scraps.remove(scrap_pickup)
                scrap_pickup.kill()
                scrap_amount = scrap_amount + 1

            gen_touch = pygame.sprite.spritecollideany(lifeform, grass_gens)
            if gen_touch is not None and lifeform.health < 100:
                lifeform.health = lifeform.health + 1

        for enemy in enemies:
            if pygame.sprite.collide_rect(enemy, lifeform) and enemy is not lifeform and lifeform.enemy == False:
                enemy.health = enemy.health - 1
                lifeform.health = lifeform.health - 1

        screen.blit(lifeform.surf, lifeform.rect)

        if lifeform.health <= 0:

            scrap = Scrap(lifeform.rect.x, lifeform.rect.y)
            scraps.add(scrap)

            if lifeform in enemies:
                enemies.remove(lifeform)


            lifeforms.remove(lifeform)


    # Fill the screen with white


    # Draw the player on the screen

    pygame.display.flip()

    # Ensure program maintains a rate of 30 frames per second
    clock.tick(30)
