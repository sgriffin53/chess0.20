import globals

def flipToMove():
    game = globals.game
    if game['tomove'] == 'White': newtomove = 'Black'
    if game['tomove'] == 'Black': newtomove = 'White'
    game['tomove'] = newtomove
    globals.game = game

def movetouci(move):
    move_uci = ''
    move_uci += chr(move[0][0] + 97)
    move_uci += chr(7 - move[0][1] + 48 + 1)
    move_uci += chr(move[1][0] + 97)
    move_uci += chr(7 - move[1][1] + 48 + 1)
    try:
        prompiece = move[2]
        move_uci += prompiece
    except:
        pass
    return move_uci

def legalMovestoOF(legalMoves):
    globals.legalMovesOF = []
    for move in legalMoves:
        move = str(move)
        startrank = (ord(move[0]) - 97)
        startfile = (8 - int(move[1]))
        endrank = (ord(move[2]) - 97)
        endfile = (8 - int(move[3]))
        if len(move) == 5:
            prompiece = move[4]
        if len(move) == 5:
            globals.legalMovesOF.append(((startrank, startfile),(endrank, endfile),prompiece))
        else:
            globals.legalMovesOF.append(((startrank, startfile), (endrank, endfile)))
    return globals.legalMovesOF

def ucitomove(move):
    move = str(move)
    startrank = (ord(move[0]) - 97)
    startfile = (8 - int(move[1]))
    endrank = (ord(move[2]) - 97)
    endfile = (8 - int(move[3]))
    return ((startrank, startfile),(endrank, endfile))

def boardtoOF(board):
    # Converts python-chess board format to old format
    piecemap = board.piece_map()
    outboard = [
        'r', 'n', 'b', 'q', 'K', 'b', 'n', 'r',
        'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p',
        '0', '0', '0', '0', '0', '0', '0', '0',
        '0', '0', '0', '0', '0', '0', '0', '0',
        '0', '0', '0', 'R', '0', '0', '0', '0',
        '0', '0', '0', '0', '0', '0', '0', '0',
        'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P',
        'R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R',
    ]
    newboard = []
    for i in range(56,64):
        try:
            newboard.append(str(piecemap[i]))
        except:
            newboard.append('0')
    for i in range(48,56):
        try:
            newboard.append(str(piecemap[i]))
        except:
            newboard.append('0')
    for i in range(40,48):
        try:
            newboard.append(str(piecemap[i]))
        except:
            newboard.append('0')
    for i in range(32,40):
        try:
            newboard.append(str(piecemap[i]))
        except:
            newboard.append('0')
    for i in range(24,32):
        try:
            newboard.append(str(piecemap[i]))
        except:
            newboard.append('0')
    for i in range(16,24):
        try:
            newboard.append(str(piecemap[i]))
        except:
            newboard.append('0')
    for i in range(8,16):
        try:
            newboard.append(str(piecemap[i]))
        except:
            newboard.append('0')
    for i in range(0,8):
        try:
            newboard.append(str(piecemap[i]))
        except:
            newboard.append('0')
    outboard = newboard
    return outboard