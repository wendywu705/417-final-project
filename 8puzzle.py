import math
import time

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
    initial = node
    state = node.state
    transpose_order = [0, 3, 6, 1, 4, 7, 2, 5, 8]
    transposed_node = []
    transposed_initial = []
    v_invcount = 0
    h_invcount = 0
    for i in transpose_order:
        if initial.parent:
            transposed_initial.append(initial.parent.state[i])
        transposed_node.append(state[i])
    if initial.parent is None:
        for i in range(len(state) - 1):
            for j in range(i + 1, len(state)):
                if (state[i] > state[j]) and state[i] != 0 and state[j] != 0:
                    v_invcount += 1
                if (transposed_node[i] > transposed_node[j]) and transposed_node[i] != 0 and transposed_node[j] != 0:
                    h_invcount += 1
        vertical_lowerbound = math.floor(v_invcount / 2) + v_invcount % 2
        horizontal_lowerbound = math.floor(h_invcount / 2) + h_invcount % 2
        returned_inversions = vertical_lowerbound + horizontal_lowerbound
        node.h_invcount = h_invcount
        node.v_invcount = v_invcount
    else:
        prev_blank = initial.parent.state.index(0)
        new_blank = state.index(0)
        moved_tile = state[prev_blank]
        # horizontal
        if initial.action == 'LEFT' or initial.action == 'RIGHT':
            prev_blank = transposed_initial.index(0)
            new_blank = transposed_node.index(0)
            smaller = min(prev_blank, new_blank)
            between_tile1 = transposed_node[smaller + 1]
            between_tile2 = transposed_node[smaller + 2]
            if initial.action == 'RIGHT':
                if between_tile1 > moved_tile and between_tile2 > moved_tile:
                    h_invcount = -2
                elif between_tile1 < moved_tile and between_tile2 < moved_tile:
                    h_invcount = 2
            else:
                if between_tile1 > moved_tile and between_tile2 > moved_tile:
                    h_invcount = 2
                elif between_tile1 < moved_tile and between_tile2 < moved_tile:
                    h_invcount = -2
            node.h_invcount += h_invcount
        # vertical
        else:
            smaller = min(prev_blank, new_blank)
            between_tile1 = state[smaller + 1]
            between_tile2 = state[smaller + 2]
            if initial.action == 'UP':
                if between_tile1 > moved_tile and between_tile2 > moved_tile:
                    v_invcount = 2
                elif between_tile1 < moved_tile and between_tile2 < moved_tile:
                    v_invcount = -2
            else:
                if between_tile1 > moved_tile and between_tile2 > moved_tile:
                    v_invcount = -2
                elif between_tile1 < moved_tile and between_tile2 < moved_tile:
                    v_invcount = 2
            node.v_invcount += v_invcount
        if node.v_invcount == 0 and node.state[8] == 0:
            returned_inversions = 0
        else:
            vertical_lowerbound = math.floor(node.v_invcount / 2) + node.v_invcount % 2
            horizontal_lowerbound = math.floor(node.h_invcount / 2) + node.h_invcount % 2
            returned_inversions = vertical_lowerbound + horizontal_lowerbound
    return returned_inversions


def walking_distance(node):
    return walking_distance_table[node.state]


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
    print("\n\nCreating Walking Distance lookup table:")
    # start_time = time.time()

    # create_walking_distance_table()       ## only need to run this for the first time to generate the lookup files
    walking_distance_table = load_table_from_file('walking_distance_db.txt')
    print(f'The Walking Distance lookup table has {len(walking_distance_table)} entries.\n\n')

    # elapsed_time = time.time() - start_time
    # print(f'elapsed time (in seconds): {elapsed_time}s\n\n')

    puzzle = make_rand_8puzzle()
    display(puzzle.initial)


    ### misplaced-tiles
    print("A* with misplaced-tiles heuristic:")
    start_time = time.time()

    sol = astar_search(puzzle, "", True).solution()
    print("Solution: ", sol)
    print("Solution length: ", len(sol))

    elapsed_time = time.time() - start_time
    print(f'elapsed time (in seconds): {elapsed_time}s')


    ### manhattan
    print("\n\nA* with manhattan heuristic:")
    start_time = time.time()

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


    ### walking distance
    print("\n\nA* with walking distance heuristic:")
    start_time = time.time()

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
