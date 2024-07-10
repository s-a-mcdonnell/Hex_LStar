import random
from hex_v2 import World, Ident

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
            s = self.generate_string()
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
            # Always reject the empty string
            if s == "":
                return False
            
            world = World()
            
            # TODO: Parse string into a world and query agent
            for i in range(len(s)/12):
                property = s[i*12 : i*12 + 4]
                mi = s[i*12 + 4 : i*12 + 8]
                li = s[i*12 + 8 : i*12 + 12]

                new_ident = Ident(mi, li, world)

                world.hex_matrix[mi][li].idents.append(new_ident)
                
                # 0000 => wall
                if property == "0000":
                    new_ident.state = -2
                    world.wall_list.append(new_ident)

                # If not a wall, it goes on the ident list
                else:
                    world.ident_list.append(new_ident)

                # 0001 => stationary (non-agent)
                if property == "0001":
                    new_ident.state = -1
                
                # 0010 => direction 0 (non-agent)
                elif property == "0010":
                    new_ident.state = 0

                # 0011 => direction 1 (non-agent)
                elif property == "0011":
                    new_ident.state = 1
                
                # 0100 => direction 2 (non-agent)
                elif property == "0100":
                    new_ident.state = 2

                # 0101 => direction 3 (non-agent)
                elif property == "0101":
                    new_ident.state = 3
                
                # 0110 => direction 4 (non-agent)
                elif property == "0110":
                    new_ident.state = 4
                
                # 0111 => direction 5 (non-agent)
                elif property == "0111":
                    new_ident.state = 5
                
                # 1000 => stationary (agent)
                if property == "1000":
                    new_ident.state = -1
                
                # 1001 => direction 0 (agent)
                elif property == "1001":
                    new_ident.state = 0
                    world.agents.append(new_ident)

                # 1010 => direction 1 (agent)
                elif property == "1010":
                    new_ident.state = 1
                    world.agents.append(new_ident)
                
                # 1011 => direction 2 (agent)
                elif property == "1011":
                    new_ident.state = 2
                    world.agents.append(new_ident)

                # 1100 => direction 3 (agent)
                elif property == "1100":
                    new_ident.state = 3
                    world.agents.append(new_ident)
                
                # 1101 => direction 4 (agent)
                elif property == "1101":
                    new_ident.state = 4
                    world.agents.append(new_ident)
                
                # 1110 => direction 5 (agent)
                elif property == "1110":
                    new_ident.state = 5
                    world.agents.append(new_ident)

                # 1111 => goal (stationary)
                elif property == "1111":
                    new_ident.state = -1
                    # Mark as goal
                    self.property = "goal"
            
            
            # TODO: Run one loop of updating the world and check was the agent's state is
            # TODO: Return a boolean corresponding to the agent's state


    ##########################################################################################################

    # TODO: Adapt for hex world
    # NOTE: For now, we will only generate 17-char strings, with the first bit indicating whether or not there are walls around the edges, the next 8 bit specifying the coordinates of the agent, the last 8 indicating the coordinates of the goal
    # NOTE issue: How will the hex world respond when quieried like a DFA when the string is the wrong length? Could we work on how we define the alphabet to allow multiple-char letters so that things will be added/removed on the level of a unit of meaning?
    def generate_string(self):

        strg = ""
            
        # NOTE: The choice of maximum length of a string is arbitrary
        # Create a string of (pseudo-)random length, with each character (pseudo-)randomly chosen from the alphabet
        for i in range(0, random.randint(0, 15)):
            strg += self.alphabet[random.randint(0, len(self.alphabet) - 1)]
        
        return strg

    ##########################################################################################################

##############################################################################################################