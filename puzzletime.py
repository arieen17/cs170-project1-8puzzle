import heapq # used for priority queue to get the lowest cost node
from copy import deepcopy

# following are helper functions for the game
def find_blank(state): # find the position fo the blank tile: 0
    size = len(state)
    for i in range(size):
        for j in range(size):
            if state[i][j] == 0:
                return (i, j)
    return (-1, -1) # if input wrong or error, then blank tile isn't found

#generate all possible moves from the current state
def generate_operation(state):
    size = len(state)
    moves = []
    blank_row, blank_col = find_blank(state)

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

def print_state(state): # printing the puzzle state
    for row in state:
        print(row)
    print()

def validate_puzzle(puzzle): # added to ensure that the input is valid, as they could input whatever...
    size = len(puzzle)
    for row in puzzle:
        if len(row) != size:
            return False, "Puzzle must be be same # of rows and columns"
    
    numbers = []
    # ensure puzzle is a n by n grid
    for row in puzzle:
        numbers.extend(row)
    expected_numbers = set(range(size * size))
    actual = set(numbers)
    if actual != expected_numbers:
        missing = expected_numbers - actual
        extra = actual - expected_numbers
        if missing:
            return False, f"Missing numbers: {missing}"
        if extra:
            return False, f"Extra numbers: {extra}"
        if len(numbers) != len(actual): # check for duplicates
            duplicates = [n for n in actual if numbers.count(n) > 1]
            return False, f"Duplicate numbers found: {duplicates}"
    return True, ""

# nodes in the search tree
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

# define the search problem: initial, goal states and moves  
class Problem:
    def __init__(self, INITIAL_STATE, goal_state):
        self.INITIAL_STATE = INITIAL_STATE
        self.goal_state = goal_state
        self.size = len(INITIAL_STATE)
    
    def GOAL_TEST(self, state):
        return state == self.goal_state
    
    def OPERATORS(self, state):
        return generate_operation(state)
# expand and to generate its successors nodes
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

# calculate h(n) as number of misplaced tiles (aka not in their goal position)
def misplaced_tile_heuristic(state, goal_state):
    count = 0
    size = len(state)
    for i in range(size):
        for j in range(size):
            if state[i][j] != 0 and state[i][j] != goal_state[i][j]:
                count += 1
    return count

# h(n) as sum of manhattan distances of all tiles from their goal positions
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

# general serach algorithms
def general_search(problem, heuristic_function=None):
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
    initial_h = 0 if heuristic_function is None else heuristic_function(problem.INITIAL_STATE, problem.goal_state)
    initial_node = Node(STATE=problem.INITIAL_STATE, PATH_COST=0, HEURISTIC_COST=initial_h)
    initial_node.A_COST = initial_node.PATH_COST + initial_node.HEURISTIC_COST
    nodes = []
    heapq.heappush(nodes, initial_node)
    
    explored_nodes = set()
    max_queue_size = 1
    nodes_expanded = 0

    while nodes:
        # track the maximum queue size reached
        max_queue_size = max(max_queue_size, len(nodes))
        node = heapq.heappop(nodes)
        
        if problem.GOAL_TEST(node.STATE):
            print(f"\nSolution found! \n Path cost: {node.PATH_COST} \n Number of nodes expanded: {nodes_expanded} \n Max queue size: {max_queue_size}")
            return node
        
        # to avoid re-expanding the same nodes
        state_str = str(node.STATE)
        if state_str in explored_nodes:
            continue
        print(f"The best state to expand with a g(n) = {node.PATH_COST} and h(n) = {node.HEURISTIC_COST} is:")
        print_state(node.STATE)

        nodes_expanded += 1
        for action, new_state in problem.OPERATORS(node.STATE):
            child_state_str = str(new_state)
            if child_state_str not in explored_nodes:
                h = 0 if heuristic_function is None else heuristic_function(
                    new_state, problem.goal_state
                )
                child = Node(STATE=new_state, PARENT=node, ACTION=action, PATH_COST=node.PATH_COST + 1, HEURISTIC_COST=h)
                child.A_COST = child.PATH_COST + child.HEURISTIC_COST
                heapq.heappush(nodes, child)
        explored_nodes.add(state_str)

    return None

# reconstructs the solution path from start to goal
def trace_back(goal_node):
    path = []
    currnode = goal_node
    while currnode is not None:
        path.append(currnode)
        currnode = currnode.PARENT
    path.reverse()
    return path

# gets user input and validates it
def get_user_puzzle():
    while True:
        print("\nEnter puzzle size")
        # size for any n by n puzzle
        try:
            size = int(input("Size: "))
            if size < 2:
                print("Size must be at least 2. Please try again.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a valid integer for size.")
    print(f"\nEnter your {size} by {size} puzzle, using 0 for the blank tile. Separate numbers with spaces.")
    while True:
        puzzle = []
        try:
            for i in range(size):
                row_input = input(f"Row {i + 1}: ")
                row = list(map(int, row_input.split()))
                if len(row) != size:
                    print(f"Each row must have exactly {size} numbers. Please re-enter the puzzle.")
                    break
                puzzle.append(row)
            is_valid, error_msg = validate_puzzle(puzzle)
            if not is_valid:
                print(f"Invalid puzzle: {error_msg} Please re-enter the puzzle.")
                continue
            return puzzle
        except ValueError as e:
            print(f"Invalid input: {e}. Please re-enter the puzzle.")

# based of the nxn it creates a goal state for that
def create_goal_state(size):
    goal = []
    num = 1
    for i in range(size):
        row = []
        for j in range(size):
            if i == size - 1 and j == size - 1:
                row.append(0)
            else:
                row.append(num)
                num += 1
        goal.append(row)
    return goal