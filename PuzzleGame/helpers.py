import numpy as np
import math
from string import ascii_uppercase


INDICES_BOARD = None  # Variable that will contain 2D numpy array corresponding to indices of game board


# Class the represents a single node in the depth first search. Contains a parent game board plus all possible children
# after one index has been flipped
class Node:
    def __init__(self, game_board, parent_depth):
        self.game_board = game_board
        self.list_of_children = {}
        self.depth = parent_depth + 1

    def add_child(self, index_coordinates, child_node):
        index_flipped = INDICES_BOARD[index_coordinates[0]][index_coordinates[1]]
        entry = {index_flipped: child_node}
        self.list_of_children.update(entry)  # append(game_board)


# Function that builds a board of indices modeled on the structure of the input board. This board of indices is used
# to show what index has been flipped to produce its corresponding child board.
def build_indices_board(game_board_dimension):
    dimensions = range(1, game_board_dimension + 1)
    list_of_indices = []
    for one_dimension in dimensions:
        list_of_indices.append([ascii_uppercase[one_dimension - 1] + f'{i}' for i in range(1, game_board_dimension+1)])
    global INDICES_BOARD
    INDICES_BOARD = np.array(list_of_indices, dtype=np.str)


# Function that receives concatenated board values from input file and returns a 2d dimensional array based on the
# given dimensions of the board
def build_initial_board(game_board_dimension, values):
    build_indices_board(game_board_dimension)
    split_values = [values[start:start + game_board_dimension] for start in range(0, len(values), game_board_dimension)]
    board = []
    # TODO Replace this with list comprehension or lambda expression, Compare performance after those changes made
    for concatenated_row in split_values:
        separated_row = []
        for number in concatenated_row:
            separated_row.append(int(number))
        board.append(separated_row)
    return board


# Function that will build all the possible variations of a parent game board after exactly one index has been flipped
# each board generated is then stored as a child to the parent node that contains the parent board
def build_boards(parent_node):
    parent_board = parent_node.game_board
    for index, values in np.ndenumerate(parent_board):
        child_board = parent_board.copy()  # .copy() to make an immutable copy as not to affect the parent board
        flip(index[0], index[1], child_board)
        child_node = Node(child_board, parent_node.depth)
        parent_node.add_child(index, child_node)


def find_best_board(parent_node):
    best_child = None
    smallest = math.inf
    for child in parent_node.list_of_children:
        first_zero_index = np.where(child == 0)[0][0]
        if first_zero_index < smallest:
            smallest = first_zero_index
            best_child = child
    return best_child


def save_to_file(list_of_moves, file_name):
    with open(file_name, 'w') as file:
        for a_move in list_of_moves:
            file.write(a_move + "\n")
        file.close()


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
