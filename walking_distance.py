import ast
from itertools import permutations

from Puzzle import Puzzle, EightPuzzle
from search import *


"""

                                    -------------------------------- 

                        ---------------- Generating WD Lookup Table ----------------

                                    --------------------------------

"""


goal_position = {'A': 0, 'B': 1, 'C': 2}

def manhanttan(node):
    total_distance = 0
    for i in range(9):
        tile = node.state[i]
        if (tile != '*'):
            tile_goal_position = goal_position[tile]

            tile_current_column = i % 3
            horizontal_distance = abs(tile_current_column - tile_goal_position)

            tile_current_row = i // 3
            vertical_distance = abs(tile_current_row - tile_goal_position)

            total_distance += horizontal_distance + vertical_distance
    return total_distance


def generate_all_solvable_8puzzles():
    solvable = list()
    states = list(permutations(range(0, 9)))

    for state in states:
        new_puzzle = EightPuzzle(state)
        if new_puzzle.check_solvability(new_puzzle.initial):
            solvable.append(state)

    return solvable


def load_table_from_file(filename):
    with open(filename) as file:
        data = file.read()
    new_dict = ast.literal_eval(data)
    return new_dict


def create_walking_distance_table():
    def write_table_to_file(filename, table):
        try:
            table_file = open(filename, 'wt')
            table_file.write(str(table))
            table_file.close()

        except:
            print("Unable to write table to file")


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

            row_distance = len(astar_search(row_puzzle, manhanttan, False).solution())
            wd_row_table[state] = row_distance

            col_distance = len(astar_search(col_puzzle, manhanttan, False).solution())
            wd_col_table[state] = col_distance

        write_table_to_file(row_filename, wd_row_table)
        write_table_to_file(col_filename, wd_col_table)


    def save_wd_full_table(wd_filename, row_filename, col_filename):
        wd_table = {}
        wd_row_table = load_table_from_file(row_filename)
        wd_col_table = load_table_from_file(col_filename)
        configurations = generate_all_solvable_8puzzles()

        for configuration in configurations:
            row_puzzle = WalkingRowDistance8Puzzle(convert_to_walking_row_distance_state(configuration))
            col_puzzle = WalkingColumnDistance8Puzzle(convert_to_walking_column_distance_state(configuration))

            row_distance = wd_row_table[row_puzzle.initial]
            col_distance = wd_col_table[col_puzzle.initial]
            wd_table[configuration] = row_distance + col_distance

        write_table_to_file(wd_filename, wd_table)

    # body of create_walking_distance_table()
    row_file = 'row_distance_db.txt'
    col_file = 'col_distance_db.txt'
    wd_file = 'walking_distance_db.txt'
    save_wd_row_col_table(row_file, col_file)
    save_wd_full_table(wd_file, row_file, col_file)


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


def convert_to_walking_row_distance_state(state):
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


def convert_to_walking_column_distance_state(state):
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


"""

                                ---------------------------- 

                        ---------------- Row Distance ----------------

                                ----------------------------

"""

row_goals = [('A', 'A', 'A', 'B', 'B', 'B', 'C', 'C', '*'),
             ('A', 'A', 'A', 'B', 'B', 'B', 'C', '*', 'C'),
             ('A', 'A', 'A', 'B', 'B', 'B', '*', 'C', 'C')]


class WalkingRowDistance8Puzzle(Puzzle):
    """ The problem of sliding tiles numbered from 1 to 8 on a 3x3 board, where one of the
    squares is a blank. A state is represented as a tuple of length 9, where  element at
    index i represents the tile number  at index i (0 if it's an empty square) """

    def __init__(self, initial, goal=row_goals):
        """ Define goal state and initialize a problem """
        super().__init__(initial, goal)

    def find_blank_square(self, state):
        """Return the index of the blank square in a given state"""

        return state.index('*')

    def actions(self, state):
        """ Return the actions that can be executed in the given state.
        The result would be a list, since there are only four possible actions
        in any given state of the environment """

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
        Action is assumed to be a valid action in the state """

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
        return True     ## all configurations are solvable

    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is
        h(n) = number of misplaced tiles """

        return sum(s != g for (s, g) in zip(node.state, self.goal))


"""

                                ---------------------------- 

                        ---------------- Column Distance ----------------

                                ----------------------------
                                
"""

col_goals = [('A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', '*'),
             ('A', 'B', 'C', 'A', 'B', '*', 'A', 'B', 'C'),
             ('A', 'B', '*', 'A', 'B', 'C', 'A', 'B', 'C')]


class WalkingColumnDistance8Puzzle(Puzzle):
    """ The problem of sliding tiles numbered from 1 to 8 on a 3x3 board, where one of the
    squares is a blank. A state is represented as a tuple of length 9, where  element at
    index i represents the tile number  at index i (0 if it's an empty square) """

    def __init__(self, initial, goal=col_goals):
        """ Define goal state and initialize a problem """
        super().__init__(initial, goal)

    def find_blank_square(self, state):
        """Return the index of the blank square in a given state"""

        return state.index('*')

    def actions(self, state):
        """ Return the actions that can be executed in the given state.
        The result would be a list, since there are only four possible actions
        in any given state of the environment """

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
        Action is assumed to be a valid action in the state """

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
        return True     ## all configurations are solvable

    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is
        h(n) = number of misplaced tiles """

        return sum(s != g for (s, g) in zip(node.state, self.goal))
