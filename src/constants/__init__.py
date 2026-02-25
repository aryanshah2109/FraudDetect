from pathlib import Path

# Project root
ROOT_DIR = Path(__file__).resolve().parents[2]

# Config path
CONFIG_PATH = ROOT_DIR / "src" / "config" / "config.yaml"

# Logging path
LOG_PATH = ROOT_DIR / "logs"
MAX_LOG_SIZE = 5 * 1024 * 1024  # 5 MB