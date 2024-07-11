import os
import sys
from learner import Learner
from movement_teacher import Movement_Teacher
from direction_teacher import Direction_Teacher

def __read_line(line):
    global alphabet
    # If the line ends in a new line character, add everything except the new line character as an entry in the alphabet
    if line[len(line) - 1] == "\n":
        assert len(line) == 4
        alphabet.append(line[0:len(line)-1])
    
    # If the line doesn't end in a new line character, add it as an entry in the alphabet
    else:
        assert len(line) == 3
        alphabet.append(line)

##########################################################################################################

alphabet = []

# reading the intial state of the hex board from a file
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
file = open(os.path.join(__location__, "alphabet.txt"), "r")
for line in file:
    __read_line(line)

print(alphabet)

'''mover = Movement_Teacher(alphabet)
director = Direction_Teacher(alphabet)'''


# Create learners:
movement_learner = Learner(alphabet=alphabet, teacher_type=0)
direction_learner = Learner(alphabet=alphabet, teacher_type=1)

# TODO: Modify teachers to make algorithm work
# TODO: Make learners return learner DFA so we can use it as desired
# Learn movement teacher using L*
movement_learner.lstar_algorithm()

# Learn direction teacher using L*
direction_learner.lstar_algorithm()