"""settings.py - Constants and configuration for Fruit Frenzy."""
import os

# ---------- Paths ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSET_DIR = os.path.join(BASE_DIR, "assets")
IMAGE_DIR = os.path.join(ASSET_DIR, "images")
SOUND_DIR = os.path.join(ASSET_DIR, "sounds")
HIGHSCORE_FILE = os.path.join(BASE_DIR, "highscore.txt")

# ---------- Window ----------
WIDTH, HEIGHT = 800, 600
FPS = 60
TITLE = "Fruit Frenzy - Falling Objects Catch Game"

# ---------- Game rules ----------
GAME_DURATION = 60      # seconds
START_LIVES = 3
MAX_LIVES = 5
LEVEL_LENGTH = 15       # seconds per level (4 levels in 60s)

# ---------- Player ----------
PLAYER_SIZE = (120, 70)
PLAYER_MAX_SPEED = 540  # pixels / second
PLAYER_ACCEL = 10       # higher = snappier movement
PLAYER_BOTTOM_MARGIN = 16

# ---------- Items / physics ----------
ITEM_SIZE = (52, 52)
GRAVITY = 260           # pixels / second^2
MAX_FALL_SPEED = 720

# ---------- Colours ----------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 214, 64)
RED = (225, 60, 60)
GREEN = (80, 200, 100)
DARK = (30, 40, 60)
PANEL = (20, 30, 50, 190)
