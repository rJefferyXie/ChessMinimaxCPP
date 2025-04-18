from constants.pieces import PIECE_NAMES, PIECE_VALUES, PIECE_MAPPING, PIECE_SQUARE_TABLES


def evaluate_board(board):
  score = 0

  # Material Evaluation
  for piece, value in PIECE_VALUES.items():
    white_count = board[PIECE_MAPPING[piece]].bit_count()
    black_count = board[PIECE_MAPPING[piece.lower()]].bit_count()
    score += (white_count - black_count) * value

  # Positional Evaluation
  for piece, table in PIECE_SQUARE_TABLES.items():
    white_squares = board[PIECE_MAPPING[piece]]
    black_squares = board[PIECE_MAPPING[piece.lower()]]
    for i in range(64):
      if (white_squares >> i) & 1:
        score += table[i]
      if (black_squares >> i) & 1:
        score -= table[63 - i]  # Mirrored for black

  return score


def order_moves_mvv_lva(moves, board):
  def mvv_lva(move):
    from_pos, target_pos = move
    piece = board.get_square_piece(from_pos)
    target = board.get_square_piece(target_pos)
    
    if piece != None and target != None:
      piece_value = PIECE_VALUES[PIECE_NAMES[piece].upper()]
      target_value = PIECE_VALUES[PIECE_NAMES[target].upper()]
      return (10 * target_value) - piece_value
      
    return -1
  
  return sorted(moves, key=mvv_lva, reverse=True)

def print_evaluation_stats(computer):
  moves_skipped = computer.total_moves_found - computer.moves_evaluated
  skipped_percentage = (moves_skipped / computer.total_moves_found) * 100 if computer.total_moves_found else 0

  print("\n--- Evaluation Statistics ---")
  print(f"Total Moves Found:        {computer.total_moves_found}")
  print(f"Moves Evaluated:          {computer.moves_evaluated}")
  print(f"Moves Skipped:            {moves_skipped} ({skipped_percentage:.2f}%)")
  print(f"Current Best Evaluation:  {computer.current_best_evaluation}")
  print(
    f"Branching Factor:         {computer.total_moves_found / computer.moves_evaluated:.2f}" if computer.moves_evaluated else "Branching Factor: N/A")
  print("--------------------------------\n")


def reset_evaluation_stats(computer):
  computer.moves_evaluated = 0
  computer.total_moves_found = 0
  computer.current_best_evaluation = 0
