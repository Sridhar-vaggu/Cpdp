#import numpy as np
import random
import time
import threading

SIZE = 9
LOW_EMPTY = 35
MEDIUM_EMPTY = 45
HIGH_EMPTY = 55




mtx = threading.Lock()

def generateSolvedSudokuThread(grid, generationComplete):
    with mtx:
        generateSolvedSudoku(grid)
        generationComplete = True
        
        
def generateSolvedSudoku(grid):
    # Initialize the grid with zeros
    for i in range(SIZE):
        for j in range(SIZE):
            grid[i][j] = 0
    # Generate a random solved Sudoku puzzle
    solveSudoku(grid, 0, 0)


def removeNumbers(grid, difficulty):
    # Remove numbers from the grid based on the difficulty level
    for i in range(difficulty):
        row = random.randint(0, SIZE-1)
        col = random.randint(0, SIZE-1)
        grid[row][col] = 0

def isSafe(grid, row, col, num):
    # Check if 'num' is present in the current row
    for i in range(SIZE):
        if grid[row][i] == num:
            return False
    # Check if 'num' is present in the current column
    for i in range(SIZE):
        if grid[i][col] == num:
            return False

    # Check if 'num' is present in the current 3x3 box
    boxRow = row - row % 3
    boxCol = col - col % 3
    for i in range(3):
        for j in range(3):
            if grid[boxRow + i][boxCol + j] == num:
                return False
    return True

def solveSudoku(grid, row, col):
    SIZE = 9
    if row == SIZE - 1 and col == SIZE:
        return True
    if col == SIZE:
        row += 1
        col = 0

    if grid[row][col] != 0:
        return solveSudoku(grid, row, col + 1)

    for num in range(1, SIZE + 1):
        if isSafe(grid, row, col, num):
            grid[row][col] = num
            if solveSudoku(grid, row, col + 1):
                return True
        grid[row][col] = 0

    return False

def printGrid(grid):
    for i in range(SIZE):
        for j in range(SIZE):
            if grid[i][j] == 0:
                print("- ", end="")
            else:
                print(str(grid[i][j]) + " ", end="")
        print()







def return_puzzle():
    grid = [[0 for i in range(SIZE)] for j in range(SIZE)]
    difficulty = 0
    generationComplete = False
    # Seed random number generator
    random.seed(time.time())
    '''
    # Get user input for difficulty
    difficultyStr = input("Select difficulty level (Low, Medium, High): ")
    
    if difficultyStr.lower() == "low":
        difficulty = LOW_EMPTY
    elif difficultyStr.lower() == "medium":
        difficulty = MEDIUM_EMPTY
    elif difficultyStr.lower() == "high":
        difficulty = HIGH_EMPTY
    else:
        print("Invalid difficulty level. Exiting.")
        exit(1)
    '''
    difficulty = HIGH_EMPTY
    # Generate solved Sudoku and remove numbers based on difficulty in a separate thread
    generationComplete = False

    t1 = threading.Thread(target=generateSolvedSudokuThread, args=(grid, generationComplete))
    t1.start()
    t1.join()

    with mtx:
        removeNumbers(grid, difficulty)
        # Print unsolved puzzle
        #print("Solve this Sudoku puzzle:")
        #printGrid(grid)
    '''
    # User input and validation
    while True:
        row, col, num = input("Enter row, column and number (1-9) separated by space (enter -1 -1 -1 to quit): ").split()
        row, col, num = int(row), int(col), int(num)

        if row == -1 and col == -1 and num == -1:
            break

        if 1 <= row <= 9 and 1 <= col <= 9 and 1 <= num <= 9:
            with mtx:
                if isSafe(grid, row - 1, col - 1, num):
                    grid[row - 1][col - 1] = num
                    printGrid(grid)
                else:
                    print("Invalid input. Try again.")
        else:
            print("Invalid input. Try again.")
    '''        
    return grid