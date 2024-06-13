import time
import copy

class Hex:
   @staticmethod
   def create_coor(x, y):
        # Making hex smaller so that borders will be visible
        return [(x+3, y+3), (x+37, y+3), (x+57, y+35), (x+37, y+67), (x+3, y+67), (x-17, y+35)]


    # Constructor
    # color is an optional parameter with a default value of red
    # moveable is an optional parameter with a default value of true
   def __init__(self, matrix_index, list_index, color=(255, 0, 0), moveable=True, occupied=False):
       self.matrix_index = matrix_index
       self.list_index = list_index

       self.x = 60*matrix_index - 20
       self.y = 35*matrix_index + 70*list_index - 490

       self.coordinates = Hex.create_coor(self.x, self.y)
       
       # Store identities of hexes
       self.idents = []
       if occupied:
           self.idents.append(Ident(color))
       '''self.color = color
       self.movable = moveable
       self.occupied = occupied
       # TODO: Make 7 states?
       self.state = [0, 0, 0, 0, 0, 0]'''

       '''# Create arrows for later use
       
       #pivot is the center of the hexagon
       pivot = pygame.Vector2(self.x + 20, self.y + 35)
        # set of arrow points should be the vectors from the pivot to the edge points of the arrow
       arrow = [(0, -15), (10, -5), (5, -5), (5, 15), (-5, 15), (-5, -5), (-10, -5)]
        # get arrow by adding all the vectors to the pivot point => allows for easy rotation
       self.arrows = []

       for i in range(6):
            self.arrows.append([(pygame.math.Vector2(x, y)).rotate(60.0*i) + pivot for x, y in arrow])
        '''

    # sets the given hex to act as a wall
   def make_wall(self):
       '''self.occupied = True
       self.movable = False'''
       self.idents = None
       self.idents = []
       # Walls are black
       # -2 state is a wall
       self.idents.append(Ident((0,0,0), -2))

    # sets the given hex to move in a given direction
   def make_move(self, dir, color=(255,0,0)):
       '''self.occupied = True
       self.movable = True
       self.state[dir] = 1'''
       self.idents.append(Ident(color, dir)) 

   def draw(self, screen):
    # Colors now determined by ident
    '''if self.occupied == False:
        # If not occupied: light blue
        self.color = (190, 240, 255)
    elif self.movable == False:
        # If occupied and not movable (wall): dark grey
        self.color = (20, 20, 20)
    elif self.state[0] | self.state[1] | self.state[2] | self.state[3] | self.state[4] | self.state[5]:
       # If moving: blue
       self.color = (0, 0, 255)
    else:
        # If occupied and not moving (but movable): teal
        self.color = (50, 175, 175)'''
    
    # Draw the hexagon
    # pygame.draw.polygon(screen, self.color, self.coordinates)
    if (len(self.idents) != 0):
        # TODO: Deal with drawing hexes containing multiple idents
        pygame.draw.polygon(screen, self.idents[0].color, self.coordinates)
    else:
        # If a hex contains no idents, draw it light blue
        pygame.draw.polygon(screen, (190, 240, 255), self.coordinates)

    # Draw text object displaying axial hex coordiantes
    # self.display_surface.blit(self.text, self.textRect)

    # TODO: No arrows drawn when using ident?
    '''# polygon rotation tips from: https://stackoverflow.com/questions/75116101/how-to-make-rotate-polygon-on-key-in-pygame

    # draw an arrow on the hex if the hex is moving
    if (self.is_moving):
        #pivot is the center of the hexagon
        pivot = pygame.Vector2(self.x + 20, self.y + 35)
        # set of arrow points should be the vectors from the pivot to the edge points of the arrow
        arrow = [(0, -15), (10, -5), (5, -5), (5, 15), (-5, 15), (-5, -5), (-10, -5)]
        # get arrow by adding all the vectors to the pivot point => allows for easy rotation
        for i in range(6):
            if self.state[i]:
                pygame.draw.polygon(screen, (0, 0, 0), self.arrows[i])''' 

    # returns a boolean indicating if the given hex is occupied, movable, and stationary (not currently moving)
   def check_movable_hex(self):
       #return (not self.is_moving) and self.movable and self.occupied
       for ident in idents:
           if ident.state == -1:
               return True
       # If none of the idents contain state -1, the hex is not movable
       return False 
       
       

    # returns a boolean indicating if the hex is currently moving
   def is_moving(self):
        return self.state[0] or self.state[1] or self.state[2] or self.state[3] or self.state[4] or self.state[5]
    
   # returns a list of length six representing the six neighboring hexes of self, with 1 if the hex neighboring in that direction is movable, nonmoving, and occupied
   def check_movables(self): 
        hex_movable = [0, 0, 0, 0, 0, 0]

        # Initializing hexToCheck with default value (reducing repeated memory allocation and deallocation)
        hexToCheck = self

        # check upper hex (pos 0)
        # If the upper hex exists and is occupied, moving, and stationary, flip the boolean in the array
        if self.list_index - 1 >= 0:
           hexToCheck = hex_matrix[self.matrix_index][self.list_index - 1]
           hex_movable[0] = hexToCheck.check_movable_hex()

        # check northeast hex (pos 1)
        if (self.matrix_index + 1 < len(hex_matrix)) and (self.list_index - 1 >= 0):
           hexToCheck = hex_matrix[self.matrix_index + 1][self.list_index - 1]
           hex_movable[1] = hexToCheck.check_movable_hex()

        # check southeast hex (pos 2)
        if self.matrix_index + 1 < len(hex_matrix):
            hexToCheck = hex_matrix[self.matrix_index + 1][self.list_index]
            hex_movable[2] = hexToCheck.check_movable_hex()

        # check down hex (pos 3)
        if self.list_index + 1 < len(hex_list):
            hexToCheck = hex_matrix[self.matrix_index][self.list_index + 1]
            hex_movable[3] = hexToCheck.check_movable_hex()

        # check southwest hex (pos 4)
        if (self.matrix_index - 1 >= 0) and (self.list_index + 1 < len(hex_list)):
            hexToCheck = hex_matrix[self.matrix_index - 1][self.list_index + 1]
            hex_movable[4] = hexToCheck.check_movable_hex()

        # check northwest hex (pos 5)
        if self.matrix_index - 1 >= 0:
            hexToCheck = hex_matrix[self.matrix_index - 1][self.list_index]
            hex_movable[5] = hexToCheck.check_movable_hex()

        return hex_movable
   
    # returns a boolean indicating if the given hex is a wall (occupied and not movable)
   def check_wall_hex(self):
       # There should never be a wall hex containing multiple idents
       # If the one ident isn't state -2, it's not a wall
       if (len(self.idents) != 1) or (self.idents[0].state != -2):
           return False
       else:
           return True

   # returns a list of length 6 to determine which of the neighbors around self hex are walls
   def check_walls(self):
        hex_walls = [0, 0, 0, 0, 0, 0]

        # Default value of hexToCheck (not used)
        hexToCheck = self

        # check upper hex (pos 0)
        if self.list_index - 1 >= 0:
           hexToCheck = hex_matrix[self.matrix_index][self.list_index - 1]
           hex_walls[0] = hexToCheck.check_wall_hex()

         # check northeast hex (pos 1)
        if (self.matrix_index + 1 < len(hex_matrix)) and (self.list_index - 1 >= 0):
           hexToCheck = hex_matrix[self.matrix_index + 1][self.list_index - 1]
           hex_walls[1] = hexToCheck.check_wall_hex()


        # check southeast hex (pos 2)
        if self.matrix_index + 1 < len(hex_matrix):
            hexToCheck = hex_matrix[self.matrix_index + 1][self.list_index]
            hex_walls[2] = hexToCheck.check_wall_hex()


        # check down hex (pos 3)
        if self.list_index + 1 < len(hex_list):
            hexToCheck = hex_matrix[self.matrix_index][self.list_index + 1]
            hex_walls[3] = hexToCheck.check_wall_hex()


        # check southwest hex (pos 4)
        if (self.matrix_index - 1 >= 0) and (self.list_index + 1 < len(hex_list)):
            hexToCheck = hex_matrix[self.matrix_index - 1][self.list_index + 1]
            hex_walls[4] = hexToCheck.check_wall_hex()


         # check northwest hex (pos 5)
        if self.matrix_index - 1 >= 0:
            hexToCheck = hex_matrix[self.matrix_index - 1][self.list_index]
            hex_walls[5] = hexToCheck.check_wall_hex()


        return hex_walls

    # handles the impacts of hitting an occupied neighbor (either a stationary object or a wall)
    # TODO: How to pass around idents?
   def hit_neighbor(self, future, neighbors_movable, neighbors_wall, dir):
        # cases for individual side glancing walls
        if (neighbors_wall[(dir-1)%6] == 1) and not (neighbors_wall[(dir+1)%6] == 1):
            future.occupied = True
            future.movable = True
            #future.state[dir] = 0
            future.state[(dir+1)%6] = 1
        elif (neighbors_wall[(dir+1)%6] == 1) and not (neighbors_wall[(dir-1)%6] == 1):
            future.occupied = True
            future.movable = True
            #future.state[dir] = 0
            future.state[(dir-1)%6] = 1
        # if my neighbor is a wall (or if I have two neighors to the side in front), bounce off
        elif (neighbors_wall[dir] == 1) or ((neighbors_wall[(dir-1)%6] == 1) and (neighbors_wall[(dir+1)%6] == 1)):
            future.occupied = True
            future.movable = True
            #future.state[dir] = 0
            future.state[(dir+3)%6] = 1
        # if I am moving toward my neighbor, and my neighbor is occupied but not moving, then I become occupied but not moving
        # TODO: Discuss order in which rules are applied
        # TODO: Also discuss if collisions off of a side wall should take priority over head-on collisions
        elif neighbors_movable[dir] == 1:
            future.occupied = True
            future.movable = True
   
   # Handles interactions between a hex and its environment with respect to the given direction
   # straight_neighbor is the neighbor in that direction (ex. when dir = 0, straight_neighbor is the upper neighbor of self)
   def motion_handler(self, future, straight_neighbor, neighbors_movable, neighbors_wall, dir):
       # if my neighbor is moving toward me and is not blocked by either of two side walls, I will gain motion
       if (not neighbors_wall[(dir+1)%6]) and (not neighbors_wall[(dir-1)%6]):
           if straight_neighbor.state[(dir+3)%6]:
                future.state[(dir+3)%6] = 1
                future.occupied = True
        
        # handle impact of hitting occupied neighbor
       if(self.state[dir] != 0):
            self.hit_neighbor(future, neighbors_movable, neighbors_wall, dir)

   #update self hexagon
   def update(self):
        # determine the state of the current hex based on the states of the hexes around it
        future = hex_matrix_new[self.matrix_index][self.list_index]

        # TODO: Make state 7 elements long?
        future.state = [0, 0, 0, 0, 0, 0]
        future.occupied = False

        neighbors_movable = self.check_movables()
        neighbors_wall = self.check_walls()

        # If the hex is a wall, it will remain occupied and not movable
        if(hex_matrix[self.matrix_index][self.list_index].movable == False):
            future.movable = False
            future.occupied = True

        # If the hex is currently occupied and not moving, it will still be occupied in the next generation
        if(hex_matrix[self.matrix_index][self.list_index].occupied == True) and (not hex_matrix[self.matrix_index][self.list_index].is_moving()):
            future.occupied = True

        if self.movable:

            # UPPER NEIGHBOR EFFECTS (0)

            # if my upper (0) neighbor is pointing down (3) then I will move down
            if self.list_index - 1 >= 0:
                # Call motion_handler, passing upper neighbor
                self.motion_handler(future, hex_matrix[self.matrix_index][self.list_index - 1], neighbors_movable, neighbors_wall, 0)


            # DOWN NEIGHBOR EFFECTS (3)
            if self.list_index + 1 < len(hex_list):
                # Call motion_handler, passing lower neighbor
                self.motion_handler(future, hex_matrix[self.matrix_index][self.list_index + 1], neighbors_movable, neighbors_wall, 3)
    

            # NORTHEAST NEIGHBOR (1)
            if (self.matrix_index + 1 < len(hex_matrix)) and (self.list_index - 1 >= 0):
                # Call motion_handler, passing northeast neighbor
                self.motion_handler(future, hex_matrix[self.matrix_index + 1][self.list_index - 1], neighbors_movable, neighbors_wall, 1)

            # NORTHWEST NEIGHBOR (5)
            if self.matrix_index - 1 >= 0:
                # Call motion_handler, passing northwest neighbor
                self.motion_handler(future, hex_matrix[self.matrix_index - 1][self.list_index], neighbors_movable, neighbors_wall, 5)


            # SOUTHEAST NEIGHBOR (2)
            if self.matrix_index + 1 < len(hex_matrix):
                # Call motion_handler, passing southeast neighbor
                self.motion_handler(future, hex_matrix[self.matrix_index + 1][self.list_index], neighbors_movable, neighbors_wall, 2)


            # SOUTHWEST NEIGHBOR (4)
            if (self.matrix_index - 1 >= 0) and (self.list_index + 1 < len(hex_list)):
                # Call motion_handler, passing southwests neighbor
                self.motion_handler(future, hex_matrix[self.matrix_index - 1][self.list_index + 1], neighbors_movable, neighbors_wall, 4)

class Ident:
    # Constructor
    # Default color white
    # Default state -1 (movable but not moving)
    def __init__(self, color=(255, 255, 255), state=-1):
        self.color = color
        self.state = state
        self.property = None
    


import pygame

pygame.init()

SCREEN_WIDTH = 800

SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Draw Hexagon")

# set up pygame timer
clock = pygame.time.Clock()
run = True
dt = 0

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

# Update the state of a few hexagons to reflect motion (test cases)
#hex_matrix[10][8].occupied = True
hex_matrix[10][4].occupied = True
# hex_matrix[4][7].occupied = True
# hex_matrix[6][10].occupied = True
# hex_matrix[3][5].occupied = True
#hex_matrix[4][6].occupied = True

hex_matrix[9][10].make_move(5)

#hex_matrix[4][6].make_move(3)

hex_matrix[7][7].make_move(3)
hex_matrix[6][8].make_move(2)
hex_matrix[8][7].make_move(4)

hex_matrix[5][5].make_move(3)
hex_matrix[4][6].make_move(2)
hex_matrix[6][5].make_move(4)


#hex_matrix[6][6].make_wall()
#hex_matrix[5][9].make_wall()
#hex_matrix[6][7].make_wall()
hex_matrix[7][9].make_wall()
hex_matrix[7][8].make_wall()

# Create walls around the edges
# Left edge
for hex in hex_matrix[0]:
    hex.make_wall()
# Right edge
for hex in hex_matrix[13]:
    hex.make_wall()
for i in range(6):
    # Top edge
    hex_matrix[1+2*i][6-i].make_wall()
    hex_matrix[2+2*i][6-i].make_wall()

    # Bottom edge
    hex_matrix[1+2*i][15-i].make_wall()
    hex_matrix[2+2*i][14-i].make_wall()

run = True
while run:

    # Reset screen
    screen.fill((0, 0, 0))

    # Draw hexagons
    r = 10
    g = 10
    b = 10

    # Draw all hexagons
    for hex_list in hex_matrix:
        for hexagon in hex_list:
            hexagon.draw(screen)

    # Event handler (closing window)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # flips to the next frame
    pygame.display.flip()

    # sets animation to n frames per second where n is inside the parentheses (feel free to change)
    dt = clock.tick(1) / 1000

    for hex_list in hex_matrix:
        for hexagon in hex_list:
            hexagon.update()

    # need to use the python deepcopy in order to copy the inner lists of a 2D array
    hex_matrix = copy.deepcopy(hex_matrix_new)
    # hex_matrix = hex_matrix_new.copy()

pygame.quit()

## making sure I remember how to commit

