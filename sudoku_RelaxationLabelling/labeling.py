import numpy as np

SIDE = 9
TOT_OBJECTS = 81


# compute the possible value of the domain for cell in row r and column c
def getPossibleValue(r, c, sudoku):
    possible_dom = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    for k in range(SIDE):
        # check the row
        if sudoku[r][k] != 0:
            possible_dom[sudoku[r][k] - 1] = 0
        # check the column
        if sudoku[k][c] != 0:
            possible_dom[sudoku[k][c] - 1] = 0
    # check the box
    boxR = r - r % 3
    boxC = c - c % 3
    for i in range(3):
        for j in range(3):
            if sudoku[boxR + i][boxC + j] != 0:
                possible_dom[sudoku[boxR + i][boxC + j] - 1] = 0

    domain = []
    for i in range(len(possible_dom)):
        if possible_dom[i] != 0:
            domain.append(possible_dom[i])
    return domain


# utility function to init the matrix of probabilities
def initBoard(board):
    p = np.ones((TOT_OBJECTS * SIDE, 1)) / SIDE

    for i in range(SIDE):
        for j in range(SIDE):
            domain_set = getPossibleValue(i, j, board)
            n = len(domain_set)
            prob = np.zeros((1, SIDE))[0]
            if board[i][j] != 0:
                val = int(board[i][j])
                prob[val - 1] = 1
            else:
                for k in domain_set:
                    prob[int(k) - 1] = np.random.uniform(1 / n - 0.005, 1 / n + 0.005)
            prob = prob / np.sum(prob)
            p.reshape(SIDE, SIDE, SIDE)[i][j] = prob
    return p


# compute the compatibility function r_{i,j}(lamda, mu)
def function_r(i, j, lmda, mu):
    if i == j:
        return 0
    if lmda != mu:
        return 1

    # get row of cells i and j
    i_r = i // SIDE
    j_r = j // SIDE
    # get column of cells i and j
    i_c = i % SIDE
    j_c = j % SIDE
    # get the indexes of column and row of the first cell of the box in which i is
    start_i_r = i_r - i_r % 3
    start_i_c = i_c - i_c % 3
    # get the indexes of column and row of the first cell of the box in which j is
    start_j_r = j_r - j_r % 3
    start_j_c = j_c - j_c % 3
    # check if cells i and j are in the same box
    if i_c == j_c or i_r == j_r or (start_i_r == start_j_r and start_i_c == start_j_c):
        return 0
    return 1


# create the matric of compatibility coefficients
def R_matrix():
    rij = np.zeros((TOT_OBJECTS * SIDE, TOT_OBJECTS * SIDE))
    for i in range(TOT_OBJECTS):
        for lmbda in range(SIDE):
            for j in range(TOT_OBJECTS):
                for mu in range(SIDE):
                    rij[i * SIDE + lmbda][j * SIDE + mu] = function_r(i, j, lmbda, mu)
    return rij


# core of the relaxation labeling
def relaxation_labelling(p):
    rij = R_matrix()
    prev = 0
    diff = 1
    step = 0

    while diff > 0.001:

        q = np.dot(rij, p)
        numeratore = p * q
        denominatore = numeratore.reshape(TOT_OBJECTS, SIDE).sum(axis=1)
        # update values in the matrix of probabilities
        p = (numeratore.reshape(TOT_OBJECTS, SIDE) / denominatore[:, np.newaxis]).reshape(TOT_OBJECTS * SIDE, 1)

        ''' with euclidian distance '''
        diff = np.linalg.norm(p-prev)
        # print("Euclidian distance: ", diff, ", step: ", step, "")
        prev = p
        step += 1
    return p


# for each sudoku cell
# look at the probability vector and assign to the cell the label with the highest value in the vector
def apply_sudoku(sudoku):
    p = relaxation_labelling(initBoard(sudoku))

    for i in range(SIDE * SIDE):
        pos = np.argmax(p.reshape(TOT_OBJECTS, SIDE)[i])
        sudoku[i // SIDE][i % SIDE] = pos + 1
    return sudoku
