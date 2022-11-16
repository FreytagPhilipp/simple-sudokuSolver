import sudokuSolver

tmp = [
    [0, 0, 5,   3, 0, 0,    0, 0, 0],
    [8, 0, 0,   0, 0, 0,    0, 2, 0],
    [0, 7, 0,   0, 1, 0,    5, 0, 0],

    [4, 0, 0,   0, 0, 5,    3, 0, 0],
    [0, 1, 0,   0, 7, 0,    0, 0, 6],
    [0, 0, 3,   2, 0, 0,    0, 8, 0],

    [0, 6, 0,   5, 0, 0,    0, 0, 9],
    [0, 0, 4,   0, 0, 0,    0, 3, 0],
    [0, 0, 0,   0, 0, 9,    7, 0, 0]
]

if __name__ == '__main__':
    
    #prints sudoku beforehand
    print("It needs to solve:")
    sudokuSolver.printSudoku(tmp)
    print()
    
    #solve sudoku    
    tmp = sudokuSolver.solveSudoku(tmp)
    
    #print solution
    print("Its solution:")
    sudokuSolver.printSudoku(tmp)
