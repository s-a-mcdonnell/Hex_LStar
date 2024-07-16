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

        # NOTE: I am commenting out this check for now. Hopefully L Star will still function with a multi-charcater alphabet :)))
        # Check the alphabet for validity (each symbol is just one character)
        # for symbol in alphabet:
        #     if len(symbol) != 1:
        #         print("Error: Invalid alphabet")
        #         exit(1)

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
        for i in range(int(len(s)/3)):
            input.append(alpha.index(s[i*3 : i*3 + 3]))
        
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
    def _create_world(self, s):
        # Assert that the length of the world-string is valid
        # NOTE: The >= 6 assertion leads to crashing, as sometimes a three-char string (one letter of the alphabet) is passed
        if len(s) < 6 or len(s)%3 != 0:
            print(f"Odd length world-string: {s}")
        # assert(len(s) >= 6)
        assert(len(s) % 3 == 0)

        new_world = World(read_file=False, display_window=False)
            
        # Parse string into world
        # TODO: the forcibly converting it into an integer could cause problems later. Note to self, be careful.
        for i in range(int((len(s))/3)):
            # splice the three character string into three one-character chunks
            property = int(s[i*3], 16)
            mi = int(s[i*3 + 1], 16)
            li = int(s[i*3 + 2], 16)

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

        if not dfa:
            dfa = self.m
        
        if not alpha:
            alpha = self.alphabet

        # Return the int boolean indicating if the final state is an accept or reject state
        final_state : list[int] = Teacher.final_state(s, dfa, alpha)
        return bool(final_state[0])
    
    ##########################################################################################################

    '''@staticmethod
    # Sorts and returns the passed ident_list using merge sort
    # Based off of code provided for merge sort here: https://www.geeksforgeeks.org/merge-sort/#
    def __merge_sort(ident_list, begin=-1, end=-1):
        # breakpoint()
        if begin == -1 and end == -1:
            begin = 0
            end = len(ident_list)
        
        assert begin != -1
        assert end != -1

        # begin is for left index and end is right index
        # of the sublist of my_list to be sorted
        if begin >= end:
            return

        mid = begin + (end - begin) // 2
        Teacher.__merge_sort(ident_list, begin, mid)
        Teacher.__merge_sort(ident_list, mid + 1, end)
        Teacher.__merge(ident_list, begin, mid, end)  

        return ident_list'''

    ##########################################################################################################

    @staticmethod
    # Returns the distance between two passed idents
    # NOTE: This distance calculation overlaps with a method Allison wrote in World
    def __get_distance(id_1:list[int], id_2:list[int]):
        
        # The difference in the matrix index of the idents (vertical)
        mi_dist = id_1[1] - id_2[1]

        # The difference in the list index of the idents (northwest to southeast)
        li_dist = id_1[2] - id_2[2]

        # The total distance is greater of the absolute values of the two partial distances
        total_dist = abs(mi_dist)
        if abs(li_dist) > total_dist:
            total_dist = abs(li_dist)
        # If the partial distances are both positive or both negative, the total distance is the sum of their absolute values
        # TODO: Will there be any issues here if mi_dist and/or li_dist == 0?
        if ((mi_dist > 0) == (li_dist > 0)) and ((mi_dist < 0) == (li_dist < 0)):
            total_dist = abs(mi_dist) + abs(li_dist)
        
        return total_dist

    @staticmethod
    # Returns a list of two numbers, where the first is the distance (in terms of number of hexes) from the given ident to the agent
    # And the second is the relative direction from the agent in which one would have to travel to reach the ident
    def __get_distance_and_direction(id:list[int], ag:list[int]):
        
        # The difference in the matrix index of the idents (vertical)
        mi_dist = id[1] - ag[1]

        # The difference in the list index of the idents (northwest to southeast)
        li_dist = id[2] - ag[2]
        
        # The direction in which the agent is currently pointing
        agent_dir = ag[0] - 9
        # If the agent is stationary, default to direction 0
        if agent_dir == -1:
            agent_dir = 0
        print(f"ag {ag}, agent_dir {agent_dir}")
        assert agent_dir >= 0
        assert agent_dir <= 5
        
        # The total distance is greater of the absolute values of the two partial distances
        total_dist = Teacher.__get_distance(id, ag)
        
        # Deal with ident in the same location as the agent
        if mi_dist == 0 and li_dist == 0:
            print("angle case -1 (overlapping)")
            
            # TODO: Return a direction other than 0? (0 also has another meaning --> straight ahead)
            # return [total_dist, 0]
            if id[0] >= 2 and id[0] <= 7:
                abs_angle = id[0] - 2
            elif id[0] >= 9 and id[0] <= 14:
                abs_angle = id[0] - 9
            else:
                assert (id[0] == 0 or id[0] == 1 or id[0] == 8 or id[0] == 15)
                print("stationary idents overlapping")
                # TODO: Return a direction other than 0? (0 also has another meaning --> straight ahead)
                return [total_dist, 0] 

        # Deal with ident on a straight northwest/southeast line
        elif li_dist == 0:
            print(f"angle case 0 for id {id}, mi_dist {mi_dist}, li_dist {li_dist}")
            assert mi_dist != 0

            abs_angle = 2 if mi_dist > 0 else 5

            # TODO: Check how direction is determined here
            # return [total_dist, ]
        
        # Deal with ident on a straight vertical line
        elif mi_dist == 0:
            print("angle case 1")
            assert li_dist != 0

            abs_angle = 3 if li_dist > 0 else 0

            # TODO: Check how direction is determined here
            # return [total_dist, 3 if mi_dist > 0 else 0]
        
        # Deal with ident on a straight northeast/southwest line
        elif mi_dist == -li_dist:
            print("angle case 2")
            # TODO: Check how direction is determined here
            abs_angle = 1 if mi_dist > li_dist else 4
            # return [total_dist, 1 if mi_dist > li_dist else 4]
        
        # TODO: Deal with all other cases (not straight lines)
        else:
            print("angle case 3 (complex)")
            # To find angle:
            # TODO: Find the hex on the same concentric ring which is one of the the 6 straight lines and is the closest to the desired ident but counter-clockwise from it
            if mi_dist > 0 and li_dist < 0:
                if abs(li_dist) > abs(mi_dist):
                    ref_angle = 0
                else:
                    assert abs(mi_dist) > abs(li_dist)
                    ref_angle = 1
            elif mi_dist > 0 and li_dist > 0:
                ref_angle = 2
            elif mi_dist < 0 and li_dist > 0:
                if abs(li_dist) > abs(mi_dist):
                    ref_angle = 3
                else:
                    assert abs(mi_dist) > abs(li_dist)
                    ref_angle = 4
            else:
                assert mi_dist < 0 and li_dist < 0
                ref_angle = 5

            # TODO: Get the distance from said reference hex to the desired ident. We can do this with a call to __get_distance_and_direction because it will be a straight line (not infinite recursion)
            match ref_angle:
                case 0:
                    offset = Teacher.__get_distance([ag[0], ag[1], ag[2] - total_dist], id)
                case 1:
                    offset = Teacher.__get_distance([ag[0], ag[1] + total_dist, ag[2] - total_dist], id)
                case 2:
                    offset = Teacher.__get_distance([ag[0], ag[1] + total_dist, ag[2]], id)
                case 3:
                    offset = Teacher.__get_distance([ag[0], ag[1], ag[2] + total_dist], id)
                case 4:
                    offset = Teacher.__get_distance([ag[0], ag[1] - total_dist, ag[2] + total_dist], id)
                case 5:
                    offset = Teacher.__get_distance([ag[0], ag[1] - total_dist, ag[2]], id)
                case _:
                    exit(f"invalid ref angle {ref_angle}")
            
            print(f"red_angle {ref_angle} for id {id}")

            # The angle of the desired ident = the angle of the reference hex + (distance from reference hex to desired ident)/(side length of ring - 1)
            # = angle of reference hex + (distance from ref hex to desired ident)/(# of ring)
            # = angle of reference hex + (distance from ref hex to desired ident)/(total_dist)
            abs_angle = ref_angle + offset/total_dist
            '''print(f"ref angle = {ref_angle}, offset = {offset}, total_dist = {total_dist}")
            print(f"angle = {angle}")'''

            print(f"abs angle between agent {ag} and ident {id} is {abs_angle}")

        print(f"agent direction {agent_dir}, ident abs angle {abs_angle}")

        # TODO: Check how relative angle is calculated
        if abs(abs_angle - agent_dir) <= 3:
            print(f"relative angle case 1 for id {id}")
            relative_angle = abs_angle - agent_dir
        elif (abs_angle - agent_dir <= 0) and (abs_angle - agent_dir < -3):
            print(f"relative angle case 2 for id {id}")
            relative_angle =  (abs_angle - agent_dir)%6

        elif abs_angle - agent_dir > 0:
            # TODO: Check this relative angle case specifically
            print(f"relative angle case 3 for id {id}")
            print(f"abs_angle {abs_angle}, agent_dir {agent_dir}")

            assert abs_angle - agent_dir > 3

            relative_angle = abs_angle - agent_dir - 6
        
        else:
            # TODO: Check this relative angle case specifically

            print(f"relative angle case 4 for id {id}")
            relative_angle = (agent_dir - abs_angle)%6
        
        assert abs(relative_angle) <= 3


        
        
        '''for i in range(4):
            if (agent_dir + i)%6 == abs_angle:
                relative_angle = i
                break
            elif (agent_dir - i)%6 == abs_angle:
                relative_angle = -i
                break'''
        print(f"id {id}, ag {ag}")
        print(f"relative angle {relative_angle} found between agent direction {agent_dir} and ident absolute angle {abs_angle}")

        return[total_dist, relative_angle]

    ##########################################################################################################

    @staticmethod
    # Returns a boolean indicating if ident_1 is less than ident_2 according to the following rules:
    # First, sort by the second hexadecimal character (matrix index)
    # Second, sort by the third hexadecimal character (list index)
    # Finally, sort by the first hexadecimal character (property)
    # TODO: Test this comparison method
    def less_than(ident_1 : str, ident_2 : str, agent : str):
        # print(f"comparing {ident_1} and {ident_2} with agent {agent}")

        # Ensure that we are comparing two idents of valid string length
        assert len(ident_1) == 3
        assert len(ident_2) == 3

        # Sort by distance from agent, then clockwise starting at direction 0 (12 o'clock)
        assert agent
        assert len(agent) == 3
        
        
        id_1 = []
        for char in ident_1:
            # Append all chars in ident_2 as ints in base 10
            id_1.append(int(char, 16))
        
        id_2 = []
        for char in ident_2:
            # Append all chars in ident_2 as ints in base 10
            id_2.append(int(char, 16))
        
        ag = []
        for char in agent:
            ag.append(int(char, 16))

        distance_1 = Teacher.__get_distance_and_direction(id_1, ag)
        distance_2 = Teacher.__get_distance_and_direction(id_2, ag)

        if distance_1[0] != distance_2[0]:
            return distance_1[0] < distance_2[0]
        else:
            
            # Idents at the same distance from the agent where one is more directly on its current path
            if abs(distance_1[1]) != abs(distance_2[1]):
                return abs(distance_1[1]) < abs(distance_2[1])
            
            # Idents at the same distance from the agent where both are symmetrically at angles to the agent's direction of motion
            elif distance_1[1] == -distance_2[1]:
                return distance_1[1] < distance_2[1]
            
            # Two idents are in the same location
            else:
                # Compare 1st hexadecimal character (property)
                # TODO: Do I need to convert into decimal?
                if ident_1[0] < ident_2[0]:
                    return True
                elif ident_1[0] > ident_2[0]:
                    return False
                else:
                    # Two identical idents (should not happen)
                    print(f"ident_1 = {ident_1}, ident_2 = {ident_2}, agent = {agent}")
                    print(f"dist_1 = {distance_1}, dist_2 = {distance_2}")
                    exit("Two equal idents found")


        # Sort up to down, left to right
        '''# Compare 2nd hexadecimal character (matrix index)
        if ident_1[1] < ident_2[1]:
            return True
        elif ident_1[1] > ident_2[1]:
            return False
        
        # Deal with two idents with the same matrix index
        else:
            # Compare 3rd hexadecimal character (list index)
            if ident_1[2] < ident_2[2]:
                return True
            elif ident_1[2] > ident_2[2]:
                return False
            
            # Deal with two idents with the same list index
            else:
                # Compare 1st hexadecimal character (property)
                if ident_1[0] < ident_2[0]:
                    return True
                elif ident_1[0] > ident_2[0]:
                    return False
                else:
                    # Two identical idents (should not happen)
                    exit("Two equal idents found")
                    return True'''


    ##########################################################################################################

    '''@staticmethod
    # Merges two sublists
    # First sublist is list[left..mid]
    # Second sublist is list[mid+1..right]
    # Code provided for merge sort here: https://www.geeksforgeeks.org/merge-sort/#
    def __merge(my_list, left, mid, right):
        # TODO: Review this base case (my code)
        if left >= right:
            return
        
        # breakpoint()
        sublist_1 = mid - left + 1
        sublist_2 = right - mid

        # Create temp lists
        left_list = [0] * sublist_1
        right_list = [0] * sublist_2

        print(f"range(sublist_1) = {range(sublist_1)}")
        print(f"range(sublist_2) = {range(sublist_2)}")

        # Copy data to temp arrays left_list[] and right_list[]
        for i in range(sublist_1):
            left_list[i] = my_list[left + i]
        for j in range(sublist_2):
            print(f"mid={mid}")
            print(f"j={j}")
            print("mid+1+j = " + str(mid+1+j))
            right_list[j] = my_list[mid + 1 + j]

        index_of_sublist_1 = 0  # Initial index of first sublist
        index_of_sublist_1 = 0  # Initial index of second sublist
        index_of_merged_list = left  # Initial index of merged list

        # Merge the temp lists back into my_list[left..right]
        while index_of_sublist_1 < sublist_1 and index_of_sublist_1 < sublist_2:
            if Teacher.__less_equal(left_list[index_of_sublist_1], right_list[index_of_sublist_1]):
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
            index_of_merged_list += 1'''      


    ##########################################################################################################

    # TODO: Adapt for hex world
    # NOTE: For now, we will only generate 17-char strings, with the first bit indicating whether or not there are walls around the edges, the next 8 bit specifying the coordinates of the agent, the last 8 indicating the coordinates of the goal
    # NOTE issue: How will the hex world respond when quieried like a DFA when the string is the wrong length? Could we work on how we define the alphabet to allow multiple-char letters so that things will be added/removed on the level of a unit of meaning?
    @staticmethod
    def generate_string():

        # print("generate_string() called")
        # print(f"rand int {random.randint(0, 10)}")

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
        # TODO: Enable the creation of multiple goals
        # NOTE: The maximum number of goals is arbitrary
        num_goals = random.randint(1, 5)
        print(f"creating {num_goals} goals")
        goals = []
        for i in range(num_goals):
            my_goal = ""
            while not (make_alphabet.check_validity(my_goal) and my_goal not in goals):
                my_goal = ""
                goal_mi = random.randint(0, 15)
                goal_li = random.randint(0, 15)
                # TODO: Check that this hex method correctly converts and returns a string
                my_goal += "f" + hex(goal_mi)[2] + hex(goal_li)[2]

            assert my_goal

            # Save new ident in the correct order
            # If other_idents is empty, add to it
            if not len(goals):
                goals.append(my_goal)
            
            # TODO: Finish sorting in multiple goals then add them to string
            # Add the final ident in other_idents in smaller than the new_ident, add at the back
            elif Teacher.less_than(goals[len(goals) - 1], my_goal, my_agent):
                goals.append(my_goal)

            # Otherwise iterate through other_ident until the correct location is found
            else:
                for goal in goals:
                    if not Teacher.less_than(goal, my_goal, my_agent):
                        goals.insert(goals.index(goal), my_goal)
                        break

        # Save valid goals to string
        for goal in goals:
            strg += goal


        # Generate a pseudo-randomly determined number of other 3-char strings (idents)
        # NOTE: The choice of maximum number of idents is arbitrary; We might want to set to 0 for testing
        num_idents = random.randint(0, 50)
        # num_idents = 3
        other_idents = []
        for i in range(num_idents):
            # breakpoint()
            new_ident = ""
            
            # Loop until we have made a novel valid ident
            while not (make_alphabet.check_validity(new_ident) and new_ident not in other_idents):
                new_ident = ""
                # breakpoint()
                # NOTE: the new idents cannot be goals
                # TODO: Only create valid idents (rather than creating potentially invalid idents and then fixing them)
                ident_prop = random.randint(0, 14)
                ident_mi = random.randint(0, 15)
                ident_li = random.randint(0, 15)
                # TODO: Check that this hex method correctly converts and returns a string
                new_ident += hex(ident_prop)[2] + hex(ident_mi)[2] + hex(ident_li)[2]

            assert new_ident
            assert new_ident not in other_idents

            # Save new ident in the correct order
            # If other_idents is empty, add to it
            if not len(other_idents):
                other_idents.append(new_ident)
            
            # Add the final ident in other_idents in smaller than the new_ident, add at the back
            elif Teacher.less_than(other_idents[len(other_idents) - 1], new_ident, my_agent):
                other_idents.append(new_ident)

            # Otherwise iterate through other_ident until the correct location is found
            else:
                for ident in other_idents:
                    if not Teacher.less_than(ident, new_ident, my_agent):
                        other_idents.insert(other_idents.index(ident), new_ident)
                        break
                    
                    


        # TODO: Sort the three-char strings first by matrix index (2nd char), then list index (2nd char), then property (1st char)
        # NOTE: I'm trying another way (not using merge sort) --> less efficient, but hopefully less buggy
        #Teacher.__merge_sort(other_idents)

        # Concatenate these ident strings in the given order then return
        for ident_string in other_idents:
            strg += ident_string


        # print(f"generated string: {strg}")
        
        return strg

    ##########################################################################################################

##############################################################################################################