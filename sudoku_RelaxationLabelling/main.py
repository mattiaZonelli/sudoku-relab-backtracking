from labeling import apply_sudoku
import time


def print_sudoku(sudoku):
    for i in range(9):
        print(sudoku[i])


if __name__ == '__main__':

    board_n = [
        [9, 0, 4, 0, 5, 0, 0, 2, 0],
        [0, 0, 7, 0, 0, 0, 0, 1, 0],
        [0, 0, 3, 2, 8, 0, 0, 0, 0],

        [0, 0, 0, 0, 9, 0, 0, 0, 0],
        [0, 0, 0, 8, 0, 0, 0, 3, 6],
        [5, 0, 0, 7, 0, 0, 0, 0, 2],

        [1, 0, 0, 0, 0, 3, 0, 4, 0],
        [0, 0, 0, 0, 0, 6, 0, 0, 5],
        [0, 4, 0, 0, 0, 0, 0, 0, 9]
    ]

    board_p = [
        [3, 7, 0, 5, 0, 0, 0, 0, 6],
        [0, 0, 0, 3, 6, 0, 0, 1, 2],
        [0, 0, 0, 0, 9, 1, 7, 5, 0],

        [0, 0, 0, 1, 5, 4, 0, 7, 0],
        [0, 0, 3, 0, 7, 0, 6, 0, 0],
        [0, 5, 0, 6, 3, 8, 0, 0, 0],

        [0, 6, 4, 9, 8, 0, 0, 0, 0],
        [5, 9, 0, 0, 2, 6, 0, 0, 0],
        [2, 0, 0, 0, 0, 5, 0, 6, 4]
    ]

    board1 = [
        [0, 4, 0, 0, 0, 0, 1, 7, 9],
        [0, 0, 2, 0, 0, 8, 0, 5, 4],
        [0, 0, 6, 0, 0, 5, 0, 0, 8],
        [0, 8, 0, 0, 7, 0, 9, 1, 0],
        [0, 5, 0, 0, 9, 0, 0, 3, 0],
        [0, 1, 9, 0, 6, 0, 0, 4, 0],
        [3, 0, 0, 4, 0, 0, 7, 0, 0],
        [5, 7, 0, 1, 0, 0, 2, 0, 0],
        [9, 2, 8, 0, 0, 0, 0, 6, 0],
    ]

    board2 = [
        [2, 0, 6, 0, 0, 0, 0, 4, 9],
        [0, 3, 7, 0, 0, 9, 0, 0, 0],
        [1, 0, 0, 7, 0, 0, 0, 0, 6],
        [0, 0, 0, 5, 8, 0, 9, 0, 0],
        [7, 0, 5, 0, 0, 0, 8, 0, 4],
        [0, 0, 9, 0, 6, 2, 0, 0, 0],
        [9, 0, 0, 0, 0, 4, 0, 0, 1],
        [0, 0, 0, 3, 0, 0, 4, 9, 0],
        [4, 1, 0, 0, 0, 0, 2, 0, 8],
    ]

    print("\n\n----------Relaxation Labeling------------")

    start = time.time()
    for t in range(100):
        solved = apply_sudoku(board_n)

    print("Time", time.time() - start, "sec")
    print_sudoku(solved)

    '''
        to solve correctly easy1 100 times, it took  37.126 sec
    '''