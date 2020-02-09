import numpy as np
from helpers import build_initial_board, build_boards, Node, Slow_Node, is_all_zeros, save_to_file, get_next_nonvisited_child, get_id, slow_build_boards

list_of_solution_moves = []  # Must be reset after every input puzzle
list_of_search_moves = []  # Ditto

def main():
    with open('PuzzleGame\one_input') as input_file:
        i = 0
        for line in input_file.readlines():
            puzzle_dimension, max_depth, max_search_path, values = line.split()
            root_board = np.array(build_initial_board(int(puzzle_dimension), values), np.int32)
            root_node = Node(root_board, 0, 0, 0)
            build_boards(root_node)
            start_dfs(root_node, max_depth)
            save_to_file(list_of_solution_moves, f'{i}_dfs_solution.txt')
            save_to_file(list_of_search_moves, f'{i}_dfs_search.txt')
            i += 1
            clean_up()

    #other solution for DFS that is 50% slower than above
    # with open('PuzzleGame\one_input') as input_file:    
    #     i = 0
    #     for line in input_file.readlines():
    #         puzzle_dimension, max_depth, max_search_path, values = line.split()
    #         root_board = np.array(build_initial_board(int(puzzle_dimension), values), np.int32)
    #         root_node = Slow_Node(root_board, 0, None, "0")
    #         start_slow_dfs(root_node, max_depth)
    #         save_to_file(list_of_solution_moves, f'{i}_slow_dfs_solution.txt')
    #         save_to_file(list_of_search_moves, f'{i}_slow_dfs_search.txt')
    #         i += 1
    #         clean_up()
            


def start_dfs(node, max_depth):
    visited = []
    starting_board_as_single_string = "".join(str(number) for number in node.game_board.flatten())
    list_of_search_moves.append(f'0  {starting_board_as_single_string}')
    if dfs(node, visited, int(max_depth)):
        list_of_solution_moves.append(f'{0}  {starting_board_as_single_string}')
        list_of_solution_moves.reverse()
    else:
        list_of_solution_moves.append('No Solution')


def dfs(node, visited_nodes, max_depth):
    board_as_single_string = ["".join(str(number) for number in node.game_board.flatten())]
    # check to see if board of the same values has been visited before
    if len(set(board_as_single_string).intersection(set(visited_nodes))) != 0:
        return False
    visited_nodes.append(board_as_single_string[0])
    # check if node is goal node
    if is_all_zeros(node.game_board):
        return True
    if node.depth == max_depth:
        return False
    build_boards(node)
    for child in node.list_of_children:
        child_board_as_single_string = "".join(str(number) for number in child.game_board.flatten())
        list_of_search_moves.append(f'{child.index} {child_board_as_single_string}')
        if dfs(child, visited_nodes, max_depth) is True:
            global list_of_solution_moves
            list_of_solution_moves.append(f'{child.index} {child_board_as_single_string}')
            return True
    return False


def clean_up():
    list_of_solution_moves.clear()
    list_of_search_moves.clear()


######################################################################################################
#another approach to DFS algorithm starts here. This is not part of final solution but an experiment. 
#Run this code by uncommenting test block in main method
######################################################################################################

def start_slow_dfs(node, max_depth):
    visited = []
    if slow_dfs(node, visited, int(max_depth)):
        list_of_solution_moves.append(f'{0}  {get_id(node)}')
        list_of_solution_moves.reverse()
    else:
        list_of_solution_moves.append('No Solution')


def slow_dfs(node, visited_nodes, max_depth):
    node_id = get_id(node)
    list_of_search_moves.append(f'{node.clicked_index} {node_id}')

    if node_id in visited_nodes:
        return False
    visited_nodes.append(node_id)
    if is_all_zeros(node.game_board):
        while node.parent is not None:
            list_of_solution_moves.append(f'{node.clicked_index} {get_id(node)}')
            node = node.parent
        return True
    if node.depth == max_depth:
        #loop until we hit parent (in case where all children were visited)
        while node is not None:
            node = node.parent
            #cant find non-visited child anywhere, exist
            if node is None:
                return False
            #get next non-visited child of parent    
            next_node = get_next_nonvisited_child(node, visited_nodes)
            if next_node is not None:
                return slow_dfs(next_node, visited_nodes, max_depth)
          
        return False

    slow_build_boards(node)
    next_node = get_next_nonvisited_child(node, visited_nodes)
    if next_node is None:
        return False
    if slow_dfs(next_node, visited_nodes, max_depth):
        return True
    return False

main()
