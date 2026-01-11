COLORS = {
    'bg': '#2c3e50',      # Background
    'btn': '#34495e',     # Board buttons
    'text': '#ecf0f1',    # Off-white for readability
    'accent': '#27ae60',  # Green for success/logs
    'reset': '#C0392B',   # Red for the Scoreboard Reset 
    'log_bg': '#1a1a1a'   # Deep black for log area
}
FONTS = {
    'title': ('Helvetica', 14, 'bold'),
    'btns': ('Arial', 20, 'bold'),
    'logs': ('Consolas', 10)
}
MESSAGES = {
    'start': "Starting Tic-Tac-Toe Pro...",
    'win': "Player {} Wins! 🏆",
    'draw': "Technical Draw! 🤝",
    'turn': "Turn: {}"
}
WINNING_COMBINATIONS = [
    (0,1,2), (3,4,5), (6,7,8), # Filas
    (0,3,6), (1,4,7), (2,5,8), # Columnas
    (0,4,8), (2,4,6)           # Diagonales
]