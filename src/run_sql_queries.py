"""
Run FieldOps SQL analysis files and export the results to CSV.

Input:
- sql/*.sql
- data/processed/fieldops.db

Output:
- reports/query_outputs/*.csv
"""

from pathlib import Path
import sqlite3

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SQL_DIR = PROJECT_ROOT / "sql"
DB_PATH = PROJECT_ROOT / "data" / "processed" / "fieldops.db"
OUTPUT_DIR = PROJECT_ROOT / "reports" / "query_outputs"


def validate_inputs() -> list[Path]:
    """Check that the database and SQL files exist."""
    if not DB_PATH.exists():
        raise FileNotFoundError(
            f"Database not found: {DB_PATH}\n\n"
            "Run this first:\npython src/load_to_sqlite.py"
        )

    sql_files = sorted(SQL_DIR.glob("*.sql"))
    if not sql_files:
        raise FileNotFoundError(f"No SQL files found in: {SQL_DIR}")

    return sql_files


def run_query(connection: sqlite3.Connection, sql_file: Path) -> pd.DataFrame:
    """Run one SQL file and return the result as a dataframe."""
    query = sql_file.read_text(encoding="utf-8")
    return pd.read_sql_query(query, connection)


def main() -> None:
    sql_files = validate_inputs()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DB_PATH) as connection:
        print(f"Running SQL queries against: {DB_PATH}")

        for sql_file in sql_files:
            result = run_query(connection, sql_file)
            output_path = OUTPUT_DIR / f"{sql_file.stem}.csv"
            result.to_csv(output_path, index=False)

            print(f"Exported {sql_file.name}: {len(result):,} rows -> {output_path}")

    print("\nAll query outputs exported successfully.")


if __name__ == "__main__":
    main()
