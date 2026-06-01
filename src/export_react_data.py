"""
Export FieldOps Analytics OS SQLite data for the React dashboard.

Output:
- frontend/public/data/dashboard-data.json
- frontend/public/data/metadata.json
"""

from datetime import datetime
from pathlib import Path
import sqlite3
import json

import pandas as pd

from src.bootstrap_data import ensure_database_exists


DB_PATH = Path("data/processed/fieldops.db")
OUTPUT_DIR = Path("frontend/public/data")


def load_dashboard_dataset() -> pd.DataFrame:
    """Load joined dashboard dataset from SQLite."""
    query = """
    SELECT
        w.work_order_id,
        w.buyer_id,
        b.company_name,
        b.industry AS buyer_industry,
        w.provider_id,
        w.category,
        w.status,
        w.country,
        w.city,
        w.created_at,
        w.assigned_at,
        w.completed_at,
        w.approved_at,
        w.total_amount,
        w.platform_fee,
        w.provider_payout,
        w.take_rate,
        p.payment_id,
        p.payment_status,
        p.payment_due_date,
        p.paid_at
    FROM work_orders w
    LEFT JOIN buyers b
        ON w.buyer_id = b.buyer_id
    LEFT JOIN payments p
        ON w.work_order_id = p.work_order_id;
    """

    with sqlite3.connect(DB_PATH) as connection:
        return pd.read_sql_query(query, connection)


def main() -> None:
    ensure_database_exists()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    df = load_dashboard_dataset()

    data_path = OUTPUT_DIR / "dashboard-data.json"
    metadata_path = OUTPUT_DIR / "metadata.json"

    df.to_json(data_path, orient="records", date_format="iso", indent=2)

    metadata = {
        "generated_at": datetime.utcnow().isoformat(),
        "total_records": int(len(df)),
        "source": "FieldOps Analytics OS SQLite export",
    }

    metadata_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    print(f"Exported dashboard data: {data_path}")
    print(f"Exported metadata: {metadata_path}")
    print(f"Total records: {len(df):,}")


if __name__ == "__main__":
    main()