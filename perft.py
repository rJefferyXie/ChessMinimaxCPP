from game.bitboard import Board
from constants.fen import STARTING_BOARD

from collections import defaultdict

board = Board()
board.setup_starting_pieces_from_fen(STARTING_BOARD)
moves_by_piece_type = defaultdict(int)

def perft(depth):
  if depth == 0:
    return 1

  moves = get_legal_moves()
  board.current_player_color = 1 if board.current_player_color == 0 else 0
  num_positions = 0

  for move in moves:
    piece = board.get_square_piece(move[0])
    moves_by_piece_type[piece] += 1
    
    board.make_move(move)
    num_positions += perft(depth - 1)
    board.undo_move()

  return num_positions

def get_legal_moves():
  moves = []
  for square in range(64):
    piece_type = board.get_square_piece(square)
    if not piece_type:
      continue
    
    piece_color = 0 if piece_type < 6 else 1
    if piece_color == board.current_player_color:
      for target_pos in board.generate_moves(piece_type, square):
        moves.append((square, target_pos))
  
  legal_moves = []
  for move in moves:
    board.make_move(move)
    if not board.king_in_check(board.current_player_color):
      legal_moves.append(move)
    board.undo_move()
  
  return legal_moves

print(perft(2))
print(moves_by_piece_type)