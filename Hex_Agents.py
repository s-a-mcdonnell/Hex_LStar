
import pygame

#######################################################################################################################
#######################################################################################################################
#                                                  AGENT CLASS                                                        #

class Agent:

    ###################################################################################################################

    def __init__(self, index=0):
        self.index = index

    ###################################################################################################################

    def get_dir(self, state, keys):
        """
        The Agent will receive a GameState (from hex) and
        must return an action from Directions.{Clockwise, CounterClockwise, Forward}
        """
        print("incorrect, please load a type of agent")

#######################################################################################################################
#######################################################################################################################
#                                              KEYBOARD AGENT CLASS                                                   #

class KeyboardAgent(Agent):

    ###################################################################################################################

    # Constructor

    def __init__(self, index=0):

        self.index = index

    ###################################################################################################################

    def get_dir(self, state, keys, cur_dir):

        if keys != None:
            if keys[pygame.K_d]:
                influence = 1
            elif keys[pygame.K_a]:
                influence = -1
            else:
                influence = 0
        else:
            influence = 0

        if cur_dir >= 0:
            cur_dir += influence
            cur_dir %= 6

        return cur_dir





