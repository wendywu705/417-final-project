from Puzzle import FifteenPuzzle
from astar_search import *
import time
import math
import json
import ast

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


def fringePDB(node):

    pat1State=[]
    pat2State=[]
    pat3State=[]
    for k in range(1,6):
        pat1State.append(node.state.index(k))
    for k in range(6,11):
        pat2State.append(node.state.index(k))
    for k in range(11,16):
        pat3State.append(node.state.index(k))

    pat1State=",".join(str(t) for t in pat1State)
    pat2State=",".join(str(t) for t in pat2State)
    pat3State=",".join(str(t) for t in pat3State)

    # db1Line=next((i for i, colour in enumerate(lines1)if pat1State in lines1),None)
    # print('found1')
    # db2Line=next((i for i, colour in enumerate(lines2)if pat2State in lines2),None)
    # print('found2')
    # db3Line=next((i for i, colour in enumerate(lines3)if pat3State in lines3),None)
    # print('found3')

    pat1Cost=lines1[pat1State]
    pat2Cost=lines2[pat2State]
    pat3Cost=lines3[pat3State]

    return max(pat1Cost,pat2Cost,pat3Cost)

""" 
                                ---------------------------- 

                        ---------------- Main Program ----------------

                                ----------------------------

"""


if __name__ == "__main__":

    with open("database1-5.txt",'r') as db1:
        lines1=db1.read()
    lines1=lines1.split('\n')
    line1dict={}
    for k in lines1:
        if k=='':
            break
        t=eval(k)
        line1dict[t[0]]=t[1]
    lines1=line1dict
    with open("database6-10.txt",'r') as db2:
        lines2=db2.read()
    lines2=lines2.split('\n')
    line2dict={}
    for k in lines2:
        if k=='':
            break
        t=eval(k)
        line2dict[t[0]]=t[1]
    lines2=line2dict
    with open("database11-15.txt",'r') as db3:
        lines3=db3.read()
    lines3=lines3.split('\n')
    line3dict={}
    for k in lines3:
        if k=='':
            break
        t=eval(k)
        line3dict[t[0]]=t[1]
    lines3=line3dict

    puzzle = FifteenPuzzle((6, 3, 4, 8, 2, 1, 7, 12, 5, 10, 15, 14, 9, 13, 0, 11))
    # puzzle = FifteenPuzzle((1,2,3,4,5,6,7,8,9,10,11,12,13,14,0,15))
    # puzzle = make_rand_15puzzle()
    display(puzzle.initial)
    print('solvability = ', puzzle.check_solvability(puzzle.initial))
    print()

    # ##misplaced-tiles
    # print("A* with misplaced-tiles heuristic:")
    # start_time = time.time()

    # sol = astar_search(puzzle, "", True).solution()
    # print("Solution: ", sol)
    # print("Solution length: ", len(sol))

    # elapsed_time = time.time() - start_time
    # print(f'elapsed time (in seconds): {elapsed_time}s')

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

    # ## inversion
    # print("\n\nA* with inversion-distance heuristic:")
    # start_time = time.time()

    # sol = astar_search(puzzle, inversion, True).solution()
    # print("Solution: ", sol)
    # print("Solution length: ", len(sol))

    # elapsed_time = time.time() - start_time
    # print(f'elapsed time (in seconds): {elapsed_time}s')

    # ###Max-misplaced-manhattan
    # print("\n\nA* with max-misplaced-manhattan heuristic:")
    # start_time = time.time()

    # sol = astar_search(puzzle, max_heuristic, True).solution()
    # print("Solution: ", sol)
    # print("Solution length: ", len(sol))

    # elapsed_time = time.time() - start_time
    # print(f'elapsed time (in seconds): {elapsed_time}s')

    print("\n\nA* with fringe pdb heuristic:")
    start_time = time.time()

    sol = astar_search(puzzle, fringePDB, True).solution()
    print("Solution: ", sol)
    print("Solution length: ", len(sol))

    elapsed_time = time.time() - start_time
    print(f'elapsed time (in seconds): {elapsed_time}s')