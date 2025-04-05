import streamlit as st
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

# Load game state
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
                # Reset dice after move (unless dice was 6 and player gets another move)
                if st.session_state.dice_value != 6:
                    st.session_state.rolled = False
                    st.session_state.dice_value = None

    if st.session_state.dice_value is not None:
        st.markdown(f"### 🎲 You rolled: `{st.session_state.dice_value}`")

    st.markdown("---")
    st.caption("Made with ❤️ using Streamlit + FastAPI")
else:
    st.error("Unable to load game. Is the backend running?")
