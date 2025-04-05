# backend/schemas/models.py

from pydantic import BaseModel
from typing import List, Dict, Optional


class PieceState(BaseModel):
    position: int


class PlayerState(BaseModel):
    name: str
    pieces: List[PieceState]


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

