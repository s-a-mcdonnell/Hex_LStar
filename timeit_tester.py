from teacher import Teacher
from learner import Learner
import timeit
import os

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

def world_init():

    s = Teacher.generate_string()
    print(s)
    movement_learner.my_teacher._create_world(s)

    del movement_learner.my_teacher.world

alphabet = []

print("start")

# reading the alphabet from a file
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
file = open(os.path.join(__location__, "alphabet.txt"), "r")
for line in file:
    __read_line(line)

print("ALPHABET PARSED")

movement_learner = Learner(alphabet=alphabet, teacher_type=0)

exec_time = timeit.timeit("world_init()", "from __main__ import world_init", number=5000)
print(f"{exec_time} secs.")

average = exec_time/float(5000)
print(f"Average time per call: {average} seconds.")