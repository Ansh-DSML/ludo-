import random

class Piece:
    def __init__(self):
        self.position = -1  # -1 means in the base

    def move(self, steps):
        if self.position == -1 and steps == 6:
            self.position = 0  # Enter the board
        elif self.position >= 0:
            self.position += steps  # Move forward

class Player:
    def __init__(self, name):
        self.name = name
        self.pieces = [Piece() for _ in range(4)]

class Game:
    def __init__(self, player_names):
        self.players = [Player(name) for name in player_names]
        self.current_turn = 0
        self.last_roll = 0
        self.six_count = 0
        self.winner = None

    def get_current_player(self):
        return self.players[self.current_turn]

    def roll_dice(self):
        roll = random.randint(1, 6)
        self.last_roll = roll
        
        if roll == 6:
            self.six_count += 1
            if self.six_count == 3:
                self.six_count = 0
                self.next_turn()  # If 6 occurs 3 times, turn ends
                return roll
        else:
            self.six_count = 0  # Reset six counter if not 6
        
        return roll

    def move_piece(self, piece_index):
        player = self.get_current_player()
        piece = player.pieces[piece_index]

        if piece.position == -1:
            if self.last_roll == 6:
                piece.position = 0  # Move from base to board
            else:
                raise ValueError("You need a 6 to enter the board")
        else:
            new_position = piece.position + self.last_roll
            
            # Ensure exact roll required to reach home
            if new_position > 57:
                raise ValueError("Invalid move: Can't overshoot home")

            piece.position = new_position

            # Check for capturing an opponent
            for opponent in self.players:
                if opponent != player:
                    for opp_piece in opponent.pieces:
                        if opp_piece.position == piece.position:
                            opp_piece.position = -1  # Send back to base
            
            # If not a 6, pass turn
            if self.last_roll != 6:
                self.next_turn()

    def next_turn(self):
        self.current_turn = (self.current_turn + 1) % len(self.players)
        self.six_count = 0

    def get_game_state(self):
        return {
        "game_state": {
            player.name: [piece.position for piece in player.pieces]
            for player in self.players
        },
        "current_turn": self.get_current_player().name
    }

