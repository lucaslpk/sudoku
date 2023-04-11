from solver import solve, is_valid, find_empty, print_board
from random import randint
from copy import deepcopy

def generatePuzzle(gameSize=9) :
    puzzle = [[0 for j in range(gameSize)] for i in range(gameSize)]  
    while True:
        pos = find_empty(puzzle)
        if pos :
            x = randint(1,9)
            puzzle[pos[0]][pos[1]] = x
            if is_valid(puzzle, x, pos) :
                temp = deepcopy(puzzle)
                if solve(temp) :
                    pass
                else: 
                    puzzle[pos[0]][pos[1]] = 0                
            else: 
                puzzle[pos[0]][pos[1]] = 0 
        else :
            return puzzle

def generateAndPrint() :
    print_board(generatePuzzle())

def puzzleAtLevel(blanks) :
    puzzle = generatePuzzle()
    zeroes = 0
    while zeroes < blanks :
        i, j = randint(0,8), randint(0,8)
        if puzzle[i][j] != 0 :
            puzzle[i][j] = 0
            zeroes += 1 

    return puzzle
