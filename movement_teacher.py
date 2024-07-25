# The first teacher (is the agent turning itself?)

from teacher import Teacher
from hex_v2 import World, Ident

import functools

def memoize(obj):
    cache = obj.cache = {}

    @functools.wraps(obj)
    def memoizer(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in cache:
            cache[key] = obj(*args, **kwargs)
        return cache[key]
    return memoizer


class Movement_Teacher(Teacher):
    
    ##########################################################################################################

    '''@staticmethod
    def final_state(s : str, dfa: list[list[int]], alpha):

        input = []

        assert (type(s) is str)
        assert len(s)%3 == 0

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
        return dfa[next_state_index]'''
    
    ##########################################################################################################

    # membership query
    # takes a string s and returns a boolean indicating whether s is accepted or rejected by the given DFA
    # TODO: Adapt for hex world
    @memoize
    def member(self, s : str, dfa: list[list[int]] = None, alpha = None):
        # print(f"membership query called on string {s}")

        if not alpha:
            alpha = self.alphabet

        # If passed a matrix, use it as the dfa and return boolen indicating final state action
        if dfa:        
            # Return the int boolean indicating if the final state is an accept or reject state
            final_state : list[int] = Movement_Teacher.final_state(s, dfa, alpha)
            return bool(final_state[0])
        
        # If not passed a matrix, return an answer as if the agent's decision-making process were a DFA
        else:
            # Always reject the empty string (arbitrary decision)
            if s == "":
                return False
            
            # Parse passed string into a world
            self._create_world(s)
            assert self.world
            assert self.my_agent

            # TODO: How to get the agent's next move when the agent is/isn't reading from a text file?
            agent_move = Ident.find_next_move(self.my_agent)
            # print(f"agent move: {agent_move}")

            # TODO: Return a boolean corresponding to the agent's state
            # TODO: Actually we want to just report the agent's action, not how it might have been affected by the physics rules
            if agent_move == 0:
                return False
            # false on first DFA => we are not manually changing the agent's direction (ie -> instruction 0)
            # true on first DFA => we are changing the agent's direction via the agent (ie -> instruction -1 or 1)
            else:
                # TODO: is this where we call the second DFA from?
                return True            
    ##########################################################################################################

    # equivalency query
    # takes the DFA hypothesis m_hat
    # returns either a counterexample or False (indicating that the DFAs match)
    # TODO: Adapt for hex world
    def equivalent(self, m_hat):
        assert m_hat

        print("equivalency query called in movement teacher")

        # Generate and test an arbitrarily large number of strings
        # for each of these strings, if self.member(s, self.m) is not self.member(s, m_hat), return s

        # TODO: Increase range
        for i in range(100):
            s = Teacher.generate_string()
            # print(f"string {s} returned from generate_string()")
            # print(f"self.member(s) = {self.member(s)}, self.member(s, m_hat) = {self.member(s, m_hat)}")
            if self.member(s) != self.member(s, m_hat):
                '''assert(type(self.member(s)) is bool)
                assert(type(self.member(s, m_hat)) is bool)'''
                # TODO: Delete debugging print statement
                # print("Counterexample found: " + s)
                print(f"returning string {s} from equivalency query")
                return s            

        # else return false (so that the truthiness of a counterexample and a matching DFA result will be different)
        print("No counterexample found")
        return False