# backend/game_engine/piece.py

class Piece:
    def __init__(self):
        self.position = -1  # -1 means in base

    def move(self, steps):
        if self.position == -1:
            if steps == 6:
                self.position = 0
        else:
            self.position += steps
            if self.position > 57:
                self.position = 57  # Cap at winning position

    def kill(self):
        self.position = -1

    def has_finished(self):
        return self.position == 57

    def is_active(self):
        return self.position != -1 and not self.has_finished()

