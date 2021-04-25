from copy import deepcopy
from collections import * 
import json
import math
import time
import itertools
from typing import List

goal_part61 = [1, 2, 3, 4, 5, -1, -1, -1,-1,-1,-1,-1,-1,-1,-1,0]
goal_part62=[-1,-1,-1,-1,-1,6,7,8,9,10,-1,-1,-1,-1,-1,0]
goal_part3=[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,11,12,13,14,15,0]

def getPossibleMoves(state):
    pos = state.index(0)

    if pos == 0:
        possible_moves = [1, 4]
    elif pos == 1:
        possible_moves = [1, 4, -1]
    elif pos == 2:
        possible_moves = [4, -1,1]
    elif pos == 3:
        possible_moves = [-1, 4]
    elif pos == 4:
        possible_moves=[-4,4,1]
    elif pos == 7:
        possible_moves = [-4, 4, -1]
    elif pos == 8:
        possible_moves = [1,-4,4]
    elif pos ==11:
        possible_moves = [-1,4,-4]
    elif pos ==12:
        possible_moves = [-4,1]
    elif pos ==13:
        possible_moves=[1,-1,-4]
    elif pos == 14:
        possible_moves = [1,-1,-4]
    elif pos == 15: 
        possible_moves = [-4,-1]
    else:
        possible_moves = [-4, 1, 4, -1]

    return possible_moves


def applyMove(state,direction):
    next_state = deepcopy(state)
    pos = state.index(0)
    # Position blank tile will move to.
    next_pos = pos + direction
    # Swap tiles.
    next_state[pos], next_state[next_pos] = next_state[next_pos], next_state[pos]

    return next_state



def accumulate(entries):
    it = itertools.groupby(entries,lambda x:x[0])
    for key, subiter in it:
        yield key, min(k[1] for k in subiter)



def generate11_15Database():
    start_time = time.time()
    start = goal_part3
    queue = deque([[start, 0]])
    visited = set()
    entries = set()
    while queue:
        state_cost = queue.popleft()
        state = state_cost[0]
        cost = state_cost[1]
        for m in getPossibleMoves(state):

            next_state = deepcopy(state)
            pos = state.index(0)
            # Position blank tile will move to.
            next_pos = pos + m
            # Swap tiles.
            next_state[pos], next_state[next_pos] = next_state[next_pos], next_state[pos]
            if next_state[pos] != -1:
                cost+=1

            indices=[]
            for k in range(11,16):
                indices.append(next_state.index(k))
            next_state_cost = [next_state, cost]

            
            entry = ",".join(str(t) for t in indices)
            state_entry = ",".join(str(t) for t in next_state)
            if not state_entry in visited:
                queue.append(next_state_cost)
                entries.add((entry,cost))
                visited.add(state_entry)
        # if len(entries) % 10000 == 0:
        # print("Entries collected: " + str(len(entries)))
        

        if len(entries) >= math.factorial(16)/math.factorial(16-6):
            print("break")
            break
    
    
    entries=sorted(entries,key=lambda x:x[0])
    entries=list(accumulate(entries))

    with open("database11-15.txt", "w") as f:
        for entry in sorted(entries,key=lambda x:x[1]):
            json.dump(entry, f)
            f.write("\n")

    elapsed_time = time.time() - start_time
    print("3 database generated")
    print(f'elapsed time (in seconds): {elapsed_time}s')

def generate1_5Database():
    start_time = time.time()
    start = goal_part61
    queue = deque([[start, 0]])
    visited = set()
    entries = set()
    while queue:
        state_cost = queue.popleft()
        state = state_cost[0]
        cost = state_cost[1]

        for m in getPossibleMoves(state):
            next_state = applyMove(state, m)
            pos = state.index(0)
            if next_state[pos] != -1:
                cost+=1


            next_state_cost = [next_state, cost]

            indices=[]
            for k in range(1,6):
                indices.append(next_state.index(k))
            next_state_cost = [next_state, cost]

            
            entry = ",".join(str(t) for t in indices)
            state_entry = ",".join(str(t) for t in next_state)
            if not state_entry in visited:
                queue.append(next_state_cost)
                entries.add((entry,cost))
                visited.add(state_entry)
        # if len(entries) % 10000 == 0:
        # print("Entries collected: " + str(len(entries)))
        

        if len(entries) >= math.factorial(16)/math.factorial(16-6):
            print("break")
            break
    
    
    entries=sorted(entries,key=lambda x:x[0])
    entries=list(accumulate(entries))
    with open("database1-5.txt", "w") as f:
        for entry in sorted(entries,key=lambda x:x[1]):
            json.dump(entry, f)
            f.write("\n")

    elapsed_time = time.time() - start_time
    print("First 6 database generated")
    print(f'elapsed time (in seconds): {elapsed_time}s')

def generate6_10Database():
    start_time = time.time()
    start = goal_part62
    queue = deque([[start, 0]])
    visited = set()
    entries = set()
    entries.add((",".join(str(t) for t in start),0))
    visited.add(",".join(str(t) for t in start))
    while queue:
        state_cost = queue.popleft()
        state = state_cost[0]
        cost = state_cost[1]

        for m in getPossibleMoves(state):
            next_state = applyMove(state, m)
            pos = state.index(0)
            if next_state[pos] != -1:
                cost+=1
            next_state_cost = [next_state, cost]

            indices=[]
            for k in range(6,11):
                indices.append(next_state.index(k))
            next_state_cost = [next_state, cost]

            
            entry = ",".join(str(t) for t in indices)
            state_entry = ",".join(str(t) for t in next_state)
            if not state_entry in visited:
                queue.append(next_state_cost)
                entries.add((entry,cost))
                visited.add(state_entry)
        # if len(entries) % 10000 == 0:
        # print("Entries collected: " + str(len(entries)))
        

        if len(entries) >= math.factorial(16)/math.factorial(16-6):
            print("break")
            break
    
    
    entries=sorted(entries,key=lambda x:x[0])
    entries=list(accumulate(entries))
    with open("database6-10.txt", "w") as f:
        for entry in sorted(entries,key=lambda x:x[1]):
            json.dump(entry, f)
            f.write("\n")

    elapsed_time = time.time() - start_time
    print("Second 6 database generated")
    print(f'elapsed time (in seconds): {elapsed_time}s')


generate11_15Database()
generate1_5Database()
generate6_10Database()