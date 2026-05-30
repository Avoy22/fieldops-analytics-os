# Data Model

FieldOps Analytics OS uses a synthetic relational data model that represents a field-service marketplace. The model is designed for business intelligence analysis across finance, operations, buyer behavior, provider performance, support, and payment risk.

## Entity Relationship Overview

```text
buyers 1--* work_orders *--1 providers
              |
              |-- payments
              |-- reviews
              `-- support_tickets
```

## Analytical Grain

| Table | Grain |
| --- | --- |
| `buyers` | One row per buyer company. |
| `providers` | One row per service provider. |
| `work_orders` | One row per field-service work order. |
| `payments` | One row per payable work order payment. |
| `reviews` | One row per buyer review. |
| `support_tickets` | One row per support issue. |

## Table Summary

### `buyers`

Stores companies that purchase field-service work.

Key fields:

- `buyer_id`
- `company_name`
- `industry`
- `buyer_tier`
- `city`, `state`, `country`
- `created_at`
- `is_active`

Common analysis:

- Top buyers by revenue
- Buyer tier performance
- Buyer concentration
- Payment risk by buyer

### `providers`

Stores service providers and vendors available in the marketplace.

Key fields:

- `provider_id`
- `provider_name`
- `business_type`
- `primary_category`
- `skills`
- `city`, `state`, `country`
- `hourly_rate`
- `average_rating`
- `is_active`

Common analysis:

- Provider payout
- Provider completion performance
- Category supply mix
- Provider rating and review volume

### `work_orders`

Stores the main marketplace transaction records.

Key fields:

- `work_order_id`
- `buyer_id`
- `provider_id`
- `category`
- `priority`
- `status`
- `created_at`, `assigned_at`, `completed_at`, `approved_at`
- `total_amount`
- `platform_fee`
- `provider_payout`
- `take_rate`
- `is_emergency`

Note: the raw CSV uses `service_category`; the SQLite loader renames this column to `category` for analysis consistency.

Common analysis:

- Gross work order value
- Platform revenue
- Provider payout
- Take rate
- Average work order value
- Work order success and cancellation rate
- Category and location performance

### `payments`

Stores payment outcomes for completed or approved work orders.

Key fields:

- `payment_id`
- `work_order_id`
- `buyer_id`
- `provider_id`
- `payment_status`
- `payment_method`
- `payment_due_date`
- `paid_at`
- `total_amount`
- `platform_fee`
- `provider_payout`
- `take_rate`
- `days_to_pay`
- `is_late`

Common analysis:

- Late payment rate
- Pending payment exposure
- Average days to pay
- Average days after due date
- Buyer-level payment risk

### `reviews`

Stores buyer reviews for a sample of completed work orders.

Key fields:

- `review_id`
- `work_order_id`
- `buyer_id`
- `provider_id`
- `rating`
- `review_date`
- `review_text`
- `would_rehire`

Common analysis:

- Provider rating
- Review count
- Customer satisfaction proxy
- Provider quality context

### `support_tickets`

Stores support issues tied to buyers and, in most cases, work orders.

Key fields:

- `ticket_id`
- `buyer_id`
- `work_order_id`
- `ticket_type`
- `priority`
- `status`
- `opened_at`
- `closed_at`
- `resolution_hours`
- `channel`

Common analysis:

- Support volume
- Escalated ticket rate
- Ticket type mix
- Operational friction by buyer or work order

## Relationship Keys

| Relationship | Join condition |
| --- | --- |
| Buyers to work orders | `buyers.buyer_id = work_orders.buyer_id` |
| Providers to work orders | `providers.provider_id = work_orders.provider_id` |
| Work orders to payments | `work_orders.work_order_id = payments.work_order_id` |
| Work orders to reviews | `work_orders.work_order_id = reviews.work_order_id` |
| Work orders to support tickets | `work_orders.work_order_id = support_tickets.work_order_id` |

## Design Notes

- The model is intentionally simple enough to run locally while still supporting realistic BI analysis.
- `work_orders` is the primary fact table for marketplace volume, revenue, and operations.
- `payments` extends the finance layer into cash-flow and collections risk.
- `reviews` and `support_tickets` add operational quality context.
- The generated data uses a fixed seed, which makes the sample outputs reproducible.

