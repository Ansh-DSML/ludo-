class Piece:
    def __init__(self):
        self.position = -1  # -1 means in the base

    def move(self, steps, all_players, current_player_name):
        if self.position == -1 and steps == 6:
            self.position = 0  # Enter the board
        elif self.position >= 0:
            self.position += steps  # Move forward

        # Check for captures (only if on board)
        if self.position > 0:
            for player in all_players:
                if player.name != current_player_name:
                    for piece in player.pieces:
                        if piece.position == self.position:
                            piece.position = -1  # send captured piece back to base
                            return player  # captured player

        return None  # No one captured
