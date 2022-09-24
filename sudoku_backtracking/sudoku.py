""" Authors:
    Garbin Eleonora 869831
    Zonelli Mattia 870038
 Backtracking with forward checking solution """
import copy


# make a matrix with full domain for each cell
def init_domain_matrix():
    return [['123456789' for i in range(9)] for j in range(9)]


# check if some cells already have a value, if yes reduce their domain to empty set
# and reduce also the domain of their peers.
def reduce_domain(puzzle, domains):
    for r in range(9):
        for c in range(9):
            if puzzle[r][c] != 0:
                domains[r][c] = ''
                domains = propagate_reduction(puzzle[r][c], domains, r, c)
    return domains


# sort the value of the domain of the cell[row][col], from the less constraining to the more constraining.
# In fact, count how much times each value of the domain is present in the domains of the cell's peers, sorts the values
# and the sorted domain.
def sort_domain(row, col, dom, domains):
    numbers = []
    for i in range(9):
        temp = list(map(int, str2list(domains[row][i])))
        for j in dom:
            if j in temp:
                numbers.append(j)

    for i in range(9):
        temp = list(map(int, str2list(domains[i][col])))
        for j in dom:
            if j in temp:
                numbers.append(j)

    boxRow = row - row % 3
    boxCol = col - col % 3
    for i in range(3):
        for j in range(3):
            temp = list(map(int, str2list(domains[boxRow + i][boxCol + j])))
            for j in dom:
                if j in temp:
                    numbers.append(j)

    result = sorted(set(numbers), key=lambda ele: numbers.count(ele))

    return result


# removes a value from the domains of all peers of the cell[row][column]
def propagate_reduction(value, domains, row, column):
    str_val = str(value)
    domains[row][column] = ''

    # for each cell in the row
    for i in range(9):
        tmp = domains[row][i]
        domains[row][i] = tmp.replace(str_val, '')

    # for each cell in the column
    for i in range(9):
        tmp = domains[i][column]
        domains[i][column] = tmp.replace(str_val, '')

    # for each cell in the box
    boxRow = row - row % 3
    boxCol = column - column % 3
    for i in range(3):
        for j in range(3):
            if str_val in domains[boxRow + i][boxCol + j]:
                tmp = domains[boxRow + i][boxCol + j]
                domains[boxRow + i][boxCol + j] = tmp.replace(str_val, '')

    return domains


# return the number of value still in the domain, 10 is returned if the domain is an empty set
def domain_length(domain):
    if domain == '':
        return 10
    else:
        return len(domain)


# this function use the MRV rule, to find the next cell to fill.
# if there isn't any cell to fill, because the sudoku is complete, then it returns (None, None)
# otherwise return (row, column) of the chosen cell.
def getNext2Fill(domains):
    flat_domains = [item for sublist in domains for item in sublist]
    dom_len_list = list(map(domain_length, flat_domains))
    min_len = min(dom_len_list)
    if min_len == 10:
        return None, None
    else:
        index = dom_len_list.index(min_len)
        return index // 9, index % 9

    # figures out whether the guess at the row/col of the puzzle is a valid guess
    # returns True or False
    # for a guess to be valid, then we need to follow the sudoku rules
    # that number must not be repeated in the row, column, or 3x3 square that it appears in


def is_valid(puzzle, guess, row, col):
    # check in the row
    row_vals = puzzle[row]
    if guess in row_vals:
        return False

        # check in the column
    col_vals = [puzzle[i][col] for i in range(9)]
    if guess in col_vals:
        return False

    # check in the square
    row_start = (row // 3) * 3  # 10 // 3 = 3, 5 // 3 = 1, 1 // 3 = 0
    col_start = (col // 3) * 3

    for r in range(row_start, row_start + 3):
        for c in range(col_start, col_start + 3):
            if puzzle[r][c] == guess:
                return False

    return True


# converts a string into a list
def str2list(string):
    list1 = []
    list1[:0] = string
    return list1


# check if there is an empty cell with an empty domain
def error_empty_domain(puzzle, domains):
    for r in range(9):
        for c in range(9):
            if puzzle[r][c] == 0 and domains[r][c] == '':
                return False
    return True


def csp_backtracking(puzzle, domains):
    # step 1: choose somewhere on the puzzle to make a guess
    row, col = getNext2Fill(domains)

    # if we don't have empty cell, the puzzle is complete
    if row is None:
        return True
    else:
        # get the domain of the chosen cell to fill in int list
        dom1 = list(map(int, str2list(domains[row][col])))

        # sort the domain of the cell according to use LCV strategy
        if len(dom1) > 1:
            dom = sort_domain(row, col, dom1, domains)
        else:
            dom = copy.deepcopy(dom1)

        # step 2: if we have an empty cell, we try tu guess its right value.
        # the guess value must be in the domain of he cell
        for guess in dom:
            tmp_dom = copy.deepcopy(domains)
            # step 3: check if guess is a valid number for the cell
            if is_valid(puzzle, guess, row, col):
                # if it is valid, then put it into the sudoku and then reduce the domains of the peers
                puzzle[row][col] = guess

                domains = propagate_reduction(guess, domains, row, col)

                # step 4: if we don't have any error for the solution until now, recursion
                if error_empty_domain(puzzle, domains):

                    if csp_backtracking(puzzle, domains):
                        return True

            # step 5 : if it isn't valid or guess don't solve the sudoku, we must do backtracking and try with
            # another number we reset the number in the sudoku, and we come back to the previous step's domains
            puzzle[row][col] = 0  # resetto il numero
            domains = tmp_dom

        # step 6: if there isnt a value that can satisfy the game rules then the sudoku can't be solve
        return False


def solve_sudoku(puzzle):
    dom_matrix = reduce_domain(puzzle, init_domain_matrix())
    csp_backtracking(puzzle, dom_matrix)
