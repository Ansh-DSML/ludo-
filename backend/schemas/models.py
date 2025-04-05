from pydantic import BaseModel
from typing import Dict, List, Optional

class GameStateResponse(BaseModel):
    game_state: Dict[str, List[int]]
    current_turn: str

class DiceRollResponse(BaseModel):
    player: str
    roll: int

class MoveRequest(BaseModel):
    piece_index: int

class MoveResponse(BaseModel):
    player: str
    moved_to: int
    killed: bool
    turn_changed: bool
    game_won: bool

class MoveLogEntry(BaseModel):
    turn: int
    player: str
    roll: int
    piece_index: int
    from_pos: int
    to_pos: int
    captured: Optional[str] = None

class GameHistoryResponse(BaseModel):
    history: List[MoveLogEntry]

class PlayerStats(BaseModel):
    wins: int = 0
    losses: int = 0
    total_moves: int = 0
    tokens_captured: int = 0

class StatsResponse(BaseModel):
    stats: Dict[str, PlayerStats]

class LeaderboardEntry(BaseModel):
    player: str
    wins: int

class LeaderboardResponse(BaseModel):
    leaderboard: List[LeaderboardEntry]