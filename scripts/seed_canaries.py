import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from windows.filesystem.canary import canary_manager
from config.settings import config

if __name__ == "__main__":
    canary_manager.seed_canary_files()
    print(f"Canary assets successfully seeded at {config.canary_dir}:")
    for f in canary_manager.list_canary_files():
        print(f" - {f}")
