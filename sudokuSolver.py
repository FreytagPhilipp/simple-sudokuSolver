try:
    import sudokuGeneralCnf
    from sudokuGeneralCnf import *
except:
    pass


# a smaller knf, which can be used to construct the full knf for the solver (is needed when sudokuGeneralCnf-Import failes)
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

def __createSudokuKnf__() -> list:
    """creates the knf 

        Returns:
            list(list(tuple(bool, str))): is the knf of sudoku
    """
    result = list()
    
    #each field can be set and needs to be set
    for row in range(0,9):
        for col in range(0,9):
            renameDict = {
                'a' : str(row) + str(col) + "-1",
                'b' : str(row) + str(col) + "-2",
                'c' : str(row) + str(col) + "-3",
                'd' : str(row) + str(col) + "-4",
                'e' : str(row) + str(col) + "-5",
                'f' : str(row) + str(col) + "-6",
                'g' : str(row) + str(col) + "-7",
                'h' : str(row) + str(col) + "-8",
                'i' : str(row) + str(col) + "-9",
            }
            tmpClause = list()
            for clause in __generalKNF__:
                for literal in clause:
                    tmpClause.append((literal[0], renameDict[literal[1]]))
                result.append(tmpClause)
                tmpClause = list()
                
    #each row can only contain each number once
    for row in range(0,9):
        for n in range(1,10):
            renameDict = {
                'a' : str(row) + "0-" + str(n),
                'b' : str(row) + "1-" + str(n),
                'c' : str(row) + "2-" + str(n),
                'd' : str(row) + "3-" + str(n),
                'e' : str(row) + "4-" + str(n),
                'f' : str(row) + "5-" + str(n),
                'g' : str(row) + "6-" + str(n),
                'h' : str(row) + "7-" + str(n),
                'i' : str(row) + "8-" + str(n),
            }
            tmpClause = list()
            for clause in __generalKNF__:
                for literal in clause:
                    tmpClause.append((literal[0], renameDict[literal[1]]))
                result.append(tmpClause)
                tmpClause = list()
                
    #each collum can only contain each number once
    for col in range(0,9):
        for n in range(1,10):
            renameDict = {
                'a' : "0" + str(col) + "-" + str(n),
                'b' : "1" + str(col) + "-" + str(n),
                'c' : "2" + str(col) + "-" + str(n),
                'd' : "3" + str(col) + "-" + str(n),
                'e' : "4" + str(col) + "-" + str(n),
                'f' : "5" + str(col) + "-" + str(n),
                'g' : "6" + str(col) + "-" + str(n),
                'h' : "7" + str(col) + "-" + str(n),
                'i' : "8" + str(col) + "-" + str(n),
            }
            tmpClause = list()
            for clause in __generalKNF__:
                for literal in clause:
                    tmpClause.append((literal[0], renameDict[literal[1]]))
                result.append(tmpClause)
                tmpClause = list()
    
    #each block can only contain each number once
    blocks = [
        {'a': '00', 'b': '01', 'c': '02', 'd': '10', 'e': '11', 'f': '12', 'g': '20', 'h': '21', 'i': '22'},
        {'a': '03', 'b': '04', 'c': '05', 'd': '13', 'e': '14', 'f': '15', 'g': '23', 'h': '24', 'i': '25'},
        {'a': '06', 'b': '07', 'c': '08', 'd': '16', 'e': '17', 'f': '18', 'g': '26', 'h': '27', 'i': '28'},
        
        {'a': '30', 'b': '31', 'c': '32', 'd': '40', 'e': '41', 'f': '42', 'g': '50', 'h': '51', 'i': '52'},
        {'a': '33', 'b': '34', 'c': '35', 'd': '43', 'e': '44', 'f': '45', 'g': '53', 'h': '54', 'i': '55'},
        {'a': '36', 'b': '37', 'c': '38', 'd': '46', 'e': '47', 'f': '48', 'g': '56', 'h': '57', 'i': '58'},
        
        {'a': '60', 'b': '61', 'c': '62', 'd': '70', 'e': '71', 'f': '72', 'g': '80', 'h': '81', 'i': '82'},
        {'a': '63', 'b': '64', 'c': '65', 'd': '73', 'e': '74', 'f': '75', 'g': '83', 'h': '84', 'i': '85'},
        {'a': '66', 'b': '67', 'c': '68', 'd': '76', 'e': '77', 'f': '78', 'g': '86', 'h': '87', 'i': '88'}
    ]
    for block in blocks:
        for n in range(1, 10):
            tmpClause = list()
            for clause in __generalKNF__:
                for literal in clause:
                    tmpClause.append((literal[0], block[literal[1]] + "-" + str(n)))
                result.append(tmpClause)
                tmpClause = list()
    
    #remove duplicates:
    tmp = list()
    for clause in result:
        if clause not in tmp:
            tmp.append(clause)
    
    return tmp

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
    """solve sudoku with tree-like testing of possible states. Import of "sudokuGeneralKNF" speeds up algorithm by a bit (removes the need to construct a huge knf describing a sudoku-game)

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

    #construct the knf
    try:
        knf = sudokuGeneral.copy()
    except:
        knf = __createSudokuKnf__()
        
    
    #read in given sudoku
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
        [0, 0, 0,    0, 0, 0,    0, 0, 0 ],
        [0, 0, 0,    0, 0, 0,    0, 0, 0 ],
        [0, 0, 0,    0, 0, 0,    0, 0, 0 ],

        [0, 0, 0,    0, 0, 0,    0, 0, 0 ],
        [0, 0, 0,    0, 0, 0,    0, 0, 0 ],
        [0, 0, 0,    0, 0, 0,    0, 0, 0 ],

        [0, 0, 0,    0, 0, 0,    0, 0, 0 ],
        [0, 0, 0,    0, 0, 0,    0, 0, 0 ],
        [0, 0, 0,    0, 0, 0,    0, 0, 0 ],
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
