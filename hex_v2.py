import time
import copy
import os
import pygame

'''
Process of the game:
0. Iterate over Idents
1. a: If an ident is in a head on collision with another ident, it flips in place
   b: Else, move the ident forward into the next hex
2. Resolve collisions. For hexes that contain multiple idents...
   a: If it has an ident of opposite direction in that hex, bounce off/reverse direction
   b: Else, take the average of all other idents EXCEPT SELF, but break ties by using the opposite ident of self
'''

# hex class is now just for graphics/displaying the board/storing idents
class Hex:
    def __init__(self):
        pass

# for storing information about a particular moving hex
class Ident:

    idents_created = 0

    def __init__(self, color=(255, 255, 255), state = -1, serial_number = -1, hist = None):
        if hist is None:
            hist = []
        self.color = color

        self.state = state
        self.hist = hist
        if serial_number == -1:
            # If no serial number is provided
            self.serial_number = Ident.idents_created

            print("Ident with serial number " + str(self.serial_number) + " created")
            if state == -2:
                print("Is a wall")
            elif state == -1:
                print("Is stationary")
            else:
                print("Is moving")
            Ident.idents_created += 1
        else:
            self.serial_number = serial_number
            print("Ident with serial number " + str(self.serial_number) + " copied")
            print("color: " + str(self.color))


# for setting initial state of the world / having a student interact
# while loop for running game goes in World
class World:
    pass