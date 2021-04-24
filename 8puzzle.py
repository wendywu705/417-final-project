from Puzzle import EightPuzzle
from search import *
import time
import math

from walking_distance import *

goal_state = (1, 2, 3, 4, 5, 6, 7, 8, 0)


def make_rand_8puzzle():
    found_solvable_puzzle = False
    new_puzzle = EightPuzzle(goal_state)
    while not found_solvable_puzzle:
        state = tuple(random.sample(goal_state, 9))
        new_puzzle = EightPuzzle(state)
        if new_puzzle.check_solvability(new_puzzle.initial):
            found_solvable_puzzle = True
    return new_puzzle


def display(state):
    cnt = 0
    for num in state:
        if num == 0:
            print("*", end=" ")
        else:
            print(num, end=" ")
        cnt += 1
        if cnt % 3 == 0:
            print(end="\n")
    print()


""" 
                                ---------------------------- 

                        ---------------- Heuristics ----------------

                                ----------------------------

"""


##taken from textbook code
def misplaced(node):
    return sum(s != g for (s, g) in zip(node.state, goal_state))


def manhattan(node):
    total_distance = 0
    for tile in node.state:
        if (tile != 0):
            tile_goal_column = (tile - 1) % 3
            tile_current_column = node.state.index(tile) % 3
            horizontal_distance = abs(tile_current_column - tile_goal_column)

            tile_goal_row = (tile - 1) // 3
            tile_current_row = node.state.index(tile) // 3
            vertical_distance = abs(tile_current_row - tile_goal_row)

            total_distance += horizontal_distance + vertical_distance
    return total_distance


def inversion(node):
    node = node.state
    # left-to-right, top-to-bottom fashion
    vertical_inversions = 0
    for i in range(9):
        if node[i] == 0:
            continue
        for j in range(i + 1, 9):
            if node[j] == 0:
                continue
            if node[j] < node[i]:
                vertical_inversions += 1
    vertical_lowerbound = math.floor(vertical_inversions / 3) + vertical_inversions % 3

    # top-to-bottom, left-to-right fashion
    new_order = [0, 3, 6, 1, 4, 7, 2, 5, 8]
    new_node = []
    for i in new_order:
        new_node.append(node[i])
    horizontal_inversions = 0
    for i in range(9):
        if new_node[i] == 0:
            continue
        for j in range(i + 1, 9):
            if new_node[j] == 0:
                continue
            if new_node[j] < new_node[i]:
                horizontal_inversions += 1
    horizontal_lowerbound = math.floor(horizontal_inversions / 3) + horizontal_inversions % 3

    # add horizontal lowerbound and vertical lowerbound
    total_inversion_distance = math.floor(horizontal_lowerbound + vertical_lowerbound)

    # TODO calculate change in version by using skipped row/column instead of recalculating the entire board
    return total_inversion_distance


def walking_distance(node):
    return calculate_walking_distance(node)


##taken from textbook code
def max_heuristic(node):
    mis_score = misplaced(node)
    man_score = manhattan(node)
    # inv_score = inversion(node)
    return max(mis_score, man_score)


""" 
                                ---------------------------- 

                        ---------------- Main Program ----------------

                                ----------------------------

"""


if __name__ == "__main__":
    puzzle = make_rand_8puzzle()
    display(puzzle.initial)

    # converted_row_puzzle = convert_to_walking_row_distance_state(puzzle)
    # display_walking_distance_state(converted_row_puzzle)
    #
    # converted_column_puzzle = convert_to_walking_column_distance_state(puzzle)
    # display_walking_distance_state(converted_column_puzzle)

    print(calculate_walking_distance(Node(puzzle.initial)))

    # ##misplaced-tiles
    # print("A* with misplaced-tiles heuristic:")
    # start_time = time.time()
    #
    # sol = astar_search(puzzle, "", True).solution()
    # print("Solution: ", sol)
    # print("Solution length: ", len(sol))
    #
    # elapsed_time = time.time() - start_time
    # print(f'elapsed time (in seconds): {elapsed_time}s')
    #
    # ###manhattan
    print("\n\nA* with manhattan heuristic:")
    start_time = time.time()

    print(astar_search(puzzle,manhattan,True).state)
    sol = astar_search(puzzle, manhattan, True).solution()
    print("Solution: ", sol)
    print("Solution length: ", len(sol))

    elapsed_time = time.time() - start_time
    print(f'elapsed time (in seconds): {elapsed_time}s')

    # ## inversion
    # print("\n\nA* with inversion-distance heuristic:")
    # start_time = time.time()
    #
    # sol = astar_search(puzzle, inversion, True).solution()
    # print("Solution: ", sol)
    # print("Solution length: ", len(sol))
    #
    # elapsed_time = time.time() - start_time
    # print(f'elapsed time (in seconds): {elapsed_time}s')
    #
    # ### walking distance
    print("\n\nA* with walking distance heuristic:")
    start_time = time.time()

    # print(astar_search(puzzle,manhattan,True).state)
    sol = astar_search(puzzle, walking_distance, True).solution()
    print("Solution: ", sol)
    print("Solution length: ", len(sol))

    elapsed_time = time.time() - start_time
    print(f'elapsed time (in seconds): {elapsed_time}s')

    # ###Max-misplaced-manhattan
    # print("\n\nA* with max-misplaced-manhattan heuristic:")
    # start_time = time.time()
    #
    # sol = astar_search(puzzle, max_heuristic, True).solution()
    # print("Solution: ", sol)
    # print("Solution length: ", len(sol))
    #
    # elapsed_time = time.time() - start_time
    # print(f'elapsed time (in seconds): {elapsed_time}s')
