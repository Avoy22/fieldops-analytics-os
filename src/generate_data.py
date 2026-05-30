"""
FieldOps Analytics OS synthetic data generator.

Version: v0.2

Creates realistic CSV files for a field-service marketplace:
- buyers
- providers
- work orders
- payments
- reviews
- support tickets
"""

import random
from pathlib import Path

import numpy as np
import pandas as pd
from faker import Faker


# ---------------------------------------------------------------------------
# Project settings
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_RAW_DIR = PROJECT_ROOT / "data" / "raw"

SEED = 42
random.seed(SEED)
rng = np.random.default_rng(SEED)
fake = Faker("en_US")
Faker.seed(SEED)

N_BUYERS = 500
N_PROVIDERS = 1_500
N_WORK_ORDERS = 10_000


# ---------------------------------------------------------------------------
# Lookup values
# ---------------------------------------------------------------------------

SERVICE_CATEGORIES = [
    "HVAC",
    "Plumbing",
    "Electrical",
    "Cleaning",
    "Landscaping",
    "Security Systems",
    "Appliance Repair",
    "General Maintenance",
    "Roofing",
    "Pest Control",
    "Snow Removal",
    "Locksmith",
]

PROVIDER_SKILLS = [
    "Preventive Maintenance",
    "Emergency Repair",
    "Installation",
    "Inspection",
    "Troubleshooting",
    "Compliance Checks",
    "Equipment Replacement",
    "Site Cleanup",
    "Warranty Service",
    "After-hours Dispatch",
]

BUYER_INDUSTRIES = [
    "Retail",
    "Hospitality",
    "Property Management",
    "Healthcare",
    "Education",
    "Logistics",
    "Manufacturing",
    "Financial Services",
    "Food Service",
    "Public Sector",
]

MARKETS = [
    {"city": "Atlanta", "state": "GA", "country": "USA"},
    {"city": "Austin", "state": "TX", "country": "USA"},
    {"city": "Boston", "state": "MA", "country": "USA"},
    {"city": "Charlotte", "state": "NC", "country": "USA"},
    {"city": "Chicago", "state": "IL", "country": "USA"},
    {"city": "Dallas", "state": "TX", "country": "USA"},
    {"city": "Denver", "state": "CO", "country": "USA"},
    {"city": "Los Angeles", "state": "CA", "country": "USA"},
    {"city": "Miami", "state": "FL", "country": "USA"},
    {"city": "Nashville", "state": "TN", "country": "USA"},
    {"city": "New York", "state": "NY", "country": "USA"},
    {"city": "Phoenix", "state": "AZ", "country": "USA"},
    {"city": "Seattle", "state": "WA", "country": "USA"},
    {"city": "Toronto", "state": "ON", "country": "Canada"},
    {"city": "Vancouver", "state": "BC", "country": "Canada"},
]


def money(value):
    """Return a clean currency value."""
    return round(float(value), 2)


def choose_market():
    """Pick one service market."""
    return random.choice(MARKETS)


def random_timestamp(start, end):
    """Return a random timestamp between two dates."""
    start_ts = pd.Timestamp(start)
    end_ts = pd.Timestamp(end)
    total_hours = int((end_ts - start_ts).total_seconds() // 3600)
    return start_ts + pd.Timedelta(hours=int(rng.integers(0, total_hours + 1)))


def blank_if_missing(value):
    """Keep missing dates readable in CSV output."""
    if pd.isna(value):
        return ""
    return value


def generate_buyers(n_buyers=N_BUYERS):
    """Generate companies that buy field-service work."""
    rows = []

    for i in range(1, n_buyers + 1):
        market = choose_market()
        rows.append(
            {
                "buyer_id": f"B{i:05d}",
                "company_name": fake.company(),
                "industry": random.choice(BUYER_INDUSTRIES),
                "buyer_tier": random.choices(
                    ["small_business", "mid_market", "enterprise"],
                    weights=[50, 35, 15],
                    k=1,
                )[0],
                "contact_name": fake.name(),
                "email": fake.company_email(),
                "phone": fake.phone_number(),
                "city": market["city"],
                "state": market["state"],
                "country": market["country"],
                "created_at": random_timestamp("2022-01-01", "2025-12-31"),
                "is_active": random.choices([True, False], weights=[94, 6], k=1)[0],
            }
        )

    return pd.DataFrame(rows)


def generate_providers(n_providers=N_PROVIDERS):
    """Generate service providers with categories, skills, and markets."""
    rows = []

    for i in range(1, n_providers + 1):
        market = choose_market()
        primary_category = random.choice(SERVICE_CATEGORIES)
        skill_count = int(rng.integers(2, 5))
        skills = random.sample(PROVIDER_SKILLS, skill_count)

        rows.append(
            {
                "provider_id": f"P{i:05d}",
                "provider_name": fake.company(),
                "business_type": random.choices(
                    ["independent_contractor", "small_business", "regional_vendor"],
                    weights=[46, 38, 16],
                    k=1,
                )[0],
                "primary_category": primary_category,
                "skills": " | ".join(skills),
                "city": market["city"],
                "state": market["state"],
                "country": market["country"],
                "onboarded_at": random_timestamp("2022-01-01", "2025-12-31"),
                "hourly_rate": money(rng.uniform(45, 175)),
                "average_rating": round(float(np.clip(rng.normal(4.35, 0.42), 2.8, 5.0)), 2),
                "is_active": random.choices([True, False], weights=[90, 10], k=1)[0],
            }
        )

    return pd.DataFrame(rows)


def work_order_amount(category, priority):
    """Create realistic order values by service category and urgency."""
    category_ranges = {
        "HVAC": (300, 3_500),
        "Plumbing": (180, 2_400),
        "Electrical": (220, 2_800),
        "Cleaning": (90, 1_200),
        "Landscaping": (150, 1_800),
        "Security Systems": (350, 4_500),
        "Appliance Repair": (120, 1_300),
        "General Maintenance": (100, 1_600),
        "Roofing": (500, 6_500),
        "Pest Control": (100, 1_000),
        "Snow Removal": (120, 1_500),
        "Locksmith": (80, 700),
    }

    low, high = category_ranges[category]
    amount = rng.uniform(low, high)

    if priority == "emergency":
        amount *= 1.45
    elif priority == "high":
        amount *= 1.18

    return money(amount)


def lifecycle_dates(status):
    """Create dates that follow a simple work-order lifecycle."""
    created_at = random_timestamp("2025-01-01", "2025-12-31")
    assigned_at = pd.NaT
    completed_at = pd.NaT
    approved_at = pd.NaT

    if status in ["assigned", "completed", "approved"]:
        assigned_at = created_at + pd.Timedelta(hours=int(rng.integers(2, 96)))

    if status in ["completed", "approved"]:
        completed_at = assigned_at + pd.Timedelta(days=int(rng.integers(1, 15)))

    if status == "approved":
        approved_at = completed_at + pd.Timedelta(days=int(rng.integers(1, 6)))

    return created_at, assigned_at, completed_at, approved_at


def generate_work_orders(buyers, providers, n_work_orders=N_WORK_ORDERS):
    """Generate work orders with valid buyer and provider references."""
    buyer_ids = buyers["buyer_id"].to_numpy()
    provider_ids = providers["provider_id"].to_numpy()
    provider_categories = providers.set_index("provider_id")["primary_category"].to_dict()

    rows = []
    for i in range(1, n_work_orders + 1):
        buyer_id = str(rng.choice(buyer_ids))
        provider_id = str(rng.choice(provider_ids))
        category = provider_categories[provider_id]
        market = choose_market()

        status = random.choices(
            ["completed", "cancelled", "assigned", "pending", "approved"],
            weights=[38, 9, 16, 12, 25],
            k=1,
        )[0]
        priority = random.choices(
            ["low", "standard", "high", "emergency"],
            weights=[12, 61, 21, 6],
            k=1,
        )[0]

        total_amount = work_order_amount(category, priority)
        take_rate = round(float(rng.uniform(0.12, 0.22)), 4)
        platform_fee = money(total_amount * take_rate)
        provider_payout = money(total_amount - platform_fee)
        created_at, assigned_at, completed_at, approved_at = lifecycle_dates(status)

        rows.append(
            {
                "work_order_id": f"WO{i:06d}",
                "buyer_id": buyer_id,
                "provider_id": provider_id,
                "service_category": category,
                "work_order_title": f"{category} - {random.choice(PROVIDER_SKILLS)}",
                "city": market["city"],
                "state": market["state"],
                "country": market["country"],
                "priority": priority,
                "status": status,
                "created_at": created_at,
                "assigned_at": blank_if_missing(assigned_at),
                "completed_at": blank_if_missing(completed_at),
                "approved_at": blank_if_missing(approved_at),
                "total_amount": total_amount,
                "platform_fee": platform_fee,
                "provider_payout": provider_payout,
                "take_rate": take_rate,
                "is_emergency": priority == "emergency",
            }
        )

    return pd.DataFrame(rows)


def generate_payments(work_orders):
    """Generate payments only for completed or approved work orders."""
    payable_orders = work_orders[work_orders["status"].isin(["completed", "approved"])].copy()
    payment_methods = ["ach", "credit_card", "wire_transfer", "check"]

    rows = []
    for i, order in enumerate(payable_orders.itertuples(index=False), start=1):
        milestone_at = pd.Timestamp(order.approved_at or order.completed_at)
        payment_due_date = milestone_at + pd.Timedelta(days=30)

        # Most payments happen before the due date, but some are late or unpaid.
        payment_status = random.choices(
            ["paid", "late", "pending"],
            weights=[72, 18, 10],
            k=1,
        )[0]

        paid_at = ""
        days_to_pay = ""
        is_late = False
        if payment_status in ["paid", "late"]:
            if payment_status == "paid":
                delay_days = int(rng.integers(3, 30))
            else:
                delay_days = int(rng.integers(31, 85))
            paid_at = milestone_at + pd.Timedelta(days=delay_days)
            days_to_pay = delay_days
            is_late = paid_at > payment_due_date

        rows.append(
            {
                "payment_id": f"PAY{i:06d}",
                "work_order_id": order.work_order_id,
                "buyer_id": order.buyer_id,
                "provider_id": order.provider_id,
                "payment_status": payment_status,
                "payment_method": random.choice(payment_methods),
                "payment_due_date": payment_due_date,
                "paid_at": paid_at,
                "total_amount": order.total_amount,
                "platform_fee": order.platform_fee,
                "provider_payout": order.provider_payout,
                "take_rate": order.take_rate,
                "days_to_pay": days_to_pay,
                "is_late": is_late,
            }
        )

    return pd.DataFrame(rows)


def generate_reviews(work_orders):
    """Generate reviews for a realistic share of completed work orders."""
    completed_orders = work_orders[work_orders["status"] == "completed"].copy()
    reviewed_orders = completed_orders.sample(frac=0.68, random_state=SEED)

    positive_comments = [
        "Professional service and clear communication.",
        "Completed the job quickly and documented the work well.",
        "Strong workmanship and easy scheduling.",
        "The provider arrived on time and resolved the issue.",
    ]
    neutral_comments = [
        "Work was completed, but communication could improve.",
        "Good outcome after a minor scheduling delay.",
        "Service was acceptable for the price.",
    ]
    negative_comments = [
        "The issue required a follow-up visit.",
        "Scheduling was difficult and the work took longer than expected.",
        "Quality did not fully meet expectations.",
    ]

    rows = []
    for i, order in enumerate(reviewed_orders.itertuples(index=False), start=1):
        rating = random.choices([1, 2, 3, 4, 5], weights=[2, 4, 11, 35, 48], k=1)[0]
        if rating >= 4:
            review_text = random.choice(positive_comments)
        elif rating == 3:
            review_text = random.choice(neutral_comments)
        else:
            review_text = random.choice(negative_comments)

        completed_at = pd.Timestamp(order.completed_at)
        review_date = completed_at + pd.Timedelta(days=int(rng.integers(1, 12)))

        rows.append(
            {
                "review_id": f"REV{i:06d}",
                "work_order_id": order.work_order_id,
                "buyer_id": order.buyer_id,
                "provider_id": order.provider_id,
                "rating": rating,
                "review_date": review_date,
                "review_text": review_text,
                "would_rehire": rating >= 4,
            }
        )

    return pd.DataFrame(rows)


def generate_support_tickets(buyers, work_orders):
    """Generate support tickets for a realistic subset of work orders."""
    ticket_count = int(len(work_orders) * 0.12)
    work_order_sample = work_orders.sample(n=ticket_count, random_state=SEED).copy()
    buyer_ids = buyers["buyer_id"].to_numpy()

    ticket_types = [
        "scheduling",
        "payment",
        "provider_quality",
        "cancellation",
        "invoice",
        "account_access",
    ]

    rows = []
    for i, order in enumerate(work_order_sample.itertuples(index=False), start=1):
        linked_to_work_order = random.choices([True, False], weights=[86, 14], k=1)[0]
        buyer_id = order.buyer_id if linked_to_work_order else str(rng.choice(buyer_ids))
        work_order_id = order.work_order_id if linked_to_work_order else ""

        opened_at = pd.Timestamp(order.created_at) + pd.Timedelta(days=int(rng.integers(0, 25)))
        status = random.choices(["open", "resolved", "escalated"], weights=[16, 76, 8], k=1)[0]
        resolution_hours = ""
        closed_at = ""

        if status == "resolved":
            resolution_hours = int(rng.integers(4, 168))
            closed_at = opened_at + pd.Timedelta(hours=resolution_hours)

        rows.append(
            {
                "ticket_id": f"TKT{i:06d}",
                "buyer_id": buyer_id,
                "work_order_id": work_order_id,
                "ticket_type": random.choice(ticket_types),
                "priority": random.choices(["low", "medium", "high"], weights=[34, 48, 18], k=1)[0],
                "status": status,
                "opened_at": opened_at,
                "closed_at": closed_at,
                "resolution_hours": resolution_hours,
                "channel": random.choice(["email", "phone", "chat", "web_form"]),
            }
        )

    return pd.DataFrame(rows)


def save_csv(dataframes):
    """Save all generated tables to data/raw."""
    DATA_RAW_DIR.mkdir(parents=True, exist_ok=True)

    for name, dataframe in dataframes.items():
        output_path = DATA_RAW_DIR / f"{name}.csv"
        dataframe.to_csv(output_path, index=False)


def print_summary(dataframes):
    """Print a simple generation summary."""
    print("\nFieldOps Analytics OS v0.2 synthetic data generated")
    print("-" * 54)
    for name, dataframe in dataframes.items():
        print(f"{name:18s} {len(dataframe):>8,} rows")
    print("-" * 54)
    print(f"Output folder: {DATA_RAW_DIR}")


def main():
    buyers = generate_buyers()
    providers = generate_providers()
    work_orders = generate_work_orders(buyers, providers)
    payments = generate_payments(work_orders)
    reviews = generate_reviews(work_orders)
    support_tickets = generate_support_tickets(buyers, work_orders)

    dataframes = {
        "buyers": buyers,
        "providers": providers,
        "work_orders": work_orders,
        "payments": payments,
        "reviews": reviews,
        "support_tickets": support_tickets,
    }

    save_csv(dataframes)
    print_summary(dataframes)


if __name__ == "__main__":
    main()
