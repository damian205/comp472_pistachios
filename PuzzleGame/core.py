import numpy as np
from helpers import build_initial_board, build_boards, Node, is_all_zeros, get_id, find_next_board


def main():
    with open('PuzzleGame\one_input') as input_file:
        for line in input_file.readlines():
            puzzle_dimension, max_depth, max_search_path, values = line.split()
            root_board = np.array(build_initial_board(int(puzzle_dimension), values), np.int32)
            root_node = Node(root_board, 0)
            start_dfs(root_node, max_depth)
            #print("game board:")
            #print(root_node.game_board)
            #build_boards(root_node)
            #print("game board:")
            #print(root_node.game_board)
            #for children in root_node.list_of_children:
                #print("child:")
                #print(children.game_board)
            


def start_dfs(node, max_depth):
    visited = []
    
    dfs(node, visited, int(max_depth))


def dfs(node, visited_nodes, max_depth):
    board_id = get_id(node.game_board)
    stack = []
    stack.append(node)
    visited_nodes.append(board_id)
    #while stack not empty
    deep = 1
    while len(stack)>0:
        current_board = stack.pop() 
        if is_all_zeros(current_board.game_board):
            print('WIN')
            break;
        print(current_board.game_board)
        children = build_boards(current_board)
        #print("--NOW process:---")
        #print(current_board.game_board)
        #get_first_child(children)
        for child in children:
            child_board_id = get_id(child.game_board)
            if child_board_id not in visited_nodes:
                #if deep > 3:
                    #try different node
                    
                   
                #print("--board--")
                #print(child.game_board)
                stack.append(child)
                visited_nodes.append(child_board_id)
                deep+=1
                break
               # visited_nodes.append(child_board_id)
    #print("depth")
    #print(node.depth)
    #if is_all_zeros(node.game_board):
    #    return True
    #if node.depth == max_depth:
    #    if len(visited_nodes) == 16:
    #        return False
        #dfs(node, visited_nodes, max_depth)
   
def get_first_nonvisited_child(children, visited):
    #TODO how to find child with first 0? 
    #For now just return random nonvisited node
    indexesOfZero = []
    for child in children:
        child_board_id = get_id(child.game_board)
        if child_board_id not in visited:
            return child
        #indexesOfZero.append(np.where(child.game_board == 0))

main()

