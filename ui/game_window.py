import threading

from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QKeyEvent
from playsound import playsound

from game.game import Game
from game.profiler import Profiler
from constants.pieces import PIECE_IMAGES
from players.minimax_player_v0 import ComputerPlayer
from players.helper import reset_evaluation_stats, print_evaluation_stats


SEARCH_DEPTH = 4


class GameWindow(QWidget):
  def __init__(self):
    super().__init__()
    self.game = Game()
    self.computer = ComputerPlayer("black")
    self.ai_thinking = False

    self.labels = [None] * 64

    self.create_window()
    self.display_pieces()
    self.prev_squares = []
    self.selected_piece = None
    self.selected_square = None
    self.valid_moves = []

  def create_window(self):
    self.setWindowTitle(f'Chess Minimax v2 - Depth ({SEARCH_DEPTH})')
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

  def multithread_minimax(self):
    move = self.computer.minimax(SEARCH_DEPTH, self.game, float('-inf'), float('inf'), False)[0]
    move_type = self.game.make_move(move)
    if self.game.is_checkmate():
      print("checkmate")

    # refactor later with all the different move types
    if move_type == "capture" or move_type == "en-passant":
      playsound("assets/sounds/capture.mp3")
    else:
      playsound("assets/sounds/move-self.mp3")

    self.ai_thinking = False
    self.prev_squares = move
    self.display_pieces()
    self.reset_selection()
    Profiler.print_profile_summary(self.computer.moves_evaluated)
    print_evaluation_stats(self.computer)
    reset_evaluation_stats(self.computer)

  def handle_square_click(self, row, col):
    def on_click(_):
      if self.ai_thinking:
        return

      self.reset_highlight()
      square_index = row * 8 + col
      piece_type = self.game.board.get_square_piece(square_index)

      if self.selected_piece != None and square_index in self.valid_moves:
        move_type = self.game.make_move((self.selected_square, square_index))
        if self.game.king_in_check(1 - self.game.current_player_color):
          self.game.undo_move()

        # refactor later with all the different move types
        if move_type == "capture" or move_type == "en-passant":
          playsound("assets/sounds/capture.mp3")
        else:
          playsound("assets/sounds/move-self.mp3")

        self.prev_squares = [self.selected_square, square_index]
        self.display_pieces()
        self.reset_selection()

        if self.game.is_checkmate():
          print("checkmate")
          return

        self.ai_thinking = True
        threading.Thread(target=self.multithread_minimax).start()

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
      label.setStyleSheet(f"background-color: {'rgba(6, 145, 75, 0.8)'};")

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
          bg_style = 'rgba(6, 107, 145, 0.8)' if row * 8 + col in self.prev_squares else 'rgb(232, 235, 239)'
          label.setStyleSheet(f"background-color: {bg_style};")
        else:
          bg_style = 'rgba(6, 107, 145, 0.8)' if row * 8 + col in self.prev_squares else 'rgb(125, 135, 150)'
          label.setStyleSheet(f"background-color: {bg_style};")
