# a2.py

from search import *
import random as r
import time

goal_state=(1,2,3,4,5,6,7,8,0)
def make_rand_8puzzle():
    while True:
        temp = tuple(random.sample((0,1,2,3,4,5,6,7,8), 9))
        puzzle = EightPuzzle(temp,goal_state)
        if(puzzle.check_solvability(temp)):
            print("State: ")
            display(temp)
            return puzzle


# temp = tuple(random.sample((0,1,2,3,4,5,6,7,8), 9))
def display(state):
    cnt = 0
    for num in state:
        if (num == 0):
            print("*", end=" ")
        else:
            print(num, end=" ")
        cnt += 1
        if(cnt%3==0):
            print(end="\n")
    print()
###Heuristics 

##taken from textbook code
def misplaced(node):
    return sum(s != g for (s, g) in zip(node.state, goal_state))

###taken from textbook
def manhattan(node):
    state = node.state
    index_goal = {0:[2,2], 1:[0,0], 2:[0,1], 3:[0,2], 4:[1,0], 5:[1,1], 6:[1,2], 7:[2,0], 8:[2,1]}
    index_state = {}
    index = [[0,0], [0,1], [0,2], [1,0], [1,1], [1,2], [2,0], [2,1], [2,2]]
    x, y = 0, 0
    
    for i in range(len(state)):
        index_state[state[i]] = index[i]
    
    mhd = 0
    
    #modified to not consider blank tile
    for i in range(1,9):
        for j in range(2):
            mhd += abs(index_goal[i][j] - index_state[i][j])
    
    return mhd




##taken from textbook code
def max_heuristic(node):
    mis_score=misplaced(node)
    man_score=manhattan(node)
    return max(mis_score,man_score)


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
                print("Nodes expanded: ",len(explored))
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

# puzzle=make_rand_8puzzle()

puzzle=EightPuzzle((8,5,3,6,1,2,4,7,0))

###misplaced-tiles
print("A* with misplaced-tiles heuristic:")
start_time = time.time()

sol=astar_search(puzzle,"",True).solution()
print("Solution: ",sol)
print("Solution length: ",len(sol))

elapsed_time = time.time() - start_time
print(f'elapsed time (in seconds): {elapsed_time}s')

###manhattan
print("\n\nA* with manhattan heuristic:")
start_time = time.time()

sol=astar_search(puzzle,manhattan,True).solution()
print("Solution: ",sol)
print("Solution length: ",len(sol))

elapsed_time = time.time() - start_time
print(f'elapsed time (in seconds): {elapsed_time}s')

###Max-misplaced-manhattan
print("\n\nA* with max-misplaced-manhattan heuristic:")
start_time = time.time()

sol=astar_search(puzzle,max_heuristic,True).solution()
print("Solution: ",sol)
print("Solution length: ",len(sol))

elapsed_time = time.time() - start_time
print(f'elapsed time (in seconds): {elapsed_time}s')
