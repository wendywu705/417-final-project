import csv
import random
from walking_dist.walking_distance import *
import time
import math


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
    inverse_order = [1, 4, 7, 2, 5, 8, 3, 6, 0]
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
                inverse_i = transposed_node[i]
                inverse_j = transposed_node[j]
                if inverse_i != 0 and inverse_j != 0 and (
                        inverse_order.index(inverse_i) > inverse_order.index(inverse_j)):
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
            between_tile1 = inverse_order.index(transposed_node[smaller + 1])
            between_tile2 = inverse_order.index(transposed_node[smaller + 2])
            inverse_moved = inverse_order.index(moved_tile)
            if initial.action == 'RIGHT':
                if between_tile1 > inverse_moved and between_tile2 > inverse_moved:
                    h_invcount = -2
                elif between_tile1 < inverse_moved and between_tile2 < inverse_moved:
                    h_invcount = 2
            else:
                if between_tile1 > inverse_moved and between_tile2 > inverse_moved:
                    h_invcount = 2
                elif between_tile1 < inverse_moved and between_tile2 < inverse_moved:
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
        vertical_lowerbound = math.floor(node.v_invcount / 2) + node.v_invcount % 2
        horizontal_lowerbound = math.floor(node.h_invcount / 2) + node.h_invcount % 2
        returned_inversions = vertical_lowerbound + horizontal_lowerbound
    return returned_inversions


def walking_distance(node):
    return walking_distance_table[node.state]




def fullPDB(node):
    state = ",".join(str(m) for m in node.state)
    return lines[state]


def append_row(file_name, new_row):
    with open(file_name, 'a', newline='') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(new_row)


def make_new(file_name):
    with open(file_name, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['puzzle', 'solution', 'length of solution', 'time(s)'])


""" 
                                ---------------------------- 

                        ---------------- Main Program ----------------

                                ----------------------------

"""

if __name__ == "__main__":
    print("\n\nCreating Walking Distance lookup table:")
    # start_time = time.time()

    # create_8puzzle_walking_distance_table()       ## only need to run this for the first time to generate the lookup files
    walking_distance_table = load_table_from_file('walking_dist/walking_distance_db_8puzzle.txt')
    print(f'The Walking Distance lookup table has {len(walking_distance_table)} entries.\n\n')

    # elapsed_time = time.time() - start_time
    # print(f'elapsed time (in seconds): {elapsed_time}s\n\n')

    # create full pdb lookup table
    print("\n\nCreating PDB lookup table...")
    with open("fringe_pdb/8puzzleDatabase.txt", 'r') as db:
        lines = db.read()
    lines = lines.split('\n')
    linedict = {}
    for k in lines:
        if k == '':
            break
        t = eval(k)
        linedict[t[0]] = t[1]
    lines = linedict

    puzzles = []
    file = open(sys.argv[1])
    Lines = file.readlines()
    for line in Lines:
        puzzles.append(eval(line.strip()))
    #
    filenames = ['results8/manhattan.csv','results8/inversion.csv', 'results8/walking_dist.csv', 'results8/fringe_PDB.csv']

    for name in filenames:
        make_new(name)

    total_start = time.time()
    mhd_time = 0
    inversion_time = 0
    wd_time = 0
    fringe_time = 0

    for line in puzzles:
        puzzle = EightPuzzle(line)
        if not puzzle.check_solvability(puzzle.initial):
            print("unsolvable puzzle")
            display(puzzle.initial)
            continue
        print("---------\nPuzzle:")
        display(puzzle.initial)

        ###manhattan
        print("\n\nA* with manhattan heuristic:")
        start_time = time.time()

        # print(astar_search(puzzle,manhattan,True).state)
        sol = astar_search(puzzle, manhattan, True).solution()
        print("Solution: ", sol)
        print("Solution length: ", len(sol))

        elapsed_time = time.time() - start_time
        mhd_time += elapsed_time
        print(f'elapsed time (in seconds): {elapsed_time}s')

        append_row('results8/manhattan.csv', [line, sol, len(sol), elapsed_time])

        ## inversion
        print("\n\nA* with inversion-distance heuristic:")
        start_time = time.time()

        sol = astar_search(puzzle, inversion, True).solution()
        print("Solution: ", sol)
        print("Solution length: ", len(sol))

        elapsed_time = time.time() - start_time
        inversion_time += elapsed_time
        print(f'elapsed time (in seconds): {elapsed_time}s')

        append_row('results8/inversion.csv', [line, sol, len(sol), elapsed_time])

        ### walking distance
        print("\n\nA* with walking distance heuristic:")
        start_time = time.time()

        sol = astar_search(puzzle, walking_distance, True).solution()
        print("Solution: ", sol)
        print("Solution length: ", len(sol))

        elapsed_time = time.time() - start_time
        wd_time += elapsed_time
        print(f'elapsed time (in seconds): {elapsed_time}s')

        append_row('results8/walking_dist.csv', [line, sol, len(sol), elapsed_time])

        #Full PDB
        print("\n\nA* with full PDB heuristic:")
        start_time = time.time()
        
        sol = astar_search(puzzle, fullPDB, True).solution()
        print("Solution: ", sol)
        print("Solution length: ", len(sol))
        
        elapsed_time = time.time() - start_time
        fringe_time += elapsed_time
        print(f'elapsed time (in seconds): {elapsed_time}s')
        
        append_row('results8/fringe_PDB.csv', [line, sol, len(sol), elapsed_time])

    total_time = time.time() - total_start
    print("\nAll puzzles:")
    print(f'elapsed time (in seconds): {total_time}s')

    print("\nAll puzzles w/ Manhattan Distance:")
    print(f'elapsed time (in seconds): {mhd_time}s')

    print("\nAll puzzles w/ Inversion Distance:")
    print(f'elapsed time (in seconds): {inversion_time}s')

    print("\nAll puzzles w/ Walking Distance:")
    print(f'elapsed time (in seconds): {wd_time}s')

    print("\nAll puzzles w/ Fringe PDB:")
    print(f'elapsed time (in seconds): {fringe_time}s')
