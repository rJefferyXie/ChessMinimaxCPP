from constants.computer import WHITE, BLACK

class ComputerPlayer:
  def __init__(self, color):
    self.color = color
  
  def minimax(self, depth, game, alpha, beta, is_maximizing):
    if depth == 0 or game.is_checkmate():
      return 0

    best_move = None
    best_score = float("-inf") if is_maximizing else float("inf")

    moves = game.get_legal_moves()
    # self.total_moves_found += len(moves)

    for move in moves:
      game.make_move(move)
      current_score = self.minimax(depth - 1, game, alpha, beta, not is_maximizing)
      game.undo_move()

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

      # self.current_best_evaluation = best_score

      # if beta <= alpha, it means that the maximizing player already has a move with a better outcome than the current branch's best possible outcome
      # this means that we can can prune this branch to reduce unneccessary computations since we know that the maximizing player will never choose this branch
      # ASIDE: alpha-beta pruning assumes that both players are making optimal moves to maximize or minimize their respective scores
      if beta <= alpha:
        break

    return best_move