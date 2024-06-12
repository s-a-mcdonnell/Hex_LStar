import time
import copy

class Hex:
   @staticmethod
   def create_coor(x, y):
        # __ x-=40
        # __ y-=490
        # __ return [(x, y), (x+40, y), (x+60, y+35), (x+40, y+70), (x, y+70), (x-20, y+35)]
        # Making hex smaller so that borders will be visible
        return [(x+3, y+3), (x+37, y+3), (x+57, y+35), (x+37, y+67), (x+3, y+67), (x-17, y+35)]


    # Constructor
    # color is an optional parameter with a default value of red
    # moveable is an optional parameter with a default value of true
   def __init__(self, matrix_index, list_index, color=(255, 0, 0), moveable=True):
       self.matrix_index = matrix_index
       self.list_index = list_index

       self.x = 60*matrix_index - 20
       self.y = 35*matrix_index + 70*list_index - 490

       self.coordinates = Hex.create_coor(self.x, self.y)
       
        # TO DO: need to make something for occupied vs unoccupied hexes

       self.color = color
       self.movable = moveable
       self.state = [0, 0, 0, 0, 0, 0]

   
   def draw(self, screen):
    if self.state[0] | self.state[1] | self.state[2] | self.state[3] | self.state[4] | self.state[5]:
       self.color = (0, 0, 255)
    elif self.movable == False:
        self.color = (20, 20, 20)
    else:
        self.color = (255, 0, 0)
    
    # Draw the hexagon
    pygame.draw.polygon(screen, self.color, self.coordinates)

    # Draw text object displaying axial hex coordiantes
    # self.display_surface.blit(self.text, self.textRect)

    #update self hexagon
    def update(self):
        
        # determine the state of the current hex based on the states of the hexes around it
        future = hex_matrix_new[self.matrix_index][self.list_index]

        future.state = [0,0,0,0,0,0]

        if self.movable:

            # UPPER NEIGHBOR EFFECTS
            # if my upper (0) neighbor is pointing down (3) then I will move down
            if self.list_index - 1 > 0:
                future.state[3] = hex_matrix[self.matrix_index][self.list_index - 1].state[3]

import pygame

pygame.init()

SCREEN_WIDTH = 800

SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Draw Hexagon")

# Create hexagons
hex_matrix = []

for x in range(15):
    hex_list = []
    hex_matrix.append(hex_list)

    for y in range(16):
        myHex = Hex(x, y)
        hex_list.append(myHex)

# create additional matrix
hex_matrix_new = []

for x in range(15):
    hex_list_new = []
    hex_matrix_new.append(hex_list_new)

    for y in range(16):
        myHex = Hex(x, y)
        hex_list_new.append(myHex)

# Update the state of a few hexagons to reflect motion
hex_matrix[10][10].state[0] = 1
hex_matrix[10][4].state[3] = 1
hex_matrix[4][7].state[3] = 3
hex_matrix[6][10].state[2] = 1
hex_matrix[5][6].movable = False

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
        
            # draw an arrow on the hex if the hex is moving
            if(str(hexagon.state) != "[0, 0, 0, 0, 0, 0]"):
                #pivot is the center of the hexagon
                pivot = pygame.Vector2(hexagon.x + 20, hexagon.y + 35)
                # set of arrow points should be the vectors from the pivot to the edge points of the arrow
                # arrow = [(hexagon.x + 20, hexagon.y + 10), (hexagon.x + 40, hexagon.y + 25), (hexagon.x + 30, hexagon.y + 25), (hexagon.x + 30, hexagon.y + 50), (hexagon.x + 10, hexagon.y + 50), (hexagon.x + 10, hexagon.y + 25), (hexagon.x, hexagon.y + 25)]
                arrow = [(0, -15), (10, -5), (5, -5), (5, 15), (-5, 15), (-5, -5), (-10, -5)]
                # get arrow by adding all the vectors to the pivot point => allows for easy rotation

                if(hexagon.state[0] != 0):
                    arrow_new = [(pygame.math.Vector2(x, y)) + pivot for x, y in arrow]
                    pygame.draw.polygon(screen, (0, 0, 0), arrow_new)

                if(hexagon.state[1] != 0):
                    arrow_new = [(pygame.math.Vector2(x, y)).rotate(60.0) + pivot for x, y in arrow]
                    pygame.draw.polygon(screen, (0, 0, 0), arrow_new)

                if(hexagon.state[2] != 0):
                    arrow_new = [(pygame.math.Vector2(x, y)).rotate(120.0) + pivot for x, y in arrow]
                    pygame.draw.polygon(screen, (0, 0, 0), arrow_new)

                if(hexagon.state[3] != 0):
                    arrow_new = [(pygame.math.Vector2(x, y)).rotate(180.0) + pivot for x, y in arrow]
                    pygame.draw.polygon(screen, (0, 0, 0), arrow_new)

                if(hexagon.state[4] != 0):
                    arrow_new = [(pygame.math.Vector2(x, y)).rotate(240.0) + pivot for x, y in arrow]
                    pygame.draw.polygon(screen, (0, 0, 0), arrow_new)

                if(hexagon.state[5] != 0):
                    arrow_new = [(pygame.math.Vector2(x, y)).rotate(300.0) + pivot for x, y in arrow]
                    pygame.draw.polygon(screen, (0, 0, 0), arrow_new)


    # Event handler (closing window)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

    # update all states in new_hex
    for hex_list_new in hex_matrix_new:
        for hexagon in hex_list_new:
            hexagon.state = [0,0,0,0,0,0]
            if(hex_matrix[hexagon.matrix_index][hexagon.list_index].movable == False):
                hexagon.movable = False

    # update states in the new one
    for hex_list in hex_matrix:
        for hexagon in hex_list:
            #check for index out of bound stuff
            if hexagon.state[0] != 0:
                if (0 <= hexagon.list_index - 1 < len(hex_list)):
                    hex_matrix_new[hexagon.matrix_index][hexagon.list_index - 1].state[0] = 1
            if hexagon.state[1] != 0:
                if (0 <= hexagon.matrix_index + 1 < len(hex_matrix)) and (0 <= hexagon.list_index - 1 < len(hex_list)):
                    hex_matrix_new[hexagon.matrix_index + 1][hexagon.list_index - 1].state[1] = 1
            if hexagon.state[2] != 0:
                if (0 <= hexagon.matrix_index + 1 < len(hex_matrix)):
                    hex_matrix_new[hexagon.matrix_index + 1][hexagon.list_index].state[2] = 1
            if hexagon.state[3] != 0:
                if(0 <= hexagon.list_index + 1 < len(hex_list)):
                    hex_matrix_new[hexagon.matrix_index][hexagon.list_index + 1].state[3] = 1
            if hexagon.state[4] != 0:
                if (0 <= hexagon.matrix_index - 1 < len(hex_matrix)) and (0 <= hexagon.list_index + 1 < len(hex_list)):
                    hex_matrix_new[hexagon.matrix_index - 1][hexagon.list_index + 1].state[4] = 1
            if hexagon.state[5] != 0:
                if (0 <= hexagon.matrix_index - 1 < len(hex_matrix)):
                    hex_matrix_new[hexagon.matrix_index - 1][hexagon.list_index].state[5] = 1

    # need to use the python deepcopy in order to copy the inner lists of a 2D array
    hex_matrix = copy.deepcopy(hex_matrix_new)
    # hex_matrix = hex_matrix_new.copy()

    time.sleep(1)

pygame.quit()

