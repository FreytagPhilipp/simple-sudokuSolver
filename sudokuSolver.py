import sudokuGeneralKNF
from sudokuGeneralKNF import *

import sudokus
from sudokus import *


def unitResolution(knf : list, unitClause : tuple) -> list:
    """makes unitresolution to given knf for new unitclause and with that newly created ones

    Args:
        knf list(list(tuple(bool, str))) : is a list of clauses
        unitClause tuple(bool, str) : is the new unitclause

    Returns:
        list(list(tuple(bool, str))): is the new knf after resolution
    """

    def makeUnitResolutionForASingleClause(knf : list, clause : tuple) -> tuple: #returns tuple(list, set) with list as new knf and set as new set of clauses
        tmpKnf = knf.copy()
        newUnitclauses = set()
        for cl in knf:
            if clause in cl:
                tmpKnf.remove(cl)
            elif (not clause[0], clause[1]) in cl:
                tmpCl = cl.copy()
                tmpCl.remove((not clause[0], clause[1]))
                tmpKnf.remove(cl)
                tmpKnf.append(tmpCl)
                if len(tmpCl) == 1 and tmpCl[0] not in newUnitclauses:
                    newUnitclauses.update({(tmpCl[0])})

        #add unitclause if neccesary
        if [clause] not in tmpKnf:
            tmpKnf.append([clause])

        return (tmpKnf, newUnitclauses)

    newClauses = {unitClause}
    while len(newClauses) > 0:
        clause = newClauses.pop()
        res = makeUnitResolutionForASingleClause(knf, clause)
        newClauses.update(res[1])
        knf = res[0].copy()

    #remove duplicates
    tmpKnf = list()
    for cl in knf:
        if cl not in tmpKnf:
            tmpKnf.append(cl.copy())

    return tmpKnf

def solveSudoku(sudoku : list) -> list:
    """solve sudoku with simple tree-like testing of possible states. Requires import of "sudokuGeneralKNF"

    Args:
        sudoku list(list(int)) : is a 2-dimensional array containing a 9 lists with 9 intergers, representing the field. If an int is 0, it is not set 

    Returns:
        list(list(int)) : returns a solved sudoku game
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
    for row in range(0,9):
        for col in range(0,9):
            if sudoku[row][col] != 0:
                knf = unitResolution(knf, (True, str(row) + str(col) + "-" + str(sudoku[row][col])))

    #stack of lists, containing all assumptions, which still need to be tested

    #contains still untried clauses and old knf
    stackAddableUnitClauses = list()

    while not isInSolvedState(knf.copy()):

        if [] in knf and len(stackAddableUnitClauses) == 0:
            raise Exception("sudoku was unsolveable")
        elif [] in knf and len(stackAddableUnitClauses) > 0:
            #check other configuration -> you made a wrong assumption
            print("conflict, try new guess")

            #check for new assumption
            newClause = stackAddableUnitClauses.pop()
            print(newClause[0][1].replace("-", " -> "))
            knf = unitResolution(newClause[1], newClause[0])
        else:
            #test further config
            print("not solved, make a further guess")

            #get non-set field
            tmp = getUnallocatetField(knf)
            row = tmp[0]
            col = tmp[1]
            allocations = tmp[2]

            print(str(row) + str(col) + " -> " + str(allocations[0]))

            #make stack and try out allocations
            for unit in allocations[1:]:
                stackAddableUnitClauses.append(((True, str(row) + str(col) + "-" + str(unit)), knf.copy()))
            knf = unitResolution(knf.copy(), (True, str(row) + str(col) + "-" + str(allocations[0])))


    #convert unit-clauses into list-structure
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
    tmp = "\n"
    for row in range(0,9):
        tmpList = sudoku[row].__str__()
        tmpList = tmpList[0: 9] + "   " + tmpList[9: 18] + "   " + tmpList[18:]
        tmp = tmp + tmpList + "\n"
        if (row + 1) % 3 == 0:
            tmp = tmp + "\n"

    print(tmp[:-2])

result6 = [
    [0, 0, 3,   9, 0, 0,    0, 0, 0],
    [0, 0, 0,   1, 0, 7,    9, 0, 0],
    [0, 0, 9,   0, 0, 5,    2, 0, 8],

    [0, 0, 7,   0, 0, 0,    1, 0, 5],
    [3, 0, 0,   0, 0, 0,    0, 0, 9],
    [2, 0, 4,   0, 0, 0,    8, 0, 0],

    [9, 0, 2,   5, 0, 0,    3, 0, 0],
    [0, 0, 1,   7, 0, 6,    0, 0, 0],
    [0, 0, 0,   0, 0, 9,    6, 0, 0]
]

result = solveSudoku(result6)
printSudoku(result)
