from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from game.bitboard import Board
from constants.fen import STARTING_BOARD
from constants.pieces import PIECE_IMAGES


class GameWindow(QWidget):
  def __init__(self):
    super().__init__()
    self.board = Board()
    self.board.setup_starting_pieces_from_fen(STARTING_BOARD)
    self.labels = {}
    self.create_window()
    self.display_pieces()

  def create_window(self):
    self.setWindowTitle('8x8 Chess Board')

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

        self.labels[(row, col)] = label
        grid.addWidget(label, row, col)

  def display_pieces(self):
    """Display the pieces on the board based on the bitboard array."""
    for i in range(64):
      row, col = divmod(i, 8)
      square = i
      for piece_type in range(12):
        if self.board.get_bit(piece_type, square):
          pixmap = QPixmap(PIECE_IMAGES[piece_type])
          pixmap = pixmap.scaled(60, 60, Qt.AspectRatioMode.KeepAspectRatio)
          self.labels[(row, col)].setPixmap(pixmap)