import globals
import GUI
import functions
import random
import engine
import time
from threading import Timer
import chess.polyglot
def makeMove(move):
    #move_uci = functions.movetouci(move)
    globals.board.push_uci(move)
    globals.boardOF = functions.boardtoOF(globals.board)
    functions.flipToMove()
    globals.legalMoves = globals.board.legal_moves
    globals.legalMovesOF = functions.legalMovestoOF(globals.legalMoves)
    GUI.drawBoard()
    GUI.drawPieces()
    GUI.tkRoot.update()
    if globals.player[globals.game['tomove']] == 'AI':
        makeAIMove()

def makeAIMove():
    starttime = time.time()
    try:
        book = chess.polyglot.open_reader("performance.bin")
        bookmoves = []
        #bookmove = str(book.find(globals.board).move())
        with book as reader:
            for entry in reader.find_all(globals.board):
                bookmoves.append(str(entry.move()))
        #print bookmoves
        bookmove = bookmoves[random.randint(0,len(bookmoves) - 1)]
        print "book move:", bookmove
       # bookmove = functions.ucitomove(bookmove)
        makeMove(bookmove)
    except:
        print "Thinking..."
        move = engine.search(1)
       # randnum = random.randint(0,len(globals.legalMovesOF) -1)
        #randmove = globals.legalMovesOF[randnum]
        makeMove(move)
    globals.timeleft -= (time.time() - starttime)
    print "Time left: " + str(int(round(globals.timeleft,1) / 60)) + ":" + str(int(globals.timeleft - (int(round(globals.timeleft,1) / 60)) * 60))