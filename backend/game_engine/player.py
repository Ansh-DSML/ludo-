# backend/game_engine/player.py

from .piece import Piece

class Player:
    def __init__(self, name):
        self.name = name
        self.pieces = [Piece() for _ in range(4)]
        self.last_roll = None

    def roll_dice(self):
        import random
        self.last_roll = random.randint(1, 6)
        return self.last_roll

    def get_active_pieces(self):
        return [p for p in self.pieces if p.is_active()]

    def get_movable_pieces(self):
        return [
            (i, p) for i, p in enumerate(self.pieces)
            if (p.position == -1 and self.last_roll == 6) or (p.is_active() and not p.has_finished())
        ]

    def all_finished(self):
        return all(p.has_finished() for p in self.pieces)

    def move_piece(self, index):
        if 0 <= index < len(self.pieces):
            self.pieces[index].move(self.last_roll)

