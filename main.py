from puzzletime import (
    Problem,
    misplaced_tile_heuristic,
    manhattan_distance_heuristic,
    get_user_puzzle,
    print_state,
    general_search,
    trace_back,
    create_goal_state
)

# example puzzles
super_easy = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 0, 8]
]
easy = [
    [1, 2, 3],
    [4, 5, 6],
    [0, 7, 8]
]
medium = [
    [1, 3, 6],
    [5, 0, 2],
    [7, 8, 4]
]
hard = [
    [1, 6, 7],
    [5, 0, 3],
    [4, 8, 2]
]
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

def main():
    print("Welcome to the 8 puzzle solver! by Arielle Haryanto")
    choice = input("Enter 1 to use the default test puzzle, or 2 to input your own puzzle: ")
    while True:
        if choice in ["1", "2"]:
            break
        print("Invalid choice. Please enter 1 or 2.")
    if choice == "1":
        print(" 1: Super Easy \n 2: Easy \n 3: Medium \n 4: Hard")
        preset_puzzles = {
            "1": ("Super Easy", super_easy),
            "2": ("Easy", easy),
            "3": ("Medium", medium),
            "4": ("Hard", hard),
        }
        while True:
            preset_choice = input("Select a preset puzzle (1-4): ")
            if preset_choice in preset_puzzles:
                name, initial_state = preset_puzzles[preset_choice]
                print(f"\nYou selected: {name}")
                break
            else:
                print("Invalid choice. Please select a valid preset puzzle (1-4).")
        goal_state_to_use = goal_state
    else:
        initial_state = get_user_puzzle()
        goal_state_to_use = create_goal_state(len(initial_state))
    print("\nInitial State:")
    print_state(initial_state)
    print("\nThis is Goal State we want to achieve:")
    print_state(goal_state_to_use)
    
    problem = Problem(initial_state, goal_state_to_use)

    algorithms = {
        "1": ("Uniform Cost Search", None),
        "2": ("A* with Misplaced Tile Heuristic", misplaced_tile_heuristic),
        "3": ("A* with Manhattan Distance Heuristic", manhattan_distance_heuristic)
    }

    while True:
        print("\nSelect a search algorithm: \n 1. Uniform Cost Search \n 2. A* with Misplaced Tile Heuristic \n 3. A* with Manhattan Distance Heuristic")
        alg_choice = input("Enter your choice: ")

        if alg_choice in algorithms:
            alg_name, queue_func = algorithms[alg_choice]
            break
        else:
            print("Invalid choice. Please select a valid algorithm (1, 2, or 3).")
            # redo if puzzle has wrong option
    print(f"\nRunning {alg_name}")
    solution = general_search(problem, queue_func)
    if solution is not None:
        path = trace_back(solution)
        print("\nSolution Path:")
        for step in path:
            print_state(step.STATE)
    else:
        print("No solution found.")

if __name__ == "__main__":
    main()
