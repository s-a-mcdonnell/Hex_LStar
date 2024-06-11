# I am following a Pygame tutorial from Coding With Russ

import pygame

pygame.init()

SCREEN_WIDTH = 800

SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Target Practice")

# Create rectangle (x-coord, y-coord, width, height)
RECT_WIDTH = 60
RECT_HEIGHT = 45
myRect = pygame.Rect(40, 30, RECT_WIDTH, RECT_HEIGHT)

# Create target
TAR_WIDTH = 100
TAR_HEIGHT = 100
target = pygame.Rect(300, 300, TAR_WIDTH, TAR_HEIGHT)

# Attempt at a hexagon just for the heck of it
hexagon = [(20, 0), (60, 0), (80, 40), (60, 80), (20, 80), (0, 40)]

run = True
while run:
    # Reset screen
    screen.fill((0, 0, 0))

    # Draw purple rectangle and red target
    # And a random blue hexagon
    pygame.draw.polygon(screen, (5, 5, 180), hexagon)
    pygame.draw.rect(screen, (255, 0, 0), target)
    pygame.draw.rect(screen, (200, 0, 200), myRect)

    key = pygame.key.get_pressed()

    # If a is pressed, move left
    if key[pygame.K_a]:
        myRect.move_ip(-1, 0)
    # If d is pressed, move right
    elif key[pygame.K_d]:
        myRect.move_ip(1, 0)
    # If w is pressed, move up
    elif key[pygame.K_w]:
        myRect.move_ip(0, -1)
    # If s is pressed, move down
    elif key[pygame.K_s]:
        myRect.move_ip(0, 1)

     # If the edge of the rectangle has moved off the screen, move it back
    if myRect.x < 0:
        myRect.x = 0
    elif myRect.x + RECT_WIDTH > SCREEN_WIDTH:
        myRect.x = SCREEN_WIDTH - RECT_WIDTH
    if myRect.y < 0:
        myRect.y = 0
    elif myRect.y + RECT_HEIGHT > SCREEN_HEIGHT:
        myRect.y = SCREEN_HEIGHT - RECT_HEIGHT

    # If rectangle is fully inside target, print winning message and close game
    insideX = (myRect.x > target.x) & (myRect.x + RECT_WIDTH < target.x + TAR_WIDTH)
    insideY = (myRect.y > target.y) & (myRect.y + RECT_HEIGHT < target.y + TAR_HEIGHT)
    if  insideX & insideY:
        print("Congrats, you win!")
        run = False

    # Event handler (closing window)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()

