import ast
from collections import Counter
from itertools import permutations
from typing import List

from Puzzle import Puzzle, EightPuzzle, FifteenPuzzle
from search import *

"""

                                    -------------------------------- 

                        ---------------- Generating WD Lookup Table ----------------

                                    --------------------------------

"""


def load_table_from_file(filename):
    with open(filename) as file:
        data = file.read()
    new_dict = ast.literal_eval(data)
    return new_dict


def write_table_to_file(filename, table):
    try:
        table_file = open(filename, 'wt')
        table_file.write(str(table))
        table_file.close()

    except:
        print("Unable to write table to file")


'''     -------------------- Generating WD Lookup Table For 8-Puzzle --------------------   '''


goal_position_8 = {'A': 0, 'B': 1, 'C': 2}


def manhanttan_row_8(node):
    total_distance = 0
    for i in range(9):
        tile = node.state[i]
        if (tile != '*'):
            tile_goal_row = goal_position_8[tile]

            tile_current_row = i // 3
            vertical_distance = abs(tile_current_row - tile_goal_row)

            total_distance += vertical_distance
    return total_distance


def manhanttan_col_8(node):
    total_distance = 0
    for i in range(9):
        tile = node.state[i]
        if (tile != '*'):
            tile_goal_column = goal_position_8[tile]

            tile_current_column = i % 3
            horizontal_distance = abs(tile_current_column - tile_goal_column)

            total_distance += horizontal_distance
    return total_distance


def generate_all_solvable_8puzzles():
    solvable = list()
    states = list(permutations(range(0, 9)))

    for state in states:
        new_puzzle = EightPuzzle(state)
        if new_puzzle.check_solvability(new_puzzle.initial):
            solvable.append(state)

    return solvable


def create_8puzzle_walking_distance_table():
    def save_wd_row_col_table(row_filename, col_filename):
        states = list(set(permutations(['A', 'A', 'A', 'B', 'B', 'B', 'C', 'C', '*'])))
        wd_row_table = {}
        wd_col_table = {}

        for state in states:
            # print('Processing state ', states.index(state))
            row_puzzle = WalkingRowDistance8Puzzle(state)
            col_puzzle = WalkingColumnDistance8Puzzle(state)
            # display_walking_distance_state(row_puzzle.initial)
            # display_walking_distance_state(col_puzzle.initial)

            row_distance = len(astar_search(row_puzzle, manhanttan_row_8, False).solution())
            wd_row_table[state] = row_distance

            col_distance = len(astar_search(col_puzzle, manhanttan_col_8, False).solution())
            wd_col_table[state] = col_distance

        write_table_to_file(row_filename, wd_row_table)
        write_table_to_file(col_filename, wd_col_table)

    def save_wd_full_table(wd_filename, row_filename, col_filename):
        wd_table = {}
        wd_row_table = load_table_from_file(row_filename)
        wd_col_table = load_table_from_file(col_filename)
        configurations = generate_all_solvable_8puzzles()

        for configuration in configurations:
            row_puzzle = WalkingRowDistance8Puzzle(convert_to_8puzzle_row_distance_state(configuration))
            col_puzzle = WalkingColumnDistance8Puzzle(convert_to_8puzzle_column_distance_state(configuration))

            row_distance = wd_row_table[row_puzzle.initial]
            col_distance = wd_col_table[col_puzzle.initial]
            wd_table[configuration] = row_distance + col_distance

        write_table_to_file(wd_filename, wd_table)

    # body of create_walking_distance_table()
    row_file = 'walking_dist/row_distance_db_8puzzle.txt'
    col_file = 'walking_dist/col_distance_db_8puzzle.txt'
    wd_file = 'walking_dist/walking_distance_db_8puzzle.txt'
    save_wd_row_col_table(row_file, col_file)
    save_wd_full_table(wd_file, row_file, col_file)


'''     -------------------- Generating WD Lookup Table For 15-Puzzle --------------------   '''

goal_position_15 = {'A': 0, 'B': 1, 'C': 2, 'D': 3}


def manhanttan_row_15(node):
    total_distance = 0
    for i in range(16):
        tile = node.state[i]
        if (tile != '*'):
            tile_goal_row = goal_position_15[tile]

            tile_current_row = i // 4
            vertical_distance = abs(tile_current_row - tile_goal_row)

            total_distance += vertical_distance
    return total_distance


def manhanttan_col_15(node):
    total_distance = 0
    for i in range(16):
        tile = node.state[i]
        if (tile != '*'):
            tile_goal_column = goal_position_15[tile]

            tile_current_column = i % 4
            horizontal_distance = abs(tile_current_column - tile_goal_column)

            total_distance += horizontal_distance
    return total_distance


def generate_all_solvable_15puzzles():
    solvable = list()
    states = list(permutations(range(0, 16)))

    for state in states:
        new_puzzle = FifteenPuzzle(state)
        if new_puzzle.check_solvability(new_puzzle.initial):
            solvable.append(state)

    return solvable


def create_15puzzle_walking_distance_table():
    def generate_unique_permutations(nums: List[int]) -> List[List[int]]:
        results = []

        def backtrack(comb, counter):
            if len(comb) == len(nums):
                # make a deep copy of the resulting permutation,
                # since the permutation would be backtracked later.
                results.append(tuple(comb))
                print(results)
                print()
                return

            for num in counter:
                if counter[num] > 0:
                    # add this number into the current combination
                    if num == 1:
                        comb.append('A')
                    elif num == 2:
                        comb.append('B')
                    elif num == 3:
                        comb.append('C')
                    elif num == 4:
                        comb.append('D')
                    else:
                        comb.append('*')
                    counter[num] -= 1
                    # continue the exploration
                    backtrack(comb, counter)
                    # revert the choice for the next exploration
                    comb.pop()
                    counter[num] += 1

        backtrack([], Counter(nums))

        return results


    def save_wd_row_col_table(row_filename, col_filename):
        states = generate_unique_permutations([1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 0])
        wd_row_table = {}
        wd_col_table = {}

        for state in states:
            # print('Processing state ', states.index(state))
            row_puzzle = WalkingRowDistance15Puzzle(state)
            col_puzzle = WalkingColumnDistance15Puzzle(state)
            # display_walking_distance_state(row_puzzle.initial)
            # display_walking_distance_state(col_puzzle.initial)

            row_distance = len(astar_search(row_puzzle, manhanttan_row_15, False).solution())
            wd_row_table[state] = row_distance

            col_distance = len(astar_search(col_puzzle, manhanttan_col_15, False).solution())
            wd_col_table[state] = col_distance

        write_table_to_file(row_filename, wd_row_table)
        write_table_to_file(col_filename, wd_col_table)


    def save_wd_full_table(wd_filename, row_filename, col_filename):
        wd_table = {}
        wd_row_table = load_table_from_file(row_filename)
        wd_col_table = load_table_from_file(col_filename)
        configurations = generate_all_solvable_15puzzles()

        for configuration in configurations:
            row_puzzle = WalkingRowDistance15Puzzle(convert_to_15puzzle_row_distance_state(configuration))
            col_puzzle = WalkingColumnDistance15Puzzle(convert_to_15puzzle_column_distance_state(configuration))

            row_distance = wd_row_table[row_puzzle.initial]
            col_distance = wd_col_table[col_puzzle.initial]
            wd_table[configuration] = row_distance + col_distance

        write_table_to_file(wd_filename, wd_table)

    # body of create_walking_distance_table()
    row_file = 'row_distance_db_15puzzle.txt'
    col_file = 'col_distance_db_15puzzle.txt'
    # wd_file = 'walking_distance_db_15puzzle.txt'
    save_wd_row_col_table(row_file, col_file)
    # save_wd_full_table(wd_file, row_file, col_file)


"""
 
                                    -------------------------------- 

                        ---------------- Utils/Helper Functions For Puzzles ----------------

                                    --------------------------------

"""


def display_walking_distance_state(state):
    count = 0
    for tile in state:
        print(tile, end=" ")
        count += 1
        if count % 3 == 0:
            print(end="\n")
    print()


def convert_to_8puzzle_row_distance_state(state):
    new_state = list()
    for tile in state:
        if tile != 0:
            if (tile - 1) // 3 == 0:
                new_state.append('A')
            elif (tile - 1) // 3 == 1:
                new_state.append('B')
            else:
                new_state.append('C')
        else:
            new_state.append('*')
    return tuple(new_state)


def convert_to_8puzzle_column_distance_state(state):
    new_state = list()
    for tile in state:
        if tile != 0:
            if tile % 3 == 1:
                new_state.append('A')
            elif tile % 3 == 2:
                new_state.append('B')
            else:
                new_state.append('C')
        else:
            new_state.append('*')
    return tuple(new_state)


def convert_to_15puzzle_row_distance_state(state):
    new_state = list()
    for tile in state:
        if tile != 0:
            if (tile - 1) // 4 == 0:
                new_state.append('A')
            elif (tile - 1) // 4 == 1:
                new_state.append('B')
            elif (tile-1) // 4 == 2:
                new_state.append('C')
            else:
                new_state.append('D')
        else:
            new_state.append('*')
    return tuple(new_state)


def convert_to_15puzzle_column_distance_state(state):
    new_state = list()
    for tile in state:
        if tile != 0:
            if tile % 4 == 1:
                new_state.append('A')
            elif tile % 4 == 2:
                new_state.append('B')
            elif tile % 4 == 3:
                new_state.append('C')
            else:
                new_state.append('D')
        else:
            new_state.append('*')
    return tuple(new_state)


"""

                                ---------------------------- 

                ---------------- Row Distance For 8-Puzzle ----------------

                                ----------------------------

"""

row_goals_8 = [('A', 'A', 'A', 'B', 'B', 'B', 'C', 'C', '*'),
               ('A', 'A', 'A', 'B', 'B', 'B', 'C', '*', 'C'),
               ('A', 'A', 'A', 'B', 'B', 'B', '*', 'C', 'C')]


class WalkingRowDistance8Puzzle(Puzzle):
    """ The problem of sliding tiles on a 3x3 board, where one of the squares is a blank.
    A state is the collapsed row version of a 8-puzzle configuration, represented as a tuple of length 9,
    where element is A, B or C, where A, B and C represent the tiles at ROW 1, ROW 2 and ROW 3 respectively
    in the goal state of 8-puzzle (* if it's an empty square, i.e. tile 0 in 8-puzzle) """

    def __init__(self, initial, goal=row_goals_8):
        """ Define goal state and initialize a problem """
        super().__init__(initial, goal)

    def find_blank_square(self, state):
        """Return the index of the blank square in a given state"""
        return state.index('*')

    def actions(self, state):
        """ Return the actions that can be executed in the given state.
        The result would be a list."""

        possible_actions = ['UP', 'UP_RIGHT', 'UP_RIGHTMOST', 'UP_LEFT', 'UP_LEFTMOST',
                            'DOWN', 'DOWN_RIGHT', 'DOWN_RIGHTMOST', 'DOWN_LEFT', 'DOWN_LEFTMOST']
        index_blank_square = self.find_blank_square(state)

        if index_blank_square < 3:
            possible_actions.remove('UP')
            possible_actions.remove('UP_RIGHT')
            possible_actions.remove('UP_RIGHTMOST')
            possible_actions.remove('UP_LEFT')
            possible_actions.remove('UP_LEFTMOST')

        if index_blank_square > 5:
            possible_actions.remove('DOWN')
            possible_actions.remove('DOWN_RIGHT')
            possible_actions.remove('DOWN_RIGHTMOST')
            possible_actions.remove('DOWN_LEFT')
            possible_actions.remove('DOWN_LEFTMOST')

        if index_blank_square % 3 == 0:
            if index_blank_square >= 3:
                possible_actions.remove('UP_LEFT')
                possible_actions.remove('UP_LEFTMOST')
            if index_blank_square <= 5:
                possible_actions.remove('DOWN_LEFT')
                possible_actions.remove('DOWN_LEFTMOST')

        if index_blank_square % 3 == 1:
            if index_blank_square >= 3:
                possible_actions.remove('UP_RIGHTMOST')
                possible_actions.remove('UP_LEFTMOST')
            if index_blank_square <= 5:
                possible_actions.remove('DOWN_RIGHTMOST')
                possible_actions.remove('DOWN_LEFTMOST')

        if index_blank_square % 3 == 2:
            if index_blank_square >= 3:
                possible_actions.remove('UP_RIGHT')
                possible_actions.remove('UP_RIGHTMOST')
            if index_blank_square <= 5:
                possible_actions.remove('DOWN_RIGHT')
                possible_actions.remove('DOWN_RIGHTMOST')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state. """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        delta = {'UP': -3, 'UP_RIGHT': -2, 'UP_RIGHTMOST': -1, 'UP_LEFT': -4, 'UP_LEFTMOST': -5,
                 'DOWN': 3, 'DOWN_RIGHT': 4, 'DOWN_RIGHTMOST': 5, 'DOWN_LEFT': 2, 'DOWN_LEFTMOST': 1}
        target = blank + delta[action]
        new_state[blank], new_state[target] = new_state[target], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state in self.goal

    def check_solvability(self, state):
        return True  ## all configurations are solvable

    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is
        h(n) = number of misplaced tiles """

        return sum(s != g for (s, g) in zip(node.state, self.goal))


"""

                                ---------------------------- 

                ---------------- Column Distance For 8-Puzzle ----------------

                                ----------------------------
                                
"""

col_goals_8 = [('A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', '*'),
             ('A', 'B', 'C', 'A', 'B', '*', 'A', 'B', 'C'),
             ('A', 'B', '*', 'A', 'B', 'C', 'A', 'B', 'C')]


class WalkingColumnDistance8Puzzle(Puzzle):
    """ The problem of sliding tiles on a 3x3 board, where one of the squares is a blank.
    A state is the collapsed row version of a 8-puzzle configuration, represented as a tuple of length 9,
    where element is A, B or C, where A, B and C represent the tiles at COLUMN 1, COLUMN 2 and COLUMN 3 respectively
    in the goal state of 8-puzzle (* if it's an empty square, i.e. tile 0 in 8-puzzle) """

    def __init__(self, initial, goal=col_goals_8):
        """ Define goal state and initialize a problem """
        super().__init__(initial, goal)

    def find_blank_square(self, state):
        """Return the index of the blank square in a given state"""
        return state.index('*')

    def actions(self, state):
        """ Return the actions that can be executed in the given state.
        The result would be a list. """

        possible_actions = ['RIGHT', 'RIGHT_UP', 'RIGHT_UPMOST', 'RIGHT_DOWN', 'RIGHT_DOWNMOST',
                            'LEFT', 'LEFT_UP', 'LEFT_UPMOST', 'LEFT_DOWN', 'LEFT_DOWNMOST']
        index_blank_square = self.find_blank_square(state)

        if index_blank_square % 3 == 0:
            possible_actions.remove('LEFT')
            possible_actions.remove('LEFT_UP')
            possible_actions.remove('LEFT_UPMOST')
            possible_actions.remove('LEFT_DOWN')
            possible_actions.remove('LEFT_DOWNMOST')

        if index_blank_square % 3 == 2:
            possible_actions.remove('RIGHT')
            possible_actions.remove('RIGHT_UP')
            possible_actions.remove('RIGHT_UPMOST')
            possible_actions.remove('RIGHT_DOWN')
            possible_actions.remove('RIGHT_DOWNMOST')

        if index_blank_square < 3:
            if index_blank_square % 3 != 0:
                possible_actions.remove('LEFT_UP')
                possible_actions.remove('LEFT_UPMOST')
            if index_blank_square % 3 != 2:
                possible_actions.remove('RIGHT_UP')
                possible_actions.remove('RIGHT_UPMOST')

        if 3 <= index_blank_square <= 5:
            if index_blank_square % 3 != 0:
                possible_actions.remove('LEFT_DOWNMOST')
                possible_actions.remove('LEFT_UPMOST')
            if index_blank_square % 3 != 2:
                possible_actions.remove('RIGHT_DOWNMOST')
                possible_actions.remove('RIGHT_UPMOST')

        if index_blank_square > 5:
            if index_blank_square % 3 != 0:
                possible_actions.remove('LEFT_DOWN')
                possible_actions.remove('LEFT_DOWNMOST')
            if index_blank_square % 3 != 2:
                possible_actions.remove('RIGHT_DOWN')
                possible_actions.remove('RIGHT_DOWNMOST')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state. """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        delta = {'RIGHT': 1, 'RIGHT_UP': -2, 'RIGHT_UPMOST': -5, 'RIGHT_DOWN': 4, 'RIGHT_DOWNMOST': 7,
                 'LEFT': -1, 'LEFT_UP': -4, 'LEFT_UPMOST': -7, 'LEFT_DOWN': 2, 'LEFT_DOWNMOST': 5}
        target = blank + delta[action]
        new_state[blank], new_state[target] = new_state[target], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """
        return state in self.goal

    def check_solvability(self, state):
        return True  ## all configurations are solvable

    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is
        h(n) = number of misplaced tiles """

        return sum(s != g for (s, g) in zip(node.state, self.goal))


"""

                                ---------------------------- 

                ---------------- Row Distance For 15-Puzzle ----------------

                                ----------------------------

"""

row_goals_15 = [('A', 'A', 'A', 'A', 'B', 'B', 'B', 'B', 'C', 'C', 'C', 'C', 'D', 'D', 'D', '*'),
                ('A', 'A', 'A', 'A', 'B', 'B', 'B', 'B', 'C', 'C', 'C', 'C', 'D', 'D', '*', 'D'),
                ('A', 'A', 'A', 'A', 'B', 'B', 'B', 'B', 'C', 'C', 'C', 'C', 'D', '*', 'D', 'D'),
                ('A', 'A', 'A', 'A', 'B', 'B', 'B', 'B', 'C', 'C', 'C', 'C', '*', 'D', 'D', 'D')]


class WalkingRowDistance15Puzzle(Puzzle):
    """ The problem of sliding tiles on a 4x4 board, where one of the squares is a blank.
    A state is the collapsed row version of a 15-puzzle configuration, represented as a tuple of length 16,
    where element is A, B, C or D, where A, B, C and D represent the tiles at ROW 1, ROW 2, ROW 3 and ROW 4
    respectively in the goal state of 15-puzzle (* if it's an empty square, i.e. tile 0 in 15-puzzle) """

    def __init__(self, initial, goal=row_goals_15):
        """ Define goal state and initialize a problem """
        super().__init__(initial, goal)

    def find_blank_square(self, state):
        """Return the index of the blank square in a given state"""
        return state.index('*')

    def actions(self, state):
        """ Return the actions that can be executed in the given state.
        The result would be a list."""

        possible_actions = ['UP', 'UP_RIGHT', 'UP_DOUBLE_RIGHT', 'UP_RIGHTMOST', 'UP_LEFT', 'UP_DOUBLE_LEFT', 'UP_LEFTMOST',
                            'DOWN', 'DOWN_RIGHT', 'DOWN_DOUBLE_RIGHT', 'DOWN_RIGHTMOST', 'DOWN_LEFT', 'DOWN_DOUBLE_LEFT', 'DOWN_LEFTMOST']
        index_blank_square = self.find_blank_square(state)

        if index_blank_square < 4:
            possible_actions.remove('UP')
            possible_actions.remove('UP_RIGHT')
            possible_actions.remove('UP_DOUBLE_RIGHT')
            possible_actions.remove('UP_RIGHTMOST')
            possible_actions.remove('UP_LEFT')
            possible_actions.remove('UP_DOUBLE_LEFT')
            possible_actions.remove('UP_LEFTMOST')

        if index_blank_square > 11:
            possible_actions.remove('DOWN')
            possible_actions.remove('DOWN_RIGHT')
            possible_actions.remove('DOWN_DOUBLE_RIGHT')
            possible_actions.remove('DOWN_RIGHTMOST')
            possible_actions.remove('DOWN_LEFT')
            possible_actions.remove('DOWN_DOUBLE_LEFT')
            possible_actions.remove('DOWN_LEFTMOST')

        if index_blank_square % 4 == 0:
            if index_blank_square >= 4:
                possible_actions.remove('UP_LEFT')
                possible_actions.remove('UP_DOUBLE_LEFT')
                possible_actions.remove('UP_LEFTMOST')
            if index_blank_square <= 11:
                possible_actions.remove('DOWN_LEFT')
                possible_actions.remove('DOWN_DOUBLE_LEFT')
                possible_actions.remove('DOWN_LEFTMOST')

        if index_blank_square % 4 == 1:
            if index_blank_square >= 4:
                possible_actions.remove('UP_RIGHTMOST')
                possible_actions.remove('UP_DOUBLE_LEFT')
                possible_actions.remove('UP_LEFTMOST')
            if index_blank_square <= 11:
                possible_actions.remove('DOWN_RIGHTMOST')
                possible_actions.remove('DOWN_DOUBLE_LEFT')
                possible_actions.remove('DOWN_LEFTMOST')

        if index_blank_square % 4 == 2:
            if index_blank_square >= 4:
                possible_actions.remove('UP_DOUBLE_RIGHT')
                possible_actions.remove('UP_RIGHTMOST')
                possible_actions.remove('UP_LEFTMOST')
            if index_blank_square <= 11:
                possible_actions.remove('DOWN_DOUBLE_RIGHT')
                possible_actions.remove('DOWN_RIGHTMOST')
                possible_actions.remove('DOWN_LEFTMOST')

        if index_blank_square % 4 == 3:
            if index_blank_square >= 4:
                possible_actions.remove('UP_RIGHT')
                possible_actions.remove('UP_DOUBLE_RIGHT')
                possible_actions.remove('UP_RIGHTMOST')
            if index_blank_square <= 11:
                possible_actions.remove('DOWN_RIGHT')
                possible_actions.remove('DOWN_DOUBLE_RIGHT')
                possible_actions.remove('DOWN_RIGHTMOST')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state. """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        delta = {'UP': -4, 'UP_RIGHT': -3, 'UP_DOUBLE_RIGHT': -2, 'UP_RIGHTMOST': -1, 'UP_LEFT': -5, 'UP_DOUBLE_LEFT': -6, 'UP_LEFTMOST': -7,
                'DOWN': 4, 'DOWN_RIGHT': 5,'DOWN_DOUBLE_RIGHT': 6, 'DOWN_RIGHTMOST': 7, 'DOWN_LEFT': 3, 'DOWN_DOUBLE_LEFT': 2, 'DOWN_LEFTMOST': 1}
        target = blank + delta[action]
        new_state[blank], new_state[target] = new_state[target], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state in self.goal

    # def check_solvability(self, state):
    #     return True  ## all configurations are solvable

    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is
        h(n) = number of misplaced tiles """

        return sum(s != g for (s, g) in zip(node.state, self.goal))


"""

                                ---------------------------- 

                ---------------- Column Distance For 15-Puzzle ----------------

                                ----------------------------

"""


col_goals_15 = [('A', 'B', 'C', 'D', 'A', 'B', 'C', 'D', 'A', 'B', 'C', 'D', 'A', 'B', 'C', '*'),
                ('A', 'B', 'C', 'D', 'A', 'B', 'C', 'D', 'A', 'B', 'C', '*', 'A', 'B', 'C', 'D'),
                ('A', 'B', 'C', 'D', 'A', 'B', 'C', '*', 'A', 'B', 'C', 'D', 'A', 'B', 'C', 'D'),
                ('A', 'B', 'C', '*', 'A', 'B', 'C', 'D', 'A', 'B', 'C', 'D', 'A', 'B', 'C', 'D')]


class WalkingColumnDistance15Puzzle(Puzzle):
    """ The problem of sliding tiles on a 4x4 board, where one of the squares is a blank.
    A state is the collapsed row version of a 15-puzzle configuration, represented as a tuple of length 16,
    where element is A, B, C or D, where A, B, C and D represent the tiles at COLUMN 1, COLUMN 2, COLUMN 3
    and COLUMN 4 respectively in the goal state of 15-puzzle (* if it's an empty square, i.e. tile 0 in 15-puzzle) """

    def __init__(self, initial, goal=col_goals_15):
        """ Define goal state and initialize a problem """
        super().__init__(initial, goal)

    def find_blank_square(self, state):
        """Return the index of the blank square in a given state"""
        return state.index('*')

    def actions(self, state):
        """ Return the actions that can be executed in the given state.
        The result would be a list."""

        possible_actions = ['RIGHT', 'RIGHT_UP', 'RIGHT_DOUBLE_UP', 'RIGHT_UPMOST', 'RIGHT_DOWN', 'RIGHT_DOUBLE_DOWN', 'RIGHT_DOWNMOST',
                            'LEFT', 'LEFT_UP', 'LEFT_DOUBLE_UP', 'LEFT_UPMOST', 'LEFT_DOWN', 'LEFT_DOUBLE_DOWN', 'LEFT_DOWNMOST']
        index_blank_square = self.find_blank_square(state)

        if index_blank_square % 4 == 0:
            possible_actions.remove('LEFT')
            possible_actions.remove('LEFT_UP')
            possible_actions.remove('LEFT_DOUBLE_UP')
            possible_actions.remove('LEFT_UPMOST')
            possible_actions.remove('LEFT_DOWN')
            possible_actions.remove('LEFT_DOUBLE_DOWN')
            possible_actions.remove('LEFT_DOWNMOST')

        if index_blank_square % 4 == 3:
            possible_actions.remove('RIGHT')
            possible_actions.remove('RIGHT_UP')
            possible_actions.remove('RIGHT_DOUBLE_UP')
            possible_actions.remove('RIGHT_UPMOST')
            possible_actions.remove('RIGHT_DOWN')
            possible_actions.remove('RIGHT_DOUBLE_DOWN')
            possible_actions.remove('RIGHT_DOWNMOST')

        if index_blank_square < 4:
            if index_blank_square % 4 != 0:
                possible_actions.remove('LEFT_UP')
                possible_actions.remove('LEFT_DOUBLE_UP')
                possible_actions.remove('LEFT_UPMOST')
            if index_blank_square % 4 != 3:
                possible_actions.remove('RIGHT_UP')
                possible_actions.remove('RIGHT_DOUBLE_UP')
                possible_actions.remove('RIGHT_UPMOST')

        if 4 <= index_blank_square <= 7:
            if index_blank_square % 4 != 0:
                possible_actions.remove('LEFT_DOWNMOST')
                possible_actions.remove('LEFT_DOUBLE_UP')
                possible_actions.remove('LEFT_UPMOST')
            if index_blank_square % 4 != 3:
                possible_actions.remove('RIGHT_DOWNMOST')
                possible_actions.remove('RIGHT_DOUBLE_UP')
                possible_actions.remove('RIGHT_UPMOST')

        if 8 <= index_blank_square <= 11:
            if index_blank_square % 4 != 0:
                possible_actions.remove('LEFT_DOUBLE_DOWN')
                possible_actions.remove('LEFT_DOWNMOST')
                possible_actions.remove('LEFT_UPMOST')
            if index_blank_square % 4 != 3:
                possible_actions.remove('RIGHT_DOUBLE_DOWN')
                possible_actions.remove('RIGHT_DOWNMOST')
                possible_actions.remove('RIGHT_UPMOST')

        if index_blank_square > 11:
            if index_blank_square % 4 != 0:
                possible_actions.remove('LEFT_DOWN')
                possible_actions.remove('LEFT_DOUBLE_DOWN')
                possible_actions.remove('LEFT_DOWNMOST')
            if index_blank_square % 4 != 3:
                possible_actions.remove('RIGHT_DOWN')
                possible_actions.remove('RIGHT_DOUBLE_DOWN')
                possible_actions.remove('RIGHT_DOWNMOST')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state. """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        delta = {'RIGHT': 1, 'RIGHT_UP': 3, 'RIGHT_DOUBLE_UP': 7, 'RIGHT_UPMOST': 11, 'RIGHT_DOWN': 5, 'RIGHT_DOUBLE_DOWN': 9, 'RIGHT_DOWNMOST': 13,
                 'LEFT': -1, 'LEFT_UP': -5, 'LEFT_DOUBLE_UP': -9, 'LEFT_UPMOST': -13, 'LEFT_DOWN': 3, 'LEFT_DOUBLE_DOWN': 7, 'LEFT_DOWNMOST': 11}
        target = blank + delta[action]
        new_state[blank], new_state[target] = new_state[target], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state in self.goal

    # def check_solvability(self, state):
    #     return True  ## all configurations are solvable

    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is
        h(n) = number of misplaced tiles """

        return sum(s != g for (s, g) in zip(node.state, self.goal))