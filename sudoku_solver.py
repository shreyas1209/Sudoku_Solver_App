#pass grids as a np array
import numpy as np
def row_check(grid,row,num):
    row_values = grid[row]
    row_items  = np.unique(row_values)
    if num in row_items:
        return True
    else:
        return False

def col_check(grid,column,num):
    col_values = (np.transpose(grid))[column]
    col_items = np.unique(col_values)
    if num in col_items:
        return True
    else:
        return False

def box_check(grid,num,box_row_start,box_col_start):
    sub_grid = grid[box_row_start:box_row_start+3,box_col_start:box_col_start+3]
    sub_grid_values = np.unique(sub_grid)
    if num in sub_grid_values:
        return True
    else:
        return False



