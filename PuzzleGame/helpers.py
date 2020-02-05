import numpy as np
from string import ascii_uppercase


INDICES_BOARD = None  # Variable that will contain 2D numpy array corresponding to indices of game board


# Class the represents a single node in the depth first search. Contains a parent game board plus all possible children
# after one index has been flipped
class Node:
    def __init__(self, game_board, parent_depth, index, priority):
        self.game_board = game_board
        self.list_of_children = []
        self.depth = parent_depth + 1
        self.index = index
        self.priority = priority

    def __eq__(self, other):
        for self_index, other_index in zip(self.priority.split(','), other.priority.split(',')):
            if int(self_index) < int(other_index):
                return False
            elif int(self_index) > int(other_index):
                return False
        return True

    def __lt__(self, other):
        for self_index, other_index in zip(self.priority.split(','), other.priority.split(',')):
            if int(self_index) < int(other_index):
                return True
            elif int(self_index) > int(other_index):
                return False
        return False

    def __gt__(self, other):
        for self_index, other_index in zip(self.priority.split(','), other.priority.split(',')):
            if int(self_index) > int(other_index):
                return True
            elif int(self_index) < int(other_index):
                return False
        return False

    def add_child(self, child_node):
        self.list_of_children.append(child_node)  # append(game_board)


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


# TODO Lump index calculation, priority calculation into one function and call that instead of doing all in
# below function
# Function that will build all the possible variations of a parent game board after exactly one index has been flipped
# each board generated is then stored as a child to the parent node that contains the parent board
def build_boards(parent_node):
    parent_board = parent_node.game_board
    for index, values in np.ndenumerate(parent_board):
        child_board = parent_board.copy()  # .copy() to make an immutable copy as not to affect the parent board
        flip(index[0], index[1], child_board)
        index_flipped = INDICES_BOARD[index[0]][index[1]]
        child_priority = find_priority(child_board, parent_board.shape[0])
        child_node = Node(child_board, parent_node.depth, index_flipped, child_priority)
        parent_node.add_child(child_node)
    # parent_node.list_of_children.sort()


# Function that assigns a priority to each game board variation. The priority is represented by a comma-separated
# string whereby each element in the string represents the index in which a "0" value is found. If no "0" value is
# found, then the priority value assigned is the maximum possible index in the game board plus one to make sure this
# board is the least prioritized.
def find_priority(game_board, game_board_dimension):
    lowest_priority_plus_one = game_board_dimension * game_board_dimension + 1
    game_board_as_string = game_board.flatten()
    index_of_all_zeros = ",".join(str(number) for number in np.where(game_board_as_string == 0)[0])
    if len(index_of_all_zeros) == 0:  # i.e. input was all 1s
        # if all 1s, set priority to max position of a zero + 1
        index_of_all_zeros = f'{lowest_priority_plus_one}'
        return index_of_all_zeros
    index_of_all_zeros = index_of_all_zeros + f',{lowest_priority_plus_one}'
    return index_of_all_zeros


# Function that saves the passed list of moves to a file with the name matching the parameter "file_name"
def save_to_file(list_of_moves, file_name):
    with open(file_name, 'w') as file:
        for a_move in list_of_moves:
            file.write(a_move + "\n")
        file.close()


# Function that will flip (0 -> 1 or 1 -> 0) of the index indicated, along with all its adjacent neighbors
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


# Function that determines whether the game board examined is the goal state(i.e. all elements in array are 0)
def is_all_zeros(array):
    return np.count_nonzero(array) == 0
