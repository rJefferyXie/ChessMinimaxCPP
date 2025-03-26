from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QKeyEvent
from game.game import Game
from constants.fen import STARTING_BOARD, KIWIPETE, POSITION3
from constants.pieces import PIECE_IMAGES

from players.minimax_player_v0 import ComputerPlayer


class GameWindow(QWidget):
  def __init__(self):
    super().__init__()
    self.game = Game()
    self.computer = ComputerPlayer("black")

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
    
    self.installEventFilter(self)

  def display_pieces(self):
    """Display the pieces on the board based on the bitboard array."""
    for square in range(64):
      piece_type = self.game.board.get_square_piece(square)
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
      piece_type = self.game.board.get_square_piece(square_index)

      if self.selected_piece != None and square_index in self.valid_moves:
        self.game.make_move((self.selected_square, square_index))
        if self.game.king_in_check(1 - self.game.current_player_color):
          self.game.undo_move()

        self.display_pieces()
        self.reset_selection()

        ai_move = self.computer.minimax(1, self.game, float('-inf'), float('inf'), False)
        self.game.make_move(ai_move)
        
        self.display_pieces()
        self.reset_selection()
        return

      self.reset_selection()
      if piece_type != None:
        piece_color = 0 if piece_type < 6 else 1
        if piece_color == self.game.current_player_color:
          self.generate_valid_moves(piece_type, square_index)

    return on_click

  def generate_valid_moves(self, piece_type, position):
    self.selected_piece = piece_type
    self.selected_square = position
    self.valid_moves = self.game.board.generate_moves(piece_type, position)
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

  def eventFilter(self, obj, event):
    """Event filter to handle key press for 'u'."""
    if event.type() == QKeyEvent.Type.KeyPress:
        if isinstance(event, QKeyEvent):
            if event.key() == Qt.Key.Key_U:
                self.game.undo_move()
                self.display_pieces()
                return True
    return super().eventFilter(obj, event)

  def reset_highlight(self):
    """Reset the highlight on all squares."""
    for row in range(8):
      for col in range(8):
        label = self.labels[row * 8 + col]
        if (row + col) % 2 == 0:
          label.setStyleSheet("background-color: rgb(232, 235, 239);")
        else:
          label.setStyleSheet("background-color: rgb(125, 135, 150);")
