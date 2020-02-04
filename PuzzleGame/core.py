import numpy as np
from helpers import build_initial_board, build_boards, Node, is_all_zeros


def main():
    with open('one_input') as input_file:
        for line in input_file.readlines():
            puzzle_dimension, max_depth, max_search_path, values = line.split()
            root_board = np.array(build_initial_board(int(puzzle_dimension), values), np.int32)
            root_node = Node(root_board, 0)
            build_boards(root_node)
            start_dfs(root_node, max_depth)


def start_dfs(node, max_depth):
    visited = []
    if dfs(node, visited, int(max_depth)):
        print(0, "  ", "".join(str(number) for number in node.game_board.flatten()))
        print("''''''''")


def dfs(node, visited_nodes, max_depth):
    board_as_single_string = "".join(str(number) for number in node.game_board.flatten())
    if len(set(board_as_single_string).intersection(set(visited_nodes))) != 0:
        return False
    visited_nodes.append(board_as_single_string)
    if is_all_zeros(node.game_board):
        return True
    if node.depth == max_depth:
        return False
    build_boards(node)
    for index, child in node.list_of_children.items():
        if dfs(child, visited_nodes, max_depth) is True:
            child_board_as_single_string = "".join(str(number) for number in child.game_board.flatten())
            print(index, " ", child_board_as_single_string)
            print("'''''''")
            return True
    return False


main()

# TODO Quantify performance difference between visited nodes with node object vs flattened array for report
# TODO Modify Node object so list of children is a dict that is child node PLUS the index moved to arrive at that board
# TODO Implement Ranking between game board variations
# TODO Output results to file
