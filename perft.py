from game.game import Game
from constants.fen import STARTING_BOARD, KIWIPETE, POSITION3
from constants.pieces import SQUARES_MAP, PIECE_IMAGES

from collections import defaultdict

from PyQt6.QtWidgets import QApplication, QWidget, QGridLayout, QLabel
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap
import sys


# change these for testing purposes as you need
# https://www.chessprogramming.org/Perft_Results
SEARCH_DEPTH = 3
SEARCH_BOARD = STARTING_BOARD


class GameWindow(QWidget):
  def __init__(self):
    super().__init__()
    self.game = Game()
    self.game.board.setup_starting_pieces_from_fen(SEARCH_BOARD)
    self.labels = [None] * 64
    self.moves_by_type = defaultdict(int)
    self.moves_by_square = defaultdict(int)

    self.move_index = 0
    self.move_list = []
    self.create_window()
    self.display_pieces()

    print(self.perft(SEARCH_DEPTH))
    self.print_move_type_results()

    self.timer = QTimer()
    self.timer.timeout.connect(self.play_next_move)
    self.timer.start(200)

    self.selected_piece = None
    self.selected_square = None
    self.valid_moves = []

  def create_window(self):
    self.setWindowTitle('8x8 Chess Board')
    self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)

    grid = QGridLayout()
    grid.setSpacing(0)
    grid.setContentsMargins(0, 0, 0, 0)
    self.setLayout(grid)
    self.setGeometry(100, 100, 480, 480)

    for row in range(8):
      for col in range(8):
        label = QLabel()
        label.setFixedSize(60, 60)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        if (row + col) % 2 == 0:
          label.setStyleSheet("background-color: rgb(232, 235, 239);")
        else:
          label.setStyleSheet("background-color: rgb(125, 135, 150);")

        self.labels[row * 8 + col] = label
        grid.addWidget(label, row, col)

  def perft(self, depth):
    if depth == 0:
      return 1

    moves = self.game.get_legal_moves()
    num_positions = 0

    for move in moves:
      try:
        piece_type = self.game.board.get_square_piece(move[0])
        if self.game.board.is_knight(piece_type):
          self.moves_by_square["N" + SQUARES_MAP[move[1]]] += 1
        if self.game.board.is_pawn(piece_type):
          self.moves_by_square[SQUARES_MAP[move[1]]] += 1

        self.move_list.append(move)
        move_type = self.game.make_move(move)
        self.moves_by_type[(depth, move_type)] += 1

        if move_type == "en-passant":
          self.moves_by_type[(depth, "capture")] += 1

        if self.game.king_in_check(self.game.current_player_color):
          self.moves_by_type[(depth, "checks")] += 1
        
        if self.game.is_checkmate():
          self.moves_by_type[(depth, "checkmates")] += 1

        num_positions += self.perft(depth - 1)

        self.move_list.append("undo")
        self.game.undo_move()
      except Exception as e:
        print(f"Error processing move: {move}")

    return num_positions

  def print_move_type_results(self):
    results_by_depths = defaultdict(dict)
    for depth, move_type in self.moves_by_type.keys():
      if move_type == "standard":
        continue

      if move_type in results_by_depths[SEARCH_DEPTH - depth]:
        results_by_depths[SEARCH_DEPTH - depth][move_type] += self.moves_by_type[(depth, move_type)]
      else:
        results_by_depths[SEARCH_DEPTH - depth][move_type] = self.moves_by_type[(depth, move_type)]

    for depth, counts in results_by_depths.items():
      if counts:
        print(f"Depth: {depth + 1} --> {counts}")

  def display_pieces(self):
    for square in range(64):
      piece_type = self.game.board.get_square_piece(square)
      if piece_type != None:
        pixmap = QPixmap(PIECE_IMAGES[piece_type])
        pixmap = pixmap.scaled(60, 60, Qt.AspectRatioMode.KeepAspectRatio)
        self.labels[square].setPixmap(pixmap)
      else:
        self.labels[square].clear()

  def play_next_move(self):
    if self.move_index < len(self.move_list):
      move = self.move_list[self.move_index]
      if move == "undo":
        self.game.undo_move()
      else:
        self.game.make_move(move)

      self.display_pieces()
      self.move_index += 1
    else:
      self.timer.stop()  # Stop when all moves are played


app = QApplication(sys.argv)
ex = GameWindow()
ex.show()
sys.exit(app.exec())
