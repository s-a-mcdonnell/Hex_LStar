import os
import sys
from learner import Learner
from movement_teacher import Movement_Teacher
from direction_teacher import Direction_Teacher
# import pdb; pdb.set_trace()

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

# Returns the agent's move in reaction to the passed world-string
def __get_move(s : str):
    movement = movement_learner.my_teacher.member(s, movement_DFA, alphabet)
    direction = direction_learner.my_teacher.member(s, direction_DFA, alphabet)
    print(f"movement {movement}, direction {direction}")

    if not movement:
        return 0
    elif direction:
        return 1
    else:
        return -1


##########################################################################################################

alphabet = []

# reading the alphabet from a file
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
file = open(os.path.join(__location__, "alphabet.txt"), "r")
for line in file:
    __read_line(line)

print("ALPHABET PARSED")

# Create learners:
# 0 -> movement teacher, 1 -> direction teacher
movement_learner = Learner(alphabet=alphabet, teacher_type=0)
direction_learner = Learner(alphabet=alphabet, teacher_type=1)

# TODO: Modify teachers to make algorithm work
# TODO: Make learners return learner DFA so we can use it as desired
# Learn movement teacher using L*
movement_DFA = movement_learner.lstar_algorithm()
print("FIRST DFA => MOVEMENT => IS DONE")

# Learn direction teacher using L*
direction_DFA = direction_learner.lstar_algorithm()
print("SECOND DFA => DIRECTION => IS DONE")

# breakpoint()

print(f"Agent move: {__get_move("947f68")}")
print(f"Agent move: {__get_move("c67f48357")}")
print(f"Agent move: {__get_move("ba6f48857")}")

# TODO: methods to predict the agent's reaction to certain states based on the two DFA's we've created