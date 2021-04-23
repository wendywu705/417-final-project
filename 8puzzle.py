from Puzzle import EightPuzzle
from astar_search import *
import time
import math

goal_state = (0, 1, 2, 3, 4, 5, 6, 7, 8)


def make_rand_8puzzle():
    while True:
        temp = tuple(random.sample((0, 1, 2, 3, 4, 5, 6, 7, 8), 9))
        new_puzzle = EightPuzzle(temp, goal_state)
        if new_puzzle.check_solvability(temp):
            print("State: ")
            display(temp)
            return new_puzzle


# temp = tuple(random.sample((0,1,2,3,4,5,6,7,8), 9))
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


###Heuristics

##taken from textbook code
def misplaced(node):
    return sum(s != g for (s, g) in zip(node.state, goal_state))


def manhattan(node):
    total_distance = 0
    for tile in node.state:
        if tile != 0:
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
    v_inv_count = 0
    h_inv_count = 0
    total_inv_change = 0
    state = node.state
    transpose_order = [0, 3, 6, 1, 4, 7, 2, 5, 8]
    transposed_node = []
    transposed_initial = []
    for i in transpose_order:
        if initial.parent:
            transposed_initial.append(initial.parent.state[i])
        transposed_node.append(state[i])
    if initial.parent is None:
        for i in range(len(state) - 1):
            for j in range(i + 1, len(state)):
                if (state[i] > state[j]) and state[i] != 0 and state[j] != 0:
                    v_inv_count += 1
                if (transposed_node[i] > transposed_node[j]) and transposed_node[i] != 0 and transposed_node[j] != 0:
                    h_inv_count += 1
        vertical_lowerbound = math.floor(v_inv_count / 2) + v_inv_count % 2
        horizontal_lowerbound = math.floor(h_inv_count / 2) + h_inv_count % 2
        returned_inversions = vertical_lowerbound + horizontal_lowerbound
        node.set_inversions(returned_inversions)
        return returned_inversions
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
                    total_inv_change = -2
                elif between_tile1 < moved_tile and between_tile2 < moved_tile:
                    total_inv_change = 2
            else:
                if between_tile1 > moved_tile and between_tile2 > moved_tile:
                    total_inv_change = 2
                elif between_tile1 < moved_tile and between_tile2 < moved_tile:
                    total_inv_change = -2
        # vertical
        else:
            smaller = min(prev_blank, new_blank)
            between_tile1 = state[smaller + 1]
            between_tile2 = state[smaller + 2]
            if initial.action == 'UP':
                if between_tile1 > moved_tile and between_tile2 > moved_tile:
                    total_inv_change = 2
                elif between_tile1 < moved_tile and between_tile2 < moved_tile:
                    total_inv_change = -2
            else:
                if between_tile1 > moved_tile and between_tile2 > moved_tile:
                    total_inv_change = -2
                elif between_tile1 < moved_tile and between_tile2 < moved_tile:
                    total_inv_change = 2
        returned_inversions = node.parent.inversions + total_inv_change / 2
        node.set_inversions(returned_inversions)
        return returned_inversions


##taken from textbook code
def max_heuristic(node):
    mis_score = misplaced(node)
    man_score = manhattan(node)
    # inv_score = inversion(node)
    return max(mis_score, man_score)


###Modifed Textbook code
def best_first_graph_search(problem, f, display=False):
    """Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have breadth-first search.
    There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    values will be cached on the nodes as they are computed. So after doing
    a best first search you can examine the f values of the path returned."""
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    while frontier:
        node = frontier.pop()
        if problem.goal_test(node.state):
            if display:
                print("Nodes expanded: ", len(explored))
            return node
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None


def astar_search(problem, h=None, display=True):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)


############################################# driver code

# puzzle = make_rand_8puzzle()
# puzzle = EightPuzzle((0, 2, 3, 1, 5, 7, 6, 4, 8))
# puzzle = EightPuzzle((0, 8, 5, 3, 4, 7, 2, 6, 1))
puzzle = EightPuzzle((2, 6, 5, 0, 3, 4, 7, 8, 1))

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
