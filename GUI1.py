from tkinter import *
from tkinter import ttk
from solver import solver
#from solver_v2 import solver
from sudoku import return_puzzle
import time 
import threading 

wrong = []

base = Tk()
base.title("Multithreaded Sudoku")
base.geometry("550x550")

label = Label(base, text="Fill in the numbers and click solve").grid(row=0, column=1, columnspan=10)

timerFrame = ttk.Frame(base, borderwidth=2, relief="groove", style="Timer.TFrame")
timerFrame.grid(row=0, column=15, columnspan=10, padx=10, pady=10)

timerLabel = ttk.Label(timerFrame, text="", font=("Helvetica", 16), style="Timer.TLabel")
timerLabel.pack(padx=10, pady=5, expand=True, fill="both")

# Define a custom style for the timer frame and label
style = ttk.Style()
style.configure("Timer.TFrame", background="#CCCCCC")
style.configure("Timer.TLabel", foreground="white", background="#CCCCCC")
timerLabel.configure(text="Time : _ seconds")
#timerLabel.configure(text="Time")

timer = None 
start_time = None 

def update_timer():
    global timer, start_time
    if(start_time != None):
        elapsed_time = int(time.time() - start_time)
        timerLabel.configure(text="Time : " + str(elapsed_time) + " seconds")
    timer = threading.Timer(1, update_timer)
    timer.start()


def start_timer():
    global timer, start_time
    start_time = time.time()
    timer = threading.Timer(1, update_timer)
    timer.start()


errorText = Label(base, text="", fg="red")
errorText.grid(row=15, column=1, columnspan=20, pady=5)

solvedLabel = Label(base, text="", fg="green")
solvedLabel.grid(row=15, column=1, columnspan=29, pady=5)

cells = {}

def checkNumber(P):
    out = (P.isdigit() or P == "") and len(P) < 2
    return out

reg = base.register(checkNumber)

def drawblock3x3(row, column, bgcolor):
    for i in range(3):
        for j in range(3):
            ent = Entry(base, width=5, bg=bgcolor, justify="center", validate="key", validatecommand=(reg, "%P"))
            ent.grid(row=row+i+1, column=column+j+1, sticky="nsew", padx=1, pady=1, ipady=5)
            cells[(row+i+1, column+j+1)] = ent

def drawblock9x9():
    color = "#D0ffff"
    for rowNum in range(1, 10, 3):
        for colNum in range(0,9,3):
            drawblock3x3(rowNum, colNum, color)
            if color == "#D0ffff":
                color = "#ffffd0"
            else:
                color = "#D0ffff"

def clearValues():
    global timer, start_time
    errorText.configure(text="")
    solvedLabel.configure(text="")
    for row in range(2, 11):
        for col in range(1 , 10):
            cell = cells[(row, col)]
            cell.delete(0, "end")
    if timer is not None:
        timer.cancel()
        timer = None
        start_time = None
        timerLabel.configure(text="Time : _ seconds")

def getNumbers():
    board = []
    errorText.configure(text="")
    solvedLabel.configure(text="")
    for row in range(2, 11):
        rows = []
        for col in range(1, 10):
            val = cells[(row, col)].get()
            if val == "":
                rows.append(0)
            else:
                rows.append(int(val))

        board.append(rows)
    updateValues(board)
    global timer, start_time
    timer = None
    if(start_time != None):
        elapsed_time = int(time.time() - start_time)
        timerLabel.configure(text="Time : " + str(elapsed_time) + " seconds")
        start_time = None
    
    
def generate():
    puzzle = return_puzzle()
    for rows in range (2,11):
        for col in range(1,10):
            cells[(rows, col)].insert(0, puzzle[rows-2][col-1])
            if (puzzle[rows-2][col-1] == 0):
                cell = cells[(rows, col)]
                cell.delete(0, "end")
    solSudoku(puzzle)
    timer = None
    if timer is None or not timer.is_alive():
        start_timer()
    
def solSudoku(s):
    global solution
    solution = solver(s)

def validate():  
    valid = True
    errorText.configure(text="")
    solvedLabel.configure(text="")
    #print(solution)
    unsolved = 0
    for row in range(2, 11):
        for col in range(1, 10):
            val = cells[(row, col)].get()
            if val == "":
                unsolved+=1
                continue
            elif int(val) != solution[row-2][col-1]:
                print(val, " ", solution[row-2][col-1])
                wrong.append([row, col])
                valid = False
                
    if valid:
        if(unsolved == 0):
            solvedLabel.configure(text="Sudoku Solved!")
            global timer, start_time
            timer = None
            if(start_time != None):
                elapsed_time = int(time.time() - start_time)
                timerLabel.configure(text="Time : " + str(elapsed_time) + " seconds")
                start_time = None
        else:
            solvedLabel.configure(text="No incorrect entries")
    else: 
        errorText.configure(text="Wrong entry")

                
def ClearWrong(): 
    errorText.configure(text="")
    solvedLabel.configure(text="")
    if len(wrong) == 0:
        errorText.configure(text="No incorrect values")
    else:
        for entry in wrong:
            cell = cells[(entry[0], entry[1])]
            cell.delete(0, "end")
        solvedLabel.configure(text="Removed all incorrect values")


def clearTimer():
    global timer, start_time
    timerLabel.configure(text="")
    solvedLabel.configure(text="")
    #if timer is not None:
    #timer.cancel()
    timer = None
    start_time = None
    timerLabel.configure(text="Time : _ seconds")

btn = Button(base, command=generate, text="Generate", width=10)
btn.grid(row=20, column=0, columnspan=10, pady=10)

btn = Button(base, command=getNumbers, text="Solve", width=5)
btn.grid(row=20, column=10, columnspan=10, pady=10)

btn = Button(base, command=clearValues, text="Clear", width=5)
btn.grid(row=20, column=20, columnspan=10, pady=10)

btn = Button(base, command=validate, text="Validate", width=10)
btn.grid(row=21, column=0, columnspan=10, pady=10)

btn = Button(base, command=ClearWrong, text="Clear Incorrect", width=10)
btn.grid(row=21, column=10, columnspan=10, pady=10)

btn = Button(base, command=clearTimer, text="Clear Timer", width=10)
btn.grid(row=21, column=20, columnspan=10, pady=10)



def updateValues(s):
    sol = solver(s)
    if sol != "no":
        for rows in range(2, 11):
            for col in range(1, 10):
                cells[(rows, col)].delete(0, "end")
                cells[(rows, col)].insert(0, sol[rows -2 ][col - 1])
        solvedLabel.configure(text="Sudoku solved!")
    else:
        errorText.configure(text="No solution exists for this sudoku")






drawblock9x9()
base.mainloop()
