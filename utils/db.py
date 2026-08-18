import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "data" / "predictive_maintenance.db"


def get_connection():
    return sqlite3.connect(DB_PATH)
