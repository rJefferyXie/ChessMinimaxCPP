from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from game.bitboard import Board
from constants.fen import STARTING_BOARD, STARTING_BOARD_NO_PAWNS
from constants.pieces import PIECE_IMAGES


class GameWindow(QWidget):
  def __init__(self):
    super().__init__()
    self.board = Board()
    self.board.setup_starting_pieces_from_fen(STARTING_BOARD)
    self.labels = [None] * 64

    self.create_window()
    self.display_pieces()

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
        label.mousePressEvent = self.handle_square_click(row, col)

        if (row + col) % 2 == 0:
          label.setStyleSheet("background-color: rgb(232, 235, 239);")
        else:
          label.setStyleSheet("background-color: rgb(125, 135, 150);")

        self.labels[row * 8 + col] = label
        grid.addWidget(label, row, col)

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

  def handle_square_click(self, row, col):
    def on_click(_):
      self.reset_highlight()
      square_index = row * 8 + col
      print(square_index)
      piece_type = self.board.get_square_piece(square_index)

      if self.selected_piece != None and square_index in self.valid_moves:
        self.board.make_move((self.selected_square, square_index))
        if self.board.king_in_check(self.board.current_player_color):
          self.board.undo_move()
        else:
          self.board.current_player_color = 1 if self.board.current_player_color == 0 else 0
        
        self.display_pieces()
        self.reset_selection()
        return

      self.reset_selection()
      if piece_type != None:
        piece_color = 0 if piece_type < 6 else 1
        if piece_color == self.board.current_player_color:
          self.generate_valid_moves(piece_type, square_index)

    return on_click

  def generate_valid_moves(self, piece_type, position):
    self.selected_piece = piece_type
    self.selected_square = position
    self.valid_moves = self.board.generate_moves(piece_type, position)
    self.show_valid_moves()

  def show_valid_moves(self):
    for target_pos in self.valid_moves:
      label = self.labels[target_pos]
      label.setStyleSheet("background-color: rgb(51, 102, 255);")

  def reset_selection(self):
    self.valid_moves = []
    self.selected_piece = None
    self.selected_square = None
    self.reset_highlight()

  def reset_highlight(self):
    """Reset the highlight on all squares."""
    for row in range(8):
      for col in range(8):
        label = self.labels[row * 8 + col]
        if (row + col) % 2 == 0:
          label.setStyleSheet("background-color: rgb(232, 235, 239);")
        else:
          label.setStyleSheet("background-color: rgb(125, 135, 150);")
