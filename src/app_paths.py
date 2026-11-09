"""Central place for filesystem locations (works from source and when frozen)."""
import sys
from pathlib import Path

# From source this is ``src/``. In a Nuitka standalone build ``__file__`` points
# into the ``main.dist`` folder, where build.ps1 places the data files.
if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
    APP_DIR = Path(sys._MEIPASS)  # PyInstaller fallback
else:
    APP_DIR = Path(__file__).resolve().parent

CONFIG_DIR: Path = APP_DIR / "config"
CONFIG_FILE: Path = CONFIG_DIR / "config.json"

ASSETS_DIR: Path = APP_DIR / "gui" / "assets"
DARK_THEME_FILE: Path = ASSETS_DIR / "styles" / "dark.qss"
LIGHT_THEME_FILE: Path = ASSETS_DIR / "styles" / "light.qss"
APP_ICON_FILE: Path = ASSETS_DIR / "images" / "matcha-latte.png"
