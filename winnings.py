import os

WINNINGS_FILE = "winnings.txt"

def load_winnings():
    if not os.path.exists(WINNINGS_FILE):
        return 0
    with open(WINNINGS_FILE, "r") as f:
        try:
            return int(f.read())
        except ValueError:
            return 0

def save_winnings(winnings):
    with open(WINNINGS_FILE, "w") as f:
        f.write(str(winnings))