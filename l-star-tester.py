from learner import Learner
import sys
import os

##########################################################################################################

# Reads chars from the alphabet file and returns list storing alphabet
def __read_alphabet(loc):

    # Default alphabet is 0 and 1
    try:
        alpha_file = open(os.path.join(loc, "alphabet.txt"), "r")
    except:
        return ['0', '1']
    
    alpha = []

    for line in alpha_file:
        # Check type and length of character in alphabet
        assert type(line) is str
        assert (len(line) == 1) or (len(line) == 2)
        if len(line) == 2:
            assert line[1] == '\n'

        # Add character to alphabet
        alpha.append(line[0])
    
    return alpha

##########################################################################################################

# Reads lines from the DFA file and returns matrix (2d list) storing DFA
def __read_dfa(loc):
    # Return None if no file is provided
    try:
        dfa_file = open(os.path.join(loc, "dfa.txt"), "r")
    except:
        print("Error: No file dfa.txt found. DFA to be learned will be randomly generated.")
        return None
    
    dfa = []

    for line in dfa_file:

        # Parsing the text file
        line_parts = line.split(" ")
        print(f"line_parts: {line_parts}")

        to_append = []

        # Save each int in the text file to the to_append list for that row
        for num in line_parts:
            to_append.append(int(num))


        # Check that the row of the DFA is the length of the alphabet plus 1
        print(f"to_append: {to_append}")
        if len(to_append) != len(alphabet) + 1:
            print(f"Error: DFA row size {len(to_append)} incompatible with alphabet of size {len(alphabet)}. Row will not be included in DFA to be learned.")
            continue

        # Append row to DFA
        dfa.append(to_append)
    
    # Check if all rows were deemed invalid (or if the file was blank)
    if not len(dfa):
        print("Error: No usable lines found in dfa.txt. DFA to be learned will be randomly generated.")
        return None
    
    # Return parsed DFA
    return dfa

##########################################################################################################

# Print usage information
print("Welcome to the L* Tester")
print("This program accepts up to three command-line arguments and up to two file inputs")
print("Command-line arguments: Boolean (True or False, 1 or 0) indicating whether or not graphs are to be drawn, int specifying the number of states in the DFA to be learned, int specifying the seed for a pseudo-randomized DFA")
print("File inputs: The alphabet to use (alphabet.txt) and a pre-made DFA for testing (dfa.txt)")
print("----------")

# Parse inputs:
# Use first command-line argument (if present) to determine whether or not to show graphs (default is not)
show_graphs = False
if len(sys.argv) > 1:
    if sys.argv[1].lower() == "true" or sys.argv[1] == '1':
        show_graphs = True
    elif sys.argv[1].lower() == "false" or sys.argv[1] == '0':
        pass
    else:
        print(f"Error: Invalid boolean specifying if graphs are to be shown: {sys.argv[1]}")
        print("Graphs will not be shown")

# Set number of states in DFA (if provided)
num_states = -1
if len(sys.argv) > 2:
    num_states = int(sys.argv[2])

# Set seed for pseudo-random number generation (if provided)
seed = 1821
if len(sys.argv) > 3:
    seed = int(sys.argv[3])

# Import alphabet from text file (if provided, else use binary alphabet)
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
alphabet = __read_alphabet(__location__)
print(f"alphabet: {alphabet}")

# Read DFA from text file (if provided and not overridden by command-line args)
if len(sys.argv) <= 2:
    dfa_for_testing = __read_dfa(__location__)
else:
    dfa_for_testing = None

# Create learner:
# If command-line arguments are provided, pass them to the learner
if len(sys.argv) > 2:
    my_learner = Learner(alphabet, num_states = num_states, seed = seed, display_graphs=show_graphs)

# Else if a DFA was provided, use it
elif dfa_for_testing:
    my_learner = Learner(alphabet, premade_dfa = dfa_for_testing, display_graphs=show_graphs)

# Else allow the DFA to be randomly generated
else:
    my_learner = Learner(alphabet=alphabet, display_graphs=show_graphs)


# Let algorithm run in learner
my_learner.lstar_algorithm()