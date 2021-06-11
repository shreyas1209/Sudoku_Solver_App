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
def find_empty(grid):
  indices = np.where(grid == 0)
  rows,cols = indices[0],indices[1]

  if (((len(rows))==0) and ((len(cols))==0)):
    return False
  else:
    row = rows[0]
    col = cols[0]
    return (True,row,col)

def valid_place(grid,row,col,num) :
  print((not(row_check(grid,row,num))))
  print((not(col_check(grid,col,num))))
  print((not(box_check(grid,(row - (row%3)) ,(col - (col%3)), num))))
  return((not(row_check(grid,row,num))) and(not(col_check(grid,col,num))) and (not(box_check(grid,(row - (row%3)) ,(col - (col%3)), num))))


def solve_sudoku(grid):
  empty_bool,empty_row,empty_col = find_empty(grid)
  if (empty_bool ==False):
    return True
  for n in range(1,10):
    print(valid_place(grid,empty_row,empty_col,n))
    if (valid_place(grid,empty_row,empty_col,n)==True):
      grid[empty_row][empty_col] = n
      print(grid)
      if (solve_sudoku(grid) == True):
        return True
      grid[empty_row][empty_col] = 0
  print(grid)
  return False

      








