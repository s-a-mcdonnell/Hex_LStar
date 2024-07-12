from l_star_tester import read_alphabet
from l_star_tester import read_dfa

import os
from teacher import Teacher
# import pdb; pdb.set_trace()


##########################################################################################################

# Returns the agent's move in reaction to the passed world-string
def __get_move(s : str):
    movement = my_teacher.member(s, movement_dfa, alphabet)
    direction = my_teacher.member(s, direction_dfa, alphabet)
    print(f"movement {movement}, direction {direction}")

    if not movement:
        return 0
    elif direction:
        return 1
    else:
        return -1
    
##########################################################################################################

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
alphabet = read_alphabet(__location__)
print("alphabet parsed")

# Parse DFAs saved to text files
movement_dfa = read_dfa(__location__, "movement_dfa.txt", alphabet=alphabet)
direction_dfa = read_dfa(__location__, "direction_dfa.txt", alphabet=alphabet)

print("dfas parsed")

my_teacher = Teacher(alphabet, num_states = 1)

print(f"Agent move: {__get_move("947f68")}")
print(f"Agent move: {__get_move("c67f48357")}")
print(f"Agent move: {__get_move("ba6f48857")}")
