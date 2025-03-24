from game.bitboard import Board
from constants.fen import STARTING_BOARD, KIWIPETE, POSITION3
from constants.pieces import SQUARES_MAP, PIECE_IMAGES

from collections import defaultdict

from PyQt6.QtWidgets import QApplication, QWidget, QGridLayout, QLabel
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap
import sys

class GameWindow(QWidget):
  def __init__(self):
    super().__init__()
    self.board = Board()
    self.board.setup_starting_pieces_from_fen(POSITION3)
    self.labels = [None] * 64
    self.moves_by_type = defaultdict(int)
    self.moves_by_square = defaultdict(int)

    self.move_index = 0
    self.move_list = []
    self.create_window()
    self.display_pieces()
    print(self.perft(2))
    print(self.moves_by_square)
    print(self.moves_by_type)

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

    moves = self.get_legal_moves()
    num_positions = 0

    for move in moves:
      try:
        piece_type = self.board.get_square_piece(move[0])
        if self.board.is_knight(piece_type):
          self.moves_by_square["N" + SQUARES_MAP[move[1]]] += 1
        if self.board.is_pawn(piece_type):
          self.moves_by_square[SQUARES_MAP[move[1]]] += 1

        self.move_list.append(move)
        move_type = self.board.make_move(move)
        self.moves_by_type[move_type] += 1
        
        if self.board.king_in_check(self.board.current_player_color):
          self.moves_by_type["checks"] += 1

        num_positions += self.perft(depth - 1)

        self.move_list.append("undo")
        self.board.undo_move()
      except Exception as e:
        print(f"Error processing:  + {move}")

    return num_positions

  def get_legal_moves(self):
    moves = []
    for square in range(64):
      piece_type = self.board.get_square_piece(square)
      if piece_type == None:
        continue

      piece_color = 0 if piece_type < 6 else 1
      if piece_color == self.board.current_player_color:
        for target_pos in self.board.generate_moves(piece_type, square):
          moves.append((square, target_pos))
    
    legal_moves = []
    for move in moves:
      self.board.make_move(move)
      if not self.board.king_in_check(1 - self.board.current_player_color):
        legal_moves.append(move)
      self.board.undo_move()
    
    return legal_moves

  def display_pieces(self):
    """Display the pieces on the board based on the bitboard array."""
    for square in range(64):
      piece_type = self.board.get_square_piece(square)
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
        self.board.undo_move()
      else:
        self.board.make_move(move)

      self.display_pieces()
      self.move_index += 1
    else:
      self.timer.stop()  # Stop when all moves are played

app = QApplication(sys.argv)
ex = GameWindow()
ex.show()
sys.exit(app.exec())