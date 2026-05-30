"""
Load synthetic FieldOps CSV data into a SQLite database.

Input:
- data/raw/buyers.csv
- data/raw/providers.csv
- data/raw/work_orders.csv
- data/raw/payments.csv
- data/raw/reviews.csv
- data/raw/support_tickets.csv

Output:
- data/processed/fieldops.db
"""

from pathlib import Path
import sqlite3

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"
DB_PATH = PROCESSED_DATA_DIR / "fieldops.db"

TABLE_FILES = {
    "buyers": "buyers.csv",
    "providers": "providers.csv",
    "work_orders": "work_orders.csv",
    "payments": "payments.csv",
    "reviews": "reviews.csv",
    "support_tickets": "support_tickets.csv",
}


def validate_csv_files() -> None:
    """Check that all required CSV files exist before loading."""
    missing_files = []

    for filename in TABLE_FILES.values():
        file_path = RAW_DATA_DIR / filename
        if not file_path.exists():
            missing_files.append(str(file_path))

    if missing_files:
        missing = "\n".join(missing_files)
        raise FileNotFoundError(
            f"Missing required CSV files:\n{missing}\n\n"
            "Run this first:\npython src/generate_data.py"
        )


def reset_database_file() -> None:
    """Remove the old SQLite database files before rebuilding from CSV."""
    for path in [
        DB_PATH,
        DB_PATH.with_name(f"{DB_PATH.name}-journal"),
        DB_PATH.with_name(f"{DB_PATH.name}-wal"),
        DB_PATH.with_name(f"{DB_PATH.name}-shm"),
    ]:
        if path.exists():
            try:
                path.unlink()
            except PermissionError as error:
                raise PermissionError(
                    f"Could not remove {path}.\n"
                    "Close any app using the database, then run this script again."
                ) from error


def load_csv_to_table(connection: sqlite3.Connection, table_name: str, filename: str) -> int:
    """Load one CSV file into a SQLite table."""
    file_path = RAW_DATA_DIR / filename
    df = pd.read_csv(file_path)

    if table_name == "work_orders" and "service_category" in df.columns:
        df = df.rename(columns={"service_category": "category"})

    df.to_sql(table_name, connection, if_exists="replace", index=False)

    return len(df)


def create_indexes(connection: sqlite3.Connection) -> None:
    """Create indexes to make analytical queries faster."""
    cursor = connection.cursor()

    index_statements = [
        "CREATE INDEX IF NOT EXISTS idx_work_orders_buyer_id ON work_orders(buyer_id);",
        "CREATE INDEX IF NOT EXISTS idx_work_orders_provider_id ON work_orders(provider_id);",
        "CREATE INDEX IF NOT EXISTS idx_work_orders_status ON work_orders(status);",
        "CREATE INDEX IF NOT EXISTS idx_work_orders_category ON work_orders(category);",
        "CREATE INDEX IF NOT EXISTS idx_work_orders_created_at ON work_orders(created_at);",
        "CREATE INDEX IF NOT EXISTS idx_payments_work_order_id ON payments(work_order_id);",
    ]

    for statement in index_statements:
        cursor.execute(statement)

    connection.commit()


def print_database_summary(connection: sqlite3.Connection) -> None:
    """Print row counts for each database table."""
    print("\nDatabase Summary")
    print("----------------")

    for table_name in TABLE_FILES.keys():
        count = pd.read_sql_query(f"SELECT COUNT(*) AS row_count FROM {table_name}", connection)
        print(f"{table_name}: {count.loc[0, 'row_count']:,} rows")


def main() -> None:
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

    validate_csv_files()
    reset_database_file()

    with sqlite3.connect(DB_PATH) as connection:
        print(f"Loading CSV files into SQLite database: {DB_PATH}")

        for table_name, filename in TABLE_FILES.items():
            row_count = load_csv_to_table(connection, table_name, filename)
            print(f"Loaded {table_name}: {row_count:,} rows")

        create_indexes(connection)
        print("Indexes created successfully.")

        print_database_summary(connection)

    print("\nSQLite database created successfully.")


if __name__ == "__main__":
    main()
