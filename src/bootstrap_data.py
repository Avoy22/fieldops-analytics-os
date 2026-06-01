"""
Bootstrap data for deployed Streamlit environment.

If the SQLite database does not exist, this script generates synthetic data
and loads it into SQLite automatically.

This is useful for Streamlit Community Cloud because generated CSV and DB files
are not committed to GitHub.
"""

import subprocess
import sqlite3
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = PROJECT_ROOT / "data" / "processed" / "fieldops.db"
GENERATE_DATA_SCRIPT = PROJECT_ROOT / "src" / "generate_data.py"
LOAD_TO_SQLITE_SCRIPT = PROJECT_ROOT / "src" / "load_to_sqlite.py"
REQUIRED_TABLES = {
    "buyers",
    "providers",
    "work_orders",
    "payments",
    "reviews",
    "support_tickets",
}


def ensure_database_exists(db_path: Path = DB_PATH) -> None:
    """Generate synthetic data and load SQLite database if missing or incomplete."""
    if _database_has_required_tables(db_path):
        return

    print("Database missing or incomplete. Generating synthetic data and loading SQLite database...")

    subprocess.run(
        [sys.executable, str(GENERATE_DATA_SCRIPT)],
        check=True,
        cwd=PROJECT_ROOT,
    )

    subprocess.run(
        [sys.executable, str(LOAD_TO_SQLITE_SCRIPT)],
        check=True,
        cwd=PROJECT_ROOT,
    )

    print("Database bootstrap completed successfully.")


def _database_has_required_tables(db_path: Path) -> bool:
    """Return True when the SQLite database exists and contains app tables."""
    if not db_path.exists():
        return False

    try:
        with sqlite3.connect(db_path) as connection:
            cursor = connection.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table';"
            )
            tables = {row[0] for row in cursor.fetchall()}
    except sqlite3.Error:
        return False

    return REQUIRED_TABLES.issubset(tables)
