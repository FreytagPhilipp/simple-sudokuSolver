import sudokuGeneralKNF
from sudokuGeneralKNF import *

import sudokus
from sudokus import *

import time


# a smaller knf, which can be used to construct the full knf for the solver
__generalKNF__ = [
    [(False, 'h'), (False, 'i')],
    [(False, 'g'), (False, 'i')],
    [(False, 'g'), (False, 'h')],
    [(False, 'f'), (False, 'i')],
    [(False, 'f'), (False, 'h')],
    [(False, 'f'), (False, 'g')],
    [(False, 'e'), (False, 'i')],
    [(False, 'e'), (False, 'h')],
    [(False, 'e'), (False, 'g')],
    [(False, 'e'), (False, 'f')],
    [(False, 'd'), (False, 'i')],
    [(False, 'd'), (False, 'h')],
    [(False, 'd'), (False, 'g')],
    [(False, 'd'), (False, 'f')],
    [(False, 'd'), (False, 'e')],
    [(False, 'c'), (False, 'i')],
    [(False, 'c'), (False, 'h')],
    [(False, 'c'), (False, 'g')],
    [(False, 'c'), (False, 'f')],
    [(False, 'c'), (False, 'e')],
    [(False, 'c'), (False, 'd')],
    [(False, 'b'), (False, 'i')],
    [(False, 'b'), (False, 'h')],
    [(False, 'b'), (False, 'g')],
    [(False, 'b'), (False, 'f')],
    [(False, 'b'), (False, 'e')],
    [(False, 'b'), (False, 'd')],
    [(False, 'b'), (False, 'c')],
    [(False, 'a'), (False, 'i')],
    [(False, 'a'), (False, 'h')],
    [(False, 'a'), (False, 'g')],
    [(False, 'a'), (False, 'f')],
    [(False, 'a'), (False, 'e')],
    [(False, 'a'), (False, 'd')],
    [(False, 'a'), (False, 'c')],
    [(False, 'a'), (False, 'b')],
    [(True, 'a'), (True, 'b'), (True, 'c'), (True, 'd'), (True, 'e'), (True, 'f'), (True, 'g'), (True, 'h'), (True, 'i')]
]


def __unitResolutionForSet__(knf : list, units : set) -> list:
    """makes unitresolution to given knf for list of clauses and for the newly created ones

    Args:
        knf list(list(tuple(bool, str))) : is a list of clauses
        units set(tuple(bool, str)) : are the unitclauses

    Returns:
        list(list(tuple(bool, str))): is the new knf after resolution
    """
    
    def makeUnitResolution(knf : list, clauses : set) -> tuple: #returns tuple(list, set) with list as new knf and set as new set of unit-clauses
        tmpKnf = knf.copy()
        newUnitclauses = set()
        for cl in knf:
            clSet = set(cl)
            if len(clSet.intersection(clauses)) > 0:
                tmpKnf.remove(cl)
                continue
            
            tmpCl = cl.copy()
            appendNewClause = False
            for clause in clauses:
                if (not clause[0], clause[1]) in cl:
                    tmpCl.remove((not clause[0], clause[1]))
                    appendNewClause = True
            
            if appendNewClause:
                tmpKnf.remove(cl)        
                tmpKnf.append(tmpCl)
                appendNewClause = False
                
                if len(tmpCl) == 1 and tmpCl[0] not in newUnitclauses:
                    newUnitclauses.update({(tmpCl[0])})
                
                
        #add unitclauses if neccesary
        for clause in clauses:
            if [clause] not in tmpKnf:
                tmpKnf.append([clause])

        return (tmpKnf, newUnitclauses)

    newClauses = units
    while len(newClauses) > 0:
        res = makeUnitResolution(knf, newClauses)
        newClauses = res[1]
        knf = res[0].copy()

    #remove duplicates
    tmpKnf = list()
    for cl in knf:
        if cl not in tmpKnf:
            tmpKnf.append(cl.copy())
    return tmpKnf


def solveSudoku(sudoku : list) -> list:
    """solve sudoku with tree-like testing of possible states. Requires import of "sudokuGeneralKNF"

    Args:
        sudoku list(list(int)) : is a 2-dimensional array containing a 9 lists with 9 intergers, representing the field. If an int is 0, it is not set 

    Returns:
        list(list(int)) : returns a solved sudoku game or an empty list (if its not solveable)
    """

    def isInSolvedState(knf : list) -> bool:
        """checks if sudoku is solved. Knf with duplicates always gives False

        Args:
            knf list(list(tuple(bool, str))) : is given knf

        Returns:
            bool : is True if solved, and False if its not solved
        """

        if len(knf) == 729: #is number of all unitclauses possible in a solved state
            #check if all of the contained clauses are unit-clauses
            for cl in knf:
                if len(cl) != 1:
                    return False

            #check if each field is only set once
            onlyOneOfEachFieldSet = False
            for row in range(0,9):
                for col in range(0,9):
                    for n in range(1, 10):
                        if [(False, str(row) + str(col) + "-" + str(n))] not in knf and [(True, str(row) + str(col) + "-" + str(n))] not in knf:
                            return False
                        elif [(True, str(row) + str(col) + "-" + str(n))] in knf and onlyOneOfEachFieldSet:
                            return False
                        elif [(True, str(row) + str(col) + "-" + str(n))] in knf and not onlyOneOfEachFieldSet:
                            onlyOneOfEachFieldSet = True
                    if not onlyOneOfEachFieldSet:
                        return False
                    onlyOneOfEachFieldSet = False
            
            #since it derived from general sudoku-sat it must be true
            return True 
        else:
            return False

    def getUnallocatetField(knf : list) -> tuple:
        """gets first unallocated field and returnas it with all possible numbers

        Args:
            knf list(list(tuple(bool, str))) : given knf

        Results:
            tuple(int, int, list(int)) : returns tuple containing row-index, collum-index and list of possible allocations or None if none was found
        """
        tmpResult = None

        for row in range(0,9):
            for col in range(0,9):
                if [(True, str(row) + str(col) + "-1")] not in knf and [(True, str(row) + str(col) + "-2")] not in knf and [(True, str(row) + str(col) + "-3")] not in knf and [(True, str(row) + str(col) + "-4")] not in knf and [(True, str(row) + str(col) + "-5")] not in knf and [(True, str(row) + str(col) + "-6")] not in knf and [(True, str(row) + str(col) + "-7")] not in knf and [(True, str(row) + str(col) + "-8")] not in knf and [(True, str(row) + str(col) + "-9")] not in knf:
                    tmpList = list()
                    for n in range(1, 10):
                        if [(False, str(row) + str(col) + "-" + str(n))] not in knf and n not in tmpList:
                            tmpList.append(n)
                    if len(tmpList) == 2:
                        return (row, col, tmpList)
                    elif tmpResult is not None and len(tmpList) < len(tmpResult[2]):
                        tmpResult = (row, col, tmpList)
                    elif tmpResult is None:
                        tmpResult = (row, col, tmpList)

        return tmpResult

    #read in the sudoku-game and construct the knf
    knf = sudokuGeneral.copy()
    setOfUnitClauses = set()
    for row in range(0,9):
        for col in range(0,9):
            if sudoku[row][col] != 0:
                setOfUnitClauses.update({(True, str(row) + str(col) + "-" + str(sudoku[row][col]))})
    knf = __unitResolutionForSet__(knf, setOfUnitClauses)
                
    #contains still untried clauses and old knf as tuples
    stackAddableUnitClauses = list()

    while not isInSolvedState(knf.copy()):
        if [] in knf and len(stackAddableUnitClauses) == 0:
            return []
        elif [] in knf and len(stackAddableUnitClauses) > 0:
            #check other configuration -> you made a wrong assumption

            newClause = stackAddableUnitClauses.pop()
            knf = __unitResolutionForSet__(newClause[1], {newClause[0]})
        else:
            #test further config
            
            #get non-set field
            tmp = getUnallocatetField(knf)
            #make stack and try out allocations
            for unit in tmp[2][1:]:
                stackAddableUnitClauses.append(((True, str(tmp[0]) + str(tmp[1]) + "-" + str(unit)), knf.copy()))
            knf = __unitResolutionForSet__(knf, {(True, str(tmp[0]) + str(tmp[1]) + "-" + str(tmp[2][0]))})


    #convert unit-clauses into list-structure and return it
    result = [
        [0, 0, 0,   0, 0, 0,    0, 0, 0],
        [0, 0, 0,   0, 0, 0,    0, 0, 0],
        [0, 0, 0,   0, 0, 0,    0, 0, 0],

        [0, 0, 0,   0, 0, 0,    0, 0, 0],
        [0, 0, 0,   0, 0, 0,    0, 0, 0],
        [0, 0, 0,   0, 0, 0,    0, 0, 0],

        [0, 0, 0,   0, 0, 0,    0, 0, 0],
        [0, 0, 0,   0, 0, 0,    0, 0, 0],
        [0, 0, 0,   0, 0, 0,    0, 0, 0]
    ]
    for clause in knf:
        if clause[0][0]:
            result[int(clause[0][1][0])][int(clause[0][1][1])] = int(clause[0][1][3])
    return result

def printSudoku(sudoku : list) -> None:
    """prints a sudoku into the command-console

    Args:
        sudoku list(list(int)) : is a list containing 9 lists (each row), which contain 9 integers (each field). If the integers is 0, the field is not set. Each field can be set with an integer from 1 to 9

    Results:
        None
    """
    tmp = ""
    for row in range(0,9):
        tmpList = sudoku[row].__str__()
        tmpList = tmpList[0: 9] + "   " + tmpList[9: 18] + "   " + tmpList[18:]
        tmp = tmp + tmpList + "\n"
        if (row + 1) % 3 == 0:
            tmp = tmp + "\n"

    print(tmp[:-2])
    
    
    
    
    
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
tmp = sudoku2

startTime = time.time()
print("It needs to solve:")
printSudoku(tmp)
print("\n\n")
tmp = solveSudoku(tmp)
print("Its solution:")
printSudoku(tmp)
print("time in seconds: " + str(time.time() - startTime))
