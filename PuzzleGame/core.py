import numpy as np
def main():

    max_d = 7
    board = np.array([[1, 1, 1], [0, 0, 1], [0, 1, 1]], np.int32)
    print(board)
    curr_x = 0
    curr_y = 0
    stack = [(curr_x, curr_y)]
  
    
    visitedArray = np.zeros_like(board, dtype=bool)

    while stack:
        vertex = stack.pop()
        visitedArray[vertex] = True
        print(visitedArray)
        flip(vertex[0], vertex[1], board)
        print(board)
        if(isGoldenState(board)):
            print(board)
        

def flip(xCoordinate, yCoordinate, array):
    #flip requested cell
    array[xCoordinate, yCoordinate] = 1 - array[xCoordinate, yCoordinate]

    #flip horizontal neibours
    if yCoordinate != 0:
        array[xCoordinate, yCoordinate-1] = 1 - array[xCoordinate, yCoordinate-1]
    if len(array[xCoordinate])-1 != yCoordinate:
        array[xCoordinate, yCoordinate+1] = 1 - array[xCoordinate, yCoordinate+1]

    #flip vertical neibours
    if xCoordinate != 0:
        array[xCoordinate-1, yCoordinate] = 1 - array[xCoordinate-1, yCoordinate]
    if len(array[yCoordinate])-1 != xCoordinate:
        array[xCoordinate+1, yCoordinate] = 1 - array[xCoordinate+1, yCoordinate]

def isGoldenState(array):
    return np.count_nonzero(array) == 0


main()







