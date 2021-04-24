from Puzzle import Puzzle, EightPuzzle
from search import *

import time


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


def calculate_walking_distance(node):
    row_puzzle = WalkingRowDistance8Puzzle(convert_to_walking_row_distance_state(node.state))
    column_puzzle = WalkingColumnDistance8Puzzle(convert_to_walking_column_distance_state(node.state))

    display_walking_distance_state(row_puzzle.initial)
    display_walking_distance_state(column_puzzle.initial)

    print('Calculating row distance...')
    row_distance = len(breadth_first_tree_search(row_puzzle).solution())
    print('row_distance = ', row_distance)

    print('Calculating column distance...')
    column_distance = len(breadth_first_tree_search(column_puzzle).solution())
    print('column_distance = ', column_distance)

    return row_distance + column_distance


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
        blank_col = blank % 3
        new_state = list(state)

        delta = {'UP': -3, 'UP_RIGHT': -2, 'UP_RIGHTMOST': -1, 'UP_LEFT': -4, 'UP_LEFTMOST': -5,
                 'DOWN': 3, 'DOWN_RIGHT': 4, 'DOWN_RIGHTMOST': 5, 'DOWN_LEFT': 2, 'DOWN_LEFTMOST': 1}
        target = blank + delta[action]
        new_state[blank], new_state[target] = new_state[target], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state in self.goal

    # def check_solvability(self, state):
    #     """ Checks if the given state is solvable """
    #
    #     inversion = 0
    #     for i in range(len(state)):
    #         for j in range(i + 1, len(state)):
    #             if (state[i] > state[j]) and state[i] != 0 and state[j] != 0:
    #                 inversion += 1
    #
    #     return inversion % 2 == 0

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
        blank_col = blank % 3
        new_state = list(state)

        delta = {'RIGHT': 1, 'RIGHT_UP': -2, 'RIGHT_UPMOST': -5, 'RIGHT_DOWN': 4, 'RIGHT_DOWNMOST': 7,
                 'LEFT': -1, 'LEFT_UP': -4, 'LEFT_UPMOST': -7, 'LEFT_DOWN': 2, 'LEFT_DOWNMOST': 5}
        target = blank + delta[action]
        new_state[blank], new_state[target] = new_state[target], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state in self.goal

    # def check_solvability(self, state):
    #     """ Checks if the given state is solvable """
    #
    #     inversion = 0
    #     for i in range(len(state)):
    #         for j in range(i + 1, len(state)):
    #             if (state[i] > state[j]) and state[i] != 0 and state[j] != 0:
    #                 inversion += 1
    #
    #     return inversion % 2 == 0

    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is
        h(n) = number of misplaced tiles """

        return sum(s != g for (s, g) in zip(node.state, self.goal))


""" 
                                ---------------------------- 

                        ---------------- Main Program ----------------

                                ----------------------------

"""

if __name__ == "__main__":
    print("It shouldn't get in here!")
    # row_puzzle = WalkingRowDistance8Puzzle(('A', 'C', 'B', 'A', '*', 'A', 'C', 'B', 'B'))
    # display(row_puzzle.initial)

    # col_puzzle = WalkingColumnDistance8Puzzle(('*', 'A', 'C', 'B', 'A', 'C', 'B', 'B', 'A'))
    # display_walking_distance_state(col_puzzle.initial)

    # print("\n\nBFS:")
    # start_time = time.time()
    #
    # sol = breadth_first_tree_search(col_puzzle).solution()
    # print("Solution: ", sol)
    # print("Solution length: ", len(sol))
    #
    # elapsed_time = time.time() - start_time
    # print(f'elapsed time (in seconds): {elapsed_time}s')
