# frontend/components/game_ui.py
import streamlit as st
import pandas as pd
import requests

SAFE_POSITIONS = [0, 8, 13, 21, 26, 34, 39, 47, 52]
BOARD_SIZE = 58  # 0 to 57 inclusive

PLAYER_COLORS = {
    "Hisoka": "🔴",
    "Gon": "🟢",
    "Killua": "🔵",
    "Kurapika": "🟡"
}

API_URL = "http://127.0.0.1:8000"

def draw_board(game_state):
    st.markdown("### 🎲 Ludo Board")

    board_data = ["⬜"] * BOARD_SIZE

    for player_name, pieces in game_state.items():
        for pos in pieces:
            if pos == -1:
                continue  # skip base pieces
            if 0 <= pos < BOARD_SIZE:
                piece_symbol = PLAYER_COLORS.get(player_name, "❔")
                board_data[pos] = piece_symbol

    df = pd.DataFrame([board_data])
    st.dataframe(df, width=1000, height=80, hide_index=True)

def draw_player_info(current_turn, game_state):
    st.markdown(f"**Current Turn:** `{current_turn}`")

    for player_name, pieces in game_state.items():
        with st.expander(f"🎮 {player_name}"):
            st.write(f"Positions: {pieces}")
            kills = sum(1 for p in pieces if p == -1)
            st.write(f"Killed: {kills} pieces")

def roll_dice():
    response = requests.post(f"{API_URL}/game/roll")
    if response.status_code == 200:
        data = response.json()
        st.success(f"Dice rolled: 🎲 {data['roll']}")
        return data
    else:
        detail = response.json().get("detail", "Failed to roll dice.")
        st.error(f"Error: {detail}")
        return None

def move_piece(player_name, piece_index):
    response = requests.post(f"{API_URL}/game/move", json={
        "piece_index": piece_index
    })
    if response.status_code == 200:
        data = response.json()
        st.success(f"Moved piece to position {data['moved_to']}")
        return data
    else:
        detail = response.json().get("detail", "Failed to move piece.")
        st.error(f"Error: {detail}")
        return None

def fetch_game_state():
    response = requests.get("http://127.0.0.1:8000/game/state")  # ✅ CORRECTED
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch game state.")
        return None

