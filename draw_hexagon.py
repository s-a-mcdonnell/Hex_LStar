class Hex:
   @staticmethod
   def create_coor(x, y):
        # __ return [(x, y), (x+40, y), (x+60, y+35), (x+40, y+70), (x, y+70), (x-20, y+35)]
        # Making hex smaller so that borders will be visible
        return [(x + 3, y + 3), (x+37, y+3), (x+57, y+35), (x+37, y+67), (x, y+67), (x-17, y+35)]


    # Constructor
    # moveable is an optional parameter with a default value of true
   def __init__(self, x, y, color=(255, 0, 0), moveable=True):
       self.coordinates = Hex.create_coor(x, y)
       self.color = color
       self.movable = moveable
       self.state = [0, 0, 0, 0, 0, 0]
   
   def draw(self, screen):
    if self.state[0] | self.state[1] | self.state[2] | self.state[3] | self.state[4] | self.state[5]:
       self.color = (0, 0, 255)
    else:
        self.color = (255, 0, 0)
    pygame.draw.polygon(screen, self.color, self.coordinates)

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
        myHex = Hex(20 + 60*x, 35*x + 70*y)
        hex_list.append(myHex)

# Update the state of a few hexagons to reflect motion
hex_matrix[1][1].state[0] = 1
hex_matrix[2][3].state[4] = 1
hex_matrix[5][2].state[2] = 1

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
            hexagon.draw(screen)

    # Event handler (closing window)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()

