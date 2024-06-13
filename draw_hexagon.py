import time
import copy

class Hex:
   @staticmethod
   def create_coor(x, y):
        # Making hex smaller so that borders will be visible
        return [(x+3, y+3), (x+37, y+3), (x+57, y+35), (x+37, y+67), (x+3, y+67), (x-17, y+35)]


    # Constructor
    # color is an optional parameter with a default value of red
    # movable is an optional parameter with a default value of true
   def __init__(self, matrix_index, list_index, color=(255, 0, 0), movable=True, occupied=False):
       self.matrix_index = matrix_index
       self.list_index = list_index

       self.x = 60*matrix_index - 20
       self.y = 35*matrix_index + 70*list_index - 490

       self.coordinates = Hex.create_coor(self.x, self.y)
       
       # Store identities of hexes
       self.idents = []
       if occupied:
           self.idents.append(Ident(color))

       if not movable:
           self.make_wall()

        # Create arrows for later use
       #pivot is the center of the hexagon
       pivot = pygame.Vector2(self.x + 20, self.y + 35)
        # set of arrow points should be the vectors from the pivot to the edge points of the arrow
       arrow = [(0, -15), (10, -5), (5, -5), (5, 15), (-5, 15), (-5, -5), (-10, -5)]
        # get arrow by adding all the vectors to the pivot point => allows for easy rotation
       self.arrows = []
       for i in range(6):
            self.arrows.append([(pygame.math.Vector2(x, y)).rotate(60.0*i) + pivot for x, y in arrow]) 

    # sets the given hex to act as a wall
   def make_wall(self):
       # Wipe idents currently stored
       self.idents = None
       self.idents = []
       # Walls are black
       # -2 state is a wall
       self.idents.append(Ident((0,0,0), -2))

    # sets the given hex to move in a given direction
   def make_move(self, dir, color=(255,0,0)):
       # Note: Does not overwrite idents currently stored
       self.idents.append(Ident(color, dir))

    # Appends the passed ident to the given hex
   def take_ident(self, ident):
       self.idents.append(ident)    

   def make_occupied(self, color=(0,255,0)):
       # TODO: Clear out current idents? (does not currently overwrite pre-existing idents)
       self.idents.append(Ident(color, -1))

   # returns a boolean indicating if a hex is occupied 
   def is_occupied(self):
       return len(self.idents != 0)   

   def draw(self, screen):
    
    # Default color (no idents): light blue
    my_color = (190, 240, 255)

    if (len(self.idents) == 1):
        # If a hex contains only one ident, take that color
        my_color = self.idents[0].color
    elif (len(self.idents) > 1):
        # If a hex contains multiple idents, draw it green
        my_color = (0, 255, 0)
        # TODO: Add cool animation here?
        
    # Draw the hexagon
    pygame.draw.polygon(screen, my_color, self.coordinates)

    # Draw text object displaying axial hex coordiantes
    # self.display_surface.blit(self.text, self.textRect)

    # polygon rotation tips from: https://stackoverflow.com/questions/75116101/how-to-make-rotate-polygon-on-key-in-pygame

    # draw an arrow on the hex if the hex is moving
    if (self.is_moving):
        #pivot is the center of the hexagon
        pivot = pygame.Vector2(self.x + 20, self.y + 35)
        # set of arrow points should be the vectors from the pivot to the edge points of the arrow
        arrow = [(0, -15), (10, -5), (5, -5), (5, 15), (-5, 15), (-5, -5), (-10, -5)]
        # get arrow by adding all the vectors to the pivot point => allows for easy rotation
        for i in range(6):
            if self.contains_direction(i):
                pygame.draw.polygon(screen, (0, 0, 0), self.arrows[i])

    # returns a boolean indicating if the given hex is occupied, movable, and stationary (not currently moving)
   def check_movable_hex(self):
       #return (not self.is_moving) and self.movable and self.occupied
       for ident in self.idents:
           if ident.state == -1:
               return True
       # If none of the idents contain state -1, the hex is not movable
       return False

    # returns a boolean indicating if the hex is currently moving
   def is_moving(self):
        return self.contains_direction(0) or self.contains_direction(1) or self.contains_direction(2) or self.contains_direction(3) or self.contains_direction(4) or self.contains_direction(5)
   
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
   
   # Checks if a hex contains an ident heading in the given directon
   # If it does, returns that ident
   # Else returns None
   def contains_direction(self, dir):

       for ident in self.idents:
           if ident.state == dir:
               return ident

       return None 
   
   # Handles interactions between a hex and its environment with respect to the given direction
   def motion_handler(self, future, my_neighbors, neighbors_movable, neighbors_wall, dir):
        # straight_neighbor is the neighbor in that direction (ex. when dir = 0, straight_neighbor is the upper neighbor of self)
       straight_neighbor = my_neighbors[dir]

        # if my neighbor is moving toward me and is not blocked by either of two side walls, I will gain motion
       # TODO: Need to distinguish between bouncing and passing through
       if (not neighbors_wall[(dir+1)%6]) and (not neighbors_wall[(dir-1)%6]):
           neighbor_ident = straight_neighbor.contains_direction((dir+3)%6)
           if neighbor_ident != None:
                # My identity pointing in the given direction, if it exists
                my_ident = self.contains_direction(dir)

                counterclockwise_neighbor_ident = None
                if my_neighbors[(dir+1)%6] != None:
                    counterclockwise_neighbor_ident = my_neighbors[(dir+1)%6].contains_direction((dir-2)%6)

                clockwise_neighbor_ident = None
                if my_neighbors[(dir-1)%6] != None:
                    clockwise_neighbor_ident = my_neighbors[(dir-1)%6].contains_direction((dir+2)%6)

                if my_ident != None:
                    # If in a head-on collision with a neighbor moving in the opposite direction, maintain identity and switch direction
                    print("case 1")
                    ident_to_flip = copy.deepcopy(my_ident)
                    ident_to_flip.state = (ident_to_flip.state+3)%6
                    future.take_ident(ident_to_flip)
                # TODO: Deal with diagonal collision (neighbor is heading towards the same hex)
                elif counterclockwise_neighbor_ident != None:
                    print("case 2")
                    # __elif I have two adjacent neighbors pointing at me
                    # __Take the ident from the straight_neighbor but flip its state to match that from the other neighbor (adjacent to straight_neighbor)
                    ident_to_flip = copy.deepcopy(counterclockwise_neighbor_ident)
                    ident_to_flip.state = (ident_to_flip.state-1)%6
                    future.take_ident(ident_to_flip)
                elif clockwise_neighbor_ident != None:
                    print("case 3")
                    ident_to_flip = copy.deepcopy(clockwise_neighbor_ident)
                    ident_to_flip.state = (ident_to_flip.state+1)%6
                    future.take_ident(ident_to_flip)
                # TODO: Write case for head-on collision with an empty hex in the middle
                # TODO: Write case for 120 degree collisions (not just 60 degree)
                else:
                # Else take on identity of neighbor
                    print("case 4")
                    future.take_ident(neighbor_ident)
        
        # handle impact of hitting occupied neighbor
       if self.contains_direction(dir): 
           self.hit_neighbor(future, neighbors_movable, neighbors_wall, dir)

    # returns an array of neighbors (the entry in the array is None when the neighbor does not exist)
   def get_neighbors(self):
        my_neighbors = [None, None, None, None, None, None]

        try:
            my_neighbors[0] = hex_matrix[self.matrix_index][self.list_index - 1]
        except:
            #print("Neighbor 0 does not exist")
            pass

        try:
            my_neighbors[1] = hex_matrix[self.matrix_index + 1][self.list_index - 1]    
        except:
            #print("Neighbor 1 does not exist")
            pass

        try:
            my_neighbors[2] = hex_matrix[self.matrix_index + 1][self.list_index]
        except:
            #print("Neighbor 2 does not exist")
            pass

        try:
            my_neighbors[3] = hex_matrix[self.matrix_index][self.list_index + 1]
        except:
            #print("Neighbor 3 does not exist")
            pass

        try:
            my_neighbors[4] = hex_matrix[self.matrix_index - 1][self.list_index + 1]
        except:
            #print("Neighbor 4 does not exist")
            pass
        
        try:
            my_neighbors[5] = hex_matrix[self.matrix_index - 1][self.list_index]
        except:
            #print("Neighbor 5 does not exist")
            pass
        
        return my_neighbors


   #update self hexagon
   def update(self):
        # determine the state of the current hex based on the states of the hexes around it
        future = hex_matrix_new[self.matrix_index][self.list_index]

        '''# TODO: Make state 7 elements long?
        future.state = [0, 0, 0, 0, 0, 0]
        future.occupied = False'''
        future.idents = []

        neighbors_movable = self.check_movables()
        neighbors_wall = self.check_walls()

        # If the hex is a wall, it will remain occupied and not movable
        if(hex_matrix[self.matrix_index][self.list_index].check_wall_hex()):
            # TODO: Pass a color?
            future.idents.append(Ident((0,0,0),-2))

        # TODO: Pretty sure this doesn't work, but I haven't tested it
        # If the hex is currently occupied and not moving, it will still be occupied in the next generation
        if hex_matrix[self.matrix_index][self.list_index].check_movable_hex():
            # TODO: pass the correct color (the color of the ident which is stationary)
            future.idents.append(Ident(-1))

        my_neighbors = self.get_neighbors()
        
        # TODO: Convert if self.movable: to ident
        if (len(self.idents) == 0) or (self.idents[0].state != -2):
            # TODO: Adjust to account for idents
            # UPPER NEIGHBOR EFFECTS (0)

            for i in range(6):
                if my_neighbors[i] != None:
                    self.motion_handler(future, my_neighbors, neighbors_movable, neighbors_wall, i)

            '''# if my upper (0) neighbor is pointing down (3) then I will move down
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
                self.motion_handler(future, hex_matrix[self.matrix_index - 1][self.list_index + 1], neighbors_movable, neighbors_wall, 4)'''

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

# Hexes approaching vertically, hex-on
hex_matrix[5][11].make_move(0, (255, 255, 102))
hex_matrix[5][6].make_move(3, (204, 0, 255))

# yellow hex
'''hex_matrix[5][6].make_move(2, (255, 255, 102))

# purple hex
hex_matrix[5][11].make_move(1, (204, 0, 255))'''



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
    # TODO: Switch to alternating between two matrices
    hex_matrix = copy.deepcopy(hex_matrix_new)

pygame.quit()

## making sure I remember how to commit

