import globals
import functions
import time
import GUI
from piecesquaretables import *
import time
import chess

def qsearch(alpha, beta,qdepth):
    #doesn't work
    if qdepth > 5:
        return alpha
    globals.nodesSearched += 1
    standpat = evalBoard(functions.boardtoOF(globals.board))
    if standpat >= beta: return beta
    if alpha < standpat: alpha = standpat
    legalMoves = sortLM(globals.board.legal_moves)
    for move in legalMoves:
        globals.board.push_uci(str(move))
        isCheck = globals.board.is_check()
        globals.board.pop()
        startfile = ord(move[0]) - 97
        startrank = int(move[1]) - 1
        endfile = ord(move[2]) - 97
        endrank = int(move[3]) - 1
        prompiece = None
        if len(move) > 4: prompiece = move[4]
        startsquare = chess.square(startfile, startrank)
        endsquare = chess.square(endfile, endrank)
        if globals.board.is_capture(chess.Move(startsquare, endsquare)) or isCheck:
            globals.board.push_uci(str(move))
            isTerminalNode = False
            if globals.board.is_checkmate():
                score = 99999
                isTerminalNode = True
            '''
            if globals.board.is_stalemate():
                score = 0
                isTerminalNode = True
            '''
            if not isTerminalNode: score = -qsearch(-beta, -alpha, qdepth+1)
            globals.board.pop()
            if score >= beta:
                return beta
            if score > alpha:
                alpha = score
    return alpha

def search(depth):
    starttime = time.time()
    bestScore = -9999
    globals.nodesSearched = 0
    legalMovesOF = functions.legalMovestoOF(sortLM(globals.board.legal_moves))
    bestMove = None
    legalMoves = sortLM(globals.board.legal_moves)
    depth = 0
    timeLimit = globals.timeleft / 25
    if timeLimit < 1: timeLimit = 1
    timeLimitExceeded = False
    GUI.tkRoot.title("Searching depth: " + str(depth + 1))
    while timeLimitExceeded == False:
        for move in legalMoves:
            timetaken = time.time() - starttime
            if timetaken > timeLimit:
                timeLimitExceeded = True
                break
            if bestMove == None: bestMove = move
            globals.board.push_uci(str(move))
            score = -alphaBeta(-99999,99999,depth)
            #score = -negaMax(2)
            if score > bestScore:
                bestScore = score
                bestMove = move
            globals.board.pop()
        newLegalMoves = []
        for move in legalMoves:
            if move != bestMove:
                newLegalMoves.append(move)
        newLegalMoves = [bestMove] + newLegalMoves
        legalMoves = newLegalMoves
        depth += 1
        GUI.tkRoot.title("Searching depth: "+str(depth+1))

    print "finished after depth:", (depth)
    print "nodes searched", globals.nodesSearched
    timetaken = time.time() - starttime
    print "time taken", timetaken
    nodespersec = round((globals.nodesSearched / timetaken),2)
    print "Nodes per second: ", nodespersec
    print "Move:", bestMove
    return bestMove

def sortLM(legalMoves):
    capmoves = []
    noncapmoves = []
    movedict = {}
    pieceVal = {'P': 1.00, 'B': 3.20, 'N': 3.00, 'R': 5.00, 'Q': 9.00, 'K': 1000.00}
    for move in legalMoves:
        if globals.board.is_capture(move):
            capmoves.append(str(move))
        else: noncapmoves.append(str(move))
    for move in capmoves:
        startfile = ord(move[0]) - 97
        startrank = int(move[1]) - 1
        endfile = ord(move[2]) - 97
        endrank = int(move[3]) - 1
        attackerpiece = str(globals.board.piece_at(chess.square(startfile, startrank))).upper()
        victimpiece = str(globals.board.piece_at(chess.square(endfile, endrank))).upper()
        if attackerpiece != 'NONE' and victimpiece != 'NONE':
            attackerval = pieceVal[attackerpiece]
            victimval = pieceVal[victimpiece]
            capscore = victimval - attackerval
        else: capscore = -100
        movedict[str(move)] = capscore
    movelist = []
    for key, value in sorted(movedict.iteritems(), key=lambda (k, v): (v, k)):
        movelist.append(key)
        #print "%s: %s" % (key, value)
    movelist.reverse()
    return movelist + noncapmoves

def alphaBeta(alpha,beta,depth):
    globals.nodesSearched += 1
    if depth == 0:
        globals.boardOF = functions.boardtoOF(globals.board)
        return qsearch(alpha,beta,0)
        #return evalBoard(globals.boardOF)
    for move in sortLM(globals.board.legal_moves):
        move = str(move)
        globals.board.push_uci(move)
        isTerminalNode = False
        if globals.board.is_checkmate():
            globals.board.pop()
            return 99999
            isTerminalNode = True
        '''
        if globals.board.is_stalemate():
            globals.board.pop()
            return 0
            isTerminalNode = True
        '''
        '''
        if globals.board.can_claim_threefold_repetition():
            globals.board.pop()
            return 0
            isTerminalNode = True
        '''
        if not isTerminalNode: score = -alphaBeta(-beta, -alpha, depth - 1)
        globals.board.pop()
        if score >= beta:
            return beta
        if score > alpha:
            alpha = score
    return alpha

def negaMax(depth):
    globals.nodesSearched += 1
    if depth == 0:
        globals.boardOF = functions.boardtoOF(globals.board)
        return evalBoard(globals.boardOF)
    maxScore = -9999
    for move in globals.board.legal_moves:
        move = str(move)
        globals.board.push_uci(move)
        score = -negaMax(depth - 1)
        globals.board.pop()
        if score > maxScore:
            maxScore = score
    return maxScore

def evalBoard(board):
    global evalMobilityCheck
    global legalMoves
    global pieceSquareTable, pieceSquareTableEndgame, pieceSquareTableOpening
    global knightVal, rookVal, gameStage, pawnCount

    pieceVal = {'P': 1.00, 'B': 3.20, 'N': 3.00, 'R': 5.00, 'Q': 9.00, 'K': 1000.00}
    rookVal = 5
    knightVal = 3
    score = 0
    gameStage = 'Midgame'
    a = 0
    #print gameStage
    #print queensLeft
    for piece in board:
        if piece != '0':
            p = int(a)
            tileYindex = int(a / 8)
            tileXindex = a - int(tileYindex * 8)
            pos = (tileXindex, tileYindex)
            if piece.islower():
                # piece belongs to Black
                val = pieceVal[piece.upper()]
                if piece.upper() == 'N':
                    val = knightVal
                if piece.upper() == 'R':
                    val = rookVal
                    if tileYindex == 6:
                        #black rook on white's 7th rank
                        val -= 0.2
                score -= val
            if piece.isupper():
                val = pieceVal[piece.upper()]
                if piece.upper() == 'N':
                    val = knightVal
                if piece.upper() == 'R':
                    val = rookVal
                    if tileYindex == 1:
                        #white rook on blacks 7th rank
                        val += 0.2
                score += val
            # add value from piece square table
            PSTVal = pieceSquareTable[piece][p]
            if piece.upper() == 'K' and gameStage == 'Endgame': PSTVal = pieceSquareTableEndgame[piece][p]
            if piece.upper() == 'Q' and gameStage == 'Opening': PSTVal = pieceSquareTableOpening[piece][p]
            score = score + (float(PSTVal) / 100)
            evalMobilityCheck = False
            if evalMobilityCheck:
                for (startPos, endPos) in legalMoves:
                    if startPos == pos:
                        amount = 0.02
                        if pos in [(3, 3), (4, 3), (3, 4), (4, 4)]: amount = 0.1
                        if piece.islower():
                            score -= amount
                        if piece.isupper():
                            score += amount
        a += 1
    #score = scoreWhite - scoreBlack
    #print piece, score
    #if piece.lower() != 'r' and piece.lower() != 'q' and piece != '0':
    #    print piece, pieceSquareTable[piece]
    #    score = score + (pieceSquareTable[piece] / 100)
    #print score
    if globals.board.turn == False: score = -score
    return score
