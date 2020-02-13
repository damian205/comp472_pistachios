

# Class the represents a single node in the depth first search. Contains a parent game board plus all possible children
# after one index has been flipped
class Node:
    def __init__(self, game_board, parent_depth, index, priority, history=None):
        self.game_board = game_board
        self.list_of_children = []
        self.depth = parent_depth + 1
        self.index = index
        self.priority = priority
        # self.history = history

    def add_child(self, child_node):
        self.list_of_children.append(child_node)  # append(game_board)


# Class that represents a DFS node. A DFS Node is a child of the Node class. Its priority is represented by a string
# whose every element represents an index where the value "0" is found.
class DfsNode(Node):

    def __eq__(self, other):
        for self_index, other_index in zip(self.priority.split(','), other.priority.split(',')):
            if int(self_index) < int(other_index):
                return False
            elif int(self_index) > int(other_index):
                return False
        return True

    def __lt__(self, other):
        for self_index, other_index in zip(self.priority.split(','), other.priority.split(',')):
            if int(self_index) < int(other_index):
                return True
            elif int(self_index) > int(other_index):
                return False
        return False

    def __gt__(self, other):
        for self_index, other_index in zip(self.priority.split(','), other.priority.split(',')):
            if int(self_index) > int(other_index):
                return True
            elif int(self_index) < int(other_index):
                return False
        return False


# Class that represents an a star node. an a star node is a child of the Node class. Its only difference is that its
# priority is defined by a two components. A g(n) that represents the cost of reaching this node (in this case, this is
# the node's depth) and a heuristic function h(n) that represents the node's distance from the goal node)
class AStarNode(Node):

    def __eq__(self, other):
        return self.priority == other.priority

    def __lt__(self, other):
        return self.priority < other.priority

    def __gt__(self, other):
        return self.priority > other.priority
