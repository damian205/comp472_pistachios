import numpy as np
from string import ascii_uppercase
from node import *

INDICES_BOARD = None  # Variable that will contain 2D numpy array corresponding to indices of game board


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
def build_boards(parent_node, search_type):
    parent_board = parent_node.game_board
    for index, values in np.ndenumerate(parent_board):
        child_board = parent_board.copy()  # .copy() to make an immutable copy as not to affect the parent board
        flip(index[0], index[1], child_board)
        index_flipped = INDICES_BOARD[index[0]][index[1]]
        if search_type == "DFS":
            child_priority = find_priority_by_first_zero(child_board, parent_board.shape[0])
            child_node = DfsNode(child_board, parent_node.depth, index_flipped, child_priority)
        elif search_type == "A*":
            child_priority = (parent_node.depth + 1) + find_priority_by_nb_of_ones(child_board)  # i.e. g(n) + h(n)
            child_node = HeuristicNode(child_board, parent_node.depth, index_flipped, child_priority)
        elif search_type == "BFS":
            child_priority = find_priority_by_clusters_of_ones(child_board) #i.e. h(n) 
            child_node =  HeuristicNode(child_board, parent_node.depth, index_flipped, child_priority)
            
#            Below is the reduction matrix by the number of ones, uncommented is another BFS search type.
#        elif search_type =="BFS":
#            child_priority = reduction_matrix_to_nb_of_ones(child_board)
#            child_node =  HeuristicNode(child_board, parent_node.depth, index_flipped, child_priority)
        
        parent_node.add_child(child_node)

#Function that assigns priority to the matrix that has the smallest hamming distance
def reduction_matrix_to_nb_of_ones(game_board, game_board_dimension):
     dimensions = range(1, game_board_dimension + 1)
    game_board_as_string = game_board.flatten()
    index_of_all_ones = np.where(game_board_as_string == 1)[0]
    if len(index_of_all_ones) == 0:
        return 0
    nb_of_ones = index_of_all_ones.shape[0] % dimensions
    return nb_of_ones     
	
# Function that assigns a priority to each game board variation. The priority is represented by a comma-separated
# string whereby each element in the string represents the index in which a "0" value is found. If no "0" value is
# found, then the priority value assigned is the maximum possible index in the game board plus one to make sure this
# board is the least prioritized.
def find_priority_by_first_zero(game_board, game_board_dimension):
    lowest_priority_plus_one = game_board_dimension * game_board_dimension + 1
    game_board_as_string = game_board.flatten()
    index_of_all_zeros = ",".join(str(number) for number in np.where(game_board_as_string == 0)[0])
    if len(index_of_all_zeros) == 0:  # i.e. input was all 1s
        # if all 1s, set priority to max position of a zero + 1
        index_of_all_zeros = f'{lowest_priority_plus_one}'
        return index_of_all_zeros
    index_of_all_zeros = index_of_all_zeros + f',{lowest_priority_plus_one}'
    return index_of_all_zeros


# Function that assigns a priority based on a heuristic that prioritizes a smaller number of 1s on a game_board
def find_priority_by_nb_of_ones(game_board):
    game_board_as_string = game_board.flatten()
    index_of_all_ones = np.where(game_board_as_string == 1)[0]
    if len(index_of_all_ones) == 0:
        return 0
    nb_of_ones = index_of_all_ones.shape[0]
    return nb_of_ones     

# Function that assigns a priority based on a heuristic that:
# Prioritizes boards with smaller number of 1s and larger clusters of 1s together
def find_priority_by_clusters_of_ones(game_board):

    adjusted_nb_of_ones = find_priority_by_nb_of_ones(game_board)
    for i in range(len(game_board)):
        for j in range(len(game_board[i])):
            ones = count_hypothetical_flip(i, j, game_board)
            #when 1s are clustered together, next more will bring us closer to the solution
            if ones == 5 or ones == 4 or ones == 3:
                adjusted_nb_of_ones = adjusted_nb_of_ones -1

    return adjusted_nb_of_ones  

# Check how many lights would go off if given move was made. 
def count_hypothetical_flip(xCoordinate, yCoordinate, array):

    ones = 0
    if array[xCoordinate, yCoordinate] == 1:
        ones = ones + 1
    
    # check horizontal neigbours
    if yCoordinate != 0:
        if array[xCoordinate, yCoordinate-1] == 1:
            ones = ones + 1
        else:
                ones = ones - 1
    
    if len(array[xCoordinate])-1 != yCoordinate:
        if array[xCoordinate, yCoordinate+1] == 1:
            ones = ones + 1
        else:
            ones = ones - 1
    # check vertical neigbours
    if xCoordinate != 0:
        if array[xCoordinate-1, yCoordinate] == 1:
            ones = ones + 1
        else:
            ones = ones - 1        

    if len(array[yCoordinate])-1 != xCoordinate:
        if array[xCoordinate+1, yCoordinate] == 1:
            ones = ones + 1
        else:
            ones = ones - 1
  
    return ones

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
