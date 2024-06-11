
def create_hex(x, y):
    return [(x, y), (x+40, y), (x+60, y+35), (x+40, y+70), (x, y+70), (x-20, y+35)]

def draw_hex(screen, hexagon, color):
    pygame.draw.polygon(screen, color, hexagon)


import pygame

pygame.init()

SCREEN_WIDTH = 800

SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Draw Hexagon")

# Create hexagons
hex_list = [create_hex(20, 0), create_hex(80, 35), create_hex(140, 0)]

run = True
while run:
    # Reset screen
    screen.fill((0, 0, 0))

    # Draw hexagons
    draw_hex(screen, hex_list[0], (5, 5, 180))
    draw_hex(screen, hex_list[1], (5, 180, 5))
    draw_hex(screen, hex_list[2], (255, 0, 0))
    # __ pygame.draw.polygon(screen, (5, 5, 180), hexagon)
    # __ pygame.draw.polygon(screen, (5, 180, 5), hexagon2)

    # Event handler (closing window)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()

