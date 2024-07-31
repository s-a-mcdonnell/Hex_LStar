# The second teacher (for an agent that is turning, is it turning clockwise or counterclockwise?)

from teacher import Teacher
from hex_world import Ident

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


class Direction_Teacher(Teacher):
    
    ##############################################################################################################

    @memoize
    def member(self, s : str, dfa: list[list[int]] = None, alpha = None):
        '''Membership query: takes a string s and returs a boolean indicated whether s is accepted or rejected by the given Teacher DFA'''

        if not alpha:
            alpha = self.alphabet

        # If passed a matrix, use it as the dfa and return boolen indicating final state action
        if dfa:        
            # Return the int boolean indicating if the final state is an accept or reject state
            final_state : list[int] = Direction_Teacher.final_state(s, dfa, alpha)
            return bool(final_state[0])
        
        # If not passed a matrix, return an answer as if the agent's decision-making process were a DFA
        else:
            # Always reject the empty string (arbitrary decision)
            if s == "":
                return False
            
            self._create_world(s)
            assert self.world
            assert self.my_agent
            
            # Find the agent's next move
            agent_move = Ident.find_next_move(self.my_agent)

            # SECOND DFA ==> acceptance is clockwise (positive) turn (next move value of 1) and rejection is everything else
            return agent_move == 1
            
    #############################################################################################################