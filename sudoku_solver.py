def row_check(grid,row,num):
    for column in range(9):
        if grid[row][column]==num:
            return True
    return False

def col_check(grid,column,num):
    for row in range(9):
        if grid[row][column]==num:
            return True
    return False

def box_check(grid,num,box_row_start,box_col_start):
    for row in range(box_row_start,box_row_start+3):
        for col in range(box_col_start,box_col_start+3):
            if grid[row][column]==num:
                return True
    return False



