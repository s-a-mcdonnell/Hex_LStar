# The second teacher (for an agent that is turning, is it turning clockwise or counterclockwise?)

from teacher import Teacher

class Direction_Teacher(Teacher):
    def __init__(self, alphabet):
        self.alphabet = alphabet
        # TODO: Write constructor
