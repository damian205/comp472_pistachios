import numpy as np
from helpers import build_initial_board, build_boards, Node, is_all_zeros


def main():
    with open('one_input') as input_file:
        for line in input_file.readlines():
            puzzle_dimension, max_depth, max_search_path, values = line.split()
            root_board = np.array(build_initial_board(int(puzzle_dimension), values), np.int32)
            root_node = Node(root_board, 0)
            # start_dfs(root_node, max_depth)
            build_boards(root_node)
            for children in root_node.list_of_children:
                print(children)
                print("''''''''")
                saveFile = open('savedOutput.txt','w')
                saveFile.write(np.array_str(children.game_board))
                saveFile.close()
#                t_matrix=map(list, zip(*np.array_str(children.game_board)))
#                print (t_matrix)
                
#                for row in np.array_str(children.game_board): 
#                    print (row)
#                    
            


def start_dfs(node, max_depth):
    visited = []
    print(dfs(node, visited, int(max_depth)))
   


def dfs(node, visited_nodes, max_depth):
    if node in visited_nodes:
        return False
    visited_nodes.append(node)
    if is_all_zeros(node.game_board):
        return True
    if node.depth == max_depth:
        return False
    build_boards(node)
    for child in node.list_of_children:
        if dfs(child, visited_nodes, max_depth) is True:
            return True
    return False
#     max_d = 7
#     board = np.array([[1, 1, 1], [0, 0, 1], [0, 1, 1]], np.int32)
#     print(board)
#     curr_x = 0
#     curr_y = 0
#     stack = [(curr_x, curr_y)]
#
#
#     visitedArray = np.zeros_like(board, dtype=bool)
#
#     while stack:
#         vertex = stack.pop()
#         visitedArray[vertex] = True
#         print(visitedArray)
#         flip(vertex[0], vertex[1], board)
#         print(board)
#         if(isGoldenState(board)):
#             print(board)


# def isGoldenState(array):
#     return np.count_nonzero(array) == 0


main()

