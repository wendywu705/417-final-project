from Puzzle import FifteenPuzzle
from astar_search import *
import time
import math

N = 4
goal_state = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0)


def make_rand_15puzzle():
    found_solvable_puzzle = False
    new_puzzle = FifteenPuzzle(goal_state)
    while not found_solvable_puzzle:
        state = tuple(random.sample(goal_state, 16))
        new_puzzle = FifteenPuzzle(state)
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
        if cnt % N == 0:
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
            tile_goal_column = (tile - 1) % 4
            tile_current_column = node.state.index(tile) % 4
            horizontal_distance = abs(tile_current_column - tile_goal_column)

            tile_goal_row = (tile - 1) // 4
            tile_current_row = node.state.index(tile) // 4
            vertical_distance = abs(tile_current_row - tile_goal_row)

            total_distance += horizontal_distance + vertical_distance
    return total_distance


def inversion(node):
    node = node.state
    # left-to-right, top-to-bottom fashion
    vertical_inversions = 0
    for i in range(N * N):
        if node[i] == 0:
            continue
        for j in range(i + 1, N * N):
            if node[j] == 0:
                continue
            if node[j] < node[i]:
                vertical_inversions += 1
    vertical_lowerbound = math.floor(vertical_inversions / N) + vertical_inversions % N

    # top-to-bottom, left-to-right fashion
    # new_order = [0, 3, 6, 1, 4, 7, 2, 5, 8]
    new_order = []
    prev = 1
    for i in range(N):
        for j in range(i, N * N, N):
            new_order.append(j)

    new_node = []
    for i in new_order:
        new_node.append(node[i])
    horizontal_inversions = 0
    for i in range(N):
        if new_node[i] == 0:
            continue
        for j in range(i + 1, N):
            if new_node[j] == 0:
                continue
            if new_node[j] < new_node[i]:
                horizontal_inversions += 1
    horizontal_lowerbound = math.floor(horizontal_inversions / N) + horizontal_inversions % N

    # add horizontal lowerbound and vertical lowerbound
    total_inversion_distance = math.floor(horizontal_lowerbound + vertical_lowerbound)

    # TODO calculate change in version by using skipped row/column instead of recalculating the entire board
    return total_inversion_distance


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
    puzzle = FifteenPuzzle((6, 3, 4, 8, 2, 1, 7, 12, 5, 10, 15, 14, 9, 13, 0, 11))
    # puzzle = make_rand_15puzzle()
    display(puzzle.initial)
    print('solvability = ', puzzle.check_solvability(puzzle.initial))
    print()

    ##misplaced-tiles
    print("A* with misplaced-tiles heuristic:")
    start_time = time.time()

    sol = astar_search(puzzle, "", True).solution()
    print("Solution: ", sol)
    print("Solution length: ", len(sol))

    elapsed_time = time.time() - start_time
    print(f'elapsed time (in seconds): {elapsed_time}s')

    ###manhattan
    print("\n\nA* with manhattan heuristic:")
    start_time = time.time()

    # print(astar_search(puzzle,manhattan,True).state)
    # print(manhattan(Node(puzzle.initial)))
    sol = astar_search(puzzle, manhattan, True).solution()
    print("Solution: ", sol)
    print("Solution length: ", len(sol))

    elapsed_time = time.time() - start_time
    print(f'elapsed time (in seconds): {elapsed_time}s')

    ## inversion
    print("\n\nA* with inversion-distance heuristic:")
    start_time = time.time()

    sol = astar_search(puzzle, inversion, True).solution()
    print("Solution: ", sol)
    print("Solution length: ", len(sol))

    elapsed_time = time.time() - start_time
    print(f'elapsed time (in seconds): {elapsed_time}s')

    ###Max-misplaced-manhattan
    print("\n\nA* with max-misplaced-manhattan heuristic:")
    start_time = time.time()

    sol = astar_search(puzzle, max_heuristic, True).solution()
    print("Solution: ", sol)
    print("Solution length: ", len(sol))

    elapsed_time = time.time() - start_time
    print(f'elapsed time (in seconds): {elapsed_time}s')
