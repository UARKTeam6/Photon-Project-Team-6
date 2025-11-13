from tkinter import *
import time
import threading
import socket

try:
    from playsound import playsound
except ImportError:
    playsound = None  # fallback in case playsound isn't installed


class PlayActionScreen:
    def __init__(self, red_team, green_team):
        """
        Initialize the play action screen.
        """
        self.red_team = red_team
        self.green_team = green_team
        self.player_score_labels = {}
        self.warning_start_time = time.time()
        self.warning_duration = 30  # 30 sec pre-game
        self.game_start_time = None
        self.game_duration = 360  # 6 minutes
        self.music_playing = False

        # Auto-detect sound path based on OS
        import os, platform
        if platform.system() == "Darwin":  # macOS
            self.mp3_file_path = os.path.join(os.getcwd(), "photon_tracks_Track08.mp3")
        elif platform.system() == "Windows":
            self.mp3_file_path = os.path.join(os.getcwd(), "Photon-Project-Team-6-main\photon_tracks_Track08.mp3")
        else:  # Debian VM or Linux
            self.mp3_file_path = "/home/student/Desktop/Photon-Project-Team-6-main/photon_tracks_Track08.mp3"

        # Networking attributes (used by listener thread)
        self._listener_host = "127.0.0.1"
        self._listener_port = 7501
        self._tg_host = "127.0.0.1"
        self._tg_port = 7500
        self._sock_timeout = 1.0
        self._net_sock = None
        self._net_thread = None
        self._net_stop = threading.Event()

        self.window = Tk()
        self.window.title("Play Action Display")
        self.window.configure(bg="black")
        self.window.geometry("1200x700")

        self.setup_ui()
        self.update_timer()
        # start the listener thread which will also send the initial '202' handshake
        

        # ensure network stops on window close
        self.window.protocol("WM_DELETE_WINDOW", self._on_close)

    # --- UI SETUP ---------------------------------------------------------
    def setup_ui(self):
        main_frame = Frame(self.window, bg="black")
        main_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        border_frame = Frame(main_frame, bg="yellow", bd=3)
        border_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)

        content_frame = Frame(border_frame, bg="black")
        content_frame.pack(fill=BOTH, expand=True, padx=2, pady=2)

        Label(content_frame, text="Current Scores", font=("Arial", 18, "bold"),
              bg="black", fg="cyan").grid(row=0, column=0, columnspan=2, pady=10)

        self.setup_team_display(content_frame)
        self.setup_action_feed(content_frame)
        self.setup_timer(content_frame)
        self.setup_warning_timer(content_frame)

    def setup_team_display(self, parent):
        def make_team(col, name, color, team):
            header_frame = Frame(parent, bg="black")
            header_frame.grid(row=1, column=col, sticky="ew", padx=20)
            Label(header_frame, text=f"{name} TEAM", font=("Arial", 16, "bold"),
                  bg="black", fg="white").pack()

            header_labels = Frame(parent, bg="black")
            header_labels.grid(row=2, column=col, sticky="n", padx=20, pady=(10, 0))
            Label(header_labels, text="Player", font=("Arial", 12, "bold"),
                  bg="black", fg="white", width=15, anchor="w").grid(row=0, column=0)
            Label(header_labels, text="Score", font=("Arial", 12, "bold"),
                  bg="black", fg="white", width=10, anchor="e").grid(row=0, column=1)

            players_frame = Frame(parent, bg="black")
            players_frame.grid(row=3, column=col, sticky="nsew", padx=20, pady=10)

            total = 0
            for pid, codename, equip, score in team:
                total += score
                pf = Frame(players_frame, bg="black")
                pf.pack(fill=X, pady=1)
                Label(pf, text=f"- {codename}", font=("Arial", 10), bg="black",
                      fg=color, anchor="w").pack(side=LEFT, fill=X, expand=True)
                score_lbl = Label(pf, text=str(score), font=("Arial", 10, "bold"),
                                  bg="black", fg=color, anchor="e")
                score_lbl.pack(side=RIGHT)
                self.player_score_labels[pid] = score_lbl

            total_lbl = Label(header_frame, text=str(total), font=("Arial", 24, "bold"),
                              bg="black", fg=color)
            total_lbl.pack()
            return total_lbl

        self.red_score_label = make_team(0, "RED", "red", self.red_team)
        self.green_score_label = make_team(1, "GREEN", "green", self.green_team)
        parent.grid_rowconfigure(3, weight=1)
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=1)

    # --- SCORE LOGIC ------------------------------------------------------
    def find_player_and_team(self, pid):
        for i, p in enumerate(self.red_team):
            if p[0] == pid:
                return "red", p, i
        for i, p in enumerate(self.green_team):
            if p[0] == pid:
                return "green", p, i
        return None, None, None

    def find_by_equipment_id(self, eid):
        for p in self.red_team + self.green_team:
            if p[2] == eid:
                return p[0]
        return None

    def process_hit(self, attacker_id, target_id):
        a_team, a_p, a_i = self.find_player_and_team(attacker_id)
        t_team, t_p, t_i = self.find_player_and_team(target_id)

        if a_team == t_team:
            a_new = max(0, a_p[3] - 10)
            t_new = max(0, t_p[3] - 10)
            if a_team == "red":
                self.red_team[a_i] = (a_p[0], a_p[1], a_p[2], a_new)
                self.red_team[t_i] = (t_p[0], t_p[1], t_p[2], t_new)
            else:
                self.green_team[a_i] = (a_p[0], a_p[1], a_p[2], a_new)
                self.green_team[t_i] = (t_p[0], t_p[1], t_p[2], t_new)
            self.add_action(f"Friendly fire: {a_p[1]} hit {t_p[1]} -> -10 pts each")
        else:
            new_score = a_p[3] + 10
            if a_team == "red":
                self.red_team[a_i] = (a_p[0], a_p[1], a_p[2], new_score)
            else:
                self.green_team[a_i] = (a_p[0], a_p[1], a_p[2], new_score)
            self.add_action(f"{a_p[1]} hit {t_p[1]} -> +10 pts")

        self.update_score_labels()

    def update_score_labels(self):
        for p in self.red_team + self.green_team:
            if p[0] in self.player_score_labels:
                self.player_score_labels[p[0]].config(text=str(p[3]))
        self.red_score_label.config(text=str(sum(p[3] for p in self.red_team)))
        self.green_score_label.config(text=str(sum(p[3] for p in self.green_team)))

    # --- UI COMPONENTS ----------------------------------------------------
    def setup_action_feed(self, parent):
        frame = Frame(parent, bg="#0033cc", bd=2, relief="ridge")
        frame.grid(row=4, column=0, columnspan=2, sticky="ew", padx=20, pady=10)
        Label(frame, text="Current Game Action", font=("Arial", 14, "bold"),
              bg="blue", fg="cyan").pack(pady=5)
        self.action_text = Text(frame, height=6, font=("Arial", 10), bg="blue",
                                fg="white", bd=0, wrap=WORD)
        self.action_text.pack(fill=BOTH, expand=True, padx=10, pady=(0, 10))
        self.action_text.config(state=DISABLED)
        self.add_action("Waiting for game events...")

    def setup_timer(self, parent):
        self.timer_label = Label(parent, text="Time Remaining: 6:00",
                                 font=("Arial", 16, "bold"),
                                 bg="black", fg="white")
        self.timer_label.grid(row=5, column=0, columnspan=2, pady=10)

    def setup_warning_timer(self, parent):
        self.warning_timer_label = Label(parent, text="Warning Time Remaining: 0:30",
                                         font=("Arial", 16, "bold"),
                                         bg="black", fg="yellow")
        self.warning_timer_label.grid(row=6, column=0, columnspan=2, pady=10)

    def add_action(self, text):
        self.action_text.config(state=NORMAL)
        self.action_text.insert(END, text + "\n")
        self.action_text.see(END)
        self.action_text.config(state=DISABLED)

    # --- TIMERS ------------------------------------------------------------
    def update_timer(self):
        if self.game_start_time is None:
            elapsed = time.time() - self.warning_start_time
            remain = max(0, self.warning_duration - elapsed)
            self.warning_timer_label.config(
                text=f"Warning! Game begins in: {int(remain // 60)}:{int(remain % 60):02d}"
            )

            if remain <= 17 and not self.music_playing and playsound:
                self.music_playing = True
                try:
                    threading.Thread(target=playsound,
                                     args=(self.mp3_file_path,),
                                     kwargs={"block": True},
                                     daemon=True).start()
                except Exception as e:
                    print(f"[AUDIO WARNING] {e}")

            if remain > 0:
                self.window.after(1000, self.update_timer)
            else:
                self.add_action("Game Started!")
                self.add_action(f"Loaded RED: {[(p[0], p[2]) for p in self.red_team]}  "
                                f"GREEN: {[(p[0], p[2]) for p in self.green_team]}")
                self.start_listener()
                self.warning_timer_label.config(text="")
                self.game_start_time = time.time()
                self.update_timer()
        else:
            elapsed = time.time() - self.game_start_time
            remain = max(0, self.game_duration - elapsed)
            self.timer_label.config(text=f"Time Remaining: {int(remain // 60)}:{int(remain % 60):02d}")
            if remain > 0:
                self.window.after(1000, self.update_timer)
            else:
                self.timer_label.config(text="Game Over!")
                self.add_action("Game Over!")
                self.stop_listener()

    # --- NETWORK -----------------------------------------------------------
    def start_listener(self):
        """Start background thread which:
        - sends an initial '202' handshake to trafficgen (so trafficgen will start),
        - listens on 127.0.0.1:7501 for messages from trafficgen,
        - replies to trafficgen on 127.0.0.1:7500 for each message,
        - sends an extra reply when friendly-fire is detected (so trafficgen's second recvfrom() is satisfied).
        """
        # ensure any previous thread/socket are cleaned up
        self._net_stop.clear()
        self._net_thread = threading.Thread(target=self._listener_loop, daemon=True)
        self._net_thread.start()

    def stop_listener(self):
        """Stop the network listener and close socket."""
        self._net_stop.set()
        if self._net_thread:
            self._net_thread.join(timeout=1.0)
        if self._net_sock:
            try:
                self._net_sock.close()
            except Exception:
                pass
        self._net_sock = None

    def _listener_loop(self):
        BUF = 1024
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((self._listener_host, self._listener_port))
            sock.settimeout(self._sock_timeout)
            self._net_sock = sock
            print(f"[LISTENER] Listening on UDP {self._listener_host}:{self._listener_port}")

            # Send initial handshake '202' to trafficgen so it begins
            try:
                sock.sendto(b"202", (self._tg_host, self._tg_port))
                print(f"[HANDSHAKE] Sent '202' to {(self._tg_host, self._tg_port)}")
            except Exception as e:
                print(f"[HANDSHAKE ERROR] {e}")

            while not self._net_stop.is_set():
                try:
                    data, addr = sock.recvfrom(BUF)
                except socket.timeout:
                    continue
                except OSError:
                    break

                if not data:
                    continue
                try:
                    msg = data.decode("utf-8").strip()
                except Exception:
                    msg = repr(data)
                print(f"[LISTENER] RX '{msg}' from {addr}")

                # default reply to unblock trafficgen
                main_reply = "200"
                extra_reply = None
                terminate_reply = False

                # message format expected: '<attacker_eid>:<target_eid>'
                if ":" in msg:
                    a_str, t_str = msg.split(":", 1)
                    # try int conversion but keep original if fails
                    try:
                        a_eid = int(a_str.strip())
                        t_eid = int(t_str.strip())
                    except ValueError:
                        a_eid = None
                        t_eid = None

                    # resolve equipment -> player ids
                    a_pid = self.find_by_equipment_id(a_eid) if a_eid is not None else None
                    t_pid = self.find_by_equipment_id(t_eid) if t_eid is not None else None
                    print(f"[DEBUG] Equip {a_eid}->{t_eid} => Players {a_pid}->{t_pid}")

                    # if unknown equipment IDs, log and reply but don't process hit
                    if t_pid is None and t_eid in (43, 53):
                        pass
                    else:
                        # determine if friendly-fire by checking team membership
                        a_team, _, _ = self.find_player_and_team(a_pid)
                        t_team, _, _ = self.find_player_and_team(t_pid)
                        if a_team == t_team:
                            # trafficgen expects two replies when friendly-fire occurs
                            extra_reply = "201"
                            print(f"[LISTENER] Detected friendly fire for {a_eid}:{t_eid}")
                            # queue the actual game logic update on the main thread
                        self.window.after(0, lambda a=a_pid, t=t_pid: self.process_hit(a, t))

                else:
                    # message is not in expected format; ignore but still reply to unblock
                    print(f"[LISTENER] Received non-standard message: {msg}")

                # send main reply back to trafficgen's listening port
                try:
                    sock.sendto(main_reply.encode("utf-8"), (self._tg_host, self._tg_port))
                    print(f"[LISTENER] Sent reply '{main_reply}' to {(self._tg_host, self._tg_port)}")
                except Exception as e:
                    print(f"[LISTENER ERROR] failed to send main reply: {e}")

                # if friendly-fire detected, send an extra reply shortly after
                if extra_reply:
                    time.sleep(0.02)
                    try:
                        sock.sendto(extra_reply.encode("utf-8"), (self._tg_host, self._tg_port))
                        print(f"[LISTENER] Sent extra reply '{extra_reply}' to {(self._tg_host, self._tg_port)}")
                    except Exception as e:
                        print(f"[LISTENER ERROR] failed to send extra reply: {e}")

                if terminate_reply:
                    try:
                        sock.sendto(b"221", (self._tg_host, self._tg_port))
                        print("[LISTENER] Sent termination '221'")
                    except Exception:
                        pass

        except Exception as e:
            print(f"[LISTENER ERROR] {e}")
        finally:
            try:
                if self._net_sock:
                    self._net_sock.close()
            except Exception:
                pass
            self._net_sock = None
            print("[LISTENER] Exiting listener loop")

    # --- RUN / CLEANUP ----------------------------------------------------
    def _on_close(self):
        # stop network first, then destroy window
        print("[UI] Closing window — stopping network")
        try:
            self.stop_listener()
        except Exception:
            pass
        try:
            self.window.destroy()
        except Exception:
            pass

    def run(self):
        try:
            self.window.mainloop()
        finally:
            # ensure cleanup if mainloop exits unexpectedly
            self.stop_listener()


def open_play_screen(red_team=None, green_team=None):
    if red_team is None:
        red_team = [[1, "Opus", 6025, 0]]
    if green_team is None:
        green_team = [[2, "Scooby Doo", 5000, 0]]
    PlayActionScreen(red_team, green_team).run()


if __name__ == "__main__":
    red_team = [[1, "Opus", 6025, 0], [3, "Alpha", 7001, 0]]
    green_team = [[2, "Scooby Doo", 5000, 0], [4, "Bravo", 8002, 0]]
    open_play_screen(red_team, green_team)

