"""BND-TOOLS — constants, paths, theme palette."""
import colorsys
import os

# ===== BASICS =====
sp = " "
VERSION = "2.0.0"

# ===== URLS =====
REMOTE_MANIFEST_URL = (
    "https://raw.githubusercontent.com/waaizy9/BND-TOOLS/main/BND/config/remote-manifest.json"
)

GITHUB = "https://github.com/waaizy9/BND-TOOLS"
STAR_GIF_URL = (
    "https://raw.githubusercontent.com/waaizy9/BND-TOOLS/main/BND/screenshots/star.PNG"
)
NUKER_GITHUB = "https://github.com/waaizy9/BND-Nuke"
DISCORD = "https://discord.gg/MJeUpXuxTZ"
SHOP = ""
AUTHOR = "BND-Team"

# ===== PATHS =====
VOID_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = os.path.dirname(VOID_DIR)
CONFIG_DIR = os.path.join(VOID_DIR, "config")
DATA_DIR = os.path.join(VOID_DIR, "data")
SETTINGS_PATH = os.path.join(CONFIG_DIR, "settings.json")
NUKER_CFG_PATH = os.path.join(CONFIG_DIR, "discord-nuker.json")
CUSTOM_TOOLS_DIR = os.path.join(VOID_DIR, "tools", "custom")

# ===== CHANGELOG =====
CHANGELOG = """BND-TOOLS v2.0.0
- Complete rebrand from Void to BND
- New Matrix Rain boot effect (#0000CD Blue)
- White scan animation through logo
"""

# ===== THEMES =====
THEMES = {
    "blue": {
        "blood": "#0a1a4a", "dark": "#1a2a6a", "mid": "#2244aa",
        "red": "#3366cc", "neon": "#4488FF", "bright": "#88BBFF",
    },
}

_THEME_ALIASES = {
    "blue": "blue",
    "dark": "dark",
    "green": "green",
    "red": "red",
    "purple": "purple",
}

_ACTIVE_THEME = "blue"

def apply_theme(theme_name):
    global _ACTIVE_THEME
    if theme_name in THEMES:
        _ACTIVE_THEME = theme_name

def get_theme():
    return THEMES.get(_ACTIVE_THEME, THEMES["blue"])

def is_rainbow():
    """Gibt zurück, ob Regenbogen-Modus aktiv ist"""
    return False

# ===== ALLE FARBEN FÜR CONSOLE =====
C_RESET = "\033[0m"
C_BOLD = "\033[1m"
C_DIM = "\033[2m"
C_RED = "\033[91m"
C_GREEN = "\033[92m"
C_YELLOW = "\033[93m"
C_BLUE = "\033[94m"
C_MAGENTA = "\033[95m"
C_CYAN = "\033[96m"
C_WHITE = "\033[97m"
C_BLACK = "\033[30m"

C_BLOOD = "\033[91m"
C_DARK = "\033[90m"
C_MID = "\033[37m"
C_NEON = "\033[96m"
C_BRIGHT = "\033[97m"
C_SILVER = "\033[38;2;192;192;192m"
C_GOLD = "\033[38;2;255;215;0m"
C_GOLD2 = "\033[38;2;255;215;0m"
C_PINK = "\033[38;2;255;192;203m"
C_PURPLE = "\033[95m"
C_ORANGE = "\033[38;2;255;165;0m"
C_BROWN = "\033[38;2;139;69;19m"
C_LIME = "\033[38;2;0;255;0m"
C_TEAL = "\033[38;2;0;128;128m"
C_LAVENDER = "\033[38;2;230;230;250m"
C_MAROON = "\033[38;2;128;0;0m"
C_NAVY = "\033[38;2;0;0;128m"
C_OLIVE = "\033[38;2;128;128;0m"
C_CORAL = "\033[38;2;255;127;80m"
C_SALMON = "\033[38;2;250;128;114m"
C_BEIGE = "\033[38;2;245;245;220m"
C_MINT = "\033[38;2;189;252;201m"

def palette(phase=0):
    """Gibt eine Farbpalette zurück (für Regenbogen-Effekt)"""
    if phase <= 0:
        return {
            "primary": C_BLUE,
            "secondary": C_CYAN,
            "accent": C_GOLD,
            "danger": C_RED,
            "success": C_GREEN,
            "info": C_WHITE,
        }
    # Regenbogen-Modus
    import colorsys
    r, g, b = colorsys.hsv_to_rgb(phase, 1.0, 1.0)
    color = f"\033[38;2;{int(r*255)};{int(g*255)};{int(b*255)}m"
    return {
        "primary": color,
        "secondary": color,
        "accent": color,
        "danger": color,
        "success": color,
        "info": color,
    }