
import Tkinter
import PIL
import tkMessageBox
import globals
global tkFrame
import gameplay
from Tkinter import *
from PIL import ImageTk, Image
import functions


class TkFrame(Frame):
    # main Tk frame

    def __init__(self, parent):
        Frame.__init__(self, parent, relief=RAISED)
        self.parent = parent
        self.img = {}
        self.initUI()

    def initUI(self):
        self.parent.title("Raven Chess Engine 0.12")
        self.parent.minsize(687, 505)
        self.pack(fill=BOTH, expand=YES)


class NewGameDialog:

    def __init__(self, parent):

        global AIOption
        global flippedVar

        flippedVar = False

        top = self.top = Toplevel(parent)
        top.title("")
        #top.iconbitmap(r'icon.ico')
        lbl = Label(top, text="New Game")
        lbl.config(font=('calibri', (15)))
        lbl.grid(row=0, column=0, columnspan=2)
        # lbl.pack()

        '''
        self.e = Entry(top)
        self.e.pack(padx=5)
        self.e.focus_set()
        '''
        master = top

        lblBlack = Label(top, text="Black")
        lblBlack.config(font=('calibri', (12)))
        lblBlack.grid(row=1, column=0)

        master.blackPlayerOption = StringVar()
        master.blackPlayerOption.set("Raven 0.1")  # default value

        self.blackPlayer = OptionMenu(master, master.blackPlayerOption, "Raven 0.1", "Human")
        self.blackPlayer.config(width=15, font=('calibri', (9)), bg='white')
        self.blackPlayer.grid(row=1, column=1)

        lblWhite = Label(top, text="White")
        lblWhite.config(font=('calibri', (12)))
        lblWhite.grid(row=2, column=0)

        master.whitePlayerOption = StringVar()
        master.whitePlayerOption.set("Human")  # default value

        self.whitePlayer = OptionMenu(master, master.whitePlayerOption, "Raven 0.1", "Human")
        self.whitePlayer.config(width=15, font=('calibri', (9)), bg='white')
        self.whitePlayer.grid(row=2, column=1)
        # w.pack()

        self.var = BooleanVar()
        chkFlipped = Checkbutton(master, command=self.setflipped, variable=self.var, text="Black plays from bottom")
        chkFlipped.grid(row=3, column=0, columnspan=3)

        b = Button(top, text="Start Game", command=self.ok)
        b.grid(row=4, column=0, columnspan=3, ipadx=50)
        # b.pack(pady=5)

    def setflipped(self):
        global flippedVar

        flippedVar = self.var.get()

    def ok(self):

        global AIDepth
        global flipped, flippedVar

        blackPlayer = None
        if self.top.blackPlayerOption.get() == "Human": blackPlayer = "Human"
        if self.top.blackPlayerOption.get() == "Raven 0.1": blackPlayer = "AI"
        whitePlayer = None
        if self.top.whitePlayerOption.get() == "Human": whitePlayer = "Human"
        if self.top.whitePlayerOption.get() == "Raven 0.1": whitePlayer = "AI"
        # AIDepth = (int(self.e.get()) - 1)
        flipped = flippedVar
        initNewGame(whitePlayer, blackPlayer)
        drawBoard()
        drawPieces()

        self.top.destroy()


class AboutDialog:
    def __init__(self, parent):
        top = self.top = Toplevel(parent)
        top.title("About")
        top.iconbitmap(r'icon.ico')
        maintext = Label(top, text="Raven Chess Engine is a simple chess engine targeted mainly towards beginners.\n\n"
                                   "It searches to a depth of 2 and will always spot a mate-in-one..\n\n"
                                   "If you enjoyed this program, feel free to donate.\n"
                                   "Bitcoin: 35L7DCSR91aqpmNFwmx47NrdXigcWquuoP")
        maintext.pack()
        btnCopy = Button(top, text="Copy to Clipboard", command=copybtcaddr)
        btnCopy.pack()
        padtext = Label(top, text="\n")
        padtext.pack()
        btnOK = Button(top, text="Close", command=self.top.destroy)
        btnOK.pack(padx=40)


def copybtcaddr():
    r = Tk()
    r.withdraw()
    r.clipboard_clear()
    r.clipboard_append('35L7DCSR91aqpmNFwmx47NrdXigcWquuoP')
    r.update()  # now it stays on the clipboard after the window is closed
    r.destroy()


class PromoteDialog:

    def __init__(self, parent):
        global game
        global promPiece
        global promTkRoot

        top = self.top = Toplevel(parent)
        top.title("Promote")
        top.iconbitmap(r'icon.ico')
        photoQ = ImageTk.PhotoImage(file='pieces\BQ.png')
        photoR = ImageTk.PhotoImage(file='pieces\BR.png')
        photoB = ImageTk.PhotoImage(file='pieces\BB.png')
        photoN = ImageTk.PhotoImage(file='pieces\BN.png')
        if globals.game['tomove'] == "White":
            photoQ = ImageTk.PhotoImage(file='pieces\WQ.png')
            photoR = ImageTk.PhotoImage(file='pieces\WR.png')
            photoB = ImageTk.PhotoImage(file='pieces\WB.png')
            photoN = ImageTk.PhotoImage(file='pieces\WN.png')
        btnQ = Button(top, command=self.selPieceQ, image=photoQ)
        btnR = Button(top, command=self.selPieceR, image=photoR)
        btnB = Button(top, command=self.selPieceB, image=photoB)
        btnN = Button(top, command=self.selPieceN, image=photoN)
        btnQ.image = photoQ
        btnR.image = photoR
        btnB.image = photoB
        btnN.image = photoN
        btnQ.grid(row=0, column=0, columnspan=1, ipadx=0)
        btnR.grid(row=0, column=1, columnspan=1, ipadx=0)
        btnB.grid(row=0, column=2, columnspan=1, ipadx=0)
        btnN.grid(row=0, column=3, columnspan=1, ipadx=0)

    def selPieceQ(self):
        global promPiece
        globals.promPiece = 'Q'
        self.top.destroy()

    def selPieceR(self):
        global promPiece
        globals.promPiece = 'R'
        self.top.destroy()

    def selPieceB(self):
        global promPiece
        globals.promPiece = 'B'
        self.top.destroy()

    def selPieceN(self):
        global promPiece
        globals.promPiece = 'N'
        self.top.destroy()


def start():
    global app
    global board
    global boardCanvas
    global movesText
    global movesTextScr
    global evalLabel
    global evalLabelText
    global thinkingLabel
    global thinkingLabelText
    global topLabel, bottomLabel
    global freePlay
    global tkRoot
    global clickDragging
    global AIDepth
    global knightVal, rookVal, gameStage, pawnCount
    global flipped, flippedVar
    global boardHistory, boardHistoryPos

    global topLabel, bottomLabel, movesText, movesTextScr, btnFirst, btnPrev, btnNext, btnLast

    boardHistory = []
    boardHistoryPos = 0

    flipped = False

    knightVal = 2.5
    rookVal = 5
    gameStage = 'Opening'
    pawnCount = 16
    AIDepth = 1

    clickDragging = False
    freePlay = False

    tkRoot = Tk()
    #tkRoot.iconbitmap(r'icon.ico')
    # position/dimensions for main tk frame
    x = 100
    y = 100
    if "tv" == "tv1":
        x = 1420
        y = 100
    w = 687
    h = 505
    oldappheight = h
    oldappwidth = w
    geostring = "%dx%d+%d+%d" % (w, h, x, y)

    tkRoot.geometry(geostring)
    app = TkFrame(tkRoot)

    app.bind("<Configure>", appresize)
    boardCanvas = Canvas(app, width=480, height=480)
    boardCanvas.bind("<Button-1>", canvasClick)
    boardCanvas.bind("<ButtonRelease-1>", canvasRelease)
    boardCanvas.bind("<B1-Motion>", canvasMotion)
    # boardCanvas.config(bg="black")
    boardCanvas.pack(expand=YES)
    boardCanvas.place(x=0, y=25)

    topLabel = Label(tkRoot, bg="#000000", fg="white", bd=2, relief=GROOVE, font=('calibri', (12), 'bold'), text="")
    topLabel.place(x=495, y=28, w=180, h=40)
    bottomLabel = Label(tkRoot, bg="white", fg="black", bd=2, relief=GROOVE, font=('calibri', (12), 'bold'), text="")
    bottomLabel.place(x=495, y=460, w=180, h=40)
    # topLabel.pack()
    # movesLbl = Label(tkRoot, text="Moves")
    # movesLbl.pack()
    # movesLbl.place(x=500, y=205)

    movesText = Text(tkRoot, width=22, height=8, background="#555555", foreground="#FFFFFF")

    movesTextScr = Scrollbar(tkRoot)
    movesTextScr.config(command=movesText.yview)
    # movesTextScr.grid(row=0, column=1, sticky='nsew')
    movesText.config(yscrollcommand=movesTextScr.set)

    movesTextScr.pack(side="right", fill="y", expand=False)
    movesText.pack(side="left", fill="both", expand=True)

    # movesText.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
    movesText.place(x=500, y=180)
    movesTextScr.place(x=669, y=180, w=10, h=132)
    movesTextScr.activate(tkRoot)

    btnFirst = Button(tkRoot, text="<<", command=skipFirst)
    btnFirst.place(x=500, y=312, w=45, h=25)

    btnPrev = Button(tkRoot, text="<", command=skipPrev)
    btnPrev.place(x=545, y=312, w=45, h=25)

    btnNext = Button(tkRoot, text=">", command=skipNext)
    btnNext.place(x=590, y=312, w=45, h=25)

    btnLast = Button(tkRoot, text=">>", command=skipLast)
    btnLast.place(x=635, y=312, w=45, h=25)

    evalLabelText = StringVar()
    thinkingLabelText = StringVar()

    evalLabel = Label(tkRoot, text="Eval: 0", textvariable=evalLabelText)
    evalLabel.pack()
    evalLabel.place(x=500, y=190)
    evalLabel.place(x=50000, y=19000)

    thinkingLabel = Label(tkRoot, text="Thinking: 0%", textvariable=thinkingLabelText)
    thinkingLabel.pack()
    thinkingLabel.place(x=500, y=210)
    thinkingLabel.place(x=50000, y=21000)
    evalLabelText.set("Eval: 0")
    thinkingLabelText.set("Thinking: 0%")

    app.menubar = Menu
    # Game menu
    Menubar = Menubutton(app, text="Game", bd=0)
    Menubar.grid()
    Menubar.menu = Menu(Menubar, tearoff=0)
    Menubar["menu"] = Menubar.menu
    Menubar.menu.add_command(label="New Game", command=newgamedlg)
    Menubar.menu.add_command(label="Resign", command=resign)
    # Menubar.menu.add_command(label="New Game(ava)", command=newgameava)
    # Menubar.menu.add_command(label="New Game(hva)", command=newgamehva)
    # Menubar.menu.add_command(label="New Game(hvh)", command=newgamehvh)
    # Menubar.menu.add_command(label="Analysis", command=analysis)
    Menubar.menu.add_command(label="Exit", command=tkRoot.destroy)

    # Practice menu
    MenuPrac = Menubutton(app, text="Practice", bd=0)
    MenuPrac.grid()
    MenuPrac.menu = Menu(MenuPrac, tearoff=0)
    MenuPrac["menu"] = MenuPrac.menu
    MenuPrac.place(x=60, y=0)
    MenuPrac.menu.add_command(label="Queen and Rook Mate", command=pracQueenRookMate)
    MenuPrac.menu.add_command(label="One Queen Mate", command=pracOneQueenMate)
    MenuPrac.menu.add_command(label="One Rook Mate", command=pracOneRookMate)
    MenuPrac.menu.add_command(label="Two Bishops Mate", command=pracTwoBishopsMate)
    MenuPrac.menu.add_command(label="Bishop and Knight Mate", command=pracBishopKnightMate)

    # About Menu
    MenuAbout = Menubutton(app, text="About", bd=0)
    MenuAbout.grid()
    MenuAbout.menu = Menu(MenuAbout, tearoff=0)
    MenuAbout["menu"] = MenuAbout.menu
    MenuAbout.place(x=120, y=0)
    MenuAbout.menu.add_command(label="About", command=aboutDlg)
    tkRoot.config(menu=Menubar)
    tkRoot.update()
    initNewGame("Human", "AI")
    # game['ended'] = True
    drawBoard()
    drawPieces()
    # drawCover()
    tkRoot.after(1, gameloop)
    tkRoot.mainloop()


def aboutDlg():
    global tkRoot
    global aboutDlg
    global app

    aboutDlg = AboutDialog(app)
    d = aboutDlg
    # x = mouse.x
    # y = mouse.y
    x = 500
    y = 200
    w = 500
    h = 185
    geostring = "%dx%d+%d+%d" % (w, h, x, y)
    d.top.geometry(geostring)

    promTkRoot = tkRoot.wait_window(d.top)


def appresize(event):
    global boardCanvas
    global canvasSize
    global board
    global app
    global tkRoot
    global boardImg
    global topLabel, bottomLabel, movesText, movesTextScr, btnFirst, btnPrev, btnNext, btnLast

    boardCanvas.pack(expand=YES)
    boardCanvas.config(width=30, height=30, bg="black")
    boardCanvas.pack(expand=NO)
    appheight = app.winfo_height()
    appwidth = app.winfo_width()
    biggestDim = "height"
    canvasSize = appwidth - 202
    if appwidth > appheight:
        biggestDim = "width"
        canvasSize = appheight - 25
    if appwidth < (canvasSize + 202):
        canvasSize = appwidth - 202
    canvasSize = (int(canvasSize / 8) * 8)
    h = canvasSize
    w = canvasSize
    # boardImg.zoom(scalew, scaleh)
    boardCanvas.place(x=00, y=25, w=w, h=h)
    topLabel.place(x=(canvasSize + 10))
    bottomLabel.place(x=(canvasSize + 10), y=(canvasSize - 20))
    mtw = (appwidth - canvasSize - 45)
    movesText.place(x=(canvasSize + 10), y=80, h=(canvasSize - 135), w=(appwidth - canvasSize - 45))
    movesTextScr.place(x=(canvasSize + 10 + appwidth - canvasSize - 45), w=20, y=80, h=(canvasSize - 135))
    btnFirst.place(x=(canvasSize + 10), y=(canvasSize - 52), w=(mtw / 4) + 5)
    btnPrev.place(x=(canvasSize + 10 + 5 + (mtw / 4)), y=(canvasSize - 52), w=(mtw / 4) + 5)
    btnNext.place(x=(canvasSize + 10 + 10 + ((2 * mtw) / 4)), y=(canvasSize - 52), w=(mtw / 4) + 5)
    btnLast.place(x=(canvasSize + 10 + 15 + ((3 * mtw) / 4)), y=(canvasSize - 52), w=(mtw / 4) + 5)

    drawBoard()
    drawPieces()
    tkRoot.update()


def skipFirst():
    global boardHistory, boardHistoryPos
    boardHistoryPos = 0
    drawBoard()
    drawPieces()
    updatemovesText()
    tkRoot.update()


def skipPrev():
    global boardHistory, boardHistoryPos
    boardHistoryPos -= 1
    if boardHistoryPos < 0: boardHistoryPos = 0
    drawBoard()
    drawPieces()
    updatemovesText()
    tkRoot.update()
    pass


def skipNext():
    global boardHistory, boardHistoryPos
    boardHistoryPos += 1
    if boardHistoryPos > (len(boardHistory) - 1): boardHistoryPos = len(boardHistory) - 1
    drawBoard()
    drawPieces()
    updatemovesText()
    tkRoot.update()
    pass


def skipLast():
    global boardHistory, boardHistoryPos
    boardHistoryPos = (len(boardHistory) - 1)
    drawBoard()
    drawPieces()
    updatemovesText()
    tkRoot.update()
    pass





def pracOneRookMate():
    initPracGame("One Rook Mate")


def pracOneQueenMate():
    initPracGame("One Queen Mate")


def pracQueenRookMate():
    initPracGame("Queen and Rook Mate")


def pracTwoBishopsMate():
    initPracGame("Two Bishops Mate")


def pracBishopKnightMate():
    initPracGame("Bishop and Knight Mate")

def promdlg():
    global tkRoot
    global promDlg
    global app

    promDlg = PromoteDialog(app)
    d = promDlg
    # x = mouse.x
    # y = mouse.y
    x = 500
    y = 200
    w = 260
    h = 70
    geostring = "%dx%d+%d+%d" % (w, h, x, y)
    d.top.geometry(geostring)
    promTkRoot = tkRoot.wait_window(d.top)
    # promTkRoot.wait_window(d.top)


def newgamedlg():
    global AIOption
    global tkRoot
    d = NewGameDialog(tkRoot)
    x = 300
    y = 300
    w = 180
    h = 150
    AIOption = StringVar()
    geostring = "%dx%d+%d+%d" % (w, h, x, y)
    d.top.geometry(geostring)
    # d.top.w.grid(row=1,column=1)
    # d.top.w.pack()
    tkRoot.wait_window(d.top)


def newgamehva():
    initNewGame("Human", "AI")
    drawBoard()
    drawPieces()


def newgamehvh():
    initNewGame("Human", "Human")
    drawBoard()
    drawPieces()


def newgameava():
    initNewGame("AI", "AI")
    drawBoard()
    drawPieces()


def setAI0():
    global AILevel
    AILevel = 0


def setAI1():
    global AILevel
    AILevel = 1


def setAI2():
    global AILevel
    AILevel = 2


def gameexit():
    tkRoot.destroy()
    sys.exit()


# conversion functions


def convertMovetoNot(pieceMoved, isCapture, startSquare, endSquare):
    # make proper notation for output
    # To Add: detect when two pieces of same type can move to/capture on same square (e.g. Rexf5)

    global board
    global game
    global legalMoves
    global promPiece

    toMove = game['tomove']

    startSquareIndex = startSquare[1] * 8 + startSquare[0]  # start square board[] position
    endSquareIndex = endSquare[1] * 8 + endSquare[0]  # end square board[] position
    notStartSquare = convertPostoNot(startSquareIndex)
    notEndSquare = convertPostoNot(endSquareIndex)
    notCapture = ''
    outputCapture = ' moves to '
    outputCheck = ''
    promString = ''
    if isCapture:
        outputCapture = ' captures on '
        notCapture = 'x'
    notSign = ''
    notPiece = pieceMoved.upper()
    if notPiece == 'P':
        notPiece = ''
        if notCapture: notPiece = notStartSquare[0]
        if endSquare[1] == 0 or endSquare[1] == 7: promString = '=' + promPiece

    # ambiguity check
    numAmbigs = 0
    notAmbig = ''
    ambigFile = False
    ambigRank = False
    ambigMoves = []
    for lMove in legalMoves:
        lPiece = board[convertSquaretoPos(lMove[0])]
        if lMove[1] == endSquare and lPiece == pieceMoved and lMove != (
        startSquare, endSquare):  # chosen move and this move both move to same square and are same piece, ambiguity
            numAmbigs += 1
            if lMove[0][0] != startSquare[0]:  # files are different
                notAmbig = convertPostoNot(startSquareIndex)[0]  # set notAmbig to the file
                ambigFile = True
            if lMove[0][0] == startSquare[0]:  # files are same
                notAmbig = convertPostoNot(startSquareIndex)[1]  # set notAmbig to the rank
                ambigRank = True
            ambigMoves.append(lMove)
    # if numAmbigs > 2: notAmbig = convertPostoNot(startSquareIndex)
    '''
    numAmbigs = 0
    for ambigMove in ambigMoves:
        ambigPiece = board[convertSquaretoPos(ambigMove[0])]
        ambigMoveSQIndex = ambigMove[0][1] * 8 + ambigMove[0][0]
        ambigMoveEQIndex = ambigMove[1][1] * 8 + ambigMove[1][0]
        if (ambigMove[1] == endSquare and ambigPiece == pieceMoved and (notAmbig == convertPostoNot(ambigMoveEQIndex)[0]) or notAmbig == convertPostoNot(ambigMoveEQIndex)[1]):
            numAmbigs+=1
    '''
    if (ambigRank and ambigFile): notAmbig = convertPostoNot(startSquareIndex)
    game['check'] = False
    inCheck = isInCheck(board, kingPos[toMove], toMove)
    origLegalMoves = list(legalMoves)
    genLegalMoves()
    if inCheck:
        game['check'] = True
        outputCheck = '[check]'
        notSign += '+'
        if len(legalMoves) == 0: notSign = '#'
    # output move
    outstring = notPiece + notAmbig + notCapture + notEndSquare + promString + notSign
    if (pieceMoved.upper() == 'K'):
        if ((startSquare, endSquare) == ((4, 7), (2, 7))): outstring = "0-0-0"
        if ((startSquare, endSquare) == ((4, 0), (2, 0))): outstring = "0-0-0"
        if ((startSquare, endSquare) == ((4, 7), (6, 7))): outstring = "0-0"
        if ((startSquare, endSquare) == ((4, 0), (6, 0))): outstring = "0-0"
    legalMoves = list(origLegalMoves)
    return outstring
    # origToMove + " " + pieceMoved.upper() + " on " + notStartSquare + outputCapture + notEndSquare + " " + outputCheck


def convertXYtoBoardIndex(x, y):
    global flipped
    global canvasSize

    squareSize = canvasSize / 8
    # Converts cursor X, Y position to board array X, Y position
    returnX = int(x / squareSize)
    returnY = int(y / squareSize)
    if flipped:
        returnX = int((canvasSize - x) / squareSize)
        returnY = int((canvasSize - y) / squareSize)
    return (returnX, returnY)


def convertBoardIndextoXY(x, y):
    global flipped
    global canvasSize

    squareSize = canvasSize / 8
    # Converts board index X, Y to tile draw position X, Y
    returnX = x * squareSize
    returnY = y * squareSize
    if flipped:
        returnX = int((7 - x) * squareSize)
        returnY = int((7 - y) * squareSize)
    return (returnX, returnY)


def convertPostoNot(pos):
    # Converts a board array position to board square (e.g. 1 = a8)
    # TODO: Make more readable

    posFile = (pos % 8)  # every 8th byte is a new row
    posRank = int(round(((63 - pos) / 8),
                        0))  # each column is the nth byte in a row # use (63 - pos) to orient board as a8 = top left
    squareFile = chr((97 + posFile))
    squareRank = str((1 + posRank))
    return squareFile + squareRank


def convertSquaretoPos(square):
    # Converts a board square (e.g. (0,0)) to the board array position (e.g. 0)
    posIndex = square[0] + 8 * square[1]
    return posIndex

def checkGameOver():
    global board
    global game
    global legalMoves
    global boardHistory, boardHistoryPos

    # draw by stalemate
    if len(legalMoves) == 0:  # no legal moves available
        game['ended'] = True
        if game['check']:
            outstring = game['nottomove'] + " wins by checkmate."
            tkMessageBox.showinfo("Game over", outstring)
        if game['check'] == False:
            tkMessageBox.showinfo("Game over", "Game drawn by stalemate.")
        return

    # draw by insufficient material
    piecesLeft = []
    for piece in board:
        if piece != '0':
            piecesLeft += piece
            piecesLeft.sort()
    if (
            (piecesLeft == ['K', 'k']) or
            (piecesLeft == ['K', 'b', 'k']) or
            (piecesLeft == ['B', 'K', 'k']) or
            (piecesLeft == ['K', 'N', 'k']) or
            (piecesLeft == ['K', 'k', 'n']) or
            (piecesLeft == ['B', 'K', 'b', 'k']) or
            (piecesLeft == ['K', 'N', 'k', 'n'])
    ):
        outstring = "Draw by insufficient material."
        tkMessageBox.showinfo("Game over", outstring)
        game['ended'] = True

    # draw by three-fold repetition
    curPos = boardHistoryPos
    numReps = 0
    while curPos >= 0:
        boardState = list(boardHistory[curPos])
        if (list(boardState) == list(board)): numReps += 1
        if numReps >= 3:  # numReps == 2 (repeated twice) means that current position has occured for third time
            game['ended'] = True
            outstring = "Draw by three-fold repetition."
            tkMessageBox.showinfo("Game over", outstring)
            return
        curPos -= 2

    # draw by 50-move rule
    if game['50-move-count'] >= 100:
        game['ended'] = True
        outstring = "Draw by 50-move rule."
        tkMessageBox.showinfo("Game over", outstring)
        return

def updatemovesText():
    global movesText
    global movesList
    global moveList
    global boardHistoryPos

    outString = ""
    halfMoveNum = 0
    fullMoveNum = 1
    outPos = 0
    for move in moveList:
        halfMoveNum += 1
        if ((halfMoveNum % 2) == 1): outString += str(fullMoveNum) + ". "
        if halfMoveNum == boardHistoryPos:
            outString += "[" + move + "] "
            outPos = len(outString)
        if halfMoveNum != boardHistoryPos: outString += move + " "
        if ((halfMoveNum % 2) == 0):
            fullMoveNum += 1
            outString += "\n"

    movesText.delete(1.0, Tkinter.END)
    movesText.insert(INSERT, outString)
    movesText.see(Tkinter.END)
    # movesText.see(Tkinter.END)

def canvasClick(event):
    global clickDragging
    global ClickStartScrPos
    global clickStartPiece
    global clickStartBoardIndex
    global lastTileXIndex, lastTileYIndex
    global clickStartSquare
    global board
    global game
    global flipped
    global boardHistory, boardHistoryPos
    global canvasSize
    global player

    squareSize = canvasSize / 8

    #if boardHistoryPos != (len(boardHistory) - 1): return
    if globals.game['ended'] == False and (globals.player[globals.game['tomove']] == 'Human'):
        # User Clicks Down within board square
        mouseX = event.x
        mouseY = event.y
        # convert mouseX, mouseY to board array indices
        (tileXIndex, tileYIndex) = convertXYtoBoardIndex(mouseX, mouseY)
        # convert board indices to screen X Y position of tiles
        (tileScrX, tileScrY) = convertBoardIndextoXY(tileXIndex, tileYIndex)
        # calculate boardIndex = board[] square index
        boardIndex = tileYIndex * 8 + tileXIndex
        piece = globals.boardOF[boardIndex]
        if (piece == '0'):  # user tries to drag empty square
            return
        if (globals.pieceCol[piece] != globals.game['tomove']):
            return
        # draw green square over tile
        # boardCanvas.draw.rect(pygScreen, (0,255,0), (tileScrX + 2, tileScrY + 2, 57, 57), 4)
        boardCanvas.create_rectangle(tileScrX + 3, tileScrY + 3, (tileScrX + squareSize - 2),
                                     (tileScrY + squareSize - 2), outline="#00FF00",
                                     width=6)
        globals.clickDragging = True
        clickStartScrPos = (tileScrX, tileScrY)  # store top left screen X, Y for tile position
        globals.clickStartBoardIndex = (tileXIndex, tileYIndex)
        globals.clickStartPiece = piece
        globals.lastTileXIndex = tileXIndex
        globals.lastTileYIndex = tileYIndex
        globals.clickStartSquare = globals.clickStartBoardIndex
    if globals.game['ended'] == True:
        newgamedlg()


def canvasMotion(event):
    global lastTileScrX
    global lastTileScrY
    global lastTileXIndex
    global lastTileYIndex
    global canvasSize
    global clickStartBoardIndex
    clickDragging = globals.clickDragging
    clickStartBoardIndex = globals.clickStartBoardIndex
    lastTileXIndex = globals.lastTileXIndex
    lastTileYIndex = globals.lastTileYIndex
    clickStartSquare = globals.clickStartSquare
    if not clickDragging: return
    squareSize = canvasSize / 8
    mouseX = event.x
    mouseY = event.y
    # convert mouseX, mouseY to board array indices
    (tileXIndex, tileYIndex) = convertXYtoBoardIndex(mouseX, mouseY)
    # convert board indices to screen X Y position of tiles
    (tileScrX, tileScrY) = convertBoardIndextoXY(tileXIndex, tileYIndex)

    # clickStartBoardIndex = (tileXIndex, tileYIndex)
    # calculate boardIndex = board[] square index
    boardIndex = tileYIndex * 8 + tileXIndex
    move = (clickStartBoardIndex, (tileXIndex, tileYIndex))
    move_uci = functions.movetouci(move)
    if clickDragging:
        moveisValid = False
        for move in globals.board.legal_moves:
            if str(move)[0:4] == move_uci:
                moveisValid = True
        if moveisValid:
            # draw green square over moused over square
            boardCanvas.create_rectangle(tileScrX + 3, tileScrY + 3, (tileScrX + (squareSize - 2)),
                                         (tileScrY + (squareSize - 2)),
                                         outline="#00FF00", width=6)
        if ((lastTileXIndex != tileXIndex) or (lastTileYIndex != tileYIndex)):  # user mouses to a new square
            if (clickStartSquare != (globals.lastTileXIndex, globals.lastTileYIndex)):  # don't redraw if it's the start square
                redrawTile(globals.lastTileXIndex, globals.lastTileYIndex)  # redraw over last square (to remove green rect)
            globals.lastTileXIndex = tileXIndex
            globals.lastTileYIndex = tileYIndex
    pass


def redrawTile(x, y):
    global count
    global board
    global flipped
    global canvasSize

    squareSize = canvasSize / 8
    # redraws a tile with its piece
    boardIndex = y * 8 + x
    i = x
    j = y
    xpos = (i * squareSize) - 3
    ypos = (j * squareSize) - 3  # each tile is 60x60 px
    flipped = globals.flipped
    if flipped:
        xpos = ((7 - i) * squareSize)
        ypos = ((7 - j) * squareSize)
    col = colLight
    if (((i + j) % 2) == 0): col = colDark  # alternate tiles are dark
    # redraw tile
    drawEndX = (xpos + squareSize)
    drawEndY = (ypos + squareSize)
    if flipped:
        drawEndX = ((7 - xpos) + squareSize)
        drawEndY = ((7 - ypos) + squareSize)

    tempDrawDir = 1
    if (globals.game['tomove'] == "Black") and (flipped == True): tempDrawDir = 0
    if (globals.game['tomove'] == "White") and (flipped == True): tempDrawDir = 0
    boardCanvas.create_rectangle(xpos + 3 * tempDrawDir, ypos + 3 * tempDrawDir, (xpos + squareSize + 3 * tempDrawDir),
                                 (ypos + squareSize + 3 * tempDrawDir), fill=col, outline=col)
    # redraw piece
    piece = globals.boardOF[boardIndex]
    pieceFile = ''

    if (piece == 'R'): pieceFile = 'pieces\WR.png'  # white rook
    if (piece == 'N'): pieceFile = 'pieces\WN.png'  # white knight
    if (piece == 'B'): pieceFile = 'pieces\WB.png'  # white bishop
    if (piece == 'Q'): pieceFile = 'pieces\WQ.png'  # white queen
    if (piece == 'K'): pieceFile = 'pieces\WK.png'  # white king
    if (piece == 'P'): pieceFile = 'pieces\WP.png'  # white pawn

    if (piece == 'r'): pieceFile = 'pieces\BR.png'  # black rook
    if (piece == 'n'): pieceFile = 'pieces\BN.png'  # black knight
    if (piece == 'b'): pieceFile = 'pieces\BB.png'  # black bishop
    if (piece == 'q'): pieceFile = 'pieces\BQ.png'  # black queen
    if (piece == 'k'): pieceFile = 'pieces\BK.png'  # black king
    if (piece == 'p'): pieceFile = 'pieces\BP.png'  # black pawn
    count += 1
    if (pieceFile != ''):
        # app.img[count] = ImageTk.PhotoImage(file=pieceFile)
        # boardCanvas.create_image((xpos), (ypos), image=app.img[count], anchor=NW)

        img = Image.open(pieceFile)
        img = img.resize((squareSize - 0, squareSize - 0), Image.ANTIALIAS)
        app.img[count] = ImageTk.PhotoImage(img)
        boardCanvas.create_image(xpos + 3 * tempDrawDir, ypos + 3 * tempDrawDir, image=app.img[count], anchor=NW)
    pass


def canvasRelease(event):
    global clickDragging
    global board, tkRoot
    global boardHistory, boardHistoryPos
    clickDragging = globals.clickDragging
    clickStartBoardIndex = globals.clickStartBoardIndex
    if (clickDragging == False):
        return
    #if boardHistoryPos != (len(boardHistory) - 1): return
    clickStartBoardIndex = globals.clickStartBoardIndex
    # tkRoot.update()
    mouseX = event.x
    mouseY = event.y

    # convert mouseX, mouseY to board array indices
    (tileXindex, tileYindex) = convertXYtoBoardIndex(mouseX, mouseY)
    # convert board indices to X Y position of tiles
    # (tileScrX, tileScrY) = convertBoardIndextoXY(tileXindex, tileYindex)
    startSquare = (clickStartBoardIndex[0], clickStartBoardIndex[1])
    endSquare = (tileXindex, tileYindex)
    pieceMoved = globals.clickStartPiece
    move = (startSquare, endSquare)
    moveIsValid = False
    prompiece = ''
    # Check if move is valid
    if ((globals.clickStartBoardIndex != (tileXindex, tileYindex)) and  # not dragging onto start square
            (pieceMoved != '0')):  # not dragging from an empty square
        # Check whether move is in legalMoves[] (is legal move)
        move_uci = functions.movetouci(move)
        if move_uci[1] == '7' and move_uci[3] == '8' and globals.game['tomove'] == 'White':
            if pieceMoved.upper() == 'P':
                promdlg()
                prompiece = globals.promPiece
        if move_uci[1] == '2' and move_uci[3] == '1' and globals.game['tomove'] == 'Black':
            if pieceMoved.upper() == 'P':
                promdlg()
                prompiece = globals.promPiece
        move_uci += prompiece.lower()
       # print (move_uci in globals.legalMoves)
        for move in globals.legalMoves:
            move = str(move)
            if move == move_uci:
                moveIsValid = True
        #if (move_uci in globals.board.legal_moves): moveIsValid = True
        if moveIsValid:
            # Valid move
            # Move on board[] endsquare and zero starting square
            # makeMove((startSquare, endSquare))
            redrawTile(tileXindex, tileYindex)
            gameplay.makeMove(move_uci)
            drawBoard()
            drawPieces()
            tkRoot.update()
    if clickDragging == True:
        globals.clickDragging = False
        drawBoard()
        drawPieces()
        tkRoot.update()

def drawCover():
    boardCanvas.delete("all")
    app.cover = ImageTk.PhotoImage(file='cover_simple.PNG')
    boardCanvas.create_image(-120, 3, image=app.cover, anchor=NW)


def drawBoard():
    global boardCanvas
    global canvasSize
    global colLight, colDark
    global app
    global boardImg
    global scalw, scaleh
    board = ''
    # img = Image.Open(file='board.PNG')
    img = Image.open("board.PNG")
    img = img.resize((canvasSize, canvasSize), Image.ANTIALIAS)
    boardImg = ImageTk.PhotoImage(img)
    # boardImg.config(file='board.PNG')
    # boardImg = PhotoImage(file='board.PNG').zoom(320,320)
    # boardImg.width = scalew
    # boardImg.height = scaleh
    boardCanvas.delete("all")
    boardCanvas.create_image(3, 3, image=boardImg, anchor=NW)
    colLight = (128, 128, 128)
    colDark = (196, 196, 196)
    colLight = '#%02x%02x%02x' % colLight
    colDark = '#%02x%02x%02x' % colDark
    return
    # Draw tiles
    boardsize = 60
    for i in range(0, 8):
        for j in range(0, 8):
            xpos = (i * 60)
            ypos = (j * 60)  # each tile is 60x60 px
            col = colLight
            if (((i + j) % 2) == 0): col = colDark  # alternate tiles are dark
            # pygame.draw.rect(pygScreen, col, (xpos, ypos, 60, 60))
            boardCanvas.create_rectangle(xpos, ypos, (xpos + 65), (ypos + 65), fill=col, outline=col)


def drawPieces():
    global board
    global boardCanvas
    global canvasSize
    global app
    global count
    global flipped
    global boardHistory, boardHistoryPos

    app.img = {}
    count = 0
    dspboard = list(globals.boardOF)
    if flipped: dspboard = reversed(board)
    if boardHistoryPos != (len(boardHistory) - 1) and boardHistory != []:
        dspboard = list(boardHistory[boardHistoryPos])
        if flipped: dspboard = reversed(dspboard)
    for i in dspboard:
        # xTile goes from 0 to 7 (files)
        # yTile goes from 0 to 7 (ranks)
        xTile = (count % 8)  # every 8th byte is a new row
        yTile = int(round((count / 8), 0))  # each column is the nth byte in a row
        squareSize = int(canvasSize / 8)
        xDrawPos = (xTile * squareSize) - 3
        yDrawPos = (yTile * squareSize) - 3
        piece = i
        pieceFile = ''

        if (piece == 'R'): pieceFile = 'pieces\WR.png'  # white rook
        if (piece == 'N'): pieceFile = 'pieces\WN.png'  # white knight
        if (piece == 'B'): pieceFile = 'pieces\WB.png'  # white bishop
        if (piece == 'Q'): pieceFile = 'pieces\WQ.png'  # white queen
        if (piece == 'K'): pieceFile = 'pieces\WK.png'  # white king
        if (piece == 'P'): pieceFile = 'pieces\WP.png'  # white pawn

        if (piece == 'r'): pieceFile = 'pieces\BR.png'  # black rook
        if (piece == 'n'): pieceFile = 'pieces\BN.png'  # black knight
        if (piece == 'b'): pieceFile = 'pieces\BB.png'  # black bishop
        if (piece == 'q'): pieceFile = 'pieces\BQ.png'  # black queen
        if (piece == 'k'): pieceFile = 'pieces\BK.png'  # black king
        if (piece == 'p'): pieceFile = 'pieces\BP.png'  # black pawn

        if (pieceFile != ''):
            img = Image.open(pieceFile)
            img = img.resize((squareSize - 0, squareSize - 0), Image.ANTIALIAS)
            app.img[count] = ImageTk.PhotoImage(img)
            boardCanvas.create_image(xDrawPos + 3, yDrawPos + 3, image=app.img[count], anchor=NW)
        count += 1

def resign():
    pass

def initNewGame(p1,p2):
    pass

def gameloop():
    pass