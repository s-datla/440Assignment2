#!/usr/bin/python
import sys
import os.path
import collections
import string
from timeit import default_timer as timer

# Authors: Srikrishna Datla, Chi Kok Pin

def main():
    if(len(sys.argv) < 3):
        print "Incorrect Format: \npython main.py <sudoku-file> <word-bank-file>"
        sys.exit(2)
    try:
        # Reading Sudoku and Word Bank Files
        sudoku = str(sys.argv[1])
        wbank = str(sys.argv[2])
        readFile(sudoku, wbank)


        solveCSP()

        # Double check file path for both files
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
        # For some reason, the files had extra escape characters that messed up my program, so we just remove escapes
        line = line.replace('\r','');
        line = line.replace('\n', '');
        wordBank.append(line.upper());

# For debugging purposes
def printBank():
    for line in wordBank:
        print line
    for (x,y),item in fillList:
        print item
    print

# For debugging and end state confirmation
def printGrid(grid):
    for line in grid:
        print line
    print


def solveCSP():

    # TIMER!
    starttimer = timer()

    # Weird way of copying 2d array in python
    gridCopy = [x[:] for x in mainGrid]
    unassigned = wordBank[:]

    boolResult, path = recursiveCSP(gridCopy,unassigned,0)
    end = timer()

    # Print Statements
    print "Computation Time: " + str((end-starttimer)*1000) + "ms"
    print "PATH:"
    for orientation,(x,y),word in path:
        print orientation + "," + str(x) + "," + str(y) + ": " + word


def recursiveCSP(grid, unassigned, count):

    # Base Case checking if all words have been included in the grid and if the grid is full
    if (not unassigned) and isFull(grid):
        printGrid(grid)
        print "Node Count : " + str(count)
        return (True, [])
    # Searching for the next word to include based on how restricted it is (how few positions it can be included in)
    nextvar = nextVariable(grid, unassigned)
    word,locations = nextvar

    # Just checking that a failure state has not been reached by having no suitable variable that can be assigned to the grid
    if word == '0':
        return (False, [])

    # Because each word could have multiple locations that it can be assigned to, we must iterate over these locations
    for (x,y),orientation in locations:

        # Generate new grid and remove variables from unassigned before calling the recursive function
        newGrid = [a[:] for a in grid]
        newBank = unassigned[:]
        updatedGrid = assign(newGrid, word, (x,y), orientation)
        newBank.remove(word);

        # As soon as we make an assignment and recursively call the function, we increment the node counter
        count += 1
        result = recursiveCSP(updatedGrid,newBank, count)
        if result[0] == True:

            # Returns a boolean value as well as the information for the sequence of assignments leading to the end state
            return (True, [(orientation,(x,y),word)] + result[1])

    # Default case, should there be no more valid assignments to make
    return (False, [])

# Computes the number of possible permutations for each word before they
def nextVariable(grid, unassigned):
    # Attempts to find the lowest number of permutations that a word can have in the horizontal and vertical
    # And then returns a variable that has the lowest count
    # By doing this, we are attempting to find the most restricted variable assignment
    lowest = float("inf")
    nextvar = ""
    locations = []
    for item in unassigned:

        # Calculate total number of horizontal and vertical permutations
        resultH = countHorizontal(grid, item)
        resultV = countVertical(grid,item)
        totalcount = resultH[0] + resultV[0]
        if (totalcount < lowest):
            lowest = totalcount
            nextvar = item
            locations[:] = []

            # This is a simple optimisation we attempted (should we have less values for a single dimension, we should try these first before going for the other direciton)
            if resultH[0] < resultV[0]:
                locations += resultH[1] if resultH[1] else []
                locations += resultV[1] if resultV[1] else []
            else :
                locations += resultV[1] if resultV[1] else []
                locations += resultH[1] if resultH[1] else []
    if lowest == 0 or nextvar == "":
        nextvar = '0'
    return (nextvar, locations)

# Counts the number of vertical assignments for a word
def countVertical(grid, word):
    wlen = len(word)
    diff = 1
    count = 0
    possXY = []

    # If a word is shorter than the length of the row / column then we should try all possible starting coordinates for the word
    if wlen < len(grid[0]):
        diff = len(grid[0]) - wlen + 1
    for i in range(len(grid[0])):
        for j in range(diff):
            if checkVertical(grid, word, (j,i)):
                count += 1
                possXY.append(((j,i),'V'))
    return (count, possXY)

# Confirms that the variables assignment is valid given the assignment for the word (checks that the overlaps are allowed)
def checkVertical(grid, word, (x,y)):
    for w in range(len(word)):
        if not (grid[x+w][y] == word[w] or grid[x+w][y] == ' '):
            return False
    updatedGrid = assign(grid,word,(x,y),'V')

    # Checks the other constraints for the board once we are given the variable assignment
    if not checkGrid(updatedGrid):
        return False
    # printGrid(updatedGrid)
    return True

# Same as countVertical but for horizontal assignments
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

# Same as above
def checkHorizontal(grid, word, (x,y)):
    for w in range(len(word)):
        if not (grid[x][y+w] == word[w] or grid[x][y+w] == ' '):
            return False
    updatedGrid = assign(grid,word,(x,y),'H')
    if not checkGrid(updatedGrid):
        return False
    # printGrid(updatedGrid)
    return True

# Returns a grid that has the requested assignment
def assign(grid,word,(x,y),c):
    newgrid = [a[:] for a in grid]
    for w in range(len(word)):
        if c == 'V':
            newgrid[x+w][y] = word[w]
        else :
            newgrid[x][y+w] = word[w]
    return newgrid

# Checks all constraints in the grid
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

# Goal state confirmation
def isFull(grid):
    for i in range(len(grid[0])):
        for j in range(len(grid[0])):
            if grid[i][j] == ' ':
                return False
    return True

if __name__ == '__main__':
    print
    print "--------------------------------"
    print "---Running Word Sudoku Solver---"
    print "--------------------------------"
    print
    main()
