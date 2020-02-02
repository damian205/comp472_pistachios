import numpy as np
from helpers import build_initial_board, build_boards, Node, is_all_zeros


def main():
    with open('one_input') as input_file:
        for line in input_file.readlines():
            puzzle_dimension, max_depth, max_search_path, values = line.split()
            root_board = np.array(build_initial_board(int(puzzle_dimension), values), np.int32)
            root_node = Node(root_board, 0)
            start_dfs(root_node, max_depth)
            # print("".join(str(number) for number in root_node.game_board.flatten()))
            # build_boards(root_node)
            # for children in root_node.list_of_children:
            #     print(children)
            #     print("''''''''")


def start_dfs(node, max_depth):
    visited = []
    print(dfs(node, visited, int(max_depth)))


# def dfs(node, visited_nodes, max_depth):
#     # print("''''''''")
#     # print("Node that has been visited")
#     # print(node.game_board)
#     # print("''''''''")
#     # board_as_single_string = "".join(str(number) for number in node.game_board.flatten())
#     if node in visited_nodes:
#         return False
#     visited_nodes.append(node)
#     # print(visited_nodes)
#     if is_all_zeros(node.game_board):
#         print('Winner')
#         print("'''''''")
#         print(node.game_board)
#         print("'''''''")
#         return True
#     if node.depth == max_depth:
#         return False
#     build_boards(node)
#     for child in node.list_of_children:
#         if dfs(child, visited_nodes, max_depth) is True:
#             print("'''''''")
#             print(node.game_board)
#             print("'''''''")
#             return True
#     return False


def dfs(node, visited_nodes, max_depth):
    # print("''''''''")
    # print("Node that has been visited")
    # print(node.game_board)
    # print("''''''''")
    board_as_single_string = "".join(str(number) for number in node.game_board.flatten())
    if len(set(board_as_single_string).intersection(set(visited_nodes))) != 0:
        return False
    # if board_as_single_string in visited_nodes:
    #     return False
    visited_nodes.append(board_as_single_string)
    # print(visited_nodes)
    if is_all_zeros(node.game_board):
        print('Winner')
        print("'''''''")
        print(node.game_board)
        print("'''''''")
        return True
    if node.depth == max_depth:
        return False
    build_boards(node)
    for child in node.list_of_children:
        if dfs(child, visited_nodes, max_depth) is True:
            print("'''''''")
            print(node.game_board)
            print("'''''''")
            return True
    return False



main()

# TODO Quantify performance difference between visited nodes with node object vs flattened array for report
# TODO Modify Node object so list of children is a dict that is child node PLUS the index moved to arrive at that board
