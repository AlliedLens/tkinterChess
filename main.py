"""INCOMPLETE CASTLING AND PAWN GOING TO THE END OF THE THING AND TURNING INTO SOMETHING ELSE NOT DONE!!!!!!!!"""

# cd C:\Users\nellissery\Desktop\python code\Chess
# python main.py

# to do
# pawn reaching the end
# castling
# checkmate condition(not done)

from tkinter import *
from tkinter import colorchooser
import itertools

"""...................Setup Menu.............................."""

# constants and bools
BOARD_X = 8
BOARD_Y = 8
CUBE_X = 64
CUBE_Y = 64
TEXT_SIZE = 48
COORDS = list(range(0, 8))
turn = "white" # / "black"
swap = False
theocracy = False

        # tile colour1, tile colour2, pieceColour1, pieceColour2
colours = ['#008000', '#ffff00', '#510051', '#0000ff']

borderColour = "Red"
bkgColour = "SteelBlue"

# setup menu intiialization
setup = Tk()
setup.title("setup")
setupMenu = Menu(setup)
setup.geometry("170x240")
setup.config(background="silver", menu=setupMenu)
setup.resizable(width=False, height=False)

# setup functions
def colourChanger(colourIndex):
    global colours, tile1Piece1Preview, tile1Piece2Preview, tile2Piece1Preview, tile2Piece2Preview
    colours[colourIndex] = colorchooser.askcolor()[1]
    print(colours)
    tile1Piece1Preview.grid_forget()
    tile2Piece2Preview.grid_forget()
    tile1Piece2Preview.grid_forget()
    tile2Piece1Preview.grid_forget()

    tile1Piece1Preview = Label(previewPanel, text="♔", bg=colours[0], fg=colours[2], font=("Helvetica", 64))
    tile2Piece2Preview = Label(previewPanel, text="♔", bg=colours[1], fg=colours[3], font=("Helvetica", 64))
    tile1Piece2Preview = Label(previewPanel, text="♔", bg=colours[0], fg=colours[3], font=("Helvetica", 64))
    tile2Piece1Preview = Label(previewPanel, text="♔", bg=colours[1], fg=colours[2], font=("Helvetica", 64))

    tile1Piece1Preview.grid(row=0, column=0)
    tile2Piece2Preview.grid(row=0, column=1)
    tile1Piece2Preview.grid(row=1, column=1)
    tile2Piece1Preview.grid(row=1, column=0)

# main loop
def setupMain():
    # setup menu
    global colours, tile1Piece1Preview, tile1Piece2Preview, tile2Piece1Preview, tile2Piece2Preview, previewPanel
    tileColorMenu = Menu(setupMenu, tearoff=0)
    setupMenu.add_cascade(label="Tile Colour", menu=tileColorMenu)
    tileColorMenu.add_cascade(label="Tile Colour 1", command= lambda: colourChanger(0))

    tileColorMenu.add_cascade(label="Tile Colour 2", command=lambda: colourChanger(1))

    pieceColourMenu =Menu(setupMenu, tearoff=0)
    setupMenu.add_cascade(label="Piece colour", menu=pieceColourMenu)
    pieceColourMenu.add_cascade(label="Piece Colour 1", command=lambda: colourChanger(2))
    pieceColourMenu.add_cascade(label="Piece Colour 2", command=lambda: colourChanger(3))

    gameModeMenu = Menu(setupMenu, tearoff=0)
    setupMenu.add_cascade(label="Game Mode", menu=gameModeMenu)
    gameModeMenu.add_cascade(label="Color Swaps", command=colorSwap)
    gameModeMenu.add_cascade(label="Helen Keller", command=helenKeller)
    gameModeMenu.add_cascade(label="Haitian", command=haitian)
    gameModeMenu.add_cascade(label="Theocratic", command=theocratic)

    # creating  and griding setup buttons
    startButton = Button(setup, text="Start Game", command=setup.destroy)
    startButton.grid(row=2, column=0, pady=10, sticky=W+E+N+S)

    # creating preview Panel
    previewPanel = PanedWindow(setup, bd=10, relief="raised", bg="SteelBlue")
    previewPanel.grid(row=0, column=0, sticky=W+E+N+S)

    # putting preview pieces on preview Panel
    tile1Piece1Preview = Label(previewPanel, text= "♔", bg=colours[0], fg=colours[2], font=("Helvetica", TEXT_SIZE))
    tile2Piece2Preview = Label(previewPanel, text= "♔", bg=colours[1], fg=colours[3], font=("Helvetica", TEXT_SIZE))
    tile1Piece2Preview = Label(previewPanel, text= "♔", bg=colours[0], fg=colours[3], font=("Helvetica", TEXT_SIZE))
    tile2Piece1Preview = Label(previewPanel, text= "♔", bg=colours[1], fg=colours[2], font=("Helvetica", TEXT_SIZE))

    tile1Piece1Preview.grid(row=0, column=0)
    tile2Piece2Preview.grid(row=0, column=1)
    tile1Piece2Preview.grid(row=1, column=1)
    tile2Piece1Preview.grid(row=1, column=0)


def helenKeller():
    global colours, borderColour
    colours[0] = "black"
    colours[1] = "black"
    colours[2] = "black"
    colours[3] = "black"
    borderColour = "blue"
    pass

def colorSwap():
    global swap
    swap = True

def haitian():
    global turn
    turn = "black"
    pass

def theocratic():
    global theocracy
    theocracy = True
    pass

setupMain()

setup.mainloop()

"""....................Game Board........................."""

# chess board variables
activePiece = [] # the active piece, i.e with highlighted piece, egs :[1, 1, '#008000', '♟', '#510051']
activePieceBool = "NoActivePiece" #/ "ActivePiece"
cellList = [] # list that contains all the pieces and their attributes
moves = [] # list that has the possible moves for a piece

# chess Board Constants and bools
justActivated = False # a bool designed specifically for the pieceActivate function, to make it so that the piece doesnt re-activate after it has moved
turnChange = False # bool to check if the turn has been changed in one round
coordList = [] # list with all the coordinates, note to self: xcoord is downward, while ycoord is vertical
kingMoved = False

# chess board class
class Cell:
    def __init__(self, master, xCoord, yCoord, tileColour, pieceType, pieceColour, ACTIVE):
        global activePiece, cellList, activePieceBool, justActivated
        self.yCoord = yCoord
        self.tileColour = tileColour
        self.pieceType = pieceType
        self.pieceColour = pieceColour

        currentCellCoord = (xCoord, yCoord)

        if len(cellList) < 64:
            cellList.append([xCoord, yCoord, tileColour, pieceType, pieceColour])

        def hoverAnimation(event=None): # func that gives red highlight when entering a cell
            global activePiece, activePieceBool, turn
            if turn == "white":                                                  
                if pieceType in "♙♖♗♘♕♔" and activePieceBool == "NoActivePiece":
                    pieceLabel["fg"] = borderColour
            if turn == "black":                                                  
                if pieceType in "♟♜♝♞♛♚" and activePieceBool == "NoActivePiece":
                    pieceLabel["fg"] = borderColour            

        def removeHover(event=None): # func that removes red highlight when leaving a cell
            global activePiece,activePieceBool
            if pieceType in "♔♝♞♚♖♛♟♜♘♗♕♔♙" and activePieceBool == "NoActivePiece":
                    pieceLabel["fg"] = pieceColour

        def blocked(x, y):
            global moves
            if pieceFromCoords(x,y)[4] != activePiece[4] and pieceFromCoords(x,y)[3] in "♔♝♞♚♖♛♟♜♘♗♕♔♙" :
                moves.append((x,y))
                return True # saying that the obj is blocked
            if pieceFromCoords(x,y)[4] == activePiece[4] and pieceFromCoords(x,y)[3] in "♔♝♞♚♖♛♟♜♘♗♕♙" and x in range(0,8) and y in range(0,8):
                return True
            else:
                return False

        def pawnMove(xCoordTo, yCoordTo, xCoordFrom, yCoordFrom):
            global moves
            if activePiece[3] in  "♟":                 # black pawn
                if xCoordFrom == 6 or xCoordFrom == 1:
                    if not blocked(xCoordFrom + 2, yCoordFrom):
                        moves.append((xCoordFrom + 2, yCoordFrom))
                    if not blocked(xCoordFrom + 1, yCoordFrom):
                        moves.append((xCoordFrom + 1, yCoordFrom))  
                elif not blocked(xCoordFrom + 1, yCoordFrom):
                        moves.append((xCoordFrom + 1, yCoordFrom))
                if pieceFromCoords(xCoordFrom + 1, yCoordFrom - 1)[4] != activePiece[4] and not blocked(xCoordFrom + 1, yCoordFrom - 1):
                    moves.append((xCoordFrom + 1, yCoordFrom - 1))
                if pieceFromCoords(xCoordFrom + 1, yCoordFrom + 1)[4] != activePiece[4] and not blocked(xCoordFrom + 1, yCoordFrom + 1):
                    moves.append((xCoordFrom + 1, yCoordFrom + 1))
                if (xCoordTo, yCoordTo) in moves:
                    moves = []
                    return True
            if activePiece[3] in  "♙":                 # white pawn
                if xCoordFrom == 6 or xCoordFrom == 1:
                    if not blocked(xCoordFrom - 2, yCoordFrom):
                        moves.append((xCoordFrom - 2, yCoordFrom))
                    if not blocked(xCoordFrom - 1, yCoordFrom):
                        moves.append((xCoordFrom - 1, yCoordFrom))  
                elif not blocked(xCoordFrom - 1, yCoordFrom):
                    moves.append((xCoordFrom - 1, yCoordFrom))
                if pieceFromCoords(xCoordFrom - 1, yCoordFrom - 1)[4] != activePiece[4] and not blocked(xCoordFrom - 1, yCoordFrom - 1):
                    moves.append((xCoordFrom - 1, yCoordFrom - 1))
                if pieceFromCoords(xCoordFrom - 1, yCoordFrom + 1)[4] != activePiece[4] and not blocked(xCoordFrom - 1, yCoordFrom + 1):
                    moves.append((xCoordFrom - 1, yCoordFrom + 1))
                if (xCoordTo, yCoordTo) in moves:
                     moves = []
                     return True

        def rookMove(xCoordTo, yCoordTo, xCoordFrom, yCoordFrom):
            global moves, coordList, run2
            run = True
            while run == True:
                i = 1
                f = -1
                while (xCoordFrom + f) in range(0,8) and not blocked(xCoordFrom + f, yCoordFrom):
                    moves.append((xCoordFrom + f, yCoordFrom))
                    f += -1
                f = -1    
                while (yCoordFrom + f) in range(0,8) and not blocked(xCoordFrom, yCoordFrom + f):
                    moves.append((xCoordFrom, yCoordFrom + f))
                    f += -1
                f = -1 
                while (yCoordFrom + i) in range(0,8)  and not blocked(xCoordFrom, yCoordFrom + i):
                    moves.append((xCoordFrom, yCoordFrom + i))
                    i += 1
                i = 1 
                while (xCoordFrom + i) in range(0,8) and not blocked(xCoordFrom + i, yCoordFrom):
                    moves.append((xCoordFrom + i, yCoordFrom))
                    i += 1
                i = 1 
                run = False
                if (xCoordTo, yCoordTo) in moves:
                    moves = []
                    return True

        def priestMove(xCoordTo, yCoordTo, xCoordFrom, yCoordFrom):
            global moves, coordList
            run = True
            while run == True:
                i = 1
                while (xCoordFrom - i) in range(0,8) and (yCoordFrom-i) in range(0,8) and not blocked(xCoordFrom - i, yCoordFrom - i):
                        moves.append((xCoordFrom - i, yCoordFrom - i))
                        i += 1
                i = 1
                while (xCoordFrom + i) in range(0,8) and (yCoordFrom - i) in range(0,8) and not blocked(xCoordFrom + i, yCoordFrom - i):
                    moves.append((xCoordFrom + i, yCoordFrom - i))
                    i += 1
                i = 1
                while (xCoordFrom- i) in range(0,8) and (yCoordFrom + i) in range(0,8) and not blocked(xCoordFrom - i, yCoordFrom + i):
                    moves.append((xCoordFrom - i, yCoordFrom + i))
                    i += 1
                i = 1
                while (xCoordFrom + i) in range(0,8) and (yCoordFrom + i) in range(0,8) and not blocked(xCoordFrom + i, yCoordFrom + i):
                    moves.append((xCoordFrom + i, yCoordFrom + i))
                    i += 1  
                i = 1
                run = False
                if (xCoordTo, yCoordTo) in moves:
                    moves = []
                    return True

        def knightMove(xCoordTo, yCoordTo, xCoordFrom, yCoordFrom):
            global moves, coordList
            if xCoordFrom + 2 in range(0,8) and yCoordFrom + 1 in range(0,8) and not blocked(xCoordFrom + 2, yCoordFrom + 1):
                moves.append((xCoordFrom + 2, yCoordFrom + 1))
            if xCoordFrom + 2 in range(0,8) and yCoordFrom - 1 in range(0,8) and not blocked(xCoordFrom + 2, yCoordFrom - 1):
                moves.append((xCoordFrom + 2, yCoordFrom - 1))
            if xCoordFrom - 2 in range(0,8) and yCoordFrom - 1 in range(0,8) and not blocked(xCoordFrom - 2, yCoordFrom - 1):
                moves.append((xCoordFrom - 2, yCoordFrom - 1)) 
            if xCoordFrom - 2 in range(0,8) and yCoordFrom + 1 in range(0,8) and not blocked(xCoordFrom - 2, yCoordFrom + 1):
                moves.append((xCoordFrom - 2, yCoordFrom + 1))
            if xCoordFrom + 1 in range(0,8) and yCoordFrom - 2 in range(0,8) and not blocked(xCoordFrom + 1, yCoordFrom - 2):
                moves.append((xCoordFrom + 1, yCoordFrom - 2))
            if xCoordFrom - 1 in range(0,8) and yCoordFrom + 2 in range(0,8) and not blocked(xCoordFrom - 1, yCoordFrom + 2):
                moves.append((xCoordFrom - 1, yCoordFrom + 2))
            if xCoordFrom + 1 in range(0,8) and yCoordFrom + 2 in range(0,8) and not blocked(xCoordFrom + 1, yCoordFrom + 2):
                moves.append((xCoordFrom + 1, yCoordFrom + 2))
            if xCoordFrom - 1 in range(0,8) and yCoordFrom - 2 in range(0,8) and not blocked(xCoordFrom - 1, yCoordFrom - 2):
                moves.append((xCoordFrom - 1, yCoordFrom - 2))
            if (xCoordTo, yCoordTo) in moves:
                moves = []
                return True

        def queenMove(xCoordTo, yCoordTo, xCoordFrom, yCoordFrom):
            global moves, coordList, run2
            run = True
            while run == True:
                i = 1
                while (xCoordFrom - i) in range(0,8) and (yCoordFrom-i) in range(0,8) and not blocked(xCoordFrom - i, yCoordFrom - i):
                        moves.append((xCoordFrom - i, yCoordFrom - i))
                        i += 1
                i = 1
                while (xCoordFrom + i) in range(0,8) and (yCoordFrom - i) in range(0,8) and not blocked(xCoordFrom + i, yCoordFrom - i):
                    moves.append((xCoordFrom + i, yCoordFrom - i))
                    i += 1
                i = 1
                while (xCoordFrom- i) in range(0,8) and (yCoordFrom + i) in range(0,8) and not blocked(xCoordFrom - i, yCoordFrom + i):
                    moves.append((xCoordFrom - i, yCoordFrom + i))
                    i += 1
                i = 1
                while (xCoordFrom + i) in range(0,8) and (yCoordFrom + i) in range(0,8) and not blocked(xCoordFrom + i, yCoordFrom + i):
                    moves.append((xCoordFrom + i, yCoordFrom + i))
                    i += 1
                i = 1
                f = -1
                while (xCoordFrom + f) in range(0,8) and not blocked(xCoordFrom + f, yCoordFrom):
                    moves.append((xCoordFrom + f, yCoordFrom))
                    f += -1
                f = -1    
                while (yCoordFrom + f) in range(0,8) and not blocked(xCoordFrom, yCoordFrom + f):
                    moves.append((xCoordFrom, yCoordFrom + f))
                    f += -1
                f = -1 
                while (yCoordFrom + i) in range(0,8)  and not blocked(xCoordFrom, yCoordFrom + i):
                    moves.append((xCoordFrom, yCoordFrom + i))
                    i += 1
                i = 1 
                while (xCoordFrom + i) in range(0,8) and not blocked(xCoordFrom + i, yCoordFrom):
                    moves.append((xCoordFrom + i, yCoordFrom))
                    i += 1  
                i = 1
                run = False
                if (xCoordTo, yCoordTo) in moves:
                    moves = []
                    return True

        def kingMove(xCoordTo, yCoordTo, xCoordFrom, yCoordFrom):
            global moves, cellList, kingMoved
            if xCoordFrom + 1 in range(0,8) and yCoordFrom + 1 in range(0,8) and not blocked(xCoordFrom + 1, yCoordFrom + 1):
                moves.append((xCoordFrom + 1, yCoordFrom + 1))
            if xCoordFrom + 1 in range(0,8) and yCoordFrom - 1 in range(0,8) and not blocked(xCoordFrom - 1, yCoordFrom - 1):
                moves.append((xCoordFrom - 1, yCoordFrom - 1))
            if xCoordFrom + 1 in range(0,8) and yCoordFrom - 1 in range(0,8) and not blocked(xCoordFrom + 1, yCoordFrom - 1):
                moves.append((xCoordFrom + 1, yCoordFrom - 1))
            if xCoordFrom - 1 in range(0,8) and yCoordFrom + 1 in range(0,8) and not blocked(xCoordFrom - 1, yCoordFrom + 1):
                moves.append((xCoordFrom - 1, yCoordFrom + 1))
            if xCoordFrom - 1 in range(0,8) and yCoordFrom in range(0,8) and not blocked(xCoordFrom - 1, yCoordFrom):
                moves.append((xCoordFrom - 1, yCoordFrom))
            if xCoordFrom + 1 in range(0,8) and yCoordFrom in range(0,8) and not blocked(xCoordFrom + 1, yCoordFrom):
                moves.append((xCoordFrom + 1, yCoordFrom))
            if xCoordFrom in range(0,8) and yCoordFrom + 1 in range(0,8) and not blocked(xCoordFrom, yCoordFrom + 1):
                moves.append((xCoordFrom, yCoordFrom + 1))
            if xCoordFrom in range(0,8) and yCoordFrom - 1 in range(0,8) and not blocked(xCoordFrom, yCoordFrom - 1):
                moves.append((xCoordFrom, yCoordFrom - 1))
            if not kingMoved:
                if activePiece[3] == "♚":
                    if (xCoordTo, yCoordTo) == (0,0):
                        pass
                    if (xCoordTo, yCoordTo) == (0,7):
                        pass
                if activePiece[3] == "♔":
                    if  (xCoordTo, yCoordTo) == (7,6) and not blocked(7,5) and not blocked(7,6) and pieceFromCoords(7,7)[3] == "♖":       
                        pieceFromCoords(7,6)[3] = "♔"
                        pieceFromCoords(7,5)[3] = "♖"
                        pieceFromCoords(7,7)[3] = "\u2003"
                        pieceFromCoords(7,4)[3] = "\u2003"
                        baseReDraw()
                    if (xCoordTo, yCoordTo) == (7,0):
                        pass

            if (xCoordTo, yCoordTo) in moves:
                    kingMoved = True
                    moves = []
                    return True

        def availableMove(xCoordTo, yCoordTo, xCoordFrom, yCoordFrom): # func that checks if anything is blocking the piece, and if it is folllowing piece rules
            global moves
            coordList = []
            [coordList.append((i[0], i[1])) for i in cellList]
            moves = []
            if activePiece[3] in "♟♙":
                return pawnMove(xCoordTo, yCoordTo, xCoordFrom, yCoordFrom)
            if activePiece[3] in "♖♜":
                return rookMove(xCoordTo, yCoordTo, xCoordFrom, yCoordFrom)
            if activePiece[3] in "♗♝":
                return priestMove(xCoordTo, yCoordTo, xCoordFrom, yCoordFrom)
            if activePiece[3] in "♘♞":
                return knightMove(xCoordTo, yCoordTo, xCoordFrom, yCoordFrom)
            if activePiece[3] in "♛♕":
                return queenMove(xCoordTo, yCoordTo, xCoordFrom, yCoordFrom)
            if activePiece[3] in "♚♔":
                return kingMove(xCoordTo, yCoordTo, xCoordFrom, yCoordFrom)

        def checkMate():
            allOpponentMoves = [] # takes every move the enemy can make, and checks if all of them restrict kings move completely
            if activePiece[3] == "♚":
                return True
            if activePiece[3] == "♔":
                return True

        def pieceMovement(event=None):
            global activePiece, activePieceBool, justActivated, turn, turnChange
            if turn == "white":                                                  
                if pieceType in "♙♖♗♘♕♔" and activePieceBool == "NoActivePiece":
                    activePiece = pieceFromCoords(currentCellCoord[0], currentCellCoord[1])
                    activePieceBool = "ActivePiece"
                    justActivated = True
            if turn == "black":
                if pieceType in "♟♜♝♞♛♚" and activePieceBool == "NoActivePiece":
                    activePiece = pieceFromCoords(currentCellCoord[0], currentCellCoord[1])
                    activePieceBool = "ActivePiece"
                    justActivated = True

            if activePieceBool == "ActivePiece" and not justActivated:
                clickedPiece = pieceFromCoords(currentCellCoord[0], currentCellCoord[1])
                print(clickedPiece)
                if clickedPiece[3] != "\u2003" and clickedPiece[4] != activePiece[4] and availableMove(currentCellCoord[0], currentCellCoord[1], activePiece[0], activePiece[1]): # for an opponent clicked cell
                    clickedPiece[3] = activePiece[3]
                    clickedPiece[4] = activePiece[4]
                    activePiece[3] = "\u2003"
                    activePiece = []
                    activePieceBool = "NoActivePiece"
                    if turn == "white" and not turnChange:
                        turn = "black"
                        turnChange = True
                    if turn == "black" and not turnChange:
                        turn = "white"
                        turnChange = True
                    turnChange = False      
                    baseReDraw()
                if clickedPiece[3] == "\u2003" and availableMove(currentCellCoord[0], currentCellCoord[1], activePiece[0], activePiece[1]):  # for a blank clicked cell
                    clickedPiece[3] = activePiece[3]
                    clickedPiece[4] = activePiece[4]
                    activePiece[3] = "\u2003"
                    activePiece = []
                    activePieceBool = "NoActivePiece"
                    if turn == "white" and not turnChange:
                        turn = "black"
                        turnChange = True
                    if turn == "black" and not turnChange:
                        turn = "white"
                        turnChange = True
                    turnChange = False                           
                    baseReDraw()

            justActivated = False

        def pieceDeactivate(event=None):
            global activePiece, activePieceBool
            if currentCellCoord == (activePiece[0], activePiece[1]):
                pieceLabel["fg"] = pieceColour
                activePiece = []
                activePieceBool = "NoActivePiece"


        # creating the label with the piece
        pieceLabel = Label(master, text=pieceType, bg=tileColour, fg=pieceColour, font=("Helvetica",TEXT_SIZE))
        pieceLabel.grid(row=xCoord, column=yCoord)
        
        # creating the bindings for one cell
        pieceLabel.bind("<Leave>", removeHover)
        pieceLabel.bind("<Button-1>", pieceMovement)
        pieceLabel.bind("<Button-3>", pieceDeactivate)
        pieceLabel.bind("<Enter>", hoverAnimation)



# board initialization
board = Tk()
board.title("Chess")
board.resizable(width=False, height=False)

# board functions

def createBase(): # function that creates base for the first base
    global cellList
    patternType = "DarkLight" # / "LightDark"

    # manually creating the initial positions for the pieces :(

    # black side
    Cell(boardPanel, 0, 0, colours[0], "♜", colours[2], False)
    Cell(boardPanel, 0, 1, colours[1], "♞", colours[2], False)
    Cell(boardPanel, 0, 2, colours[0], "♝", colours[2], False)
    if not theocracy:
        Cell(boardPanel, 0, 3, colours[1], "♛", colours[2], False)
    else:
        Cell(boardPanel, 0, 3, colours[1], "\u2003", colours[2], False)
    Cell(boardPanel, 0, 4, colours[0], "♚", colours[2], False)
    Cell(boardPanel, 0, 5, colours[1], "♝", colours[2], False)
    Cell(boardPanel, 0, 6, colours[0], "♞", colours[2], False)
    Cell(boardPanel, 0, 7, colours[1], "♜", colours[2], False)
    for y in COORDS:
        while y % 2 == 0:
            Cell(boardPanel, 1, y, colours[1], "♟", colours[2], False)
            break
        while y % 2 != 0:
            Cell(boardPanel, 1, y, colours[0], "♟", colours[2], False)
            break

    for x in COORDS[2:6]:
        for y in COORDS:
            if patternType == "DarkLight":
                while y % 2 == 0:
                    Cell(boardPanel, x, y, colours[0], " ", colours[2], False)
                    break
                while y % 2 != 0:
                    Cell(boardPanel, x, y, colours[1], " ", colours[3], False)
                    break
            if patternType == "LightDark":
                while y % 2 != 0:
                    Cell(boardPanel, x, y, colours[0], " ", colours[2], False)
                    break
                while y % 2 == 0:
                    Cell(boardPanel, x, y, colours[1], " ", colours[3], False)
                    break
        if patternType == "DarkLight":
           patternType = "LightDark"
        elif patternType == "LightDark":
           patternType = "DarkLight"

    # white side
    for y in COORDS:
        while y % 2 == 0:
            Cell(boardPanel, 6, y, colours[0], "♙", colours[3], False)
            break
        while y % 2 != 0:
            Cell(boardPanel, 6, y, colours[1], "♙", colours[3], False)
            break
    Cell(boardPanel, 7, 0, colours[1], "♖", colours[3], False)
    Cell(boardPanel, 7, 1, colours[0], "♘", colours[3], False)
    Cell(boardPanel, 7, 2, colours[1], "♗", colours[3], False)
    if not theocracy:
        Cell(boardPanel, 7, 3, colours[0], "♕", colours[3], False)
    else:
        Cell(boardPanel, 7, 3, colours[0], "\u2003", colours[3], False)
    Cell(boardPanel, 7, 4, colours[1], "♔", colours[3], False)
    Cell(boardPanel, 7, 5, colours[0], "♗", colours[3], False)
    Cell(boardPanel, 7, 6, colours[1], "♘", colours[3], False)
    Cell(boardPanel, 7, 7, colours[0], "♖", colours[3], False)

def baseReDraw():
    global cellList
    if not swap:
        for cell in cellList:
            Cell(boardPanel, cell[0], cell[1], cell[2], cell[3], cell[4], False)
            print(cell)
    else:
        for cell in cellList:
            x = False
            y = False
            # [7, 0, '#ffff00', '♖', '#0000ff']
            if cell[2] == colours[0] and not x:
                cell[2] = colours[1]
                x = True
            if cell[2] == colours[1] and not x:
                cell[2] = colours[0]
                x = True
            x = False
            if cell[4] == colours[2] and not y:
                cell[4] = colours[3]
                y = True
            if cell[4] == colours[3] and not y:
                cell[4] = colours[2]
                y = True
            y = False                
            Cell(boardPanel, cell[0], cell[1], cell[2], cell[3], cell[4], False)


def pieceFromCoords(row, column):
    global cellList
    y = 0
    x = column
    if row != 0:
        y = row*8
        return cellList[y + x]
    if row == 0:
        return cellList[y + x]


# note:   is a very large whitespace
# creating the panel that has the pieces
boardPanel = PanedWindow(board, bd=10, relief="raised", bg="SteelBlue")
boardPanel.grid(row=0, column=0, sticky=W + E + N + S)

# creating blank chessboard for the first time
createBase()




board.mainloop()
