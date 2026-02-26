from pathlib import Path

# Project root
ROOT_DIR = Path(__file__).resolve().parents[2]

# Config path
CONFIG_PATH = ROOT_DIR / "src" / "config" / "config.yaml"

# Logging path
LOG_PATH = ROOT_DIR / "logs"
MAX_LOG_SIZE = 5 * 1024 * 1024  # 5 MB

# Data path
RAW_DATA_PATH = ROOT_DIR / "data" / "raw" / "data.csv"

INTERIM_TRAIN_DATA_PATH = ROOT_DIR / "data" / "interim" / "train.csv"
INTERIM_TEST_DATA_PATH = ROOT_DIR / "data" / "interim" / "test.csv"

PROCESSED_TRAIN_DATA_PATH = ROOT_DIR / "data" / "processed" / "train.csv"
PROCESSED_TEST_DATA_PATH = ROOT_DIR / "data" / "processed" / "test.csv"

