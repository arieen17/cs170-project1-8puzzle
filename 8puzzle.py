import heapq # used for priorirty queue to get the lowest cost node
from copy import deepcopy

test_puzzle = [
    [1, 2, 3],
    [4, 8, 0],
    [7, 6, 5]
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

    possible_directions = [
        ("up", -1, 0),
        ("down", 1, 0),
        ("left", 0, -1),
        ("right", 0, 1)
    ]

    # first code when creating moves (add)
    # but then utilized deepcopy to create a new state, rather than modifying og state

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

def print_state(state):
    for row in state:
        print(row)
    print()

class Node:
    def __init__(self, STATE, PARENT=None, ACTION="", PATH_COST=0, HEURISTIC_COST=0):
        self.STATE = STATE
        self.PARENT = PARENT
        self.ACTION = ACTION
        self.PATH_COST = PATH_COST
        self.HEURISTIC_COST = HEURISTIC_COST
        self.A_COST = PATH_COST + HEURISTIC_COST
    def __lt__(self, other):
        return self.A_COST < other.A_COST
    
class Problem:
    def __init__(self, INITIAL_STATE, GOAL_TEST):
        self.INITIAL_STATE = INITIAL_STATE
        self.goal_state = goal_state
        self.size = len(INITIAL_STATE)
    
    def GOAL_TEST(self, state):
        return state == self.goal_state
    
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
            HEURISTIC_COST=0
        )
        successors.append(new_node)
    return successors

def general_search(problem, QUEUEING_FUNCTION):
#     initial_node = Node(STATE=problem.INITIAL_STATE)
#     nodes = []
#     heapq.heappush(nodes, initial_node)
#     
#     while nodes:
#         node = heapq.heappop(nodes)
#         
#         if problem.GOAL_TEST(node.STATE):
#             return node
#         successors = EXPAND(node, problem)
#         nodes = QUEUEING_FUNCTION(nodes, successors, problem)
#     
#    return "failed"
    initial_node = Node(STATE=problem.INITIAL_STATE)
    nodes = []
    heapq.heappush(nodes, initial_node)
    
    explored_nodes = set()
    max_queue_size = 0
    nodes_expanded = 0

    while True:
        max_queue_size = max(max_queue_size, len(nodes))
        if len(nodes) == 0:
            return "failed, no soltion found"
        node = heapq.heappop(nodes)
        if problem.goal_state(node.STATE):
            print(f"\nSolution found! \n Path cost: {node.PATH_COST} \n Max queue size: {max_queue_size}")
            return node
        
        # to avoid re-expanding the same nodes
        state_str = str(node.STATE)
        if state_str in explored_nodes:
            continue
        explored_nodes.add(state_str)
        nodes_expanded +=1
        successors = EXPAND(node, problem)
        nodes = QUEUEING_FUNCTION(nodes, successors, problem)
    return "failed, no solution found"

def misplaced_tile_heuristic(state, goal_state):
    count = 0
    size = len(state)
    for i in range(size):
        for j in range(size):
            if state[i][j] != 0 and state[i][j] != goal_state[i][j]:
                count += 1
    return count

def manhattan_distance_heuristic(state, goal_state):
    distance = 0
    size = len(state)
    for i in range(size):
        for j in range(size):
            value = state[i][j]
            if value == 0:
                continue
            for goal_i in range(size):
                for goal_j in range(size):
                    if goal_state[goal_i][goal_j] == value:
                        distance += abs(i - goal_i) + abs(j - goal_j)
                        break
    return distance

if __name__ == "__main__":
    print("Test puzzle:")

    # Test heuristics
    h_misplaced = misplaced_tile_heuristic(test_puzzle, goal_state)
    h_manhattan = manhattan_distance_heuristic(test_puzzle, goal_state)
    
    print(f"Misplaced tile heuristic: h(n) = {h_misplaced}")
    print(f"Manhattan distance heuristic: h(n) = {h_manhattan}")