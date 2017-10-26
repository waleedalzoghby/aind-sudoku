assignments = []

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s + t for s in A for t in B]

rows = 'ABCDEFGHI'
cols = '123456789'
rev_cols = cols[::-1]

boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]

d1units = [[rows[i] + cols[i] for i in range(9)]]
d2units = [[rows[i] + rev_cols[i] for i in range(9)]]

solve_diagonal_sudoko = True

if solve_diagonal_sudoko is True:
    unitlist = row_units + column_units + square_units + d1units + d2units
else:
    unitlist = row_units + column_units + square_units

units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[])) - set([s])) for s in boxes)

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any
    # values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers

    boxes_twin_values = [box for box in values.keys() if len(values[box]) == 2]
    naked_twin = [[box1,box2] for box1 in boxes_twin_values for box2 in peers[box1] if set(values[box1]) == set(values[box2])]

    for i in range(len(naked_twin)):
        Common_peers = set(peers[naked_twin[i][0]]) & set(peers[naked_twin[i][1]])
        for peer in Common_peers:
            if len(values[peer]) >= 2:
                for val_to_remove in values[naked_twin[i][0]]:
                        assign_value(values, peer, values[peer].replace(val_to_remove,''))
                        values[peer] = values[peer].replace(val_to_remove,'')
            
    return values

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    dic = dict(zip(boxes, chars))

    return dic

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """

    if values is False:
        print(False)
        return

    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    """
    looping through all boxes and applying the eliminate technique
    Once done, return the suduko in dictionary form.
    Args:
        values(dict): The sudoku in dictionary form
    """

    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            assign_value(values, peer, values[peer])
            values[peer] = values[peer].replace(digit,'')
            
    return values

def only_choice(values):
    """
    looping through all boxes and applying the only choice technique
    Once done, return the suduko in dictionary form.
    Args: 
        values(dict): The sudoku in dictionary form
    """

    for unit in unitlist:
       for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                assign_value(values, dplaces[0], digit)
                values[dplaces[0]] = digit
                
    return values

def reduce_puzzle(values):
    """
    Iterate eliminate(), only_choice() and naked_twins(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of all functions, the sudoku remains the same, return the sudoku.
    Args: 
        values(dict): The sudoku in dictionary form
    Output: The resulting sudoku in dictionary form.

    """

    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):

    """
    Using depth-first search and propagation, create a search tree and solve the sudoku
    Args: 
        values(dict): The sudoku in dictionary form
    Output: The resulting sudoku in dictionary form.

    """

    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)

    return search(values)

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
