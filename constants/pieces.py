# Constants for piece types
PIECE_WHITE_KING = 0
PIECE_WHITE_QUEEN = 1
PIECE_WHITE_ROOK = 2
PIECE_WHITE_BISHOP = 3
PIECE_WHITE_KNIGHT = 4
PIECE_WHITE_PAWN = 5
PIECE_BLACK_KING = 6
PIECE_BLACK_QUEEN = 7
PIECE_BLACK_ROOK = 8
PIECE_BLACK_BISHOP = 9
PIECE_BLACK_KNIGHT = 10
PIECE_BLACK_PAWN = 11

PIECE_VALUES = {
  'K': 20000,
  'Q': 900,
  'R': 500,
  'B': 330,
  'N': 320,
  'P': 100,
}

# Mapping for FEN piece characters to bitboard index
PIECE_MAPPING = {
  'K': PIECE_WHITE_KING,
  'Q': PIECE_WHITE_QUEEN,
  'R': PIECE_WHITE_ROOK,
  'B': PIECE_WHITE_BISHOP,
  'N': PIECE_WHITE_KNIGHT,
  'P': PIECE_WHITE_PAWN,
  'k': PIECE_BLACK_KING,
  'q': PIECE_BLACK_QUEEN,
  'r': PIECE_BLACK_ROOK,
  'b': PIECE_BLACK_BISHOP,
  'n': PIECE_BLACK_KNIGHT,
  'p': PIECE_BLACK_PAWN
}

PIECE_NAMES = {
  PIECE_WHITE_KING: 'K',
  PIECE_WHITE_QUEEN: 'Q',
  PIECE_WHITE_ROOK: 'R',
  PIECE_WHITE_BISHOP: 'B',
  PIECE_WHITE_KNIGHT: 'N',
  PIECE_WHITE_PAWN: 'P',
  PIECE_BLACK_KING: 'k',
  PIECE_BLACK_QUEEN: 'q',
  PIECE_BLACK_ROOK: 'r',
  PIECE_BLACK_BISHOP: 'b',
  PIECE_BLACK_KNIGHT: 'n',
  PIECE_BLACK_PAWN: 'p'
}

PIECE_IMAGES = {
  PIECE_WHITE_KING: "assets/White_King.png", PIECE_WHITE_QUEEN: "assets/White_Queen.png",
  PIECE_WHITE_ROOK: "assets/White_Rook.png", PIECE_WHITE_BISHOP: "assets/White_Bishop.png",
  PIECE_WHITE_KNIGHT: "assets/White_Knight.png", PIECE_WHITE_PAWN: "assets/White_Pawn.png",
  PIECE_BLACK_KING: "assets/Black_King.png", PIECE_BLACK_QUEEN: "assets/Black_Queen.png",
  PIECE_BLACK_ROOK: "assets/Black_Rook.png", PIECE_BLACK_BISHOP: "assets/Black_Bishop.png",
  PIECE_BLACK_KNIGHT: "assets/Black_Knight.png", PIECE_BLACK_PAWN: "assets/Black_Pawn.png"
}

SQUARES_MAP = {
  0: 'a8', 1: 'b8', 2: 'c8', 3: 'd8', 4: 'e8', 5: 'f8', 6: 'g8', 7: 'h8',
  8: 'a7', 9: 'b7', 10: 'c7', 11: 'd7', 12: 'e7', 13: 'f7', 14: 'g7', 15: 'h7',
  16: 'a6', 17: 'b6', 18: 'c6', 19: 'd6', 20: 'e6', 21: 'f6', 22: 'g6', 23: 'h6',
  24: 'a5', 25: 'b5', 26: 'c5', 27: 'd5', 28: 'e5', 29: 'f5', 30: 'g5', 31: 'h5',
  32: 'a4', 33: 'b4', 34: 'c4', 35: 'd4', 36: 'e4', 37: 'f4', 38: 'g4', 39: 'h4',
  40: 'a3', 41: 'b3', 42: 'c3', 43: 'd3', 44: 'e3', 45: 'f3', 46: 'g3', 47: 'h3',
  48: 'a2', 49: 'b2', 50: 'c2', 51: 'd2', 52: 'e2', 53: 'f2', 54: 'g2', 55: 'h2',
  56: 'a1', 57: 'b1', 58: 'c1', 59: 'd1', 60: 'e1', 61: 'f1', 62: 'g1', 63: 'h1'
}

PAWN_PS_TABLE = [
  0, 0, 0, 0, 0, 0, 0, 0,
  50, 50, 50, 50, 50, 50, 50, 50,
  10, 10, 20, 30, 30, 20, 10, 10,
  5, 5, 10, 25, 25, 10, 5, 5,
  0, 0, 0, 20, 20, 0, 0, 0,
  5, -5, -10, 0, 0, -10, -5, 5,
  5, 10, 10, -20, -20, 10, 10, 5,
  0, 0, 0, 0, 0, 0, 0, 0
]

KNIGHT_PS_TABLE = [
  -50, -40, -30, -30, -30, -30, -40, -50,
  -40, -20, 0, 0, 0, 0, -20, -40,
  -30, 0, 10, 15, 15, 10, 0, -30,
  -30, 5, 15, 20, 20, 15, 5, -30,
  -30, 0, 15, 20, 20, 15, 0, -30,
  -30, 5, 10, 15, 15, 10, 5, -30,
  -40, -20, 0, 5, 5, 0, -20, -40,
  -50, -40, -30, -30, -30, -30, -40, -50
]

BISHOP_PS_TABLE = [
  -20, -10, -10, -10, -10, -10, -10, -20,
  -10, 0, 0, 0, 0, 0, 0, -10,
  -10, 0, 5, 10, 10, 5, 0, -10,
  -10, 5, 5, 10, 10, 5, 5, -10,
  -10, 0, 10, 10, 10, 10, 0, -10,
  -10, 10, 10, 10, 10, 10, 10, -10,
  -10, 5, 0, 0, 0, 0, 5, -10,
  -20, -10, -10, -10, -10, -10, -10, -20
]

ROOK_PS_TABLE = [
  0, 0, 0, 0, 0, 0, 0, 0,
  5, 10, 10, 10, 10, 10, 10, 5,
  -5, 0, 0, 0, 0, 0, 0, -5,
  -5, 0, 0, 0, 0, 0, 0, -5,
  -5, 0, 0, 0, 0, 0, 0, -5,
  -5, 0, 0, 0, 0, 0, 0, -5,
  -5, 0, 0, 0, 0, 0, 0, -5,
  0, 0, 0, 5, 5, 0, 0, 0
]

QUEEN_PS_TABLE = [
  -20, -10, -10, -5, -5, -10, -10, -20,
  -10, 0, 0, 0, 0, 0, 0, -10,
  -10, 0, 5, 5, 5, 5, 0, -10,
  -5, 0, 5, 5, 5, 5, 0, -5,
  0, 0, 5, 5, 5, 5, 0, -5,
  -10, 5, 5, 5, 5, 5, 0, -10,
  -10, 0, 5, 0, 0, 0, 0, -10,
  -20, -10, -10, -5, -5, -10, -10, -20
]

KING_PS_TABLE = [
  -30, -40, -40, -50, -50, -40, -40, -30,
  -30, -40, -40, -50, -50, -40, -40, -30,
  -30, -40, -40, -50, -50, -40, -40, -30,
  -30, -40, -40, -50, -50, -40, -40, -30,
  -20, -30, -30, -40, -40, -30, -30, -20,
  -10, -20, -20, -20, -20, -20, -20, -10,
  20, 20, 0, 0, 0, 0, 20, 20,
  20, 30, 10, 0, 0, 10, 30, 20
]

PIECE_SQUARE_TABLES = {
  'P': PAWN_PS_TABLE,
  'N': KNIGHT_PS_TABLE,
  'B': BISHOP_PS_TABLE,
  'R': ROOK_PS_TABLE,
  'Q': QUEEN_PS_TABLE,
  'K': KING_PS_TABLE
}