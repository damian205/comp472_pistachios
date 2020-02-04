import numpy as np
from helpers import build_initial_board, build_boards, Node, is_all_zeros, save_to_file

list_of_solution_moves = []  # Must be reset after every input puzzle
list_of_search_moves = []  # Ditto


def main():
    with open('one_input') as input_file:
        i = 0
        for line in input_file.readlines():
            puzzle_dimension, max_depth, max_search_path, values = line.split()
            root_board = np.array(build_initial_board(int(puzzle_dimension), values), np.int32)
            root_node = Node(root_board, 0)
            build_boards(root_node)
            start_dfs(root_node, max_depth)
            save_to_file(list_of_solution_moves, f'{i}_dfs_solution.txt')
            save_to_file(list_of_search_moves, f'{i}_dfs_search.txt')
            i += 1
            clean_up()


def start_dfs(node, max_depth):
    visited = []
    starting_board_as_single_string = "".join(str(number) for number in node.game_board.flatten())
    list_of_search_moves.append(f'0  {starting_board_as_single_string}')
    if dfs(node, visited, int(max_depth)):
        list_of_solution_moves.append(f'{0}  {starting_board_as_single_string}')
        list_of_solution_moves.reverse()
    else:
        list_of_solution_moves.append('No Solution')


# TODO after putting board_as_single_string within [], the algorithm detects same strings correctly BUT becomes
# less capable of finding solutions as when there were no []... WHY??!!


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
    for index, child in node.list_of_children.items():
        child_board_as_single_string = "".join(str(number) for number in child.game_board.flatten())
        list_of_search_moves.append(f'{index} {child_board_as_single_string}')
        if dfs(child, visited_nodes, max_depth) is True:
            global list_of_solution_moves
            list_of_solution_moves.append(f'{index} {child_board_as_single_string}')
            return True
    return False


def clean_up():
    list_of_solution_moves.clear()
    list_of_search_moves.clear()


main()

# TODO Quantify performance difference between visited nodes with node object vs flattened array for report
# TODO Modify Node object so list of children is a dict that is child node PLUS the index moved to arrive at that board
# TODO Implement Ranking between game board variations
# TODO Output results to file
