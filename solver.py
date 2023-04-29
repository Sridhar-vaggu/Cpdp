import queue
import threading 

N = 9

count = 0
def checkRow(sudoku, row, num, result_queue):
    for i in range(9):
        if sudoku[row][i] == num:
            result_queue.put(False)
            return
        
    result_queue.put(True)

def checkCol(sudoku, col, num, result_queue):
    for i in range(9):
        if sudoku[i][col] == num:
            result_queue.put(False)
            return

    result_queue.put(True)

def checkBlock(sudoku, row, col, num, result_queue):
    startRow = row - row % 3
    startCol = col - col % 3
    for i in range(3):
        for j in range(3):
            if sudoku[startRow + i][startCol + j] == num:
                result_queue.put(False)
                return

    result_queue.put(True)

def isSafe(sudoku, row, col, num):
    result_queue = queue.Queue()

    # Create threads to check the row, column, and block
    row_thread = threading.Thread(target=checkRow, args=(sudoku, row, num, result_queue))
    col_thread = threading.Thread(target=checkCol, args=(sudoku, col, num, result_queue))
    block_thread = threading.Thread(target=checkBlock, args=(sudoku, row, col, num, result_queue))

    # Start the threads
    row_thread.start()
    col_thread.start()
    block_thread.start()

    # Wait for the threads to finish
    row_thread.join()
    col_thread.join()
    block_thread.join()

    # Get the results from the queue
    row_result = result_queue.get()
    col_result = result_queue.get()
    block_result = result_queue.get()

    # If all three checks pass, return True
     
    return row_result and col_result and block_result


def solveSudoku(sudoku, row, col):
    global count 
    count += 1
    
    if count > 1000:
        return False
    
    if row== N - 1 and col == N:
        return True

    if col == N:
        row += 1
        col = 0

    if sudoku[row][col] > 0:
        return solveSudoku(sudoku, row, col + 1)

    for num in range(1, N + 1):
        if isSafe(sudoku, row, col, num):
            sudoku[row][col] = num
            
            if solveSudoku(sudoku, row, col + 1):
                return True
    
        sudoku[row][col] = 0
    return False



def solver(sudoku):
    global count
    if solveSudoku(sudoku, 0, 0):
        count = 0
        return sudoku
    else:
        count = 0
        return "no"
    
