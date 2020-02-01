import numpy as np
import math


# Class the represents a single node in the depth first search. Contains a parent game board plus all possible children
# after one index has been flipped
class Node:
    def __init__(self, game_board, parent_depth):
        self.game_board = game_board
        self.list_of_children = []
        self.depth = parent_depth + 1
        self.str_id = ''

    def add_child(self, game_board):
        self.list_of_children.append(game_board)


# Function that receives concatenated board values from input file and returns a 2d dimensional array based on the
# given dimensions of the board
def build_initial_board(dimension, values):
    split_values = [values[start:start+dimension] for start in range(0, len(values), dimension)]
    board = []
    # TODO Replace this with list comprehension or lambda expression, Compare performance after those changes made
    for concatenated_row in split_values:
        separated_row = []
        for number in concatenated_row:
            separated_row.append(int(number))
        board.append(separated_row)
    return board

def get_id(game_board):
    str_id = ''
    for row in game_board:
        for el in row:
            str_id = str_id + str(el)   
    return str_id  

# Function that will build all the possible variations of a parent game board after exactly one index has been flipped
# each board generated is then stored as a child to the parent node that contains the parent board
def build_boards(parent_node):
    parent_board = parent_node.game_board
    for index, values in np.ndenumerate(parent_board):
        child_board = parent_board.copy()  # .copy() to make an immutable copy as not to affect the parent board
        flip(index[0], index[1], child_board)
        child_node = Node(child_board, parent_node.depth)
        parent_node.add_child(child_node)
    return parent_node.list_of_children

def find_best_board(parent_node):
    best_child = None
    smallest = math.inf
    for child in parent_node.list_of_children:
        first_zero_index = np.where(child == 0)[0][0]
        if first_zero_index < smallest:
            smallest = first_zero_index
            best_child = child
    return best_child


def find_solution(board, max_depth):
    pass


def flip(xCoordinate, yCoordinate, array):

    # flip requested cell
    array[xCoordinate, yCoordinate] = 1 - array[xCoordinate, yCoordinate]

    # flip horizontal neigbours
    if yCoordinate != 0:
        array[xCoordinate, yCoordinate-1] = 1 - array[xCoordinate, yCoordinate-1]
    if len(array[xCoordinate])-1 != yCoordinate:
        array[xCoordinate, yCoordinate+1] = 1 - array[xCoordinate, yCoordinate+1]

    # flip vertical neigbours
    if xCoordinate != 0:
        array[xCoordinate-1, yCoordinate] = 1 - array[xCoordinate-1, yCoordinate]
    if len(array[yCoordinate])-1 != xCoordinate:
        array[xCoordinate+1, yCoordinate] = 1 - array[xCoordinate+1, yCoordinate]


def is_all_zeros(array):
    return np.count_nonzero(array) == 0


def get_answer():
    """Get an answer."""
    return True
