import game as Game

import pygame


pygame.init()

window = pygame.display.set_mode((1600, 900))
pygame.display.set_caption("Presidents and Insects")

run = True
while run:
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

pygame.quit()