import random
from backend.schemas.models import PlayerStats, MoveLogEntry, LeaderboardEntry


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

class Player:
    def __init__(self, name):
        self.name = name
        self.pieces = [Piece() for _ in range(4)]

class Game:
    def __init__(self, player_names):
        self.players = [Player(name) for name in player_names]
        self.current_player_index = 0
        self.last_roll = None
        self.turn_count = 0
        self.history = []  # move log
        self.stats = {name: PlayerStats() for name in player_names}
        self.winner = None

    def get_game_state(self):
        return {
            "game_state": {p.name: [piece.position for piece in p.pieces] for p in self.players},
            "current_turn": self.get_current_player().name,
        }

    def get_current_player(self):
        return self.players[self.current_player_index]

    def roll_dice(self):
        from random import randint
        self.last_roll = randint(1, 6)
        return self.last_roll

    def move_piece(self, piece_index):
        player = self.get_current_player()
        roll = self.last_roll
        piece = player.pieces[piece_index]
        from_pos = piece.position

        captured_player = piece.move(roll, self.players, player.name)


        to_pos = piece.position
        self.stats[player.name].total_moves += 1

        if captured_player:
            self.stats[player.name].tokens_captured += 1

        self.history.append(MoveLogEntry(
            turn=self.turn_count,
            player=player.name,
            roll=roll,
            piece_index=piece_index,
            from_pos=from_pos,
            to_pos=to_pos,
            captured=captured_player.name if captured_player else None,
        ))

        if all(p.position == 57 for p in player.pieces):
            self.winner = player.name
            self.stats[player.name].wins += 1
            for p in self.players:
                if p.name != player.name:
                    self.stats[p.name].losses += 1

        if roll != 6:
            self.next_turn()

    def next_turn(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        self.turn_count += 1

    def get_history(self):
        return self.history

    def get_stats(self):
        return self.stats

    def get_leaderboard(self):
        return sorted(
            [LeaderboardEntry(player=name, wins=stat.wins) for name, stat in self.stats.items()],
            key=lambda x: x.wins,
            reverse=True,
        )
