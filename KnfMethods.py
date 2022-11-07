def __doc__() -> str:
    documentation = "KnfMethods:\nholds all functions used to construct, minimize and validate KNFs.\n"
    return documentation

def subsumAndRemoveDuplicatesFromKNF(knf : list) -> list:
    """removes duplicates and subsums a list of clauses

    Args:
        knf list(list(tuple(bool, str))): is a list of clauses

    Returns:
        list(list(tuple(bool, str))): preprocessed list
    """
    
    tmp = list()
    #delete duplicates
    for clause in knf[:-1]:
        if clause in knf[knf.index(clause) + 1:]:
            knf.remove(clause)
    
    def subsums(smallerC, biggerC) -> bool:
        result = True
        for literal1 in smallerC:
            if literal1 not in biggerC:
                result = False
                break
        return result
    
    #collect broader clauses
    for clauseOrg in knf[:-1]:
        for clauseOther in knf[knf.index(clauseOrg) + 1:]:
            if len(clauseOther) > len(clauseOrg) and subsums(clauseOrg, clauseOther) and clauseOther not in tmp:
                #add clauseOther to delete-List
                tmp.append(clauseOther)
            elif len(clauseOther) < len(clauseOrg) and subsums(clauseOther, clauseOrg) and clauseOrg not in tmp:
                #add clauseOrg to delete-List
                tmp.append(clauseOrg)
    
    #delete all occurences of broader clauses in result
    for clause in tmp:
        while clause in knf:
            knf.remove(clause)
            
    return knf.copy()

def minimizeClausesRoughly(knf : list) -> list:
    """checks all clauses and removes clauses with A+!A and removes unnessecary Literals when A+A

    Args:
        knf list(list(tuple(bool, str))) : is the list of clauses, that will be checked

    Returns:
        list(list(tuple(bool, str))) : returns the new slightly smaller list of clauses
    """
    
    #remove clauses with A+!A and remove Literals with A+A
    tmp = knf.copy()
    for clause in knf:
        for literal in clause:
            if (not literal[0], literal[1]) in clause and clause in tmp:
                tmp.remove(clause)
    removableLiterals = None

    for clause in tmp:
        removableLiterals = list()
        for litIndex in range(0, len(clause) - 1):
            literal = clause[litIndex]
            if literal in clause[litIndex + 1:]:
                removableLiterals.append(literal)
        for rmLiteral in removableLiterals:
            clause.remove(rmLiteral)
    return tmp.copy()

def makeUnitResolutionWithinKNF(knf : list) -> list:
    """makes unit-resolution in given knf if possible

    Args:
        knf list(list(Tuple(bool, str))) : is the given knf for unit-resolution 

    Returns:
        list(list(tuple(bool, str))) : returns the new knf after resolution
    """

    #remove clauses with A+!A and remove Literals with A+A
    knf = minimizeClausesRoughly(knf)
    tmp = knf.copy()
    changesMade = True
    while changesMade:
        changesMade = False

        removableClauses = list()
        for unitClause in knf:
            if len(unitClause) == 1:
                for clause in tmp:
                    if len(clause) > 1 and unitClause[0] in clause and clause not in removableClauses:
                        removableClauses.append(clause)
                        changesMade = True
                    elif len(clause) > 1 and (not unitClause[0][0], unitClause[0][1]) in clause:
                        newClause = clause.copy()
                        while (not unitClause[0][0], unitClause[0][1]) in newClause:
                            newClause.remove((not unitClause[0][0], unitClause[0][1]))
                        tmp[tmp.index(clause)] = newClause.copy()
                        changesMade = True
        for clause in removableClauses:
            while clause in tmp:
                tmp.remove(clause)
        knf = tmp.copy()
    return tmp.copy()


def __checkForPossibleResolution(clauseOrg : list, clauseCheck : list):
    """checks if 2 clauses differ in exactly one literal

    Args:
        clauseOrg list(tuple(bool, str)): first clause in within literal will get deleted
        clauseCheck list(tuple(bool, str)): second clause for comparison

    Returns:
        bool: boolean is true if resolution is possible and false if not
        tuple(bool, str): resolutionLiteral in clauseOrg when resolution is possible
    """
    resPossible = False
    literalTmp = None

    for literal in clauseOrg:
        if literal not in clauseCheck:
            if (not literal[0], literal[1]) in clauseCheck and not resPossible:
                resPossible = True
                literalTmp = literal
            elif (not literal[0], literal[1]) in clauseCheck and resPossible:
                resPossible = False
                literalTmp = None
                break
            else:
                resPossible = False
                literalTmp = None
                break
    return resPossible, literalTmp

def minimzeKNF(knf : list, progressMessages : bool = False) -> list:
    """tries to find a smaller knf out of the given one

    Args:
        knf list(list(tuple(bool, str))) : knf, that needs to be minimized
        progressMessages bool : prints every loop a message if True

    Returns:
        list(list(tuple(bool, str))): smaller knf
    """
    
    #remove clauses with A+!A and remove Literals with A+A
    knf = minimizeClausesRoughly(knf)

    #delete duplicates and subsum
    knf = subsumAndRemoveDuplicatesFromKNF(knf)
    #make unit resolution if possible
    knf = makeUnitResolutionWithinKNF(knf)
    
    maxResolutionTimes = 0
    for c in knf:
        if len(c) > maxResolutionTimes:
            maxResolutionTimes = len(c)
        
    for i in range(maxResolutionTimes):
        if progressMessages:
            print(str(i + 1) + ". loop of " + str(maxResolutionTimes))

        tempRes = list()
        resultCombi = list()
        
        for clauseOrg in knf[:-1]:
            for clauseCheck in knf[knf.index(clauseOrg) + 1:]:
                if len(clauseCheck) == len(clauseOrg):
                    #make resolution if possible
                    resPossible = False
                    literalTmp = None
                    resPossible, literalTmp = __checkForPossibleResolution(clauseOrg, clauseCheck)
                    
                    #resolution
                    if resPossible:
                        tmp = clauseOrg.copy()
                        tmp.remove(literalTmp)
                        tempRes.append(tmp)
        
        
        #add resolution to endlist
        resultCombi.extend(tempRes.copy())
        resultCombi.extend(knf.copy())
        
        #remove duplicates and broader clauses
        knf = subsumAndRemoveDuplicatesFromKNF(resultCombi)
        
        #make unit resolution if possible
        knf = makeUnitResolutionWithinKNF(knf)
    
    return knf

"""

def createFeld() -> list:
    #return []
    
    feld = list()
    for n1 in [True, False]:
        for n2 in [True, False]:
            for n3 in [True, False]:
                for n4 in [True, False]:
                    for n5 in [True, False]:
                        for n6 in [True, False]:
                            for n7 in [True, False]:
                                for n8 in [True, False]:
                                    for n9 in [True, False]:
                                        feld.append([(n1, "a"), (n2, "b"), (n3, "c"), (n4, "d"), (n5, "e"), (n6, "f"), (n7, "g"), (n8, "h"), (n9, "i")])
    feld.remove([(False, "a"), (True, "b"), (True, "c"), (True, "d"), (True, "e"), (True, "f"), (True, "g"), (True, "h"), (True, "i")])
    feld.remove([(True, "a"), (False, "b"), (True, "c"), (True, "d"), (True, "e"), (True, "f"), (True, "g"), (True, "h"), (True, "i")])
    feld.remove([(True, "a"), (True, "b"), (False, "c"), (True, "d"), (True, "e"), (True, "f"), (True, "g"), (True, "h"), (True, "i")])
    feld.remove([(True, "a"), (True, "b"), (True, "c"), (False, "d"), (True, "e"), (True, "f"), (True, "g"), (True, "h"), (True, "i")])
    feld.remove([(True, "a"), (True, "b"), (True, "c"), (True, "d"), (False, "e"), (True, "f"), (True, "g"), (True, "h"), (True, "i")])
    feld.remove([(True, "a"), (True, "b"), (True, "c"), (True, "d"), (True, "e"), (False, "f"), (True, "g"), (True, "h"), (True, "i")])
    feld.remove([(True, "a"), (True, "b"), (True, "c"), (True, "d"), (True, "e"), (True, "f"), (False, "g"), (True, "h"), (True, "i")])
    feld.remove([(True, "a"), (True, "b"), (True, "c"), (True, "d"), (True, "e"), (True, "f"), (True, "g"), (False, "h"), (True, "i")])
    feld.remove([(True, "a"), (True, "b"), (True, "c"), (True, "d"), (True, "e"), (True, "f"), (True, "g"), (True, "h"), (False, "i")])
    
    feld = minimzeKNF(feld, progressMessages=True)
    
    return feld.copy()

def createFill9() -> list:
    feld = list()
    i = 1
    for n1 in [True, False]:
        for n2 in [True, False]:
            for n3 in [True, False]:
                for n4 in [True, False]:
                    for n5 in [True, False]:
                        for n6 in [True, False]:
                            for n7 in [True, False]:
                                for n8 in [True, False]:
                                    for n9 in [True, False]:
                                        feld.append([(n1, "a-" + str(i)), (n2, "b-" + str(i)), (n3, "c-" + str(i)), (n4, "d-" + str(i)), (n5, "e-" + str(i)), (n6, "f-" + str(i)), (n7, "g-" + str(i)), (n8, "h-" + str(i)), (n9, "i-" + str(i))])
    feld.remove([(False, "a-" + str(i)), (True, "b-" + str(i)), (True, "c-" + str(i)), (True, "d-" + str(i)), (True, "e-" + str(i)), (True, "f-" + str(i)), (True, "g-" + str(i)), (True, "h-" + str(i)), (True, "i-" + str(i))])
    feld.remove([(True, "a-" + str(i)), (False, "b-" + str(i)), (True, "c-" + str(i)), (True, "d-" + str(i)), (True, "e-" + str(i)), (True, "f-" + str(i)), (True, "g-" + str(i)), (True, "h-" + str(i)), (True, "i-" + str(i))])
    feld.remove([(True, "a-" + str(i)), (True, "b-" + str(i)), (False, "c-" + str(i)), (True, "d-" + str(i)), (True, "e-" + str(i)), (True, "f-" + str(i)), (True, "g-" + str(i)), (True, "h-" + str(i)), (True, "i-" + str(i))])
    feld.remove([(True, "a-" + str(i)), (True, "b-" + str(i)), (True, "c-" + str(i)), (False, "d-" + str(i)), (True, "e-" + str(i)), (True, "f-" + str(i)), (True, "g-" + str(i)), (True, "h-" + str(i)), (True, "i-" + str(i))])
    feld.remove([(True, "a-" + str(i)), (True, "b-" + str(i)), (True, "c-" + str(i)), (True, "d-" + str(i)), (False, "e-" + str(i)), (True, "f-" + str(i)), (True, "g-" + str(i)), (True, "h-" + str(i)), (True, "i-" + str(i))])
    feld.remove([(True, "a-" + str(i)), (True, "b-" + str(i)), (True, "c-" + str(i)), (True, "d-" + str(i)), (True, "e-" + str(i)), (False, "f-" + str(i)), (True, "g-" + str(i)), (True, "h-" + str(i)), (True, "i-" + str(i))])
    feld.remove([(True, "a-" + str(i)), (True, "b-" + str(i)), (True, "c-" + str(i)), (True, "d-" + str(i)), (True, "e-" + str(i)), (True, "f-" + str(i)), (False, "g-" + str(i)), (True, "h-" + str(i)), (True, "i-" + str(i))])
    feld.remove([(True, "a-" + str(i)), (True, "b-" + str(i)), (True, "c-" + str(i)), (True, "d-" + str(i)), (True, "e-" + str(i)), (True, "f-" + str(i)), (True, "g-" + str(i)), (False, "h-" + str(i)), (True, "i-" + str(i))])
    feld.remove([(True, "a-" + str(i)), (True, "b-" + str(i)), (True, "c-" + str(i)), (True, "d-" + str(i)), (True, "e-" + str(i)), (True, "f-" + str(i)), (True, "g-" + str(i)), (True, "h-" + str(i)), (False, "i-" + str(i))])
    feld = minimzeKNF(feld, progressMessages=True)
    
    return feld.copy()


import tmp
from tmp import *
kl = minimzeKNF(sudokuGeneral, progressMessages=True)
strTmp = "sudokuGeneral = [\n"
for clause in kl[:-1]:
    strTmp = strTmp + "    " + clause.__str__() + ",\n"
strTmp = strTmp + kl[-1].__str__() + "\n]"

with open('sudokuGeneralKNF.txt', 'w') as file:
    file.write(strTmp)





lastContent = "sudokuGeneral = [\n"
with open('sudokuGeneralKNF.txt', 'w') as file:
    tmpStr = ""
    feld = createFeld()
    for i in range(0,9):
        for j in range(0,9):
            for clause in feld.copy():
                tmpStr = tmpStr + "    " + clause.__str__() + ", \n"
            for exchange in [('a', '-1'), ('b', '-2'), ('c', '-3'), ('d', '-4'), ('e', '-5'), ('f', '-6'), ('g', '-7'), ('h', '-8'), ('i', '-9')]:
                tmpStr = tmpStr.replace("'" + exchange[0] + "'", "'" + str(i) + str(j) + exchange[1] + "'")
    lastContent = lastContent + tmpStr
    
    feld = createFill9()
    tmpStr = ""
    for n in range(1, 10):
        for i in range(0,9):
            for clause in feld.copy():
                tmpStr = tmpStr + "    " + clause.__str__() + ", \n"
            for exchange in [('a', '0'), ('b', '1'), ('c', '2'), ('d', '3'), ('e', '4'), ('f', '5'), ('g', '6'), ('h', '7'), ('i', '8')]:
                tmpStr = tmpStr.replace("'" + exchange[0] + "-1'", "'" + str(i) + exchange[1] + "-" + str(n) + "'")
    lastContent = lastContent + tmpStr
    
    tmpStr = ""
    for n in range(1, 10):
        for i in range(0,9):
            for clause in feld.copy():
                tmpStr = tmpStr + "    " + clause.__str__() + ", \n"
            for exchange in [('a', '0'), ('b', '1'), ('c', '2'), ('d', '3'), ('e', '4'), ('f', '5'), ('g', '6'), ('h', '7'), ('i', '8')]:
                tmpStr = tmpStr.replace("'" + exchange[0] + "-1'", "'" + exchange[1] + str(i) + "-" + str(n) + "'")
    lastContent = lastContent + tmpStr
    
    kasten = [
        [('a', '00'), ('b', '01'), ('c', '02'), ('d', '10'), ('e', '11'), ('f', '12'), ('g', '20'), ('h', '21'), ('i', '22')],
        [('a', '03'), ('b', '04'), ('c', '05'), ('d', '13'), ('e', '14'), ('f', '15'), ('g', '23'), ('h', '24'), ('i', '25')],
        [('a', '06'), ('b', '07'), ('c', '08'), ('d', '16'), ('e', '17'), ('f', '18'), ('g', '26'), ('h', '27'), ('i', '28')],
        
        [('a', '30'), ('b', '31'), ('c', '32'), ('d', '40'), ('e', '41'), ('f', '42'), ('g', '50'), ('h', '51'), ('i', '52')],
        [('a', '33'), ('b', '34'), ('c', '35'), ('d', '43'), ('e', '44'), ('f', '45'), ('g', '53'), ('h', '54'), ('i', '55')],
        [('a', '36'), ('b', '37'), ('c', '38'), ('d', '46'), ('e', '47'), ('f', '48'), ('g', '56'), ('h', '57'), ('i', '58')],
        
        [('a', '60'), ('b', '61'), ('c', '62'), ('d', '70'), ('e', '71'), ('f', '72'), ('g', '80'), ('h', '81'), ('i', '82')],
        [('a', '63'), ('b', '64'), ('c', '65'), ('d', '73'), ('e', '74'), ('f', '75'), ('g', '83'), ('h', '84'), ('i', '85')],
        [('a', '66'), ('b', '67'), ('c', '68'), ('d', '76'), ('e', '77'), ('f', '78'), ('g', '86'), ('h', '87'), ('i', '88')]
    ]
    #kasten 1
    tmpStr = ""
    for kast in kasten:
        for n in range(1, 10):
            for clause in feld.copy():
                tmpStr = tmpStr + "    " + clause.__str__() + ", \n"
            for exchange in kast:
                tmpStr = tmpStr.replace("'" + exchange[0] + "-1'", "'" + exchange[1] + "-" + str(n) + "'")
        lastContent = lastContent + tmpStr
    
    file.write(lastContent)
"""



