import sys
import time
from copy import deepcopy
from Puzzle import EightPuzzle
import random

goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]


def getPossibleMoves(state):
    pos = state.index(0)
    possible_moves=[]
    if pos == 0:
        possible_moves = [1, 3]
    elif pos == 1:
        possible_moves = [1, 3, -1]
    elif pos == 2:
        possible_moves = [3, -1]
    elif pos == 3:
        possible_moves = [-3, 1, 3]
    elif pos == 4:
        possible_moves = [-3, 3, 1, -1]
    elif pos == 5:
        possible_moves = [-3, -1, 3]
    elif pos == 6:
        possible_moves = [-3, 1]
    elif pos == 7:
        possible_moves = [-3, -1, 1]
    elif pos == 8:
        possible_moves = [-1, -3]
    return possible_moves


def applyMove(state, direction):
    next_state = deepcopy(state)
    pos = state.index(0)
    # Position blank tile will move to.
    next_pos = pos + direction
    # Swap tiles.
    next_state[pos], next_state[next_pos] = next_state[next_pos], next_state[pos]
    return next_state


def generate_puzzle(goal=None, num=10, moves=5, file='generated8.txt'):
    if goal is None:
        goal = goal_state
    generated = []
    for i in range(num):
        state = goal
        for j in range(moves):
            possible_move = getPossibleMoves(state)
            rand_move = random.sample(possible_move, 1)[0]
            state = applyMove(state, rand_move)
        puzzle = EightPuzzle(state)
        if puzzle.check_solvability(puzzle.initial):
            generated.append(tuple(puzzle.initial))
        else:
            num += 1

    with open(file, "w") as f:
        for puzzle in generated:
            f.write(str(puzzle))
            f.write("\n")


if __name__ == "__main__":
    num_tests = int(sys.argv[1])
    moves_from_goal = int(sys.argv[2])
    filename = sys.argv[3]
    start_time = time.time()
    generate_puzzle(goal_state, num_tests, moves_from_goal, filename)
    elapsed_time = time.time() - start_time
    print("done generating tests...")
    print(f'elapsed time (in seconds): {elapsed_time}s')
