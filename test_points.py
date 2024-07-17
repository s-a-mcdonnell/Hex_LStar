from l_star_tester import read_alphabet
from l_star_tester import read_dfa
import os
import sys
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
    
def __get_direction(s : str):
    direction = my_teacher.member(s, direction_dfa, alphabet)
    print(f"direction {direction}")

    if direction:
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

print(f"Agent move from string 979f88: {__get_move("979f88")}")
print(f"Agent move from string c67f48357: {__get_move("c67f48357")}")
print(f"Agent move from string ba6f48857: {__get_move("ba6f48857")}")

print()

'''for i in range(1, len(sys.argv)):
    assert len(sys.argv[i])%3 == 0
    assert len(sys.argv[i]) >= 6
    print(f"Agent move from string {sys.argv[i]}: {__get_move(sys.argv[i])}")'''    

'''for i in range(20):
    new_string = Teacher.generate_string()
    print(f"Agent move from string {new_string}: {__get_move(new_string)}")'''

goals = ["fc0", "fe0", "fe1", "fd3", "fb4", "fa2", "fa4", "fb2", "fc1", "fd1", "fd2", "fc3", "fb3"]

strng = "cc2"

goals2 = []
# Save new ident in the correct order
for goal in goals:
    # If other_idents is empty, add to it
    if not len(goals2):
        goals2.append(goal)

    # Add the final ident in other_idents in smaller than the new_ident, add at the back
    elif Teacher.less_than(goals2[len(goals2) - 1], goal, strng):
        goals2.append(goal)

    # Otherwise iterate through other_ident until the correct location is found
    else:
        for ident in goals2:
            if not Teacher.less_than(ident, goal, strng):
                goals2.insert(goals2.index(ident), goal)
                break


for goal in goals2:
    strng += goal

print(f"final string: {strng}")