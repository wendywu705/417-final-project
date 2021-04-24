from copy import deepcopy
from collections import * 
import json
import math
import time

goal_part61 = [1, 2, 3, 4, 5, 6, -1, -1,-1,-1,-1,-1,-1,-1,-1,0]
goal_part62=[-1,-1,-1,-1,-1,-1,7,8,9,10,11,12,-1,-1,-1,0]
goal_part3=[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,13,14,15,0]

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

def generatePart3Database():
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
            for k in range(13,16):
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
        

        if len(entries) >= math.factorial(16)/math.factorial(16-4):
            print("break")
            break
    
    entries=sorted(entries,key=lambda x:x[1])
    finalEntries=set()
    for k in entries:
        result = next((i for i, v in enumerate(finalEntries) if v[0] == k[0]), None)
        if result==None:
            finalEntries.add(k)

    finalEntries = sorted(finalEntries,key=lambda x:x[1])
    with open("database3.txt", "w") as f:
        for entry in finalEntries:
            json.dump(entry, f)
            f.write("\n")

    elapsed_time = time.time() - start_time
    print("3 database generated")
    print(f'elapsed time (in seconds): {elapsed_time}s')

def generateFirstPart6Database():
    start_time = time.time()
    start = goal_part61
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
            for k in range(1,7):
                indices.append(next_state.index(k))
            next_state_cost = [next_state, cost]

            
            entry = ",".join(str(t) for t in indices)
            state_entry = ",".join(str(t) for t in next_state)
            if not entry in visited:
                queue.append(next_state_cost)
                entries.add((entry,cost))
                visited.add(state_entry)
        
        # if len(entries) % 10000 == 0:
        #     print("Entries collected: " + str(len(entries)))
        
        if len(entries) >= math.factorial(16)/math.factorial(16-7):
            print("breaking")
            break
    
    print("checking dups")
    entries=sorted(entries,key=lambda x:x[1])
    finalEntries=set()
    for k in entries:
        result = next((i for i, v in enumerate(finalEntries) if v[0] == k[0]), None)
        if result==None:
            finalEntries.add(k)

    print("sorting")
    finalEntries = sorted(finalEntries,key=lambda x:x[1])
    print("writing")
    with open("database3.txt", "w") as f:
        for entry in finalEntries:
            json.dump(entry, f)
            f.write("\n")

    elapsed_time = time.time() - start_time
    print("First 6 database generated")
    print(f'elapsed time (in seconds): {elapsed_time}s')

def generateSecondPart6Database():
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
            for k in range(8,13):
                indices.append(next_state.index(k))
            next_state_cost = [next_state, cost]

            
            entry = ",".join(str(t) for t in indices)
            state_entry = ",".join(str(t) for t in next_state)
            result = next((i for i, v in enumerate(entries) if v[0] == entry), None)
            if not state_entry in visited:
                queue.append(next_state_cost)
                if(result==None):
                    entries.add((entry,cost))
                visited.add(state_entry)
        
        # if len(entries) % 10000 == 0:
        #     print("Entries collected: " + str(len(entries)))
        
        if len(entries) >= math.factorial(16)/math.factorial(16-7):
            print("breaking")
            break    
    

    with open("database6_second.txt", "w") as f:
        for entry in sorted(entries, key=lambda c: c[1]):
            json.dump(entry, f)
            f.write("\n")

    elapsed_time = time.time() - start_time
    print("First 6 database generated")
    print(f'elapsed time (in seconds): {elapsed_time}s')


# generatePart3Database()
generateFirstPart6Database()
# generateSecondPart6Database()