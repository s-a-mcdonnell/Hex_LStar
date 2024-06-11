# I am following a Pygame tutorial from Coding With Russ

import pygame

pygame.init()

SCREEN_WIDTH = 800

SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Draw Hexagon")

# Attempt at a hexagon just for the heck of it
hexagon = [(20, 0), (60, 0), (80, 35), (60, 70), (20, 70), (0, 35)]

run = True
while run:
    # Reset screen
    screen.fill((0, 0, 0))

    # Draw blue hexagon
    pygame.draw.polygon(screen, (5, 5, 180), hexagon)

    # Event handler (closing window)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()

