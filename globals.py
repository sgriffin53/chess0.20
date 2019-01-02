global game
global player
global pieceCol
global board
global boardOF
global legalMoves
global legalMovesOF
global flipped
global clickStartBoardIndex
global clickStartPiece
global lastTileXIndex
global lastTileYIndex
global clickStartBoardIndex
global clickDragging
global clickStartSquare
global nodesSearched
global promPiece
global timeleft

timeleft = 0
promPiece = ''

nodesSearched = 0
clickDragging = False
clickStartSquare = 0
flipped = False
board = []
boardOF = []
legalMoves = []
legalMovesOF = []
pieceCol = {'P': 'White', 'R': 'White', 'N': 'White', 'B': 'White', 'Q': 'White', 'K': 'White',
            'p': 'Black', 'r': 'Black', 'n': 'Black', 'b': 'Black', 'q': 'Black', 'k': 'Black',
            '0': '0'}

player = {}
game = {}
