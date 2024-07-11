# The first teacher (is the agent turning itself?)

from teacher import Teacher
from hex_v2 import World, Ident

class Movement_Teacher(Teacher):
    def __init__(self, alphabet, seed=-1):
        self.alphabet = alphabet
        self.seed = seed
        if seed == -1:
            self.seed = 1821
        # TODO: Write constructor
    
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
            # Always reject the empty string (arbitrary decision)
            if s == "":
                return False
            
            # Parse passed string into a world
            self.__create_world(s)
            assert self.world
            assert self.my_agent
            
            original_agent_state = self.my_agent.state

            # TODO: Run one loop of updating the world and check was the agent's state is
            # TODO: How to know what part of the agent instructions the world should be looking at? (potentially big issue, since we've created a world from scratch)
            # self.world.update()

            new_state = Ident.find_next_move(self.my_agent)
            # TODO: the world updating effects the agent though????

            # TODO: Return a boolean corresponding to the agent's state
            # TODO: Actually we want to just report the agent's action, not how it might have been affected by the physics rules
            if new_state == 0:
                return False
            # false on first DFA => we are not manually changing the agent's direction (ie -> instruction 0)
            # true on first DFA => we are changing the agent's direction via the agent (ie -> instruction -1 or 1)
            else:
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
