import random
from hex_v2 import World, Ident
import make_alphabet
import pdb

##############################################################################################################

class Teacher:

    ##########################################################################################################

    # Constructor
    def __init__(self, alphabet, num_states = -1, seed = 1821, premade_dfa = None):
        # TODO: Delete debugging print statement
        # print("teacher created")

        # The teacher will use the provided alphabet
        self.alphabet = alphabet

        # Check the alphabet for validity (each symbol is just one character)
        for symbol in alphabet:
            if len(symbol) != 1:
                print("Error: Invalid alphabet")
                exit(1)

        # Using this guide to PRN generation in Python: https://www.tutorialspoint.com/generate-pseudo-random-numbers-in-python
        random.seed(seed)
        
        # If a premade DFA was provided, use it
        if premade_dfa:
            self.m = premade_dfa

        # Else, create a DFA
        else:
            # Determine the number of states in the DFA (between 1 and 100, inclusive)
            # NOTE: The upper limit here is arbitrarily chosen
            # NOTE: Not all of these will be accessible, depending on how the arrows point
            if num_states == -1:
                num_states = random.randint(1, 100)

            # The DFA (M) is a matrix in which the rows are the states
            # The first entry in each row is a boolean in int form (0 or 1) indicating whether the state is an accept (1) or reject (0) state
            # The remaining entries in each row are the numbers of the states which the corresponding alphabet value at that index points to
            self.m = []
            
            # Initialize all values in M to -1 (invalid)
            for i in range(num_states):
                new_state = []
                self.m.append(new_state)
                for j in range(len(alphabet) + 1):
                    self.m[i].append(-1)

            arrows_created = 0
            accept_states = 0
            reject_states = 0
            # Set each arrow in each state to point at a random state
            for state in self.m:
                # The first entry in each state is a boolean indicating whether it is an accept or reject state
                state[0] = random.randint(0, 1)
                if state[0]:
                    accept_states += 1
                else:
                    reject_states += 1

                # The subsequent entries indicate which state a given alphabet value directs to
                for i in range(1, len(state)):
                    arrow = random.randint(0, num_states - 1)
                    state[i] = arrow
                    arrows_created += 1
            
            # Print DFA
            print("DFA to learn:")
            print(self.m)

    ##########################################################################################################

    # equivalency query
    # takes the DFA hypothesis m_hat
    # returns either a counterexample or False (indicating that the DFAs match)
    # TODO: Adapt for hex world
    def equivalent(self, m_hat):
        assert m_hat
        if len(self.m[0]) != len(m_hat[0]):
            print("Incompatable alphabet size")
            return True

        # print("equivalency query called")

        # Generate and test an arbitrarily large number of strings
        # for each of these strings, if self.member(s, self.m) is not self.member(s, m_hat), return s

        for i in range(1000000):
            s = Teacher.generate_string()
            if self.member(s) != self.member(s, m_hat):
                assert(type(self.member(s)) is bool)
                assert(type(self.member(s, m_hat)) is bool)
                # TODO: Delete debugging print statement
                # print("Counterexample found: " + s)
                return s            

        # else return false (so that the truthiness of a counterexample and a matching DFA result will be different)
        print("No counterexample found")
        return False

    ##########################################################################################################
    
    @staticmethod
    def final_state(s : str, dfa: list[list[int]], alpha):

        input = []

        assert (type(s) is str)

        # Convert passed string into an array of ints, where each int is the index in the alphabet array corresponding to that character
        for char in s:
            input.append(alpha.index(char))
        
        # Enter the DFA (M) at state 0
        next_state_index = 0

        # Navigate through the DFA to the final state
        for char_index in input:
            current_state = dfa[next_state_index]
            next_state_index = current_state[char_index + 1]
        
        # Return final state
        return dfa[next_state_index]
        
    ##########################################################################################################
    # TODO: Create option not to read agent file?
    def __create_world(self, s):
        new_world = World(read_file=False)
            
        # Parse string into world
        for i in range(len(s)/3):
            # splice the three character string into three one-character chunks
            property = int(s[i*3], 16)
            mi = int(input[i*3 + 1], 16)
            li = int(input[i*3 + 2], 16)

            new_ident = Ident(mi, li, new_world)

            new_world.hex_matrix[mi][li].idents.append(new_ident)
            
            # The first char in ever "letter" (3-char string) form the property
            # The properties are wall (0), stationary non-agent (1), moving agent (in directions 0 through 5, 1 through 7),
            # stationary agent (8), moving agent (in directions 0 through 5, 9 through e), and goal (f)

            # 0 => wall
            if property == 0:
                new_ident.state = -2
                new_world.wall_list.append(new_ident)

            # If not a wall, it goes on the ident list
            else:
                new_world.ident_list.append(new_ident)

            # 1 => stationary (non-agent)
            if property == 1:
                new_ident.state = -1
            
            # 2 => direction 0 (non-agent)
            # 3 => direction 1 (non-agent)
            # 4 => direction 2 (non-agent)
            # 5 => direction 3 (non-agent)
            # 6 => direction 4 (non-agent)
            # 7 => direction 5 (non-agent)
            elif property >= 2 and property <= 7:
                new_ident.state = property - 2
            
            # 8 => stationary (agent)
            if property == 8:
                new_ident.state = -1
                new_world.agents.append(new_ident)
            
            # 9 => direction 0 (agent)
            # 10 => direction 1 (agent)
            # 11 => direction 2 (agent)
            # 12 => direction 3 (agent)
            # 13 => direction 4 (agent)
            # 14 => direction 5 (agent)
            elif property >= 9 and property <= 14:
                new_ident.state = property - 9
                new_world.agents.append(new_ident)

            # 15 => goal (stationary)
            elif property == 15:
                new_ident.state = -1
                # Mark as goal
                new_ident.property = "goal"
            
            # Save the first ident described in the string as my_agent
            if i == 0:
                self.my_agent = new_ident
        
        self.world = new_world    


    # membership query
    # takes a string s and returns a boolean indicating whether s is accepted or rejected by the given DFA
    # TODO: Adapt for hex world
    def member(self, s : str, dfa: list[list[int]] = None, alpha = None):
        # print("membership query called")

        if not alpha:
            alpha = self.alphabet

        # If passed a matrix, use it as the dfa and return boolen indicating final state action
        if dfa:        
            # Return the int boolean indicating if the final state is an accept or reject state
            final_state : list[int] = Teacher.final_state(s, dfa, alpha)
            return bool(final_state[0])
        
        # If not passed a matrix, return an answer as if the agent's decision-making process were a DFA
        else:
            # Always reject the empty string (arbitrary decision)
            if s == "":
                return False
            
            self.__create_world(s)
            assert self.world
            assert self.my_agent
            
            original_agent_state = self.my_agent.state
            new_state = Ident.find_next_move(self.my_agent)
            # NOTE: hopefully find_next_move will be updated 

            # TODO: Run one loop of updating the world and check was the agent's state is
            # TODO: How to know what part of the agent instructions the world should be looking at? (potentially big issue, since we've created a world from scratch)
            # self.world.update()

            # TODO: Return a boolean corresponding to the agent's state
            # TODO: Actually we want to just report the agent's action, not how it might have been affected by the physics rules
            if new_state == 0:
                return False
            # false on first DFA => we are not manually changing the agent's direction (ie -> instruction 0)
            # true on first DFA => we are changing the agent's direction via the agent (ie -> instruction -1 or 1)
            else:
                return True
    
    ##########################################################################################################

    @staticmethod
    # Sorts and returns the passed ident_list using merge sort
    # Based off of code provided for merge sort here: https://www.geeksforgeeks.org/merge-sort/#
    def __merge_sort(ident_list, begin=-1, end=-1):
        if begin == -1 and end == -1:
            begin = 0
            end = len(ident_list)
        
        assert begin != -1
        assert end != -1

        # begin is for left index and end is right index
        # of the sub-array of arr to be sorted
        if begin >= end:
            return

        mid = begin + (end - begin) // 2
        Teacher.__merge_sort(ident_list, begin, mid)
        Teacher.__merge_sort(ident_list, mid + 1, end)
        Teacher.__merge(ident_list, begin, mid, end)  

        return ident_list

    ##########################################################################################################

    @staticmethod
    # Merges two sublists
    # First sublist is list[left..mid]
    # Second sublist is list[mid+1..right]
    # Code provided for merge sort here: https://www.geeksforgeeks.org/merge-sort/#
    def __merge(my_list, left, mid, right):
        sublist_1 = mid - left + 1
        sublist_2 = right - mid

        # Create temp lists
        left_list = [0] * sublist_1
        right_list = [0] * sublist_2

        # Copy data to temp arrays leftArray[] and rightArray[]
        for i in range(sublist_1):
            left_list[i] = my_list[left + i]
        for j in range(sublist_2):
            right_list[j] = my_list[mid + 1 + j]

        index_of_sublist_1 = 0  # Initial index of first sub-array
        index_of_sublist_1 = 0  # Initial index of second sub-array
        index_of_merged_list = left  # Initial index of merged array

        # Merge the temp arrays back into array[left..right]
        while index_of_sublist_1 < sublist_1 and index_of_sublist_1 < sublist_2:
            if left_list[index_of_sublist_1] <= right_list[index_of_sublist_1]:
                my_list[index_of_merged_list] = left_list[index_of_sublist_1]
                index_of_sublist_1 += 1
            else:
                my_list[index_of_merged_list] = right_list[index_of_sublist_1]
                index_of_sublist_1 += 1
            index_of_merged_list += 1

        # Copy the remaining elements of left[], if any
        while index_of_sublist_1 < sublist_1:
            my_list[index_of_merged_list] = left_list[index_of_sublist_1]
            index_of_sublist_1 += 1
            index_of_merged_list += 1

        # Copy the remaining elements of right[], if any
        while index_of_sublist_1 < sublist_2:
            my_list[index_of_merged_list] = right_list[index_of_sublist_1]
            index_of_sublist_1 += 1
            index_of_merged_list += 1      


    ##########################################################################################################

    # TODO: Adapt for hex world
    # NOTE: For now, we will only generate 17-char strings, with the first bit indicating whether or not there are walls around the edges, the next 8 bit specifying the coordinates of the agent, the last 8 indicating the coordinates of the goal
    # NOTE issue: How will the hex world respond when quieried like a DFA when the string is the wrong length? Could we work on how we define the alphabet to allow multiple-char letters so that things will be added/removed on the level of a unit of meaning?
    @staticmethod
    def generate_string():
        strg = ""

        # Generate a valid agent of random direction and location
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

        # Generate a valid goal of random location
        my_goal = ""
        while not make_alphabet.check_validity(my_goal):
            my_goal = ""
            goal_mi = random.randint(0, 15)
            goal_li = random.randint(0, 15)
            # TODO: Check that this hex method correctly converts and returns a string
            my_goal += "f" + hex(goal_mi)[2] + hex(goal_li)[2]

        assert my_goal

        # Save valid goal
        strg += my_goal

        # TODO: Generate a pseudo-randomly determined number of other 3-char strings (idents)
        # NOTE: The choice of maximum number of idents is arbitrary
        # num_idents = random.randint(0, 50)
        num_idents = 3
        other_idents = []
        for i in range(num_idents):
            # breakpoint()
            new_ident = ""
            
            # Loop until we have made a novel valid ident
            while not (make_alphabet.check_validity(new_ident) and new_ident not in other_idents):
                new_ident = ""
                # breakpoint()
                # NOTE: the new idents cannot be goals
                ident_prop = random.randint(0, 14)
                ident_mi = random.randint(0, 15)
                ident_li = random.randint(0, 15)
                # TODO: Check that this hex method correctly converts and returns a string
                new_ident += hex(ident_prop)[2] + hex(ident_mi)[2] + hex(ident_li)[2]

            assert new_ident
            assert new_ident not in other_idents

            # Save new ident
            other_idents.append(new_ident)

        # TODO: Sort the three-char strings first by matrix index (2nd char), then list index (2nd char), then property (1st char)
        Teacher.__merge_sort(other_idents)

        # Concatenate these ident strings in the given order then return
        for ident_string in other_idents:
            strg += ident_string
        
        return strg

    ##########################################################################################################

##############################################################################################################