from constants.pieces import PIECE_MAPPING, PIECE_NAMES

class Board:
  def __init__(self):
    self.board = [0] * 12  # One for each piece type (6 types, 2 colors each)

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
