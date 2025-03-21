from constants.pieces import PIECE_MAPPING, PIECE_NAMES
from game.precomputed_moves import direction_offsets, PrecomputeMoveData


class Board:
  def __init__(self):
    # Bitboard representation: 12 arrays (6 white, 6 black)
    self.bitboard = [0] * 12  # Index 0-5 = White pieces, 6-11 = Black pieces
    self.num_squares_to_edge = PrecomputeMoveData()
    
    self.all_pieces = 0
    self.pieces_by_color = [0, 0]
    self.black_attacking_squares = set()
    self.white_attacking_squares = set()

  def setup_starting_pieces_from_fen(self, fen):
    """Set up the pieces on the bitboard based on the FEN string."""
    row = 0
    for fen_row in fen.split('/'):
      col = 0
      for char in fen_row:
        if char.isdigit():
          # Empty squares (represented by numbers in FEN)
          col += int(char)
        else:
          piece_type = self.get_piece_type(char)
          bit_index = row * 8 + col
          self.set_bit(piece_type, bit_index)
          col += 1
      row += 1

  def get_piece_type(self, piece_char):
    """Map piece characters to bitboard indices."""
    return PIECE_MAPPING.get(piece_char)

  def set_bit(self, piece_type, index):
    """Set a bit for a given piece at the board index."""
    if piece_type is not None:
      self.board[piece_type] |= (1 << index)

  def clear_bit(self, piece_type, index):
    """Clear a bit for a given piece at the board index."""
    if piece_type is not None:
      self.board[piece_type] &= ~(1 << index)

  def get_bit(self, piece_type, index):
    """Get the bit for a given piece at the board index."""
    if piece_type is not None:
      return (self.board[piece_type] >> index) & 1
    return 0

  def print_board(self):
    """Print the current board (bitboard representation)."""
    for i in range(64):
      square = i
      for piece_type in range(12):
        if self.get_bit(piece_type, square):
          print(f"Piece: {PIECE_NAMES[piece_type]} at square {i}")

  def is_attacked(self, color, index):
    if color == 0:  # player is white, check which squares black attacks
      return index in self.black_attacking_squares

    if color == 1:  # player is black, check which squares white attacks
      return index in self.white_attacking_squares

  def is_occupied(self, index):
    return (self.all_pieces >> index) & 1  # 1 if occupied, 0 if empty

  def is_occupied_by_color(self, color, index):
    return (self.pieces_by_color[color] >> index) & 1

  def get_attacking_squares(self):
    self.white_attacking_squares.clear()
    self.black_attacking_squares.clear()

    for square in range(64):
      piece_type = self.get_square_piece(square)
      if piece_type:
        piece_color = 0 if piece_type < 6 else 1

        moves = self.generate_moves(piece_type, square)
        if piece_color == 0:
          self.white_attacking_squares.update(moves)
        if piece_color == 1:
          self.black_attacking_squares.update(moves)

  def is_pawn(self, piece_type):
    return piece_type == 5 or piece_type == 11

  def is_knight(self, piece_type):
    return piece_type == 4 or piece_type == 10

  def is_bishop(self, piece_type):
    return piece_type == 3 or piece_type == 9

  def is_rook(self, piece_type):
    return piece_type == 2 or piece_type == 8

  def is_queen(self, piece_type):
    return piece_type == 1 or piece_type == 7

  def is_king(self, piece_type):
    return piece_type == 0 or piece_type == 6

  def is_sliding_piece(self, piece_type):
    return self.is_queen(piece_type) or self.is_rook(piece_type) or self.is_bishop(piece_type)