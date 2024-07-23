import cProfile
import pstats

import os
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

##############################################################################################

def __write_dfa_to_file(dfa, loc, file_name):
    # Return None if no file is provided
    try:
        dfa_file = open(os.path.join(loc, file_name), "w")
    except:
        print(f"Error: No file {file_name} found.")
        return

    for row in dfa:
        for entry in row:
            dfa_file.write(str(entry))

            # Space between entries in a row
            if row.index(entry) < len(row) - 1:
                dfa_file.write(' ')
        
        # New line between rows     
        if dfa.index(row) < len(dfa) - 1:
            dfa_file.write('\n')
    
    # TODO: Close file?


##########################################################################################################

with cProfile.Profile() as profile:

    alphabet = []

    print("start")

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

    print("DFAs INITIALIZED")
    print()

    # Learn movement teacher using L*
    movement_DFA = movement_learner.lstar_algorithm()
    print("FIRST DFA => MOVEMENT => IS DONE")

    # write first DFA to a file for ease of access
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    __write_dfa_to_file(movement_DFA, __location__, "movement_dfa.txt")


    # Learn direction teacher using L*
    direction_DFA = direction_learner.lstar_algorithm()
    print("SECOND DFA => DIRECTION => IS DONE")

    # write direction teacher to a file
    __write_dfa_to_file(direction_DFA, __location__, "direction_dfa.txt")

    # NOTE: use test_points.py to test the results of the DFAs generated in this solver.py file

    print("end")

results = pstats.Stats(profile)
results.sort_stats(pstats.SortKey.TIME)

# results.print_stats() 
# NOTE: uncomment thr above if you want to have the stats printed into the terminal

results.dump_stats("results.prof")
# NOTE: the above allows the tuna package "pip install tuna" to provide a visual representation of function time using "tuna results.prof"