import heapq # used for priorirty queue to get the lowest cost node
from copy import deepcopy

test_puzzle = [
    [1, 2, 3],
    [5, 6, 0],
    [7, 8, 4]
]

goal_state = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]

print("Welcome to the 8 puzzle solver! by Arielle Haryanto")
# following are helper functions for the game
def find_blank(state):
    size = 3 # size can be changed based on the size of the puzzle (right now: 3 by 3)
    for i in range(size):
        for j in range(size):
            if state[i][j] == 0:
                return (i, j)
    return (-1, -1) # if input wrong or error, then blank tile isn't found

def generate_operation(state):
    size = 3
    moves = []
    blank_row, blank_col = find_blank(state)

    # possible moves: up, down, left, right
    possible_directions = [
        ("up", -1, 0),
        ("down", 1, 0),
        ("left", 0, -1),
        ("right", 0, 1)
    ]

    for action, drow, dcol in possible_directions:
        new_row = blank_row + drow
        new_col = blank_col + dcol
        if 0 <= new_row < size and 0 <= new_col < size: # check if the move is within bounds
            new_state = deepcopy(state)
            # swap the blank tile with the adjacent tile
            new_state[blank_row][blank_col], new_state[new_row][new_col] = \
                new_state[new_row][new_col], new_state[blank_row][blank_col]
            moves.append((action, new_state))
    return moves

def print(state):
    for row in state:
        print(row)
    print()

class Node:
    def __init__(self, STATE, PARENT=None, ACTION="", PATH_COST=0):
        self.STATE = STATE
        self.PARENT = PARENT
        self.ACTION = ACTION
        self.PATH_COST = PATH_COST
    
    def __lt__(self, other):
        return self.PATH_COST < other.PATH_COST 
class Problem:
    def __init__(self, INITIAL_STATE, GOAL_TEST):
        self.INITIAL_STATE = INITIAL_STATE
        self.GOAL_TEST = GOAL_TEST
    
    def GOAL_TEST(self, state):
        return state == self.GOAL_TEST
    
    def OPERATORS(self, state):
        return generate_operation(state)
    
def EXPAND(node, problem):
    successors = []
    for action, new_state in problem.OPERATORS(node.STATE):
        new_node = Node(
            STATE=new_state,
            PARENT=node,
            ACTION=action,
            PATH_COST=node.PATH_COST + 1,
        )
        successors.append(new_node)
    return successors

def general_search_BUGGY(problem, QUEUEING_FUNCTION):
    initial_node = Node(STATE=problem.INITIAL_STATE)
    nodes = []
    heapq.heappush(nodes, initial_node)
    
    while nodes:
        node = heapq.heappop(nodes)
        
        if problem.GOAL_TEST(node.STATE):
            return node
        successors = EXPAND(node, problem)
        nodes = QUEUEING_FUNCTION(nodes, successors, problem)
    
    return "failed"
