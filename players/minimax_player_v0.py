from players.helper import evaluate_board, order_moves_mvv_lva


class ComputerPlayer:
  def __init__(self, color):
    self.color = color

    self.moves_evaluated = 0
    self.total_moves_found = 0
    self.current_best_evaluation = 0

  def minimax(self, depth, game, alpha, beta, is_maximizing):
    if depth == 0 or game.is_checkmate():
      return evaluate_board(game.board.bitboard)

    best_move = None
    best_score = float("-inf") if is_maximizing else float("inf")

    moves = game.get_all_moves()
    moves = order_moves_mvv_lva(moves, game.board)
    self.total_moves_found += len(moves)

    for move in moves:
      game.make_move(move)
      self.moves_evaluated += 1
      result = self.minimax(depth - 1, game, alpha, beta, not is_maximizing)
      game.undo_move()

      current_score = result if isinstance(result, (int, float)) else result[1]

      if is_maximizing:
        if current_score > best_score:
          best_score = current_score
          best_move = move
          alpha = max(alpha, best_score)

      if not is_maximizing:
        if current_score < best_score:
          best_score = current_score
          best_move = move
          beta = min(beta, best_score)

      self.current_best_evaluation = best_score

      if beta <= alpha:
        break

    return (best_move, best_score)
