from game.bitboard import Board
from constants.fen import STARTING_BOARD, KIWIPETE, POSITION3
from constants.pieces import SQUARES_MAP

from collections import defaultdict

board = Board()
board.setup_starting_pieces_from_fen(KIWIPETE)
moves_by_type = defaultdict(int)
moves_by_square = defaultdict(int)

def perft(depth):
  if depth == 0:
    return 1

  moves = get_legal_moves()
  num_positions = 0

  for move in moves:
    piece_type = board.get_square_piece(move[0])
    if board.is_knight(piece_type):
      moves_by_square["N" + SQUARES_MAP[move[1]]] += 1
    if board.is_pawn(piece_type):
      moves_by_square[SQUARES_MAP[move[1]]] += 1

    move_type = board.make_move(move)
    moves_by_type[move_type] += 1

    if board.king_in_check(board.current_player_color):
      moves_by_type["checks"] += 1

    num_positions += perft(depth - 1)
    board.undo_move()

  return num_positions

def get_legal_moves():
  moves = []
  for square in range(64):
    piece_type = board.get_square_piece(square)
    if piece_type == None:
      continue

    piece_color = 0 if piece_type < 6 else 1
    if piece_color == board.current_player_color:
      for target_pos in board.generate_moves(piece_type, square):
        moves.append((square, target_pos))
  
  legal_moves = []
  for move in moves:
    board.make_move(move)
    if not board.king_in_check(1 - board.current_player_color):
      legal_moves.append(move)
    board.undo_move()
  
  return legal_moves

print(perft(1))
print(moves_by_type)
# print(sorted(moves_by_square.items(), key=lambda x: (-x[1], x[0])))
moves_by_type.clear()
moves_by_square.clear()

print(perft(2))
print(moves_by_type)
# print(sorted(moves_by_square.items(), key=lambda x: (-x[1], x[0])))
moves_by_type.clear()
moves_by_square.clear()

print(perft(3))
print(moves_by_type)
# # print(sorted(moves_by_square.items(), key=lambda x: (-x[1], x[0])))
# moves_by_type.clear()
# moves_by_square.clear()

# print(perft(4))
# print(moves_by_type)
# # print(sorted(moves_by_square.items(), key=lambda x: (-x[1], x[0])))
# moves_by_type.clear()
# moves_by_square.clear()