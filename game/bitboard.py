from constants.pieces import PIECE_MAPPING, PIECE_NAMES
from game.precomputed_moves import direction_offsets, PrecomputeMoveData


class Board:
  def __init__(self):
    # Bitboard representation: 12 arrays (6 white, 6 black)
    self.bitboard = [0] * 12  # Index 0-5 = White pieces, 6-11 = Black pieces
    self.num_squares_to_edge = PrecomputeMoveData()
    self.current_player_color = 0

    self.all_pieces = 0
    self.pieces_by_color = [0, 0]
    self.black_attacking_squares = set()
    self.white_attacking_squares = set()

    self.king_castling_squares = set([4, 60])
    self.rook_castling_squares = set([0, 7, 56, 63])
    self.black_king_pos = 4
    self.white_king_pos = 60

    # used for undo functionality
    self.last_moves = []

    # if a pawn moves 2 tiles in one turn, this will store its position until another move is played
    self.en_passant_square = None

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
    self.all_pieces = sum(self.bitboard)
    self.pieces_by_color = [sum(self.bitboard[:6]), sum(self.bitboard[6:])]
    self.get_attacking_squares()

  def get_piece_type(self, piece_char):
    """Map piece characters to bitboard indices."""
    return PIECE_MAPPING.get(piece_char)

  def set_bit(self, piece_type, index):
    """Set a bit for a given piece at the board index."""
    if piece_type is not None:
      self.bitboard[piece_type] |= (1 << index)

  def clear_bit(self, piece_type, index):
    """Clear a bit for a given piece at the board index."""
    if piece_type is not None:
      self.bitboard[piece_type] &= ~(1 << index)

  def get_bit(self, piece_type, index):
    """Get the bit for a given piece at the board index."""
    if piece_type is not None:
      return (self.bitboard[piece_type] >> index) & 1

    return 0

  def print_board(self):
    """Print the current board (bitboard representation)."""
    for i in range(64):
      square = i
      for piece_type in range(12):
        if self.get_bit(piece_type, square):
          print(f"Piece: {PIECE_NAMES[piece_type]} at square {i}")

  def get_square_piece(self, index):
    if not self.is_occupied(index):
      return None

    for piece_type in range(12):
      if self.get_bit(piece_type, index):
        return piece_type

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
      if piece_type != None:
        piece_color = 0 if piece_type < 6 else 1

        if piece_type == 0:
          self.white_king_pos = square
        
        if piece_type == 6:
          self.black_king_pos = square

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

  def king_in_check(self, color):
    if color == 0:
      return self.white_king_pos in self.black_attacking_squares

    if color == 1:
      return self.black_king_pos in self.white_attacking_squares

  def make_move(self, move):
    from_pos, target_pos = move
    piece_type = self.get_square_piece(from_pos)
    piece_color = 0 if piece_type < 6 else 1
    move_type = "standard"

    self.last_moves.append({
      'piece_type': piece_type,
      'from_pos': from_pos,
      'target_pos': target_pos,
      'en_passant_square': self.en_passant_square,
    })

    # pawn stuff
    dir = -8 if piece_color == 0 else 8
    if self.is_pawn(piece_type) and abs(target_pos - dir) == self.en_passant_square:
      enemy_pawn = self.get_square_piece(self.en_passant_square)
      self.last_moves[-1]['target_piece_type'] = enemy_pawn
      self.clear_bit(enemy_pawn, self.en_passant_square)  # perform en passant
      move_type = "en-passant"
    
    if self.is_pawn(piece_type) and abs(target_pos - from_pos) == 16:
      self.en_passant_square = target_pos
    else:
      self.en_passant_square = None

    if self.is_king(piece_type):
      if piece_color == 0:
        self.white_king_pos = target_pos
      if piece_color == 1:
        self.black_king_pos = target_pos
        
      if from_pos in self.king_castling_squares:
        self.last_moves[-1]['king_castling_square'] = from_pos
        self.king_castling_squares.discard(from_pos)

      if target_pos in self.rook_castling_squares:
        self.castle(piece_type, piece_color, from_pos, target_pos)
        move_type = "castle"
      
    if self.is_rook(piece_type) and from_pos in self.rook_castling_squares:
      self.last_moves[-1]['rook_castling_square'] = from_pos
      self.rook_castling_squares.discard(from_pos)

    target_piece = self.get_square_piece(target_pos)
    if target_piece:
      self.last_moves[-1]['target_piece_type'] = target_piece
      self.clear_bit(target_piece, target_pos)
      move_type = "capture"

    if move_type != "castle":
      self.clear_bit(piece_type, from_pos)
      self.set_bit(piece_type, target_pos)

    self.all_pieces = sum(self.bitboard)
    self.pieces_by_color = [sum(self.bitboard[:6]), sum(self.bitboard[6:])]
    self.get_attacking_squares()
    self.current_player_color = 1 - self.current_player_color

    return move_type

  def undo_move(self):
    if not self.last_moves:
      return

    last_move = self.last_moves.pop()
    self.en_passant_square = last_move['en_passant_square']

    piece_type = last_move['piece_type']
    piece_color = 0 if piece_type < 6 else 1

    from_pos = last_move['from_pos']
    target_pos = last_move['target_pos']
    target_piece_type = last_move.get('target_piece_type')
    castling_squares = last_move.get('castling_squares')
    removed_rook_castling_square = last_move.get('rook_castling_square')
    removed_king_castling_square = last_move.get('king_castling_square')

    if removed_rook_castling_square != None:
      self.rook_castling_squares.add(removed_rook_castling_square)
    
    if removed_king_castling_square:
      self.king_castling_squares.add(removed_king_castling_square)

    dir = -8 if piece_color == 0 else 8
    if self.is_pawn(piece_type) and abs(target_pos - dir) == self.en_passant_square:
      self.set_bit(target_piece_type, self.en_passant_square)
    else:
      self.set_bit(target_piece_type, target_pos)

    if castling_squares:
      self.rook_castling_squares.add(target_pos)
      self.king_castling_squares.add(from_pos)

      self.clear_bit(piece_type, castling_squares[1])
      self.clear_bit(target_piece_type, castling_squares[0])

      self.set_bit(piece_type, from_pos)
      self.set_bit(target_piece_type, target_pos)

    self.clear_bit(piece_type, target_pos)
    self.set_bit(piece_type, from_pos)

    self.all_pieces = sum(self.bitboard)
    self.pieces_by_color = [sum(self.bitboard[:6]), sum(self.bitboard[6:])]
    self.get_attacking_squares()
    self.current_player_color = 1 - self.current_player_color

  def castle(self, piece_type, piece_color, from_pos, target_pos):
    rook_piece = self.get_square_piece(target_pos)
    new_king_pos = None
    new_castling_squares = None

    if target_pos - from_pos == 3:  # short-side castle
      new_king_pos = target_pos - 1
      new_castling_squares = [target_pos - 2, new_king_pos]

      self.clear_bit(rook_piece, target_pos)
      self.set_bit(rook_piece, target_pos - 2)

      self.clear_bit(piece_type, from_pos)
      self.set_bit(piece_type, new_king_pos)

    elif from_pos - target_pos == 4:  # long-side castle
      new_king_pos = target_pos + 2
      new_castling_squares = [target_pos + 3, new_king_pos]

      self.clear_bit(rook_piece, target_pos)
      self.set_bit(rook_piece, target_pos + 3)

      self.clear_bit(piece_type, from_pos)
      self.set_bit(piece_type, new_king_pos)

    if piece_color == 0:
      self.white_king_pos = new_king_pos
    if piece_color == 1:
      self.black_king_pos = new_king_pos

    self.last_moves[-1]['target_piece_type'] = rook_piece
    self.last_moves[-1]['castling_squares'] = new_castling_squares
    self.king_castling_squares.discard(from_pos)
    self.rook_castling_squares.discard(target_pos)
    self.all_pieces = sum(self.bitboard)
    self.pieces_by_color = [sum(self.bitboard[:6]), sum(self.bitboard[6:])]
    self.get_attacking_squares()

  def bit_scan(self, bitboard):
    """Extracts move squares from a bitboard."""
    moves = []
    while bitboard:
      index = (bitboard & -bitboard).bit_length() - 1  # Get LS1B index
      moves.append(index)
      bitboard &= bitboard - 1  # Clear LS1B
    return moves

  def generate_moves(self, piece_type, position):
    piece_color = 0 if piece_type < 6 else 1

    if self.is_sliding_piece(piece_type):
      return self.generate_sliding_moves(piece_color, position)

    if self.is_knight(piece_type):
      return self.generate_knight_moves(piece_color, position)

    if self.is_pawn(piece_type):
      return self.generate_pawn_moves(piece_color, position)

    if self.is_king(piece_type):
      return self.generate_king_moves(piece_color, position)

  def generate_sliding_moves(self, color, position):
    moves = 0
    piece_type = self.get_square_piece(position)
    start_index = 4 if self.is_bishop(piece_type) else 0
    end_index = 4 if self.is_rook(piece_type) else 8

    for direction in range(start_index, end_index):
      for i in range(self.num_squares_to_edge[position][direction]):
        square = position + direction_offsets[direction] * (i + 1)

        # blocked by friendly piece, can't move further in this direction
        if self.is_occupied_by_color(color, square):
          break

        moves |= (1 << square)

        # blocked by enemy piece, can't move any further in this direction
        if self.is_occupied_by_color(not color, square):
          break

    return self.bit_scan(moves)

  def generate_pawn_moves(self, color, position):
    pawn_moves = 0

    # if white, moving up
    if color == 0:
      if 0 <= position <= 7:  # should never be possible, pawn would have been promoted
        return []

      row_range = 2 if 48 <= position <= 55 else 1
      for i in range(row_range):
        square = position - 8 * (i + 1)

        if self.is_occupied(square):
          break

        pawn_moves |= (1 << square)  # Set bit for each upward square

      # capture diagonally
      top_left_square, top_right_square = position - 9, position - 7
      if top_left_square % 8 != 7 and self.is_occupied_by_color(not color, top_left_square):
        pawn_moves |= (1 << top_left_square)

      if top_right_square % 8 != 0 and self.is_occupied_by_color(not color, top_right_square):
        pawn_moves |= (1 << top_right_square)

    if color == 1:
      if 56 <= position <= 63:  # should never be possible, pawn would have been promoted
        return []

      row_range = 2 if 8 <= position <= 15 else 1
      for i in range(row_range):
        square = position + 8 * (i + 1)

        if self.is_occupied(square):
          break

        pawn_moves |= (1 << square)

      bottom_left_square, bottom_right_square = position + 7, position + 9
      if bottom_left_square % 8 != 7 and self.is_occupied_by_color(not color, bottom_left_square):
        pawn_moves |= (1 << bottom_left_square)

      if bottom_right_square % 8 != 0 and self.is_occupied_by_color(not color, bottom_right_square):
        pawn_moves |= (1 << bottom_right_square)

    # en passant
    if self.en_passant_square:
      en_passant_left = position - 1
      en_passant_right =  position + 1

      if (en_passant_left % 8 != 7 and self.en_passant_square == en_passant_left) or (en_passant_right % 8 != 0 and self.en_passant_square == en_passant_right):
        if self.is_occupied_by_color(not color, self.en_passant_square):
          if color == 0:
            pawn_moves |= (1 << (self.en_passant_square - 8))
          if color == 1:
            pawn_moves |= (1 << (self.en_passant_square + 8))

    return self.bit_scan(pawn_moves)

  def generate_knight_moves(self, color, position):
    knight_offsets = [-17, -15, -10, -6, 6, 10, 15, 17]
    knight_moves = 0

    row, col = position // 8, position % 8

    for offset in knight_offsets:
      target_pos = position + offset
      target_row, target_col = target_pos // 8, target_pos % 8

      if abs(target_row - row) > 2 or abs(target_col - col) > 2:
        continue

      if not 0 <= target_pos < 64:
        continue
      
      if not self.is_occupied_by_color(color, target_pos):
        knight_moves |= (1 << target_pos)

    return self.bit_scan(knight_moves)

  def generate_king_moves(self, color, position):
    king_moves = 0

    for direction in range(8):
      for i in range(min(1, self.num_squares_to_edge[position][direction])):
        square = position + direction_offsets[direction] * (i + 1)

        if self.is_occupied_by_color(color, square):
          continue

        king_moves |= (1 << square)

    # check left rook and right rook to see if we can castle
    if position in self.king_castling_squares and not self.is_attacked(color, position):
      for direction in range(2, 4):
        for i in range(self.num_squares_to_edge[position][direction]):
          square = position + direction_offsets[direction] * (i + 1)

          if self.is_occupied(square) and square not in self.rook_castling_squares:
            break

          if self.is_attacked(color, square) and abs(position - square) <= 2:  # the opponent attacks a square that the castling path needs to go over
            break

          if self.is_occupied_by_color(color, square) and square in self.rook_castling_squares:
            king_moves |= (1 << square)

    return self.bit_scan(king_moves)
