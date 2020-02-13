import numpy as np
from helpers import build_initial_board, build_boards, is_all_zeros, save_to_file
from node import *
import heapq

list_of_solution_moves = []  # Must be reset after every input puzzle
list_of_search_moves = []  # Ditto
test_list_of_priorities = []
list_of_nodes_a_star = []  # List used for the a star algorithm


# TODO provide a copy() function for the Node class that will maintain all values but just clear the existing list of
# children


def main():
    with open('one_input') as input_file:
        i = 0
        for line in input_file.readlines():
            puzzle_dimension, max_depth, max_search_path, values = line.split()
            root_board = np.array(build_initial_board(int(puzzle_dimension), values), np.int32)
            root_node = Node(root_board, 0, 0, 0)
            start_dfs(root_node, max_depth, i)
            root_node = Node(root_board, 0, 0, 0)  # reinitialize to remove preexisting list of children
            start_a_star(root_node, max_search_path, i)
            i += 1


def start_dfs(node, max_depth, i):
    node.__class__ = DfsNode
    build_boards(node, "DFS")
    visited = []
    starting_board_as_single_string = "".join(str(number) for number in node.game_board.flatten())
    list_of_search_moves.append(f'0  {starting_board_as_single_string}')
    if dfs(node, visited, int(max_depth)):
        list_of_solution_moves.append(f'{0}  {starting_board_as_single_string}')
        list_of_solution_moves.reverse()
    else:
        list_of_solution_moves.append('No Solution')
    save_to_file(list_of_solution_moves, f'{i}_dfs_solution.txt')
    save_to_file(list_of_search_moves, f'{i}_dfs_search.txt')
    clean_up()
    sort_experiment(test_list_of_priorities)


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
    build_boards(node, "DFS")
    node.list_of_children.sort()
    for child in node.list_of_children:
        child_board_as_single_string = "".join(str(number) for number in child.game_board.flatten())
        list_of_search_moves.append(f'{child.index} {child_board_as_single_string}')
        global test_list_of_priorities
        test_list_of_priorities.append(child)
        if dfs(child, visited_nodes, max_depth) is True:
            global list_of_solution_moves
            list_of_solution_moves.append(f'{child.index} {child_board_as_single_string}')
            return True
    return False


def start_a_star(node, max_search, i):
    node.__class__ = AStarNode
    global list_of_nodes_a_star, list_of_solution_moves, list_of_search_moves
    list_of_nodes_a_star.append(node)
    goal_node = a_star([], int(max_search))
    if goal_node is None:
        list_of_solution_moves.append('No Solution')
    else:
        list_of_solution_moves = goal_node.print_history()
    list_of_solution_moves.reverse()
    save_to_file(list_of_solution_moves, f'{i}_A_solution.txt')
    save_to_file(list_of_search_moves, f'{i}_A_search.txt')
    clean_up()
    sort_experiment(test_list_of_priorities)


def a_star(visited_nodes, max_search):
    global list_of_nodes_a_star, list_of_search_moves, list_of_solution_moves
    while len(list_of_nodes_a_star) > 0 and len(list_of_search_moves) <= max_search:
        current_best_node = list_of_nodes_a_star.pop(0)
        board_as_single_string = "".join(str(number) for number in current_best_node.game_board.flatten())
        list_of_search_moves.append(f'{current_best_node.index} {board_as_single_string}')
        # check to see if board of the same values has been visited before
        if len(set([board_as_single_string]).intersection(set(visited_nodes))) != 0:
            continue
        visited_nodes.append(board_as_single_string)
        if is_all_zeros(current_best_node.game_board):
            # list_of_solution_moves.append(f'{current_best_node.index} {board_as_single_string}')
            return current_best_node
        build_boards(current_best_node, "A*")
        for child in current_best_node.list_of_children:
            list_of_nodes_a_star.append(child)
        list_of_nodes_a_star.sort()
    return None

    # if len(list_of_nodes_a_star) == 0:
    #     return False
    # if len(list_of_search_moves) >= max_search:
    #     return False
    # current_best_node = list_of_nodes_a_star.pop(0)
    # board_as_single_string = "".join(str(number) for number in current_best_node.game_board.flatten())
    # list_of_search_moves.append(f'{current_best_node.index} {board_as_single_string}')
    # # check to see if board of the same values has been visited before
    # if len(set([board_as_single_string]).intersection(set(visited_nodes))) != 0:
    #     return False
    # visited_nodes.append(board_as_single_string)
    # if is_all_zeros(current_best_node.game_board):
    #     list_of_solution_moves.append(f'{current_best_node.index} {board_as_single_string}')
    #     return True
    # build_boards(current_best_node, "A*")
    # for child in current_best_node.list_of_children:
    #     list_of_nodes_a_star.append(child)
    # list_of_nodes_a_star.sort()
    # if a_star(visited_nodes, max_search):
    #     list_of_solution_moves.append(f'{current_best_node.index} {board_as_single_string}')
    #     return True
    # return False


def clean_up():
    list_of_solution_moves.clear()
    list_of_search_moves.clear()
    test_list_of_priorities.clear()
    list_of_nodes_a_star.clear()


def sort_experiment(list_of_stuff):
    for i in range(0, len(list_of_stuff) - 1):
        print(list_of_stuff[i].priority)
    print('''''''')
    print('''''''')
    print('''''''')
    print('''''''')
    list_of_stuff.sort()
    for i in range(0, len(list_of_stuff) - 1):
        print(list_of_stuff[i].priority)


main()

# TODO Quantify performance difference between visited nodes with node object vs flattened array for report
