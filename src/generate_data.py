"""
Synthetic data generator for FieldOps Analytics OS.

This script creates a small, realistic marketplace dataset for field-service
analytics. It is intentionally beginner-friendly: each table has its own
function, and IDs are created first so relationships stay valid.
"""

from pathlib import Path

import numpy as np
import pandas as pd
from faker import Faker


# Keep paths relative to the project folder, even when the script is run from
# another directory.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_RAW_DIR = PROJECT_ROOT / "data" / "raw"

# A fixed seed makes the CSVs reproducible every time the script runs.
SEED = 42
fake = Faker("en_US")
Faker.seed(SEED)
rng = np.random.default_rng(SEED)


SERVICE_CATEGORIES = [
    "HVAC",
    "Plumbing",
    "Electrical",
    "Cleaning",
    "Landscaping",
    "Security Systems",
    "Appliance Repair",
    "General Maintenance",
]

US_MARKETS = [
    ("Atlanta", "GA"),
    ("Austin", "TX"),
    ("Charlotte", "NC"),
    ("Chicago", "IL"),
    ("Dallas", "TX"),
    ("Denver", "CO"),
    ("Miami", "FL"),
    ("Nashville", "TN"),
    ("Phoenix", "AZ"),
    ("Seattle", "WA"),
]


def money(value):
    """Round dollar amounts to two decimals for cleaner CSV output."""
    return round(float(value), 2)


def random_date(start, end):
    """Return a random date between two pandas timestamps."""
    days_between = (end - start).days
    return (start + pd.Timedelta(days=int(rng.integers(0, days_between + 1)))).date()


def generate_buyers(n_buyers=120):
    """Create companies that purchase field-service work."""
    industries = [
        "Retail",
        "Hospitality",
        "Property Management",
        "Healthcare",
        "Education",
        "Logistics",
        "Manufacturing",
    ]

    rows = []
    for i in range(1, n_buyers + 1):
        city, state = US_MARKETS[int(rng.integers(0, len(US_MARKETS)))]
        rows.append(
            {
                "buyer_id": f"B{i:04d}",
                "company_name": fake.company(),
                "industry": rng.choice(industries),
                "buyer_tier": rng.choice(["SMB", "Mid-Market", "Enterprise"], p=[0.55, 0.30, 0.15]),
                "contact_name": fake.name(),
                "email": fake.company_email(),
                "phone": fake.phone_number(),
                "city": city,
                "state": state,
                "account_created_date": random_date(pd.Timestamp("2023-01-01"), pd.Timestamp("2025-12-31")),
            }
        )

    return pd.DataFrame(rows)


def generate_providers(n_providers=80):
    """Create technicians or service businesses that complete work orders."""
    rows = []
    for i in range(1, n_providers + 1):
        city, state = US_MARKETS[int(rng.integers(0, len(US_MARKETS)))]
        category = rng.choice(SERVICE_CATEGORIES)
        rows.append(
            {
                "provider_id": f"P{i:04d}",
                "provider_name": fake.company(),
                "business_type": rng.choice(["Independent Contractor", "Small Business", "Regional Vendor"]),
                "primary_category": category,
                "city": city,
                "state": state,
                "onboarding_date": random_date(pd.Timestamp("2023-01-01"), pd.Timestamp("2025-12-31")),
                "hourly_rate": money(rng.uniform(45, 140)),
                "average_rating": round(float(rng.normal(4.4, 0.35)), 2),
                "is_active": rng.choice([True, False], p=[0.88, 0.12]),
            }
        )

    providers = pd.DataFrame(rows)
    providers["average_rating"] = providers["average_rating"].clip(3.0, 5.0)
    return providers


def generate_work_orders(buyers, providers, n_work_orders=900):
    """Create work orders that connect buyers to providers."""
    status_options = ["Completed", "Cancelled", "In Progress", "Assigned"]
    status_probabilities = [0.72, 0.10, 0.10, 0.08]
    priority_options = ["Low", "Standard", "High", "Emergency"]
    priority_probabilities = [0.15, 0.58, 0.20, 0.07]

    buyer_ids = buyers["buyer_id"].to_numpy()
    provider_ids = providers["provider_id"].to_numpy()
    provider_category = providers.set_index("provider_id")["primary_category"].to_dict()

    rows = []
    for i in range(1, n_work_orders + 1):
        buyer_id = rng.choice(buyer_ids)
        provider_id = rng.choice(provider_ids)
        status = rng.choice(status_options, p=status_probabilities)
        priority = rng.choice(priority_options, p=priority_probabilities)
        category = provider_category[provider_id]
        city, state = US_MARKETS[int(rng.integers(0, len(US_MARKETS)))]

        created_date = pd.Timestamp(random_date(pd.Timestamp("2025-01-01"), pd.Timestamp("2025-12-31")))
        scheduled_date = created_date + pd.Timedelta(days=int(rng.integers(1, 15)))

        completed_date = pd.NaT
        if status == "Completed":
            completion_days = int(rng.integers(0, 8))
            completed_date = scheduled_date + pd.Timedelta(days=completion_days)

        base_amount = rng.uniform(150, 2200)
        if priority == "Emergency":
            base_amount *= 1.35
        elif priority == "High":
            base_amount *= 1.15

        quoted_amount = money(base_amount)
        platform_fee = money(quoted_amount * rng.uniform(0.12, 0.20))
        provider_payout = money(quoted_amount - platform_fee)

        is_delayed = False
        if status == "Completed":
            is_delayed = completed_date > scheduled_date + pd.Timedelta(days=2)
        elif status == "In Progress":
            is_delayed = rng.choice([True, False], p=[0.35, 0.65])

        rows.append(
            {
                "work_order_id": f"WO{i:05d}",
                "buyer_id": buyer_id,
                "provider_id": provider_id,
                "category": category,
                "city": city,
                "state": state,
                "priority": priority,
                "status": status,
                "created_date": created_date.date(),
                "scheduled_date": scheduled_date.date(),
                "completed_date": completed_date.date() if pd.notna(completed_date) else "",
                "quoted_amount": quoted_amount,
                "platform_fee": platform_fee,
                "provider_payout": provider_payout,
                "is_delayed": bool(is_delayed),
            }
        )

    return pd.DataFrame(rows)


def generate_payments(work_orders):
    """Create one payment record for each non-cancelled work order."""
    payable_orders = work_orders[work_orders["status"] != "Cancelled"].copy()
    payment_methods = ["ACH", "Credit Card", "Wire Transfer", "Check"]

    rows = []
    for i, order in enumerate(payable_orders.itertuples(index=False), start=1):
        invoice_date = pd.Timestamp(order.completed_date or order.scheduled_date)
        due_date = invoice_date + pd.Timedelta(days=30)

        if order.status == "Completed":
            payment_status = rng.choice(["Paid", "Late", "Pending"], p=[0.78, 0.14, 0.08])
        else:
            payment_status = rng.choice(["Pending", "Paid"], p=[0.75, 0.25])

        paid_date = ""
        days_to_pay = ""
        is_late = False
        if payment_status in ["Paid", "Late"]:
            extra_days = int(rng.integers(5, 26)) if payment_status == "Paid" else int(rng.integers(31, 76))
            paid_timestamp = invoice_date + pd.Timedelta(days=extra_days)
            paid_date = paid_timestamp.date()
            days_to_pay = (paid_timestamp - invoice_date).days
            is_late = paid_timestamp > due_date

        rows.append(
            {
                "payment_id": f"PAY{i:05d}",
                "work_order_id": order.work_order_id,
                "buyer_id": order.buyer_id,
                "provider_id": order.provider_id,
                "invoice_date": invoice_date.date(),
                "due_date": due_date.date(),
                "paid_date": paid_date,
                "payment_status": payment_status,
                "payment_method": rng.choice(payment_methods),
                "gross_amount": order.quoted_amount,
                "platform_fee": order.platform_fee,
                "provider_payout": order.provider_payout,
                "days_to_pay": days_to_pay,
                "is_late": bool(is_late),
            }
        )

    return pd.DataFrame(rows)


def generate_reviews(work_orders):
    """Create buyer reviews for most completed work orders."""
    completed_orders = work_orders[work_orders["status"] == "Completed"].copy()
    reviewed_orders = completed_orders.sample(frac=0.82, random_state=SEED)
    comments = [
        "Professional service and clear communication.",
        "Work completed as expected.",
        "Good quality, but scheduling could improve.",
        "Fast response and strong workmanship.",
        "Issue required follow-up after the first visit.",
    ]

    rows = []
    for i, order in enumerate(reviewed_orders.itertuples(index=False), start=1):
        rating = int(rng.choice([1, 2, 3, 4, 5], p=[0.02, 0.04, 0.12, 0.34, 0.48]))
        completed_date = pd.Timestamp(order.completed_date)
        review_date = completed_date + pd.Timedelta(days=int(rng.integers(1, 10)))

        rows.append(
            {
                "review_id": f"REV{i:05d}",
                "work_order_id": order.work_order_id,
                "buyer_id": order.buyer_id,
                "provider_id": order.provider_id,
                "rating": rating,
                "review_date": review_date.date(),
                "review_text": rng.choice(comments),
                "would_rehire": rating >= 4,
            }
        )

    return pd.DataFrame(rows)


def generate_support_tickets(buyers, work_orders, n_tickets=180):
    """Create support tickets, usually linked to a buyer and sometimes to a work order."""
    ticket_types = ["Scheduling", "Payment", "Provider Quality", "Cancellation", "Account", "Invoice"]
    statuses = ["Open", "Resolved", "Escalated"]
    status_probabilities = [0.16, 0.76, 0.08]
    channels = ["Email", "Phone", "Chat", "Web Form"]

    buyer_ids = buyers["buyer_id"].to_numpy()
    work_order_lookup = work_orders.set_index("work_order_id")["buyer_id"].to_dict()
    work_order_ids = work_orders["work_order_id"].to_numpy()

    rows = []
    for i in range(1, n_tickets + 1):
        has_work_order = rng.choice([True, False], p=[0.72, 0.28])
        if has_work_order:
            work_order_id = rng.choice(work_order_ids)
            buyer_id = work_order_lookup[work_order_id]
        else:
            work_order_id = ""
            buyer_id = rng.choice(buyer_ids)

        status = rng.choice(statuses, p=status_probabilities)
        opened_date = pd.Timestamp(random_date(pd.Timestamp("2025-01-01"), pd.Timestamp("2026-01-31")))
        closed_date = ""
        resolution_hours = ""

        if status == "Resolved":
            resolution_hours = int(rng.integers(4, 168))
            closed_date = (opened_date + pd.Timedelta(hours=resolution_hours)).date()

        rows.append(
            {
                "ticket_id": f"TKT{i:05d}",
                "buyer_id": buyer_id,
                "work_order_id": work_order_id,
                "ticket_type": rng.choice(ticket_types),
                "priority": rng.choice(["Low", "Medium", "High"], p=[0.35, 0.45, 0.20]),
                "status": status,
                "opened_date": opened_date.date(),
                "closed_date": closed_date,
                "resolution_hours": resolution_hours,
                "channel": rng.choice(channels),
            }
        )

    return pd.DataFrame(rows)


def save_csv(dataframes):
    """Save each generated table as a CSV file in data/raw."""
    DATA_RAW_DIR.mkdir(parents=True, exist_ok=True)
    for name, dataframe in dataframes.items():
        output_path = DATA_RAW_DIR / f"{name}.csv"
        dataframe.to_csv(output_path, index=False)
        print(f"Saved {len(dataframe):,} rows to {output_path}")


def main():
    buyers = generate_buyers()
    providers = generate_providers()
    work_orders = generate_work_orders(buyers, providers)
    payments = generate_payments(work_orders)
    reviews = generate_reviews(work_orders)
    support_tickets = generate_support_tickets(buyers, work_orders)

    save_csv(
        {
            "buyers": buyers,
            "providers": providers,
            "work_orders": work_orders,
            "payments": payments,
            "reviews": reviews,
            "support_tickets": support_tickets,
        }
    )

    print("Synthetic data generation complete.")


if __name__ == "__main__":
    main()
