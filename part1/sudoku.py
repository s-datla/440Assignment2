#!/usr/bin/python
import sys
import os.path
import collections
import string
from timeit import default_timer as timer



def main():
    if(len(sys.argv) < 3):
        print "Incorrect Format: \npython main.py <sudoku-file> <word-bank-file>"
        sys.exit(2)
    try:
        sudoku = str(sys.argv[1])
        wbank = str(sys.argv[2])
        readFile(sudoku, wbank)
        solveCSP()

        # Double check file path for the maze file
        if not(os.path.exists("./" + sudoku)):
            print "Incorrect file currentPath for sudoku file, retype"
            sys.exit(2)
        if not(os.path.exists("./" + wbank)):
            print "Incorrect file currentPath for word bank file, retype"
            sys.exit(2)


    # Handle exception
    except Exception as inst:
        print inst
        sys.exit(2)

# SETUP

def readFile(sfile, wfile):
    grid = open(sfile, "r")
    bank = open(wfile, "r")

    gridlines = grid.readlines()
    banklines = bank.readlines()

    generateGrid(gridlines)
    # printGrid(mainGrid)
    generateWordBank(banklines)
    # printBank(wordBank)

def generateGrid(gridlines):
    global mainGrid
    global fillList
    fillList = []
    mainGrid = [[' ' for j in range(9)] for i in range(9)]
    for i, line in enumerate(gridlines):
        for j,c in enumerate(line):
            if not ((c == '_') or (c =='\n') or (c == '\r')):
                mainGrid[i][j] = c
                fillList.append(((i,j),c))

def generateWordBank(banklines):
    global wordBank
    wordBank = []
    for i, line in enumerate(banklines):
        line = line.replace('\r','');
        line = line.replace('\n', '');
        wordBank.append(line.upper());

def printBank():
    for line in wordBank:
        print line
    for (x,y),item in fillList:
        print item
    print

def printGrid(grid):
    for line in grid:
        print line
    print

def solveCSP():
    starttimer = timer()
    gridCopy = [x[:] for x in mainGrid]
    unassigned = wordBank[:]
    boolResult, path = recursiveCSP(gridCopy,unassigned,0)
    end = timer()
    print "Computation Time: " + str((end-starttimer)*1000) + "ms"
    print "PATH:"
    for orientation,(x,y),word in path:
        print orientation + "," + str(x) + "," + str(y) + ": " + word


def recursiveCSP(grid, unassigned, count):
    if (not unassigned) and isFull(grid):
        printGrid(grid)
        print "Node Count : " + str(count)
        return (True, [])
    nextvar = nextVariable(grid, unassigned)
    word,locations = nextvar
    if word == '0':
        return (False, [])
    for (x,y),orientation in locations:
        newGrid = [a[:] for a in grid]
        newBank = unassigned[:]
        updatedGrid = assign(newGrid, word, (x,y), orientation)
        newBank.remove(word);
        count += 1
        result = recursiveCSP(updatedGrid,newBank, count + 1)
        if result[0] == True:
            return (True, [(orientation,(x,y),word)] + result[1])
    return (False, [])

def nextVariable(grid, unassigned):
    lowest = float("inf")
    nextvar = ""
    locations = []
    for item in unassigned:
        resultH = countHorizontal(grid, item)
        resultV = countVertical(grid,item)
        totalcount = resultH[0] + resultV[0]
        if (totalcount < lowest):
            lowest = totalcount
            nextvar = item
            locations[:] = []
            if resultH[0] < resultV[0]:
                locations += resultH[1] if resultH[1] else []
                locations += resultV[1] if resultV[1] else []
            else :
                locations += resultV[1] if resultV[1] else []
                locations += resultH[1] if resultH[1] else []
    if lowest == 0 or nextvar == "":
        nextvar = '0'
    return (nextvar, locations)

def countVertical(grid, word):
    wlen = len(word)
    diff = 1
    count = 0
    possXY = []
    if wlen < len(grid[0]):
        diff = len(grid[0]) - wlen + 1
    for i in range(len(grid[0])):
        for j in range(diff):
            if checkVertical(grid, word, (j,i)):
                count += 1
                possXY.append(((j,i),'V'))
    return (count, possXY)

def checkVertical(grid, word, (x,y)):
    for w in range(len(word)):
        if not (grid[x+w][y] == word[w] or grid[x+w][y] == ' '):
            return False
    updatedGrid = assign(grid,word,(x,y),'V')
    if not checkGrid(updatedGrid):
        return False
    # printGrid(updatedGrid)
    return True

def countHorizontal(grid, word):
    wlen = len(word)
    diff = 1
    count = 0
    possXY = []
    if wlen < len(grid[0]):
        diff = len(grid[0]) - wlen + 1
    for i in range(len(grid[0])):
        for j in range(diff):
            if checkHorizontal(grid, word, (i,j)):
                count += 1
                possXY.append(((i,j),'H'))
    return (count,possXY)

def checkHorizontal(grid, word, (x,y)):
    for w in range(len(word)):
        if not (grid[x][y+w] == word[w] or grid[x][y+w] == ' '):
            return False
    updatedGrid = assign(grid,word,(x,y),'H')
    if not checkGrid(updatedGrid):
        return False
    # printGrid(updatedGrid)
    return True

def assign(grid,word,(x,y),c):
    newgrid = [a[:] for a in grid]
    for w in range(len(word)):
        if c == 'V':
            newgrid[x+w][y] = word[w]
        else :
            newgrid[x][y+w] = word[w]
    return newgrid

def checkGrid(grid):
    for i in range(len(grid[0])):
        # Check if horizontal are unique
        y = set()
        for j in range(len(grid[0])):
            if grid[i][j] in y:
                return False
            if not grid[i][j] == ' ':
                y.add(grid[i][j])

        # Check if vertical are unique
        x = set()
        for k in range(len(grid[0])):
            if grid[k][i] in x:
                return False
            if not grid[k][i] == ' ':
                x.add(grid[k][i])

    # Check if subgrids are unique
    '''
        1 | 2 | 3
        ----------
        4 | 5 | 6
        ----------
        7 | 8 | 9
    '''

    for i in range(len(grid[0]) / 3):
        for j in range(len(grid[0])/ 3):
            a = set()
            for x in range(3):
                for y in range(3):
                    if grid[i * 3 + x][j * 3 + y] in a:
                        return False
                    if not grid[i * 3 + x][j * 3 + y] == ' ':
                        a.add(grid[i * 3 + x][j * 3 + y])
    return True

def isFull(grid):
    for i in range(len(grid[0])):
        for j in range(len(grid[0])):
            if grid[i][j] == ' ':
                return False
    return True

if __name__ == '__main__':
    print "--------------------------------"
    print "---Running Word Sudoku Solver---"
    print "--------------------------------"

    main()
