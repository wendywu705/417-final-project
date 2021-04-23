from search import *
import time
import math

N = 4
goal_state = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15)

def make_rand_8puzzle():
    while True:
        temp = tuple(random.sample(goal_state, 16))
        new_puzzle = EightPuzzle(temp, goal_state)
        if new_puzzle.check_solvability(temp):
            print("State: ")
            display(temp)
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


###Heuristics

##taken from textbook code
def misplaced(node):
    return sum(s != g for (s, g) in zip(node.state, goal_state))


###taken from textbook
def manhattan(node):
    state = node.state
    index_goal = {}
    index = []
    count = 0
    for i in range(N):
        for j in range(N):
            index_goal[count] = [i, j]
            count += 1
            index.append([i, j])
    # index_goal = {0: [0, 0], 1: [0, 1], 2: [0, 2], 3: [1, 0], 4: [1, 1], 5: [1, 2], 6: [2, 0], 7: [2, 1], 8: [2, 2]}
    index_state = {}
    # index = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]
    x, y = 0, 0

    for i in range(len(state)):
        index_state[state[i]] = index[i]
    mhd = 0

    # modified to not consider blank tile
    # for i in range(1, 9):
    for i in range(1, N * N):
        for j in range(2):
            mhd += abs(index_goal[i][j] - index_state[i][j])
    return mhd


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
puzzle = EightPuzzle((1, 0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15), goal_state)
display(puzzle.initial)

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
