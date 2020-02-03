import numpy as np
import math


def get_id(node):
    str_id = ''
    for row in node.game_board:
        for el in row:
            str_id = str_id + str(el)   
    return str_id  

# Class the represents a single node in the depth first search. Contains a parent game board plus all possible children
# after one index has been flipped
class Node:
    def __init__(self, game_board, parent_depth, parent, clicked_index):
        self.game_board = game_board
        self.list_of_children = []
        self.depth = parent_depth + 1
        self.parent = parent
        self.clicked_index = clicked_index

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


# Function that will build all the possible variations of a parent game board after exactly one index has been flipped
# each board generated is then stored as a child to the parent node that contains the parent board
def build_boards(parent_node):
    parent_board = parent_node.game_board
    for index, values in np.ndenumerate(parent_board):
        board_coordinates = turn_indexes_into_board_coordinates(index)
        child_board = parent_board.copy()  # .copy() to make an immutable copy as not to affect the parent board
        flip(index[0], index[1], child_board)
        child_node = Node(child_board, parent_node.depth, parent_node, board_coordinates)
        parent_node.add_child(child_node)

def turn_indexes_into_board_coordinates(indexes):
    coordinates =""
    if indexes[0]==0:
        coordinates="A"
    if indexes[0]==1:
        coordinates="B"
    if indexes[0]==2:
        coordinates="C"
    if indexes[0]==3:
        coordinates="D"
    if indexes[1]==0:
        coordinates=coordinates+"1"
    if indexes[1]==1:
        coordinates=coordinates+"2"
    if indexes[1]==2:
        coordinates=coordinates+"3"
    if indexes[1]==3:
        coordinates=coordinates+"4"     
    return coordinates

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

#return a board which has 0 at the top left corner
def find_next_board(boards):
    #print("WINNER")
    no = find_next_boards(boards, 0)
    #print(no.game_board)
    return  no

#return an array of boards where 0 is at the leftmost index
def find_next_boards(boards, index_offset):
    if len(boards)==0:
        return None

    #store all boards with 0 in first index from the top left
    winner_boards = []
    #initially start with assuming that 0 is at the very end
    best_index = len(boards[0].game_board.flatten()-1)
  

    for child in boards:
        i = index_offset
        child_board = child.game_board.flatten()

        while i < len(child_board):
            if child_board[i] == 0:
                #we found better index. absolute winner, remove the rest
                if i < best_index:
                    best_index = i
                    winner_boards = []
                    winner_boards.append(child)
                    break
                #we have multiple baords with 0 at same spot
                if i == best_index:
                    winner_boards.append(child)
            i+=1
            
    #none of the boards have any zeros. return whatever was passed
    if(len(winner_boards) == 0):
        return boards[0]        
    #call method recursively with an offset that skips index where we have 0s. We will be able to find next 0
    if len(winner_boards) > 1:
        return find_next_boards(winner_boards, best_index+1)
    else:
        return winner_boards[0]

#look at all the children of node and return next child in the priority that was not yet visited
def get_next_nonvisited_child(node, visited):
    
    next_node = find_next_board(node.list_of_children)
    if next_node is None:
        return None
    next_node_as_single_string = get_id(next_node)
    if next_node_as_single_string in visited:
        node.list_of_children.remove(next_node)
        return get_next_nonvisited_child(node, visited)
    else:
        return next_node
