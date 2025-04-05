# backend/game_engine/board.py

SAFE_POSITIONS = {0, 8, 13, 21, 26, 34, 39, 47, 52}
WINNING_POSITION = 57

class Board:
    def __init__(self):
        self.safe_positions = SAFE_POSITIONS
        self.winning_position = WINNING_POSITION

    def is_safe(self, position):
        return position in self.safe_positions

    def is_winning(self, position):
        return position == self.winning_position

