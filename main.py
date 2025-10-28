# main.py
from splash_screen import show_splash
from entry_screen import entry_screen
from ActionScreen import open_play_screen

def main():
    # Start splash after done, move to entry screen
    show_splash(on_done=entry_screen)
if __name__ == "__main__":
    main()
