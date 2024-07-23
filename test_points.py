from l_star_tester import read_alphabet
from l_star_tester import read_dfa
import os
import sys
from teacher import Teacher
import make_alphabet
import random
from hex_v2 import World, Ident
# import pdb; pdb.set_trace()


##########################################################################################################

# Returns the agent's move in reaction to the passed world-string
def __get_move(s : str):
    
    movement = mov_teach.member(s, movement_dfa, alphabet)
    direction = dir_teach.member(s, direction_dfa, alphabet)
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

mov_teach = Teacher(alphabet, num_states = 1, premade_dfa = movement_dfa)
dir_teach = Teacher(alphabet, num_states = 1, premade_dfa = direction_dfa)

print(f"Agent move from string 979f88: {__get_move("979f88")}")
print(f"Agent move from string b77f98f78: {__get_move("b77f98f78")}")
print()

# TODO: more direction test cases for the one DFA that we have :P

'''for i in range(1, len(sys.argv)):
    assert len(sys.argv[i])%3 == 0
    assert len(sys.argv[i]) >= 6
    print(f"Agent move from string {sys.argv[i]}: {__get_move(sys.argv[i])}")'''    

'''for i in range(20):
    new_string = Teacher.generate_string()
    print(f"Agent move from string {new_string}: {__get_move(new_string)}")'''

goals = ["f77", "f78", "f79", "f87", "f88", "f89", "f97", "f98", "f99"]

tally = 0
true_tally = 0

for i in range(0, 10000):
    strg = ""

    my_agent = ""
    while not make_alphabet.check_validity(my_agent):
        my_agent = ""
        agent_dir = random.randint(9, 14)
        agent_mi = random.randint(0, 15)
        agent_li = random.randint(0, 15)
        # TODO: Check that this hex method correctly converts and returns a string
        my_agent += hex(agent_dir)[2] + hex(agent_mi)[2] + hex(agent_li)[2]

    assert my_agent

    # Save valid agent
    strg += my_agent

    goal = goals[random.randint(0, 8)]

    strg += goal

    dir_teach._create_world(strg)
    assert dir_teach.my_agent
    agent_dir = Ident.find_next_move(dir_teach.my_agent)

    print(f"World says result is agent move: {agent_dir}")
    test = __get_move(strg)
    print(f"DFA says agent move from string {strg}: {test}")
    if(agent_dir != test):
        tally += 1
    if(agent_dir == test):
        true_tally += 1

    print()

print(f"Incorrect DFA outcomes: {tally} / 10,000")
print(f"Correct DFA outcomes: {true_tally} / 10,000")