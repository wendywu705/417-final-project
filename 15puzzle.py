from walking_dist.walking_distance import *
from search import *
import time
import math
import csv
import random

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
        if cnt % 4 == 0:
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
            tile_goal_column = (tile - 1) % 4
            tile_current_column = node.state.index(tile) % 4
            horizontal_distance = abs(tile_current_column - tile_goal_column)

            tile_goal_row = (tile - 1) // 4
            tile_current_row = node.state.index(tile) // 4
            vertical_distance = abs(tile_current_row - tile_goal_row)

            total_distance += horizontal_distance + vertical_distance
    return total_distance


def inversion(node):
    initial = node
    state = node.state
    transpose_order = [0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15]
    inverse_order = [1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15, 4, 8, 12]
    transposed_node = []
    transposed_initial = []
    v_invcount = 0
    h_invcount = 0
    for i in transpose_order:
        if initial.parent:
            transposed_initial.append(initial.parent.state[i])
        transposed_node.append(state[i])
    if node.parent is None:
        for i in range(len(state) - 1):
            for j in range(i + 1, len(state)):
                if (state[i] > state[j]) and state[i] != 0 and state[j] != 0:
                    v_invcount += 1
                inverse_i = transposed_node[i]
                inverse_j = transposed_node[j]
                if inverse_i != 0 and inverse_j != 0 and (
                        inverse_order.index(inverse_i) > inverse_order.index(inverse_j)):
                    h_invcount += 1
        vertical_lowerbound = math.floor(v_invcount / 3) + v_invcount % 3
        horizontal_lowerbound = math.floor(h_invcount / 3) + h_invcount % 3
        returned_inversions = vertical_lowerbound + horizontal_lowerbound
        node.h_invcount = h_invcount
        node.v_invcount = v_invcount
    else:
        v_invcount = 0
        h_invcount = 0
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
            between_tile3 = transposed_node[smaller + 3]
            tiles = [between_tile1, between_tile2, between_tile3]
            bigger_tiles = 0
            smaller_tiles = 0
            for tile in tiles:
                if inverse_order.index(tile) > inverse_order.index(moved_tile):
                    bigger_tiles += 1
                else:
                    smaller_tiles += 1
            if initial.action == 'RIGHT':
                if smaller_tiles == 3:
                    h_invcount = 3
                elif bigger_tiles == 3:
                    h_invcount = -3
                elif bigger_tiles == 2 and smaller_tiles == 1:
                    h_invcount = -1
                elif bigger_tiles == 1 and smaller_tiles == 2:
                    h_invcount = 1
            else:
                if smaller_tiles == 3:
                    h_invcount = -3
                elif bigger_tiles == 3:
                    h_invcount = 3
                elif bigger_tiles == 2 and smaller_tiles == 1:
                    h_invcount = 1
                elif bigger_tiles == 1 and smaller_tiles == 2:
                    h_invcount = -1
            node.h_invcount += h_invcount
        # vertical
        else:
            smaller = min(prev_blank, new_blank)
            between_tile1 = state[smaller + 1]
            between_tile2 = state[smaller + 2]
            between_tile3 = state[smaller + 3]
            tiles = [between_tile1, between_tile2, between_tile3]
            bigger_tiles = 0
            smaller_tiles = 0
            for tile in tiles:
                if tile > moved_tile:
                    bigger_tiles += 1
                else:
                    smaller_tiles += 1
            if initial.action == 'UP':
                if smaller_tiles == 3:
                    v_invcount = -3
                elif bigger_tiles == 3:
                    v_invcount = 3
                elif bigger_tiles == 2 and smaller_tiles == 1:
                    v_invcount = 1
                elif bigger_tiles == 1 and smaller_tiles == 2:
                    v_invcount = -1
            else:
                if smaller_tiles == 3:
                    v_invcount = 3
                elif bigger_tiles == 3:
                    v_invcount = -3
                elif bigger_tiles == 2 and smaller_tiles == 1:
                    v_invcount = -1
                elif bigger_tiles == 1 and smaller_tiles == 2:
                    v_invcount = 1
            node.v_invcount += v_invcount
        vertical_lowerbound = math.floor(node.v_invcount / 3) + node.v_invcount % 3
        horizontal_lowerbound = math.floor(node.h_invcount / 3) + node.h_invcount % 3
        returned_inversions = vertical_lowerbound + horizontal_lowerbound
    return returned_inversions


def walking_distance(node):
    '''
    row_state = convert_to_15puzzle_row_distance_state(node.state)
    row_distance = walking_distance_row_table[row_state]

    col_state = convert_to_15puzzle_column_distance_state(node.state)
    col_distance = walking_distance_col_table[col_state]
    return row_distance + col_distance
    '''


def fringePDB(node):
    pat1State = []
    pat2State = []
    pat3State = []
    for k in range(1, 6):
        pat1State.append(node.state.index(k))
    for k in range(6, 11):
        pat2State.append(node.state.index(k))
    for k in range(11, 16):
        pat3State.append(node.state.index(k))

    pat1State = ",".join(str(t) for t in pat1State)
    pat2State = ",".join(str(t) for t in pat2State)
    pat3State = ",".join(str(t) for t in pat3State)

    # db1Line=next((i for i, colour in enumerate(lines1)if pat1State in lines1),None)
    # print('found1')
    # db2Line=next((i for i, colour in enumerate(lines2)if pat2State in lines2),None)
    # print('found2')
    # db3Line=next((i for i, colour in enumerate(lines3)if pat3State in lines3),None)
    # print('found3')

    pat1Cost = lines1[pat1State]
    pat2Cost = lines2[pat2State]
    pat3Cost = lines3[pat3State]

    return pat1Cost + pat2Cost + pat3Cost


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
    print("\n\nCreating PDB lookup table...")
    with open("fringe_pdb/database1-5.txt", 'r') as db1:
        lines1 = db1.read()
    lines1 = lines1.split('\n')
    line1dict = {}
    for k in lines1:
        if k == '':
            break
        t = eval(k)
        line1dict[t[0]] = t[1]
    lines1 = line1dict
    with open("fringe_pdb/database6-10.txt", 'r') as db2:
        lines2 = db2.read()
    lines2 = lines2.split('\n')
    line2dict = {}
    for k in lines2:
        if k == '':
            break
        t = eval(k)
        line2dict[t[0]] = t[1]
    lines2 = line2dict
    with open("fringe_pdb/database11-15.txt", 'r') as db3:
        lines3 = db3.read()
    lines3 = lines3.split('\n')
    line3dict = {}
    for k in lines3:
        if k == '':
            break
        t = eval(k)
        line3dict[t[0]] = t[1]
    lines3 = line3dict

    # print("\n\nCreating Walking Distance lookup table:")
    # start_time = time.time()
    #
    # create_15puzzle_walking_distance_table()  ## only need to run this for the first time to generate the lookup files
    # walking_distance_row_table = load_table_from_file('row_distance_db_15puzzle.txt')
    # walking_distance_col_table = load_table_from_file('col_distance_db_15puzzle.txt')
    #
    # elapsed_time = time.time() - start_time
    # print(f'elapsed time (in seconds): {elapsed_time}s\n\n')

    puzzles = []
    file = open(sys.argv[1])
    Lines = file.readlines()
    for line in Lines:
        puzzles.append(eval(line.strip()))
    #
    filenames = ['results15/manhattan.csv', 'results15/inversion.csv', 'results15/fringe_PDB.csv']

    for name in filenames:
        make_new(name)

    total_start = time.time()
    mhd_time = 0
    inversion_time = 0
    fringe_time = 0

    for line in puzzles:
        puzzle = FifteenPuzzle(line)
        display(puzzle.initial)

        ###manhattan
        print("\n\nA* with manhattan heuristic:")
        start_time = time.time()

        sol = astar_search(puzzle, manhattan, True).solution()
        print("Solution: ", sol)
        print("Solution length: ", len(sol))

        elapsed_time = time.time() - start_time
        mhd_time += elapsed_time
        print(f'elapsed time (in seconds): {elapsed_time}s')

        append_row('results15/manhattan.csv', [line, sol, len(sol), elapsed_time])

        ## inversion
        print("\n\nA* with inversion-distance heuristic:")
        start_time = time.time()

        sol = astar_search(puzzle, inversion, True).solution()
        print("Solution: ", sol)
        print("Solution length: ", len(sol))

        elapsed_time = time.time() - start_time
        inversion_time += elapsed_time
        print(f'elapsed time (in seconds): {elapsed_time}s')

        append_row('results15/inversion.csv', [line, sol, len(sol), elapsed_time])

        ## walking distance
        # print("\n\nA* with walking distance heuristic:")
        # start_time = time.time()
        #
        # sol = astar_search(puzzle, walking_distance, True).solution()
        # print("Solution: ", sol)
        # print("Solution length: ", len(sol))
        #
        # elapsed_time = time.time() - start_time
        # inversion_time += elapsed_time
        # print(f'elapsed time (in seconds): {elapsed_time}s')

        # append_row('results15/walking_dist.csv', [line, sol, len(sol), elapsed_time])

        # FUll PDB
        print("\n\nA* with fringe pdb heuristic:")
        start_time = time.time()

        sol = astar_search(puzzle, fringePDB, True).solution()
        print("Solution: ", sol)
        print("Solution length: ", len(sol))

        elapsed_time = time.time() - start_time
        fringe_time += elapsed_time
        print(f'elapsed time (in seconds): {elapsed_time}s')

        append_row('results15/fringe_PDB.csv', [line, sol, len(sol), elapsed_time])

    total_time = time.time() - total_start
    print("\nAll puzzles:")
    print(f'elapsed time (in seconds): {total_time}s')

    print("\nAll puzzles w/ Manhattan Distance:")
    print(f'elapsed time (in seconds): {mhd_time}s')

    print("\nAll puzzles w/ Inversion Distance:")
    print(f'elapsed time (in seconds): {inversion_time}s')

    print("\nAll puzzles w/ Fringe PDB:")
    print(f'elapsed time (in seconds): {fringe_time}s')
