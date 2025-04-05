from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.schemas.models import GameStateResponse, DiceRollResponse, MoveRequest, MoveResponse
from backend.game_engine.game import Game

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize game with 4 players
player_names = ["Hisoka", "Gon", "Killua", "Kurapika"]
game = Game(player_names)

@app.get("/game/state", response_model=GameStateResponse)
def get_game_state():
    return game.get_game_state()

@app.post("/game/roll", response_model=DiceRollResponse)
def roll_dice():
    if game.winner:
        raise HTTPException(status_code=400, detail="Game is already over.")

    roll = game.roll_dice()
    return {"player": game.get_current_player().name, "roll": roll}

@app.post("/game/move", response_model=MoveResponse)
def move_piece(move_request: MoveRequest):
    if game.winner:
        raise HTTPException(status_code=400, detail="Game is already over.")

    player = game.get_current_player()
    piece = player.pieces[move_request.piece_index]
    old_position = piece.position
    roll = game.last_roll

    try:
        game.move_piece(move_request.piece_index)
    except ValueError as e:
        game.next_turn()
        raise HTTPException(status_code=400, detail=str(e))

    new_position = piece.position
    game_won = all(p.position == 57 for p in player.pieces)  # Check if all tokens reached home

    return MoveResponse(
        player=player.name,
        moved_to=new_position,
        killed=False,
        turn_changed=(roll != 6),
        game_won=game_won
    )
