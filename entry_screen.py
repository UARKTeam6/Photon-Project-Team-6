from tkinter import *
from tkinter import messagebox
from DatabaseInterface import get_player, add_player
from ActionScreen import open_play_screen

MAX_TEAM_SIZE = 15
broadcast_ip = None


def send_message(msg: str):
    """Placeholder for UDP broadcast (replace with your real one)."""
    print(f"[UDP SEND] {msg}")


def entry_screen():
    global broadcast_ip
    window = Tk()
    window.title("Player Entry")
    window.configure(bg="black")

    # --- Dynamic sizing (smaller width, tall height for Debian VM) ---
    screen_w = window.winfo_screenwidth()
    screen_h = window.winfo_screenheight()
    width = int(screen_w * 0.7)   # narrower
    height = int(screen_h * 0.9)  # tall
    window.geometry(f"{width}x{height}")
    window.minsize(650, 600)
    window.resizable(True, True)
    window.update_idletasks()

    # --- Scrollable main area ---
    canvas = Canvas(window, bg="black", highlightthickness=0)
    scroll_y = Scrollbar(window, orient="vertical", command=canvas.yview)
    scroll_frame = Frame(canvas, bg="black")

    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scroll_y.set)

    canvas.grid(row=0, column=0, sticky="nsew")
    scroll_y.grid(row=0, column=1, sticky="ns")

    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)

    # --- Content inside scroll_frame ---
    Label(scroll_frame, text="Game Setup!", font=("Arial", 24, "bold"),
          fg="blue", bg="black").grid(row=0, column=0, columnspan=2, pady=10)

    # Broadcast IP selection
    broadcast_ip = StringVar(value="127.0.0.1")
    Label(scroll_frame, text="Broadcast IP:", bg="black", fg="white").grid(row=1, column=0, sticky="e", padx=5)
    Entry(scroll_frame, textvariable=broadcast_ip, width=20).grid(row=1, column=1, sticky="w", padx=5, pady=5)

    # Frames for teams
    red_frame = Frame(scroll_frame, bg="darkred", padx=10, pady=10)
    green_frame = Frame(scroll_frame, bg="darkgreen", padx=10, pady=10)
    red_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
    green_frame.grid(row=2, column=1, sticky="nsew", padx=10, pady=10)

    Label(red_frame, text="RED TEAM", bg="darkred", fg="white",
          font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=4, pady=5)
    Label(green_frame, text="GREEN TEAM", bg="darkgreen", fg="white",
          font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=4, pady=5)

    for frame in [red_frame, green_frame]:
        Label(frame, text="#", bg=frame["bg"], fg="white", width=3).grid(row=1, column=0, padx=2, pady=2)
        Label(frame, text="Player ID", bg=frame["bg"], fg="white").grid(row=1, column=1, padx=2, pady=2)
        Label(frame, text="Name", bg=frame["bg"], fg="white").grid(row=1, column=2, padx=2, pady=2)
        Label(frame, text="Equipment ID", bg=frame["bg"], fg="white").grid(row=1, column=3, padx=2, pady=2)

    red_entries, green_entries = [], []

    def handle_player_id(pid_entry, cname_entry):
        pid = pid_entry.get()
        if pid.isdigit():
            codename = get_player(int(pid))
            if codename:
                cname_entry.delete(0, END)
                cname_entry.insert(0, codename)
            else:
                messagebox.showinfo("Info", f"Player {pid} not found. Please enter new codename.")

    def handle_equipment(pid_entry, cname_entry, equip_entry):
        pid, cname, equip = pid_entry.get(), cname_entry.get(), equip_entry.get()
        if not (pid.isdigit() and equip.isdigit()):
            messagebox.showerror("Error", "Player ID and Equipment ID must be integers")
            return
        if not cname:
            messagebox.showerror("Error", "Codename cannot be empty")
            return
        add_player(int(pid), cname)
        send_message(str(equip))
        print(f"[ENTRY] Added {pid}:{cname} with equip {equip}")

    for i in range(1, MAX_TEAM_SIZE + 1):
        Label(red_frame, text=str(i), bg="darkred", fg="white", width=3).grid(row=i+1, column=0, padx=2, pady=2)
        Label(green_frame, text=str(i), bg="darkgreen", fg="white", width=3).grid(row=i+1, column=0, padx=2, pady=2)

        pid_entry = Entry(red_frame, width=6)
        cname_entry = Entry(red_frame, width=15)
        equip_entry = Entry(red_frame, width=6)
        pid_entry.grid(row=i+1, column=1, padx=2, pady=2)
        cname_entry.grid(row=i+1, column=2, padx=2, pady=2)
        equip_entry.grid(row=i+1, column=3, padx=2, pady=2)
        pid_entry.bind("<Return>", lambda e, p=pid_entry, c=cname_entry: handle_player_id(p, c))
        equip_entry.bind("<Return>", lambda e, p=pid_entry, c=cname_entry, eq=equip_entry: handle_equipment(p, c, eq))
        red_entries.append((pid_entry, cname_entry, equip_entry))

        pid_entry2 = Entry(green_frame, width=6)
        cname_entry2 = Entry(green_frame, width=15)
        equip_entry2 = Entry(green_frame, width=6)
        pid_entry2.grid(row=i+1, column=1, padx=2, pady=2)
        cname_entry2.grid(row=i+1, column=2, padx=2, pady=2)
        equip_entry2.grid(row=i+1, column=3, padx=2, pady=2)
        pid_entry2.bind("<Return>", lambda e, p=pid_entry2, c=cname_entry2: handle_player_id(p, c))
        equip_entry2.bind("<Return>", lambda e, p=pid_entry2, c=cname_entry2, eq=equip_entry2: handle_equipment(p, c, eq))
        green_entries.append((pid_entry2, cname_entry2, equip_entry2))

    def clear_all():
        for row in red_entries + green_entries:
            for widget in row:
                widget.delete(0, END)

    def start_game():
        send_message("202")
        print("[GAME] Starting Play Action Screen...")
        red_team, green_team = [], []
        for pid_entry, cname_entry, equip_entry in red_entries:
            pid, cname, equip = pid_entry.get(), cname_entry.get(), equip_entry.get()
            if pid and cname and equip:
                red_team.append([int(pid), cname, int(equip), 0])
        for pid_entry, cname_entry, equip_entry in green_entries:
            pid, cname, equip = pid_entry.get(), cname_entry.get(), equip_entry.get()
            if pid and cname and equip:
                green_team.append([int(pid), cname, int(equip), 0])
        window.destroy()
        open_play_screen(red_team, green_team)

    window.bind('<F5>', lambda e: start_game())
    window.bind('<F12>', lambda e: clear_all())
    window.bind('<Control-F5>', lambda e: start_game())
    window.bind('<Control-F12>', lambda e: clear_all())

    btn_frame = Frame(scroll_frame, bg="black")
    btn_frame.grid(row=3, column=0, columnspan=2, pady=15)
    Button(btn_frame, text="Clear Entries", command=clear_all, width=20).grid(row=0, column=0, padx=10)
    Button(btn_frame, text="Start Game", command=start_game, width=20).grid(row=0, column=1, padx=10)

    # --- Footer ---
    footer = Label(
        scroll_frame,
        text="Shortcuts:  F5 → Start Game   |   F12 → Clear All",
        bg="black",
        fg="yellow",
        font=("Consolas", 10, "bold")
    )
    footer.grid(row=4, column=0, columnspan=2, pady=5)

    window.mainloop()
