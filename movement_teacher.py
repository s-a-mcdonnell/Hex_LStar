# Tteacher type 0 -> determines whether or not the agent is turning

from teacher import Teacher
from hex_v2 import World, Ident

import functools

def memoize(obj):
    '''
    Memoize function from https://wiki.python.org/moin/PythonDecoratorLibrary#Memoize
    Caches inputs of a deterministic function with their associated outputs for quicker access time overall
    '''
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

    # membership query
    # takes a string s and returns a boolean indicating whether s is accepted or rejected by the given DFA
    @memoize
    def member(self, s : str, dfa: list[list[int]] = None, alpha = None):
        '''
        Membership query: takes a string s and returs a boolean indicated whether s is accepted or rejected by the given Teacher DFA.
        In this case, specifically, return False if the agent move from the Hex World is 0 (ie, the agent does not manually turn.)
        '''

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

            # Find the agent's next move
            agent_move = Ident.find_next_move(self.my_agent)

            # true on first DFA => we are changing the agent's direction via the agent (ie -> instruction -1 or 1)
            # false on first DFA => we are not manually changing the agent's direction (ie -> instruction 0)
            return agent_move != 0          
    ##########################################################################################################