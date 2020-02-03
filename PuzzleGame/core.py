import numpy as np
from helpers import build_initial_board, build_boards, Node, is_all_zeros, find_next_board, get_next_nonvisited_child, get_id


def main():
    with open('PuzzleGame\one_input') as input_file:
        for line in input_file.readlines():
            puzzle_dimension, max_depth, max_search_path, values = line.split()
            root_board = np.array(build_initial_board(int(puzzle_dimension), values), np.int32)
            root_node = Node(root_board, 0, None, "0")
            start_dfs(root_node, max_depth) 


def start_dfs(node, max_depth):
    visited = []
    print(dfs(node, visited, int(max_depth)))


def dfs(node, visited_nodes, max_depth):
    print("---")
    print(node.game_board)
    #print("depth")
    #print(node.depth)
    node_id = get_id(node)
    if node_id in visited_nodes:
        return False
    visited_nodes.append(node_id)
    if is_all_zeros(node.game_board):
        print('Winner')
        print("'''''''")
        print(node.game_board)
        print("'''''''")
        print('Path in Revert order')
        root_node = node
        while node.parent is not None:
            print(node.clicked_index)
            print(node.game_board)
            node = node.parent
        print(node.clicked_index)
        print(node.game_board)
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
                return dfs(next_node, visited_nodes, max_depth)
          
        return False

    build_boards(node)
    next_node = get_next_nonvisited_child(node, visited_nodes)
    if next_node is None:
        return False
    if dfs(next_node, visited_nodes, max_depth):
        return True
    return False




main()

# TODO Quantify performance difference between visited nodes with node object vs flattened array for report
# TODO Modify Node object so list of children is a dict that is child node PLUS the index moved to arrive at that board
