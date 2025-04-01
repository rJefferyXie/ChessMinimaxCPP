from game.bitboard import Board
from constants.fen import STARTING_BOARD, KIWIPETE, POSITION3
from game.profiler import Profiler


class Game:
  def __init__(self):
    self.board = Board()
    self.board.setup_starting_pieces_from_fen(STARTING_BOARD)

    self.current_player_color = 0

    # used for undo functionality
    self.last_moves = []

  def king_in_check(self, color):
    if color == 0:
      return self.board.white_king_pos in self.board.black_attacking_squares

    if color == 1:
      return self.board.black_king_pos in self.board.white_attacking_squares

  def is_checkmate(self):
    if not self.king_in_check(self.current_player_color):
      return False

    moves = []
    for square in range(64):
      piece_type = self.board.get_square_piece(square)
      if piece_type == None:
        continue

      piece_color = 0 if piece_type < 6 else 1
      if piece_color == self.current_player_color:
        for target_pos in self.board.generate_moves(piece_type, square):
          moves.append((square, target_pos))

    for move in moves:
      self.make_move(move)
      if not self.king_in_check(1 - self.current_player_color):
        self.undo_move()
        return False
      self.undo_move()

    return True

  @Profiler.profile_function
  def get_all_moves(self):
    moves = []
    for square in range(64):
      piece_type = self.board.get_square_piece(square)
      if piece_type == None:
        continue

      piece_color = 0 if piece_type < 6 else 1
      if piece_color == self.current_player_color:
        for target_pos in self.board.generate_moves(piece_type, square):
          moves.append((square, target_pos))

    return moves

  def get_legal_moves(self):
    moves = self.get_all_moves()

    legal_moves = []
    for move in moves:
      self.make_move(move)
      if not self.king_in_check(1 - self.current_player_color):
        legal_moves.append(move)
      self.undo_move()

    return legal_moves

  @Profiler.profile_function
  def make_move(self, move):
    from_pos, target_pos = move
    piece_type = self.board.get_square_piece(from_pos)
    piece_color = 0 if piece_type < 6 else 1
    move_type = "standard"

    self.last_moves.append({
      'piece_type': piece_type,
      'from_pos': from_pos,
      'target_pos': target_pos,
      'en_passant_square': self.board.en_passant_square,
    })

    # pawn stuff
    dir = -8 if piece_color == 0 else 8
    if self.board.is_pawn(piece_type) and abs(target_pos - dir) == self.board.en_passant_square:
      enemy_pawn = self.board.get_square_piece(self.board.en_passant_square)
      self.last_moves[-1]['target_piece_type'] = enemy_pawn
      self.board.clear_bit(enemy_pawn, self.board.en_passant_square)  # perform en passant
      move_type = "en-passant"

    if self.board.is_pawn(piece_type) and abs(target_pos - from_pos) == 16:
      self.board.en_passant_square = target_pos
    else:
      self.board.en_passant_square = None

    if self.board.is_king(piece_type):
      if piece_color == 0:
        self.board.white_king_pos = target_pos
      if piece_color == 1:
        self.board.black_king_pos = target_pos

      if from_pos in self.board.king_castling_squares:
        self.last_moves[-1]['king_castling_square'] = from_pos
        self.board.king_castling_squares.discard(from_pos)

      if target_pos in self.board.rook_castling_squares:
        self.castle(piece_type, piece_color, from_pos, target_pos)
        move_type = "castle"

    if self.board.is_rook(piece_type) and from_pos in self.board.rook_castling_squares:
      self.last_moves[-1]['rook_castling_square'] = from_pos
      self.board.rook_castling_squares.discard(from_pos)

    target_piece = self.board.get_square_piece(target_pos)
    if target_piece:
      self.last_moves[-1]['target_piece_type'] = target_piece
      self.board.clear_bit(target_piece, target_pos)
      move_type = "capture"

    if move_type != "castle":
      self.board.clear_bit(piece_type, from_pos)
      self.board.set_bit(piece_type, target_pos)

    self.board.all_pieces = sum(self.board.bitboard)
    self.board.pieces_by_color = [sum(self.board.bitboard[:6]), sum(self.board.bitboard[6:])]
    self.board.get_attacking_squares()
    self.current_player_color = 1 - self.current_player_color

    return move_type

  @Profiler.profile_function
  def undo_move(self):
    if not self.last_moves:
      return

    last_move = self.last_moves.pop()
    self.board.en_passant_square = last_move['en_passant_square']

    piece_type = last_move['piece_type']
    piece_color = 0 if piece_type < 6 else 1

    from_pos = last_move['from_pos']
    target_pos = last_move['target_pos']
    target_piece_type = last_move.get('target_piece_type')
    castling_squares = last_move.get('castling_squares')
    removed_rook_castling_square = last_move.get('rook_castling_square')
    removed_king_castling_square = last_move.get('king_castling_square')

    if removed_rook_castling_square != None:
      self.board.rook_castling_squares.add(removed_rook_castling_square)

    if removed_king_castling_square:
      self.board.king_castling_squares.add(removed_king_castling_square)

    dir = -8 if piece_color == 0 else 8
    if self.board.is_pawn(piece_type) and abs(target_pos - dir) == self.board.en_passant_square:
      self.board.set_bit(target_piece_type, self.board.en_passant_square)
    else:
      self.board.set_bit(target_piece_type, target_pos)

    if castling_squares:
      self.board.rook_castling_squares.add(target_pos)
      self.board.king_castling_squares.add(from_pos)

      self.board.clear_bit(piece_type, castling_squares[1])
      self.board.clear_bit(target_piece_type, castling_squares[0])

      self.board.set_bit(piece_type, from_pos)
      self.board.set_bit(target_piece_type, target_pos)

    self.board.clear_bit(piece_type, target_pos)
    self.board.set_bit(piece_type, from_pos)

    self.board.all_pieces = sum(self.board.bitboard)
    self.board.pieces_by_color = [sum(self.board.bitboard[:6]), sum(self.board.bitboard[6:])]
    self.board.get_attacking_squares()
    self.current_player_color = 1 - self.current_player_color

  @Profiler.profile_function
  def castle(self, piece_type, piece_color, from_pos, target_pos):
    rook_piece = self.board.get_square_piece(target_pos)
    new_king_pos = None
    new_castling_squares = None

    if target_pos - from_pos == 3:  # short-side castle
      new_king_pos = target_pos - 1
      new_castling_squares = [target_pos - 2, new_king_pos]

      self.board.clear_bit(rook_piece, target_pos)
      self.board.set_bit(rook_piece, target_pos - 2)

      self.board.clear_bit(piece_type, from_pos)
      self.board.set_bit(piece_type, new_king_pos)

    elif from_pos - target_pos == 4:  # long-side castle
      new_king_pos = target_pos + 2
      new_castling_squares = [target_pos + 3, new_king_pos]

      self.board.clear_bit(rook_piece, target_pos)
      self.board.set_bit(rook_piece, target_pos + 3)

      self.board.clear_bit(piece_type, from_pos)
      self.board.set_bit(piece_type, new_king_pos)

    if piece_color == 0:
      self.board.white_king_pos = new_king_pos
    if piece_color == 1:
      self.board.black_king_pos = new_king_pos

    self.last_moves[-1]['target_piece_type'] = rook_piece
    self.last_moves[-1]['castling_squares'] = new_castling_squares
    self.board.king_castling_squares.discard(from_pos)
    self.board.rook_castling_squares.discard(target_pos)
    self.board.all_pieces = sum(self.board.bitboard)
    self.board.pieces_by_color = [sum(self.board.bitboard[:6]), sum(self.board.bitboard[6:])]
    self.board.get_attacking_squares()
