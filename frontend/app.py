import streamlit as st
import requests
from components.game_ui import (
    draw_board,
    draw_player_info,
    roll_dice,
    move_piece,
    fetch_game_state,
)

st.set_page_config(page_title="Simplified Ludo", layout="centered")
st.title("🎯 Simplified Ludo")

# Initialize state
if "dice_value" not in st.session_state:
    st.session_state.dice_value = None
if "rolled" not in st.session_state:
    st.session_state.rolled = False

# ====== New Feature: Stats and History Functions ======

def show_history():
    st.subheader("📜 Game History")
    response = requests.get("http://localhost:8000/game/history")
    if response.status_code == 200:
        history = response.json()
        for move in history:
            st.markdown(
                f"Turn {move['turn']}: **{move['player']}** rolled 🎲 {move['roll']} and moved piece `{move['piece_index']}` "
                f"from `{move['from_pos']}` to `{move['to_pos']}`"
                + (f", captured **{move['captured']}**" if move['captured'] else "")
            )
    else:
        st.error("Failed to fetch game history.")

def show_stats():
    st.subheader("📊 Player Stats")
    response = requests.get("http://localhost:8000/game/stats")
    if response.status_code == 200:
        stats = response.json()
        for player, stat in stats.items():
            with st.expander(f"🔹 {player}"):
                st.write(f"Wins: {stat['wins']}")
                st.write(f"Losses: {stat['losses']}")
                st.write(f"Total Moves: {stat['total_moves']}")
                st.write(f"Tokens Captured: {stat['tokens_captured']}")
    else:
        st.error("Failed to fetch player stats.")

def show_leaderboard():
    st.subheader("🏆 Leaderboard")
    response = requests.get("http://localhost:8000/game/leaderboard")
    if response.status_code == 200:
        leaderboard = response.json()
        for i, entry in enumerate(leaderboard, 1):
            st.write(f"{i}. **{entry['player']}** - 🏅 {entry['wins']} wins")
    else:
        st.error("Failed to fetch leaderboard.")

# ====== Load Game State ======

game_data = fetch_game_state()

if game_data:
    st.session_state.game_state = game_data["game_state"]
    st.session_state.current_turn = game_data["current_turn"]

    draw_board(st.session_state.game_state)
    draw_player_info(st.session_state.current_turn, st.session_state.game_state)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🎲 Roll Dice"):
            result = roll_dice()
            if result:
                st.session_state.dice_value = result["roll"]
                st.session_state.rolled = True

    with col2:
        player = st.session_state.current_turn
        piece_index = st.selectbox("Select Piece Index (0-3)", [0, 1, 2, 3], key="piece_select")
        if st.button("🚀 Move Piece"):
            if not st.session_state.rolled:
                st.warning("Roll the dice before moving a piece!")
            else:
                move_result = move_piece(player, piece_index)
                if move_result:
                    st.success(f"{player}'s piece moved to {move_result['moved_to']}")
                if st.session_state.dice_value != 6:
                    st.session_state.rolled = False
                    st.session_state.dice_value = None

    if st.session_state.dice_value is not None:
        st.markdown(f"### 🎲 You rolled: `{st.session_state.dice_value}`")

    st.markdown("---")
    st.header("📈 Stats & History")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📜 Show History"):
            show_history()

    with col2:
        if st.button("📊 Show Stats"):
            show_stats()

    with col3:
        if st.button("🏆 Leaderboard"):
            show_leaderboard()

    st.caption("Made with ❤️ using Streamlit + FastAPI")
else:
    st.error("Unable to load game. Is the backend running?")
