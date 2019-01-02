import GUI
import chess
global game
global player
import globals
import functions
import gameplay

def initNewGame(p1,p2):

    globals.game['ended'] = False
    globals.game['tomove'] = 'White'
    globals.game['nottomove'] = 'Black'
    globals.player['White'] = p1
    globals.player['Black'] = p2
    globals.timeleft = 300
    globals.board = chess.Board()
    globals.boardOF = functions.boardtoOF(globals.board)
    globals.legalMoves = globals.board.legal_moves
    globals.legalMovesOF = functions.legalMovestoOF(globals.legalMoves)

initNewGame("Human","AI")
GUI.start()