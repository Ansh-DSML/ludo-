# backend/shared/config.py

# Safe positions (cannot be killed)
SAFE_POSITIONS = {0, 8, 13, 21, 26, 34, 39, 47, 52}

# Maximum board position before a piece finishes
WINNING_POSITION = 57

# Player names (can be used for frontend ordering or game resets)
PLAYER_NAMES = ["Hisoka", "Gon", "Killua", "Kurapika"]

# Total number of pieces per player
PIECES_PER_PLAYER = 4

# API base URL (useful if frontend wants to dynamically fetch)
API_BASE_URL = "http://localhost:8000"

