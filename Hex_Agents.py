
import pygame

#######################################################################################################################
#######################################################################################################################
#                                                  AGENT CLASS                                                        #

class Agent:
    """
    An agent must define a getAction method, but may also define the
    following methods which will be called if they exist:

    def registerInitialState(self, state): # inspects the starting state
    """
    def __init__(self, index=0):
        self.index = index

    def get_inf(self, state, keys):
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

    def get_inf(self, state, keys):

        if keys != None:
            if keys[pygame.K_d]:
                influence = 1
            elif keys[pygame.K_a]:
                influence = -1
            else:
                influence = 0
        else:
            influence = 0

        return influence





