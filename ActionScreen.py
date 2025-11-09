from tkinter import *
from playsound import playsound
import time
import threading

class PlayActionScreen:
    def __init__(self, red_team, green_team):
        """
        Initialize the play action screen.
        
        Args:
            red_team: List of lists [player_id, codename, equipment_id, score]
            green_team: List of lists [player_id, codename, equipment_id, score]
        """
        self.red_team = red_team
        self.green_team = green_team
        # map player_id -> Label widget for that player's score (for quick updates)
        self.player_score_labels = {}
        self.warning_start_time = time.time()
        self.warning_duration = 30 # 30 seconds
        self.game_start_time = None  # will be set when warning ends
        self.game_duration = 360  # 6 minutes in seconds
        self.mp3_file_path = "photon_tracks_Track08.mp3"
        self.music_playing = False
        
        self.window = Tk()
        self.window.title("Play Action Display")
        self.window.configure(bg="black")
        self.window.geometry("1200x700")

        self.setup_ui()
        self.update_timer()
        
    def setup_ui(self):
        # Main container
        main_frame = Frame(self.window, bg="black")
        main_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        # Border frame
        border_frame = Frame(main_frame, bg="yellow", bd=3)
        border_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        
        # Content frame inside border
        content_frame = Frame(border_frame, bg="black")
        content_frame.pack(fill=BOTH, expand=True, padx=2, pady=2)
        
        # Current Scores header
        scores_label = Label(
            content_frame,
            text="Current Scores",
            font=("arial", 18, "bold"),
            bg="black",
            fg="cyan"
        )
        scores_label.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Team headers and scores
        self.setup_team_display(content_frame)
        
        # Game action feed
        self.setup_action_feed(content_frame)
        
        # Timer at bottom
        self.setup_timer(content_frame)
        self.setup_warning_timer(content_frame)
        
    def setup_team_display(self, parent):
        # Red Team Column
        red_header_frame = Frame(parent, bg="black")
        red_header_frame.grid(row=1, column=0, sticky="ew", padx=20)
        
        Label(
            red_header_frame,
            text="RED TEAM",
            font=("arial", 16, "bold"),
            bg="black",
            fg="white"
        ).pack()
        
        # Add Player / Score headers
        header_frame_red = Frame(parent, bg="black")
        header_frame_red.grid(row=2, column=0, sticky="n", padx=20, pady=(10, 0))
        Label(header_frame_red, text="Player", font=("arial", 12, "bold"), bg="black", fg="white", width=15, anchor="w").grid(row=0, column=0, padx=(0, 100))
        Label(header_frame_red, text="Score", font=("arial", 12, "bold"), bg="black", fg="white", width=10, anchor="e").grid(row=0, column=1, padx=(100, 100))

        # Red team players frame
        self.red_players_frame = Frame(parent, bg="black")
        self.red_players_frame.grid(row=3, column=0, sticky="nsew", padx=20, pady=10)
        
        # Calculate total red team score 
        red_score = sum(player[3] for player in self.red_team) if self.red_team else 0
        
        # Display red team players
        for player in self.red_team:
            player_id, codename, equip_id, score = player
            player_frame = Frame(self.red_players_frame, bg="black")
            player_frame.pack(fill=X, pady=1)
            #
            Label(
                player_frame,
                text=f"- {codename}",
                font=("arial", 10),
                bg="black",
                fg="red",
                anchor="w"
            ).pack(side=LEFT, fill=X, expand=True)
            # right side, individual score (keep reference so we can update)
            score_label = Label(
                player_frame,
                text=str(score),
                font=("arial", 10, "bold"),
                bg="black",
                fg="red",
                anchor="e"
            )
            score_label.pack(side=RIGHT)
            self.player_score_labels[player_id] = score_label
        
        # Red team total score
        self.red_score_label = Label(
            red_header_frame,
            text=str(red_score),
            font=("arial", 24, "bold"),
            bg="black",
            fg="red"
        )
        self.red_score_label.pack()

        # --------------------------------------------------------------------------------------
        
        # Green Team Column
        green_header_frame = Frame(parent, bg="black")
        green_header_frame.grid(row=1, column=1, sticky="ew", padx=20)
        
        Label(
            green_header_frame,
            text="GREEN TEAM",
            font=("arial", 16, "bold"),
            bg="black",
            fg="white"
        ).pack()

        # Add Player / Score headers
        header_frame_green = Frame(parent, bg="black")
        header_frame_green.grid(row=2, column=1, sticky="n", padx=20, pady=(10, 0))
        Label(header_frame_green, text="Player", font=("arial", 12, "bold"), bg="black", fg="white", width=15, anchor="w").grid(row=0, column=0, padx=(0, 100))
        Label(header_frame_green, text="Score", font=("arial", 12, "bold"), bg="black", fg="white", width=10, anchor="e").grid(row=0, column=1, padx=(100, 225))
        
        # Green team players frame
        self.green_players_frame = Frame(parent, bg="black")
        self.green_players_frame.grid(row=3, column=1, sticky="nsew", padx=20, pady=10)
        
        # Calculate total green team score 
        green_score = sum(player[3] for player in self.green_team) if self.green_team else 0
        
        # Display green team players
        for player in self.green_team:
            player_id, codename, equip_id, score = player
            player_frame = Frame(self.green_players_frame, bg="black")
            player_frame.pack(fill=X, pady=1)
            
            Label(
                player_frame,
                text=f"- {codename}",
                font=("arial", 10),
                bg="black",
                fg="green",
                anchor="w"
            ).pack(side=LEFT, fill=X, expand=True)
            # right side, individual score (keep reference so we can update)
            score_label = Label(
                player_frame,
                text=str(score),
                font=("arial", 10, "bold"),
                bg="black",
                fg="green",
                anchor="e"
            )
            score_label.pack(side=RIGHT, padx=(0,123))
            self.player_score_labels[player_id] = score_label

        
        # Green team total score
        self.green_score_label = Label(
            green_header_frame,
            text=str(green_score),
            font=("arial", 24, "bold"),
            bg="black",
            fg="green"
        )
        self.green_score_label.pack()
        
        parent.grid_rowconfigure(3, weight=1)
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=1)

    # --- Game logic helpers -------------------------------------------------
    def find_player_and_team(self, player_id):
        """Return tuple (team_name, player_list_ref, index) where team_name is 'red' or 'green'."""
        for idx, p in enumerate(self.red_team):
            if p[0] == player_id:
                return 'red', p, idx
        for idx, p in enumerate(self.green_team):
            if p[0] == player_id:
                return 'green', p, idx
        return None, None, None

    def process_hit(self, attacker_id, target_id, points=1):
        """Handle a hit event: normal hit awards points to attacker; friendly fire deducts points.

        - attacker_id and target_id are player IDs (first element of player list).
        - points is how many points to add (or deduct on friendly fire).
        """
        a_team, a_player, a_idx = self.find_player_and_team(attacker_id)
        t_team, t_player, t_idx = self.find_player_and_team(target_id)

        if a_player is None or t_player is None:
            # Unknown players (could be off-field or not registered)
            missing = []
            if a_player is None:
                missing.append(f"attacker ({attacker_id})")
            if t_player is None:
                missing.append(f"target ({target_id})")
            self.add_action(f"Unknown {' and '.join(missing)}")
            return

        attacker_name = a_player[1]
        target_name = t_player[1]

        if a_team == t_team:
            # friendly fire: deduct 10 points from both players (but don't go below 0)
            a_old = a_player[3]
            t_old = t_player[3]
            a_new_score = max(0, a_old - 10)
            t_new_score = max(0, t_old - 10)
            if a_team == 'red':
                self.red_team[a_idx] = (a_player[0], a_player[1], a_player[2], a_new_score)
                self.red_team[t_idx] = (t_player[0], t_player[1], t_player[2], t_new_score)
            else:
                self.green_team[a_idx] = (a_player[0], a_player[1], a_player[2], a_new_score)
                self.green_team[t_idx] = (t_player[0], t_player[1], t_player[2], t_new_score)
            self.add_action(
                f"Friendly fire: {attacker_name} ({attacker_id}) hit teammate {target_name} ({target_id}) -> Both lose 10 pts"
            )
        else:
            # normal hit: award 10 points to attacker
            new_score = a_player[3] + 10
            if a_team == 'red':
                self.red_team[a_idx] = (a_player[0], a_player[1], a_player[2], new_score)
            else:
                self.green_team[a_idx] = (a_player[0], a_player[1], a_player[2], new_score)
            self.add_action(
                f"{attacker_name} ({attacker_id}) hit {target_name} ({target_id}) -> +10 pts"
            )
        # update UI scores
        self.update_score_labels()

    def update_score_labels(self):
        """Refresh individual and team total score labels from team data."""
        # update individual labels
        for p in (self.red_team or []) + (self.green_team or []):
            pid = p[0]
            score = p[3]
            lbl = self.player_score_labels.get(pid)
            if lbl:
                lbl.config(text=str(score))

        # update totals
        red_total = sum(p[3] for p in self.red_team) if self.red_team else 0
        green_total = sum(p[3] for p in self.green_team) if self.green_team else 0
        self.red_score_label.config(text=str(red_total))
        self.green_score_label.config(text=str(green_total))

        
    def setup_action_feed(self, parent):
        # Action feed section
        action_frame = Frame(parent, bg="#0033cc", bd=2, relief = "ridge")
        action_frame.grid(row=4, column=0, columnspan=2, sticky="ew", padx=20, pady=10)
        
        action_header = Label(
            action_frame,
            text="Current Game Action",
            font=("arial", 14, "bold"),
            bg="blue",
            fg="cyan"
        )
        action_header.pack(pady=5)
        
        # Action feed text area
        self.action_text = Text(
            action_frame,
            height=6,
            font=("arial", 10),
            bg="blue",
            fg="white",
            bd=0,
            highlightthickness=0,
            wrap=WORD
        )
        self.action_text.pack(fill=BOTH, expand=True, padx=10, pady=(0, 10))
        self.action_text.config(state=DISABLED)
        
        # Placeholder message
        self.add_action("Waiting for game events...")
        
    def setup_timer(self, parent):
        # Timer label at bottom
        self.timer_label = Label(
            parent,
            text="Time Remaining: 6:00",
            font=("arial", 16, "bold"),
            bg="black",
            fg="white"
        )
        self.timer_label.grid(row=5, column=0, columnspan=2, pady=10)
    def setup_warning_timer(self, parent):
        # Warning timer label at bottom
        self.warning_timer_label = Label(
            parent,
            text="Warning Time Remaining: 0:30",
            font=("arial", 16, "bold"),
            bg="black",
            fg="yellow"
        )
        self.warning_timer_label.grid(row=6, column=0, columnspan=2, pady=10)
    def add_action(self, action_text):
        """Add an action to the action feed."""
        self.action_text.config(state=NORMAL)
        self.action_text.insert(END, action_text + "\n")
        self.action_text.see(END)
        self.action_text.config(state=DISABLED)
        
    def update_timer(self):
        """Start with warning timer, then switch to game timer."""
        
        # Determine which phase we're in
        if self.game_start_time is None:
            # Still in warning phase
            elapsed_warning = time.time() - self.warning_start_time
            remaining_warning = max(0, self.warning_duration - elapsed_warning)
            
            minutes = int(remaining_warning // 60)
            seconds = int(remaining_warning % 60)
            self.warning_timer_label.config(text=f"Warning! Game begins in: {minutes}:{seconds:02d}")

            if remaining_warning <= 17 and not self.music_playing:
                self.music_playing = True
                try:
                    threading.Thread(target=playsound, args=(self.mp3_file_path,), kwargs={"block": True}, daemon=True).start()
                except Exception as e:
                    print(f"Error playing sound: {e}")

            if remaining_warning > 0:
                self.window.after(1000, self.update_timer)
            else:
                # Switch to main game timer
                self.add_action("Game Started!")
                self.warning_timer_label.config(text="")
                self.game_start_time = time.time()
                self.update_timer()
        else:
            # Main game phase
            elapsed = time.time() - self.game_start_time
            remaining = max(0, self.game_duration - elapsed)
            
            minutes = int(remaining // 60)
            seconds = int(remaining % 60)
            
            self.timer_label.config(text=f"Time Remaining: {minutes}:{seconds:02d}")
            
            if remaining > 0:
                self.window.after(1000, self.update_timer)
            else:
                self.timer_label.config(text="Game Over!")
                self.add_action("Game Over!")
            
    def run(self):
        """Start the main loop."""
        self.window.mainloop()


def open_play_screen(red_team=None, green_team=None):
    """
    Open the play action screen with the given teams.
    
    Args:
        red_team: List of lists [player_id, codename, equipment_id, score]
        green_team: List of lists [player_id, codename, equipment_id, score]
    """
    # Use sample data if no teams provided
    if red_team is None:
        red_team = [[1, "Opus", 6025, 0]]
    if green_team is None:
        green_team = [[2, "Scooby Doo", 5000, 0]]
    
    screen = PlayActionScreen(red_team, green_team)
    screen.run()


if __name__ == "__main__":
    # Test with sample data
    red_team = [[1, "Opus", 6025, 0], [3, "Alpha", 7001, 0]]
    green_team = [[2, "Scooby Doo", 5000, 0], [4, "Bravo", 8002, 0]]
    open_play_screen(red_team, green_team)
