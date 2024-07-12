

# # Code from pacman repo -> search.py
class PriorityQueue:
    """
      Implements a priority queue data structure. Each inserted item
      has a priority associated with it and the client is usually interested
      in quick retrieval of the lowest-priority item in the queue. This
      data structure allows O(1) access to the lowest-priority item.
    """
    def  __init__(self):
        self.heap = []
        self.count = 0

    def push(self, item, priority):
        entry = (priority, self.count, item)
        heapq.heappush(self.heap, entry)
        self.count += 1

    def pop(self):
        (_, _, item) = heapq.heappop(self.heap)
        return item

    def isEmpty(self):
        return len(self.heap) == 0

    def update(self, item, priority):
        # If item already in priority queue with higher priority, update its priority and rebuild the heap.
        # If item already in priority queue with equal or lower priority, do nothing.
        # If item not in priority queue, do the same thing as self.push.
        for index, (p, c, i) in enumerate(self.heap):
            if i == item:
                if p <= priority:
                    break
                del self.heap[index]
                self.heap.append((priority, c, item))
                heapq.heapify(self.heap)
                break
        else:
            self.push(item, priority)

class Node:
    def __init__(self, state, direction = 0, cost = 0, parent = None):
        self.state = state
        self.pathCost = cost
        self.direction = direction
        self.parent = parent

# Code influenced by pacman repo -> searchAgents.py
class SearchProblem:

    def __init__(self, line):
        line_parts = line.split(" ")
        matrix_index = int(line_parts[0])
        list_index = int(line_parts[1])
        command = line_parts[2]
        self.wall = []

        self.goal = None
        self.startState = None


        # For display purposes
        self._visited, self._visitedlist, self._expanded = {}, [], 0 # DO NOT CHANGE


        if command == "agent" or command == "agent\n":
            # NOTE: This is currently only equipped to create one agent
            
            direction = int(line_parts[4])
            color_text = line_parts[3]
            color = World.__get_color(color_text)

            new_agent = Ident(matrix_index, list_index, self, color = color, state = direction, serial_number = -1, hist = None, property = "agent")

            # Add ident to ident list
            self.ident_list.append(new_agent)
            
            # Add ident to hex
            self.hex_matrix[matrix_index][list_index].idents.append(new_agent)

            # Store ident as agent
            self.agents.append(new_agent)

        elif command == "goal" or command == "goal\n":
            self.goal = (matrix_index, list_index)
        elif command == "wall" or command == "wall\n":
            self.wall.append((matrix_index, list_index))
        # Print error message
        elif command == "agent" or command == "agent\n":
            self.startState = (matrix_index, list_index)
        else:
            print("Command " + command + " invalid.")


    def getStartState(self):
        return self.startState
    
    def isGoalState(self, state):
        return state == self.goal
    
    def getSuccessors(self, state, dir):
        successors = []
        if dir == 0:
            try:
                straight = (state[0], state[1]-1)
                left = (state[0] - 1, state[1])
                right = (state[0] + 1, state[1] - 1)
            except:
                return None
            
        elif dir == 1:
            try:
                straight = (state[0] + 1, state[1] - 1)
                left = (state[0], state[1] - 1)
                right = (state[0] + 1, state[1])
            except:
                return None

        elif dir == 2:
            try:
                straight = (state[0] + 1, state[1])
                left = (state[0] + 1, state[1] - 1)
                right = (state[0], state[1] + 1)
            except:
                return None

        elif dir == 3:

            try:
                straight = (state[0], state[1] + 1)
                left = (state[0]+1, state[1])
                right = (state[0]-1, state[1]+1)
            except:
                return None

        elif dir == 4:

            try:
                straight = (state[0] - 1, state[1] + 1)
                left = (state[0], state[1] + 1)
                right = (state[0]-1, state[1])
            except:
                return None
            
        elif dir == 5:

            try:
                straight = (state[0] - 1, state[1])
                left = (state[0]-1, state[1]+1)
                right = (state[0], state[1]-1)
            except:
                return None
            
        else:
            print("Invalid direction " + str(dir) + " passed to Ident.__get_neighbor(dir)")
            return None
        
        newStates = [left, straight, right]
        i = -1
        for state in newStates:
            successors.append(state, dir + 1, 1)     # returns tuples of (nextState, new_direction, stepCost)
            i += 1

        # for debugging
        self.expanded += 1
        for state in newStates:
            if state not in self._visited:
                self._visited[state] = True
                self._visitedlist.append(state)


    # not required right now
    def getCostOfActions(self, actions):
        util.raiseNotDefined()

def Solution(node):
    actions = []
    while node.parent != None:
        actions.append(node.action)
        node = node.parent
    #print("actions: ", actions)
    #print("actions reversed: ", actions[::-1])
    return actions[::-1]

# Code from pacman repo -> search.py
def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    startState = problem.getStartState()
    root = Node(startState)
    frontier = util.PriorityQueue()
    frontier.push(root, 0)

    explored = []   # list of explored states

    while True:
        if frontier.isEmpty():
            print("returning empty list")
            return []
        node = frontier.pop()
        if problem.isGoalState(node.state):
            return Solution(node)
        if node.state not in explored:
            explored.append(node.state)
            successors = problem.getSuccessors(node.state)
            for item in successors:
                #manhattan = util.manhattanDistance(item[0][0], item[0][1])
                heur = heuristic(item[0], problem)
                child = Node(item[0], item[1], item[2] + node.pathCost, node)
                #print("child.pathCost: ", child.pathCost)
                frontier.push(child, child.pathCost + heur)
