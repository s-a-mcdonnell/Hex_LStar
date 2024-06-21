import time
import copy
import os
import pygame

# Debugger
import pdb

'''
Process of the game:
0. Iterate over Idents
1. a: If an ident is in a head on collision with another ident, it flips in place
   b: Else, move the ident forward into the next hex
2. Resolve collisions. For hexes that contain multiple idents...
   a: If it has an ident of opposite direction in that hex, bounce off/reverse direction
   b: Else, take the average of all other idents EXCEPT SELF, but break ties by using the opposite ident of self
'''

# for storing information about a particular moving hex
class Ident:


    # TODO: Do we still need this?
    idents_created = 0

    ##########################################################################################################
    
    def __init__(self, matrix_index, list_index, world, color=(255, 255, 255), state: int = -1, serial_number = -1, hist = None):
        if hist is None:
            hist = []
        self.color = color

        self.state : int = state

        self.hist = hist
        if serial_number == -1:
            # If no serial number is provided
            self.serial_number = Ident.idents_created

            '''print("Ident with serial number " + str(self.serial_number) + " created")
            if state == -2:
                print("Is a wall")
            elif state == -1:
                print("Is stationary")
            else:
                print("Is moving")'''
            Ident.idents_created += 1
        else:
            self.serial_number = serial_number
            
            '''if self.state != -2:
                print("Ident with serial number " + str(self.serial_number) + " copied")
                print("color: " + str(self.color))'''

        self.matrix_index = matrix_index
        self.list_index = list_index

        self.world = world
    
    ##########################################################################################################

    # Returns the neighboring hex in the given direction in the given matrix
    # If that hex does not exist, returns None
    def __get_neighbor(self, matrix, dir):
        if dir == 0:
            try:
                return matrix[self.matrix_index][self.list_index - 1]
            except:
                return None
            
        elif dir == 1:
            try:
                return matrix[self.matrix_index + 1][self.list_index - 1]  
            except:
                return None

        elif dir == 2:
            try:
                return matrix[self.matrix_index + 1][self.list_index]
            except:
                return None

        elif dir == 3:

            try:
                return matrix[self.matrix_index][self.list_index + 1]
            except:
                return None

        elif dir == 4:

            try:
                return matrix[self.matrix_index - 1][self.list_index + 1]
            except:
                return None
            
        elif dir == 5:

            try:
                return matrix[self.matrix_index - 1][self.list_index]
            except:
                return None
            
        else:
            print("Invalid direction " + str(dir) + " passed to Ident.__get_neighbor(dir)")
            return None

    ##########################################################################################################

    # Helper method for resolve_collisions()
    # Takes the hex in which the ident is located and the direcs list of other idents in that hex
    # Returns the direcs list with pairs of idents which cancel out removed
    @staticmethod
    def __remove_pairs(hex, dir, directions):
        # breakpoint()
        direcs = directions.copy()


        if dir == -1:
            '''# TODO: Explain how this needs to be written weirdly to work for dir = -1 (can't math right)
            return Ident.__remove_pairs(hex, 0, Ident.__remove_pairs(hex, 1, direcs))'''

            hex_zero = hex.contains_direction(0)
            hex_three = hex.contains_direction(3)
            if hex_zero and hex_three:
                direcs.remove(hex_zero)
                direcs.remove(hex_three)
            
            hex_one = hex.contains_direction(1)
            hex_four = hex.contains_direction(4)
            if hex_one and hex_four:
                direcs.remove(hex_one)
                direcs.remove(hex_four)

            hex_two = hex.contains_direction(2)
            hex_five = hex.contains_direction(5)
            if hex_two and hex_five:
                direcs.remove(hex_two)
                direcs.remove(hex_five)
            
            return direcs

        else:
            
            # TODO: Note that using contains_direction leaves us vulnerable if there are somehow multiple idents in the hex that share a direction

            hex_plus_one = hex.contains_direction((dir + 1) % 6)
            hex_minus_two = hex.contains_direction((dir - 2) % 6)
            if hex_plus_one and hex_minus_two:
                direcs.remove(hex_plus_one)
                direcs.remove(hex_minus_two)
            
            hex_plus_two = hex.contains_direction((dir + 2) % 6)
            hex_minus_one = hex.contains_direction((dir - 1) % 6)
            if hex_plus_two and hex_minus_one:
                direcs.remove(hex_plus_two)
                direcs.remove(hex_minus_one)
        
        return direcs

    ##########################################################################################################


     # TODO: Write this method
    # note that I should never have to deal with walls in this method
    # note that this reads from hex_matrix_new and ident_list_new and writes to hex_matrix and ident_list
    def resolve_collisions(self):

        w = self.world

        # breakpoint()

        # The hex to which we will be writing
        write_to_hex = w.hex_matrix[self.matrix_index][self.list_index]

        # obtain the hex that this ident is currently a part of
        hex = w.hex_matrix_new[self.matrix_index][self.list_index]
        if len(hex.idents) <= 1:
            print("No collision to resolve")

            # TODO: Is copying necessary here?
            w.ident_list.append(self.__copy())
            write_to_hex.idents.append(self.__copy())

            return
        
        # now we have determined that the ident has other idents with it
        # TODO: I think we can do this without getting index (just only append to directions if ident is not self)
        '''my_index = hex.get_ident_index(self)'''
        dir = self.state

        directions = []

        # TODO: consider appending just the directions/states of the idents instead of appending the idents themselves
        for ident in hex.idents:
            '''if i != my_index:
                directions.append(hex.idents[i])'''
            # TODO: This is the only way I've found to not accidentally append self when examining a stationary hex. Why is that?
            if ident.serial_number != self.serial_number:
                directions.append(ident)
            '''if ident is not self:
                directions.append(ident)'''

        # if there was only one other ident in the collision, take its attributes
        # Note that this also deals with the most simple collision betwen a moving ident and a stationary one
        # TODO: ^^ Check if this is true ^^

        # TODO: I think this whole section can be collapsed downwards into after the pairs are removed from directions
        '''if len(directions) == 1:
            # breakpoint()
            if directions[0].state != -1:
                # If colliding with a single moving ident, take its direction
                # breakpoint()
                self.__rotate_adopt(write_to_hex, w.ident_list, dir_final = directions[0].state)
            else:
                # TODO: Move this down to section dealing with stationary hexes?
                # If colliding with a stationary ident, become stationary in the hex from whence you came
                assert self.state != -1
                # The place it came from must exist, or else this ident couldn't be here, right?
                # TODO: Move ident back and make stationary
                hex_of_origin = self.__get_neighbor(w.hex_matrix, (self.state + 3)%6)

                assert hex_of_origin

                self.__rotate_adopt(hex_of_origin, w.ident_list, dir_final = -1)

        # if there is more than one other ident than self, we do averaging things
        # if the idents contain an opposite direction ident, we bounce!! :)
        el'''
        
        '''# If colliding with an ident pointing in the opposite direction, bounce off
        if (dir != -1) and (hex.contains_direction((dir + 3) % 6) is not None):
            # TODO: Can this section just be dealt with in the stationary/not stationary section?
            self.__rotate_adopt(write_to_hex, w.ident_list)

            return
        
        # otherwise, determine whether we contain a stationary hex or not
        # if not, we are all moving hexes and none of them are opposite me, so we average them
        el'''
        
        if hex.contains_direction(-1) is None:
            # if we contain opposite pairs, remove them from the directions list
            directions = self.__remove_pairs(hex, dir, directions)
            
            # if we ended up with a net zero average (all other idents in the hex cancelled out in opposite pairs),
            # bounce off in the opposite direction from what is currently held
            if len(directions) == 0:
                self.__rotate_adopt(write_to_hex, w.ident_list)

            # if, at this point, there is only one direction left, take that one
            elif len(directions) == 1:
                print("rotate call e")
                self.__rotate_adopt(write_to_hex, w.ident_list, dir_final = directions[0].state)

            # otherwise, there are exactly two other directions stored in this hex
            else:
                # Sanity checks
                assert(len(directions) == 2)
                assert(directions[0].state != directions[1].state)
                assert(directions[0].state != self.state)
                assert(directions[1].state != self.state)

                # if the other two are at 120 degrees to each other, take the value in between
                if (directions[0].state + 2)%6 == directions[1].state:
                    print("rotate call a")
                    self.__rotate_adopt(write_to_hex, w.ident_list, dir_final = (directions[0].state + 1)%6)
                elif (directions[0].state - 2)%6 == directions[1].state:
                    print("rotate call b")
                    self.__rotate_adopt(write_to_hex, w.ident_list, dir_final = (directions[0].state - 1)%6)
                
                # if the other two cohabitants are adjacent to one another (60 degrees), take the state of the one we are further away from
                else:
                    assert(((directions[0].state + 1)%6 == directions[1].state) or ((directions[0].state - 1)%6 == directions[1].state))
                    
                    closer_to_dir_0 = (abs(self.state - directions[0].state)%6) < (abs(self.state - directions[1].state)%6)
                    
                    # if current direction is closer to directions[0] than directions[1], take the state of directions[1]
                    if closer_to_dir_0:
                        print("rotate call c")
                        self.__rotate_adopt(write_to_hex, w.ident_list, dir_final = directions[1].state)
                    # else take the state of directions[0]
                    else:
                        print("rotate call d")
                        self.__rotate_adopt(write_to_hex, w.ident_list, dir_final = directions[0].state)

        # else, we are dealing with multiple hexes, including a stationary hex
        # TODO: Did you mean idents in the above comment? - Skyler
        # TODO: stationary cases here!!!
        else:
            assert(hex.contains_direction(-1))
            
            # A stationary ident colliding with a moving ident
            if self.state == -1:
                # breakpoint()                

                # if we contain opposite pairs, remove them from the directions list
                directions = self.__remove_pairs(hex, dir, directions)

                # If there are no idents left in directions, remain stationary
                if len(directions) == 0:
                    # TODO: Is copying necessary?
                    my_copy = self.__copy()
                    write_to_hex.idents.append(my_copy)
                    w.ident_list.append(my_copy)

                # If there is only one ident left in directions, take its state
                elif len(directions) == 1:
                    self.__rotate_adopt(write_to_hex, w.ident_list, dir_final = directions[0].state)
            
                elif len(directions) == 2:
                    # TODO: Note that this is copied directly from above --> how can we restructure?
                        # if the other two are at 120 degrees to each other, take the value in between
                    if (directions[0].state + 2)%6 == directions[1].state:
                        print("rotate call a")
                        self.__rotate_adopt(write_to_hex, w.ident_list, dir_final = (directions[0].state + 1)%6)
                    elif (directions[0].state - 2)%6 == directions[1].state:
                        print("rotate call b")
                        self.__rotate_adopt(write_to_hex, w.ident_list, dir_final = (directions[0].state - 1)%6)
                    
                    # if the other two cohabitants are adjacent to one another (60 degrees), take one of the states (arbitrary formula)
                    # TODO: ^^ Note that this is an arbitrary decision ^^
                    else:
                        assert(((directions[0].state + 1)%6 == directions[1].state) or ((directions[0].state - 1)%6 == directions[1].state))
                        
                        # TODO: Change decision-making for which state to take?
                        state_to_take = directions[0].state
                        if (directions[0].state - directions[1].state)%6 > 2:
                            state_to_take = directions[1].state
                        
                        self.__rotate_adopt(write_to_hex, w.ident_list, dir_final = state_to_take)
                        
                        
                elif len(directions) == 3:
                    # If there are three moving idents which have not been removed from directions,
                    # they are either all adjacent to one another
                    # or they are symmetrical (all at 120 degrees from one another)
                    
                    # Symmetrical case --> stationary hex does not move
                    if (abs(directions[0].state - directions[1].state) == 2 or 4) and (abs(directions[0].state - directions[2].state) == 2 or 4):
                        # TODO: Is copying necessary?
                        my_copy = self.__copy()
                        write_to_hex.idents.append(my_copy)
                        w.ident_list.append(my_copy)
                    
                    # Adjacent case (the three moving idents are clumped together) --> stationary hex is bumped in the direction of the middle ident
                    else:
                        assert ((directions[0].state - directions[1].state)%6 == 1) or ((directions[0].state - directions[2].state)%6 == 1)
                        direc_0_1_offset = (directions[0].state - directions[1].state)%3
                        direc_1_2_offset = (directions[1].state - directions[2].state)%3
                        direc_0_2_offset = (directions[0].state - directions[2].state)%3
                        
                        # If directions[0] has the middle state, take that state
                        if direc_0_1_offset == 1 and direc_0_2_offset == 1:
                            # TODO: Is copying necessary?
                            self.__rotate_adopt(write_to_hex, w.ident_list, dir_final = directions[0].state)
                        
                        # If directions[1] has the middle state, take that state
                        elif direc_1_2_offset == 1 and direc_0_1_offset == 1:
                            # TODO: Is copying necessary?
                            self.__rotate_adopt(write_to_hex, w.ident_list, dir_final = directions[1].state)

                        # If directions[2] has the middle state, take that state
                        elif direc_0_2_offset == 1 and direc_1_2_offset == 1:
                            # TODO: Is copying necessary?
                            self.__rotate_adopt(write_to_hex, w.ident_list, dir_final = directions[2].state)

                        else:
                            # None of the three idents have been calcualted to be in the middle
                            print("Error: No middle direction found")
                            pass

                else:
                    print("Error: Unexpected length of directions")
                    pass

            # A moving ident colliding with a stationary ident
            else:
                # breakpoint()

                assert self.state >= 0

                hex_of_origin = self.__get_neighbor(w.hex_matrix, (self.state + 3)%6)
                assert hex_of_origin

                # If an ident with the opposite state is present, bounce off
                if hex.contains_direction((dir + 3) % 6):
                    self.__rotate_adopt(hex_of_origin, w.ident_list)
                
                # Else become stationary
                else:
                    self.__rotate_adopt(hex_of_origin, w.ident_list, dir_final = - 1)
                

    ##########################################################################################################

    # If the head-on (direction of self.state) neighboring hex contains an ident with the given direction, returns said ident
    # Else returns None
    # TODO: Does this method still have a purpose?
    def __neighbor_contains_direction(self, neighbor_state, neighbor_index=None, ):
        # Default value
        if neighbor_index == None:
            neighbor_index = self.state

        try:
            return self.__get_neighbor(self.world.hex_matrix, neighbor_index).contains_direction(neighbor_state)
        except:
            print("Neighbor DNE")
            return None

    ##########################################################################################################


    # If the neighbor in the direction in which the ident is pointing is a wall, returns that ident
    # Else returns None
    def __neighbor_is_wall(self, neighbor_index_offset=0):
        neighbor_index = (self.state + neighbor_index_offset)%6

        return self.__neighbor_contains_direction(-2, neighbor_index)
        
    ##########################################################################################################

    # If there will be a head-on-collision, returns the ident with which it will collide
    # Else returns none
    # TODO: Could just use a boolean
    def __head_on_collision(self):
        return self.__neighbor_contains_direction((self.state + 3)%6)

    ##########################################################################################################
    
    # Copies self and rotates it by the indicated number of directions
    # Adopts said rotated ident
    def __rotate_adopt(self, future_hex, future_ident_list, dir_offset: int = 3, dir_final : int =-3):

        # Calculate final direction if none is given
        if dir_final == -3:
            dir_final = (self.state + dir_offset)%6
        
        
        print("Rotating ident " + str(self.serial_number) + " from state " + str(self.state) + " to " + str(dir_final))

        ident = self.__copy()
        ident.state = dir_final

        # This is necessary for moving hexes colliding with stationary hexes
        ident.matrix_index = future_hex.matrix_index
        ident.list_index = future_hex.list_index

        future_ident_list.append(ident)
        future_hex.idents.append(ident)

    ##########################################################################################################
    
    # If an ident is stationary or a wall, writes this value to the hex_matrix_new
    # Elif an ident is running into a wall or a head-on collision, flips it in place (writing to hex_matrix_new)
    # Else advances an ident by one hex in its direction of motion (if that hex exists)
    def advance_or_flip(self):
        
        future_matrix = self.world.hex_matrix_new
        future_hex = future_matrix[self.matrix_index][self.list_index]
        future_list = self.world.ident_list_new
    
        # Maintain stationaries and return
        if self.state == -1:
            future_list.append(self.__copy())
            future_hex.idents.append(self.__copy())

            return

        # If need to bounce head-on off of a wall, then bounce and return
        head_on_wall = self.__neighbor_is_wall() and not (self.__neighbor_is_wall(1) or self.__neighbor_is_wall(-1))
        double_adjacent_wall = self.__neighbor_is_wall(1) and self.__neighbor_is_wall(-1)
        if head_on_wall or double_adjacent_wall:
            
            self.__rotate_adopt(future_hex, future_list)
            
            return


        # If need to bounce diagonally off of a wall, then bounce and return
        if self.__neighbor_is_wall(-1):
            self.__rotate_adopt(future_hex, future_list, dir_offset=1)

            return
        
        # Other diagonal wall bounce case
        if self.__neighbor_is_wall(1):
            self.__rotate_adopt(future_hex, future_list, dir_offset=-1)

            return
                
        # If need to bounce head-on off of another ident, then bounce and return
        if self.__head_on_collision():
            self.__rotate_adopt(future_hex, future_list)

            return

        # Advance all others (if the location where they would advance to exists)
        future_neighbor = self.__get_neighbor(future_matrix, self.state)
        if future_neighbor:
            print("advance to future neighbor")
            copy_to_move = self.__copy()
            copy_to_move.matrix_index = future_neighbor.matrix_index
            copy_to_move.list_index = future_neighbor.list_index
                
            future_list.append(copy_to_move)
            future_neighbor.idents.append(copy_to_move)

    ##########################################################################################################

    def visited(self, m, l):
        # push onto stack history
        # pushed onto the history is
            # hex matrix index
            # hex list index
            # current state

        # note, we want to keep up to 5 past states at a time
        # to change amount, just change limit #
        limit = 5

        if len(self.hist) == limit + 1:
            self.hist.pop(0)
            self.hist.append((m, l, self.state))
        else:
            self.hist.append((m, l, self.state))

    ##########################################################################################################

    def __copy(self):
        # TODO: Should any of these components be done with .copy()?
        new_copy = Ident(self.matrix_index, self.list_index, self.world, color = self.color, state = self.state, serial_number = self.serial_number, hist = self.hist)
        return new_copy
    
###############################################################################################################

# hex class is now just for graphics/displaying the board/storing idents
class Hex:
    # Default color (no idents): light blue
    DEFAULT_COLOR =(190, 240, 255)

    ##########################################################################################################

    # Checks where a specific ident occurs within this hex's list
    # If it contains the ident, returns the index
    # Else returns -1
    def get_ident_index(self, to_find):

        # TODO: What if the hex contains multiple idents with that state?
        for i in range(len(self.idents)):
            if self.idents[i] == to_find:
                return i
        return -1

    ###############################################################################################################

    # Takes x and y (Cartesian coordinates where (0, 0) is the top left corner)
    # Returns a list of 6 coordinates defining a hexagon
    @staticmethod
    def __create_coor(x, y):
        # Making hex smaller so that borders will be visible
        return [(x+3, y+3), (x+37, y+3), (x+57, y+35), (x+37, y+67), (x+3, y+67), (x-17, y+35)]

    ##########################################################################################################

    # Constructor
    def __init__(self, matrix_index, list_index):
        self.matrix_index = matrix_index
        self.list_index = list_index

        # Store relevant idents
        self.idents = []

        # Map matrix_index and list_index to Cartesian coordinates
        self.x = 60*matrix_index - 20
        self.y = 35*matrix_index + 70*list_index - 490

        self.coordinates = Hex.__create_coor(self.x, self.y)

       
        # TODO: Move arrows and smaller hexagon to idents? (maybe)
        # Create arrows for later use
        #pivot is the center of the hexagon
        pivot = pygame.Vector2(self.x + 20, self.y + 35)
        # set of arrow points should be the vectors from the pivot to the edge points of the arrow
        arrow = [(0, -15), (10, -5), (5, -5), (5, 15), (-5, 15), (-5, -5), (-10, -5)]
        # get arrow by adding all the vectors to the pivot point => allows for easy rotation
        self.arrows = []
        for i in range(6):
            self.arrows.append([(pygame.math.Vector2(x, y)).rotate(60.0*i) + pivot for x, y in arrow]) 
    
        # Coordinates used to draw smaller hexagon later if the hex becomes stationary
        self.small_hexagon = [(self.x+9, self.y+11), (self.x+31, self.y+11), (self.x+47, self.y+35), (self.x+31, self.y+59), (self.x+9, self.y+59), (self.x-7, self.y+35)]
    ##########################################################################################################

    # Returns a boolean indicating if the given hex contains any moving idents
    def is_moving(self):

        for ident in self.idents:
            if ident.state >= 0:
            # if (ident.state != -1) and (ident.state != -2):
                return True
        
        return False
    
    ##########################################################################################################

    # Gives the designated hex a wall identity
    # TODO: Could also clear other idents?
    def make_wall(self, world, list_to_append):
        wall_ident = Ident(self.matrix_index, self.list_index, world, color = (0,0,0), state = -2)
        self.idents.append(wall_ident)
        list_to_append.append(wall_ident)

    ##########################################################################################################

    # Checks if a hex contains an ident heading in the given directon
    # If it does, returns that ident
    # Else returns None
    def contains_direction(self, dir: int):

        # TODO: What if the hex contains multiple idents with that state?
        for ident in self.idents:
            if ident.state == dir:
                return ident

        return None

    ##########################################################################################################

    # Graphics (drawing hexes and the corresponding idents)
    def draw(self, screen):
            
        color_to_draw = Hex.DEFAULT_COLOR


        if (len(self.idents) >= 1):
            # If a hex contains only one ident, take that color
            # If a hex contains multiple idents, the ident stored first will be the outermost color
            color_to_draw = self.idents[0].color
        
        # Draw the hexagon
        pygame.draw.polygon(screen, color_to_draw, self.coordinates)

        # Draw an extra hexagon to visually show that a hexagon is stationary even with the different colors
        if self.contains_direction(-1) != None:
            new_color = [max(0, c - 120) for c in color_to_draw]
            pygame.draw.polygon(screen, new_color, self.small_hexagon)
        
    
        # Draw multiple nesting circles indicating colors for hexes with superimposed idents/states
        for i in range(1, len(self.idents)):
            if (33 - 5*i) > 0:
                pygame.draw.circle(screen, self.idents[i].color, (self.x+20, self.y+35), 33-5*i)
    
        # Draw an arrow on the hex if the hex is moving
        if self.is_moving():
            for i in range(6):
                if self.contains_direction(i):
                    pygame.draw.polygon(screen, (0, 0, 0), self.arrows[i])

    ##########################################################################################################


# for setting initial state of the world / having a student interact
# while loop for running game goes in World
class World:
    def __init__(self):
        pygame.init()

        SCREEN_WIDTH = 800

        SCREEN_HEIGHT = 600

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Hex Simulator")

        # TODO: Copy over timer

        # Set up hex matrix
        self.hex_matrix = []

        for x in range(15):
            hex_list = []
            self.hex_matrix.append(hex_list)

            for y in range(16):
                myHex = Hex(x, y)
                hex_list.append(myHex)
        
        # Set up new hex matrix
        self.hex_matrix_new = []

        for x in range(len(self.hex_matrix)):
            hex_list_new = []
            self.hex_matrix_new.append(hex_list_new)

            for y in range(len(self.hex_matrix[x])):
                myHex = Hex(x, y)
                hex_list_new.append(myHex)

        # Set up ident list
        self.ident_list = []

        # Set up new ident list
        self.ident_list_new = []

        # Set up wall list
        self.wall_list = []

        # reading the intiial state of the hex board from a file
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        file = open(os.path.join(__location__, "initial_state.txt"), "r")
        for line in file:
            self.__read_line(line)
            # pass
            # TODO: uncomment the above line for proper fie reading once we implement moving, stationary, wall hexes back into the program

        
        # Create walls around the edges
        # TODO: Could add boolean so user can specify if they want walls or not
        # Left edge
        for hex in self.hex_matrix[0]:
            hex.make_wall(self, self.wall_list)
        # Right edge
        for hex in self.hex_matrix[13]:
            hex.make_wall(self, self.wall_list)
        for i in range(6):
            # Top edge
            self.hex_matrix[1+2*i][6-i].make_wall(self, self.wall_list)
            self.hex_matrix[2+2*i][6-i].make_wall(self, self.wall_list)

            # Bottom edge
            self.hex_matrix[1+2*i][15-i].make_wall(self, self.wall_list)
            self.hex_matrix[2+2*i][14-i].make_wall(self, self.wall_list)

    ##########################################################################################################

    @classmethod
    def __get_color(self, color_text):
        if color_text == "YELLOW" or color_text == "YELLOW\n":
            return (255, 255, 102)
        elif color_text == "PURPLE" or color_text == "PURPLE\n":
            return (204, 0, 255)
        elif color_text == "ORANGE" or color_text == "ORANGE\n":
            return(255, 102, 0)
        elif color_text == "GREEN" or color_text == "GREEN\n":
            return(106, 232, 100)
        elif color_text == "BLUE" or color_text == "BLUE\n":
            return(45, 70, 181)
        elif color_text == "CYAN" or color_text == "CYAN\n":
            return (71, 230, 216) 
        elif color_text == "RED" or color_text == "RED\n":
            return(219, 24, 24)
        elif color_text == "MAROON" or color_text == "MAROON\n":
            return (143, 6, 15)
        elif color_text == "PINK" or color_text == "PINK\n":
            return(230, 57, 129)
        else:
            return (100, 100, 100)

    ##########################################################################################################

    def __read_line(self, line):
        # actual parsing of the text file
        line_parts = line.split(" ")
        
        matrix_index = int(line_parts[0])
        list_index = int(line_parts[1])
        command = line_parts[2]

        if command == "move":
            direction = int(line_parts[4])
            color_text = line_parts[3]
            color = World.__get_color(color_text)
            new_ident = Ident(matrix_index, list_index, self, color = color, state = direction)
            
            # Add ident to ident list
            self.ident_list.append(new_ident)
            
            # Add ident to hex
            self.hex_matrix[matrix_index][list_index].idents.append(new_ident)
        elif command == "occupied":
            color_text = line_parts[3]
            color = World.__get_color(color_text)
            new_ident = Ident(matrix_index, list_index, self, color = color)
            
            # Add ident to ident list
            self.ident_list.append(new_ident)
            
            # Add ident to hex
            self.hex_matrix[matrix_index][list_index].idents.append(new_ident)
        elif command == "wall" or command == "wall\n":
            new_ident = Ident(matrix_index, list_index, self, color = (0,0,0), state = -2)
            
            # Add wall ident to wall list instead of ident list
            self.wall_list.append(new_ident)     
               
            # Add ident to hex
            self.hex_matrix[matrix_index][list_index].idents.append(new_ident)

    ##########################################################################################################

    # Draws world
    def __draw(self):
        # Reset screen
        self.screen.fill((0, 0, 0))

        # Draw all hexes with idents
        for hex_list in self.hex_matrix:
            for hex in hex_list:
                hex.draw(self.screen)

    ##########################################################################################################

    # Swaps which matrix is being used
    def __swap_matrices_and_lists(self):
        temp_matrix = self.hex_matrix
        self.hex_matrix = self.hex_matrix_new
        self.hex_matrix_new = temp_matrix

        temp_list = self.ident_list
        self.ident_list = self.ident_list_new
        self.ident_list_new = temp_list

    ##########################################################################################################

    def __update(self):
        # TODO: Note that this (calling swap_matrices) will just cause flashing until these two methods are written

        # TODO: Don't overwrite wall idents? (trying to save computation of constantly erasing and re-writing them)

        # Clear the _new matrix and list so that advance_or_flip can write to it
        for hex_list in self.hex_matrix_new:
            for hex in hex_list:
                # Save wall_ident to add back in, if applicable
                wall_ident = hex.contains_direction(-2)
                
                hex.idents.clear()
                
                if wall_ident:
                    self.hex_matrix_new[wall_ident.matrix_index][wall_ident.list_index].idents.append(wall_ident)
        
        self.ident_list_new.clear()

        # Move or flip all idents (except for walls)
        for ident in self.ident_list:
            ident.advance_or_flip()

        # Clear the current matrix and list so that resolve_collisions can write to it
        for hex_list in self.hex_matrix:
            for hex in hex_list:
                # Save wall_ident to add back in, if applicable
                wall_ident = hex.contains_direction(-2)
                
                hex.idents.clear()
                
                if wall_ident:
                    self.hex_matrix[wall_ident.matrix_index][wall_ident.list_index].idents.append(wall_ident)
        
        self.ident_list.clear()
                
        # Fix collisions in all idents (except for walls)
        for ident in self.ident_list_new:
            ident.resolve_collisions()

        # Pause between each frame
        pygame.time.delay(600)

    ##########################################################################################################

    def run(self):
        run = True
        while run:

            # Event handler (closing window)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            
            self.__draw()

            # flips to the next frame
            pygame.display.flip()
            
            self.__update()
        
        # Exit
        pygame.quit()
