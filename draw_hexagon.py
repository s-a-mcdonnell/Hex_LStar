class Hex:
   def __init__(self, x, y, color):
       self.coordinates = create_hex(x, y)
       self.color = color

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
hex_matrix = []

for x in range(10):
    hex_list = []
    hex_matrix.append(hex_list)

    for y in range(10):
        myHex = Hex(20 + 60*x, 35*x + 70*y, (255, 0, 0))
        hex_list.append(myHex)
        # __ hex_list.append(create_hex(20 + 60*x, 35*x + 70*y))


# __ hex_list = []
# __ hex_list.append(create_hex(20, 0))
# __ hex_list.append(create_hex(80, 35))
# __ hex_list.append(create_hex(140, 0))

run = True
while run:
    # Reset screen
    screen.fill((0, 0, 0))

    # Draw hexagons
    r = 10
    g = 10
    b = 10
    for hex_list in hex_matrix:
        for hexagon in hex_list:
            draw_hex(screen, hexagon.coordinates, hexagon.color)
            '''draw_hex(screen, hexagon.coordinates, (r, g, b))
            if r <= 245:
                r += 10
            elif g <= 245:
                g += 10
            elif b <= 245:
                b += 10
            else:
                r=0
                g=0
                b=0'''

    # Event handler (closing window)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()

