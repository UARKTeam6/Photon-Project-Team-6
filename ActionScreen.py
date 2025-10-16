from tkinter import *
import time

class PlayActionScreen:
    def __init__(self, red_team, green_team):
        """
        Initialize the play action screen.
        
        Args:
            red_team: List of tuples (player_id, codename, equipment_id)
            green_team: List of tuples (player_id, codename, equipment_id)
        """
        self.red_team = red_team
        self.green_team = green_team
        self.game_start_time = time.time()
        self.game_duration = 360  # 6 minutes in seconds
        
        self.window = Tk()
        self.window.title("Play Action Display")
        self.window.configure(bg="black")
        self.window.geometry("1400x900")
        
        self.setup_ui()
        self.update_timer()
        
    def setup_ui(self):
        # Main container
        main_frame = Frame(self.window, bg="black")
        main_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = Label(
            main_frame,
            text="Entry Terminal",
            font=("Arial", 16, "bold"),
            bg="black",
            fg="white"
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky="w")
        
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
            font=("Arial", 18, "bold"),
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
        
    def setup_team_display(self, parent):
        # Red Team Column
        red_header_frame = Frame(parent, bg="black")
        red_header_frame.grid(row=1, column=0, sticky="ew", padx=20)
        
        Label(
            red_header_frame,
            text="RED TEAM",
            font=("Arial", 16, "bold"),
            bg="black",
            fg="white"
        ).pack()
        
        # Red team players frame
        self.red_players_frame = Frame(parent, bg="black")
        self.red_players_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)
        
        # Calculate total red team score
        red_score = sum(player[0] for player in self.red_team) if self.red_team else 0
        
        # Display red team players
        for player_id, codename, equip_id in self.red_team:
            player_frame = Frame(self.red_players_frame, bg="black")
            player_frame.pack(fill=X, pady=1)
            
            Label(
                player_frame,
                text=f"⬛ {codename}",
                font=("Arial", 10),
                bg="black",
                fg="red",
                anchor="w"
            ).pack(side=LEFT, fill=X, expand=True)
            
            Label(
                player_frame,
                text=str(player_id),
                font=("Arial", 10, "bold"),
                bg="black",
                fg="red",
                anchor="e"
            ).pack(side=RIGHT)
        
        # Red team total score
        self.red_score_label = Label(
            red_header_frame,
            text=str(red_score),
            font=("Arial", 24, "bold"),
            bg="black",
            fg="red"
        )
        self.red_score_label.pack()
        
        # Green Team Column
        green_header_frame = Frame(parent, bg="black")
        green_header_frame.grid(row=1, column=1, sticky="ew", padx=20)
        
        Label(
            green_header_frame,
            text="GREEN TEAM",
            font=("Arial", 16, "bold"),
            bg="black",
            fg="white"
        ).pack()
        
        # Green team players frame
        self.green_players_frame = Frame(parent, bg="black")
        self.green_players_frame.grid(row=2, column=1, sticky="nsew", padx=20, pady=10)
        
        # Calculate total green team score
        green_score = sum(player[0] for player in self.green_team) if self.green_team else 0
        
        # Display green team players
        for player_id, codename, equip_id in self.green_team:
            player_frame = Frame(self.green_players_frame, bg="black")
            player_frame.pack(fill=X, pady=1)
            
            Label(
                player_frame,
                text=f"{codename}",
                font=("Arial", 10),
                bg="black",
                fg="green",
                anchor="w"
            ).pack(side=LEFT, fill=X, expand=True)
            
            Label(
                player_frame,
                text=str(player_id),
                font=("Arial", 10, "bold"),
                bg="black",
                fg="green",
                anchor="e"
            ).pack(side=RIGHT)
        
        # Green team total score
        self.green_score_label = Label(
            green_header_frame,
            text=str(green_score),
            font=("Arial", 24, "bold"),
            bg="black",
            fg="green"
        )
        self.green_score_label.pack()
        
        parent.grid_rowconfigure(2, weight=1)
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=1)
        
    def setup_action_feed(self, parent):
        # Action feed section
        action_frame = Frame(parent, bg="blue", bd=0)
        action_frame.grid(row=3, column=0, columnspan=2, sticky="ew", padx=20, pady=10)
        
        action_header = Label(
            action_frame,
            text="Current Game Action",
            font=("Arial", 14, "bold"),
            bg="blue",
            fg="cyan"
        )
        action_header.pack(pady=5)
        
        # Action feed text area
        self.action_text = Text(
            action_frame,
            height=6,
            font=("Arial", 10),
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
            font=("Arial", 16, "bold"),
            bg="black",
            fg="white"
        )
        self.timer_label.grid(row=4, column=0, columnspan=2, pady=10)
        
    def add_action(self, action_text):
        """Add an action to the action feed."""
        self.action_text.config(state=NORMAL)
        self.action_text.insert(END, action_text + "\n")
        self.action_text.see(END)
        self.action_text.config(state=DISABLED)
        
    def update_timer(self):
        """Update the countdown timer."""
        elapsed = time.time() - self.game_start_time
        remaining = max(0, self.game_duration - elapsed)
        
        minutes = int(remaining // 60)
        seconds = int(remaining % 60)
        
        self.timer_label.config(text=f"Time Remaining: {minutes}:{seconds:02d}")
        
        if remaining > 0:
            self.window.after(1000, self.update_timer)
        else:
            self.timer_label.config(text="Game Over!")
            
    def run(self):
        """Start the main loop."""
        self.window.mainloop()


def open_play_screen(red_team=None, green_team=None):
    """
    Open the play action screen with the given teams.
    
    Args:
        red_team: List of tuples (player_id, codename, equipment_id)
        green_team: List of tuples (player_id, codename, equipment_id)
    """
    # Use sample data if no teams provided
    if red_team is None:
        red_team = [(1, "Opus", 6025)]
    if green_team is None:
        green_team = [(2, "Scooby Doo", 5000)]
    
    screen = PlayActionScreen(red_team, green_team)
    screen.run()


if __name__ == "__main__":
    # Test with sample data
    red_team = [(1, "Opus", 6025)]
    green_team = [(2, "Scooby Doo", 5000)]
    open_play_screen(red_team, green_team)
