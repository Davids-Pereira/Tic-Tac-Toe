import tkinter as tk
from tkinter import scrolledtext, messagebox
import random
import time
import os
import json
from constants import *

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATS_FILE = os.path.join(BASE_DIR, "game_stats.json")

def load_scores():
    if os.path.exists(STATS_FILE):
        try:
            with open(STATS_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError): 
            return {"X": 0, "O": 0, "Draw": 0}
    return {"X": 0, "O": 0, "Draw": 0}

def save_scores():
    try:
        with open(STATS_FILE, 'w') as f:
            json.dump(scores, f, indent=4)
    except IOError:
        messagebox.showerror("Error", "Could not save scores!")

#Lógica 
board = [""] * 9
current_player = "X"
game_active = True
btns = []
scores = load_scores()

def update_log(log_area, message, emoji="📝"):
    timestamp = time.strftime("%H:%M:%S")
    log_area.configure(state='normal')
    log_area.insert(tk.END, f"{emoji} [{timestamp}] {message}\n")
    log_area.configure(state='disabled')
    log_area.see(tk.END)

def update_ui_status():
    lbl_score.config(text=f"X: {scores['X']} | O: {scores['O']} | Draws: {scores['Draw']}")
    lbl_turn.config(text=f"Turn: {current_player}", fg=COLORS['accent'])

def check_winner():
    for a, b, c in WINNING_COMBINATIONS:
        if board[a] == board[b] == board[c] != "":
            return board[a]
    return "Draw" if "" not in board else None

def handle_click(idx, log_widget):
    global current_player, game_active
    
    if board[idx] == "" and game_active:
        board[idx] = current_player
        btns[idx].config(text=current_player, state="disabled", disabledforeground=COLORS['text'])
        
        update_log(log_widget, f"Player {current_player} marked cell {idx}", "🎯")
        
        res = check_winner()
        if res:
            game_active = False
            scores[res] += 1
            save_scores()
            update_ui_status()
            msg = MESSAGES['draw'] if res == "Draw" else MESSAGES['win'].format(res)
            update_log(log_widget, msg, "🏁")
            messagebox.showinfo("Game Over", msg)
        else:
            current_player = "O" if current_player == "X" else "X"
            update_ui_status()
            
            if current_player == "O" and vs_ai.get():
                root.after(500, lambda: ai_play(log_widget))

def ai_play(log_widget):
    if not game_active: return
    
    options = [i for i in range(9) if board[i] == ""]

    #Intentar ganar
    for a, b, c in WINNING_COMBINATIONS:
        line = [board[a], board[b], board[c]]
        if line.count("O") == 2 and line.count("") == 1:
            move = [a, b, c][line.index("")]
            handle_click(move, log_widget)
            return
        
    #Bloquear al jugador para que no gane
    for a, b, c in WINNING_COMBINATIONS:
        line = [board[a], board[b], board[c]]
        if line.count("X") == 2 and line.count("") == 1:
            move = [a, b, c][line.index("")]
            handle_click(move, log_widget)
            return

    #Movimiento al azar si no hay nada
    if options:
        move = random.choice(options)
        handle_click(move, log_widget)

def reset_game(log_widget):
    global board, current_player, game_active
    board = [""] * 9
    current_player = "X"
    game_active = True
    for b in btns:
        b.config(text="", state="normal", bg=COLORS['btn'])
    update_ui_status()
    update_log(log_widget, "Game Board Reset", "🔄")

def reset_all(log_widget):
    global scores
    scores = {"X": 0, "O": 0, "Draw": 0}
    save_scores()
    reset_game(log_widget)
    update_log(log_widget, "Scoreboard reset to zero", "🧹")

#Interfaz Gráfica
root = tk.Tk()
root.title("Tic-Tac-Toe")
root.configure(bg=COLORS['bg'], padx=20, pady=20)

vs_ai = tk.BooleanVar(value=True)
log = scrolledtext.ScrolledText(root, height=5, width=45, font=FONTS['logs'], bg=COLORS['log_bg'], fg=COLORS['accent'], state='disabled')

#Marcador
lbl_score = tk.Label(root, text="", font=FONTS['logs'], bg=COLORS['bg'], fg=COLORS['text'])
lbl_score.pack()

btn_reset_score = tk.Button(root, text="RESET SCOREBOARD", font=("Consolas", 9, "bold"), bg=COLORS['reset'], fg="white", relief="raised", activebackground="#E74C3C", command=lambda: reset_all(log))
btn_reset_score.pack(pady=(5, 15))

lbl_turn = tk.Label(root, text="", font=FONTS['title'], bg=COLORS['bg'], fg=COLORS['accent'])
lbl_turn.pack()

#Tablero
frame = tk.Frame(root, bg=COLORS['bg'])
frame.pack()

for i in range(9):
    btn = tk.Button(frame, text="", font=FONTS['btns'], width=5, height=2, bg=COLORS['btn'], fg=COLORS['text'], command=lambda x=i: handle_click(x, log))
    btn.grid(row=i//3, column=i%3, padx=5, pady=5)
    btns.append(btn)

chk_ai = tk.Checkbutton(root, text="Enable AI (Player O)", variable=vs_ai, bg=COLORS['bg'], fg=COLORS['text'], selectcolor=COLORS['btn'], font=FONTS['logs'], activebackground=COLORS['bg'])
chk_ai.pack(pady=5)
log.pack(pady=10)

tk.Button(root, text="RESTART CURRENT GAME", command=lambda: reset_game(log), bg=COLORS['accent'], fg=COLORS['bg'], font=FONTS['title']).pack(fill="x")

update_ui_status()
update_log(log, MESSAGES['start'], "🚀")
root.mainloop()