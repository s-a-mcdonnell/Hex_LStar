
def draw_hex(screen, x, y, color):
    hexagon = [(x, y), (x+40, y), (x+60, y+35), (x+40, y+70), (x, y+70), (x-20, y+35)]
    pygame.draw.polygon(screen, color, hexagon)


import pygame

pygame.init()

SCREEN_WIDTH = 800

SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Draw Hexagon")

# Create hexagons
# __ hexagon = [(20, 0), (60, 0), (80, 35), (60, 70), (20, 70), (0, 35)]
# __ hexagon2 = [(80, 35), (120, 35), (140, 70), (120, 105), (80, 105), (60, 70)]


run = True
while run:
    # Reset screen
    screen.fill((0, 0, 0))

    # Draw hexagons
    draw_hex(screen, 20, 0, (5, 5, 180))
    draw_hex(screen, 80, 35, (5, 180, 5))
    draw_hex(screen, 140, 0, (255, 0, 0))
    # __ pygame.draw.polygon(screen, (5, 5, 180), hexagon)
    # __ pygame.draw.polygon(screen, (5, 180, 5), hexagon2)

    # Event handler (closing window)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()

