import type {
  BuyerRevenuePoint,
  CategoryRevenuePoint,
  DashboardRecord,
  KpiMetrics,
  MonthlyRevenuePoint,
  PaymentDelayRiskPoint,
  StatusBreakdownPoint,
} from "../types/dashboard";

const SUCCESS_STATUSES = new Set(["completed", "approved"]);

export function numberValue(value: number | null | undefined): number {
  return typeof value === "number" && Number.isFinite(value) ? value : 0;
}

export function getServiceCategory(record: DashboardRecord): string {
  return record.category || record.service_category || "Uncategorized";
}

export function getBuyerName(record: DashboardRecord): string {
  return record.company_name || record.buyer_id || "Unknown buyer";
}

export function getStatus(record: DashboardRecord): string {
  return record.status || "unknown";
}

export function parseDate(value: string | null | undefined): Date | null {
  if (!value) {
    return null;
  }

  const parsed = new Date(value);
  return Number.isNaN(parsed.getTime()) ? null : parsed;
}

export function getPaymentDelayDays(record: DashboardRecord): number | null {
  if (typeof record.payment_delay_days === "number" && Number.isFinite(record.payment_delay_days)) {
    return record.payment_delay_days;
  }

  const dueDate = parseDate(record.payment_due_date);
  const paidAt = parseDate(record.paid_at);

  if (!dueDate || !paidAt) {
    return null;
  }

  const millisecondsPerDay = 1000 * 60 * 60 * 24;
  const delayDays = Math.ceil((paidAt.getTime() - dueDate.getTime()) / millisecondsPerDay);

  return Math.max(delayDays, 0);
}

function uniqueWorkOrders(records: DashboardRecord[]): DashboardRecord[] {
  const workOrders = new Map<string, DashboardRecord>();

  for (const record of records) {
    if (!workOrders.has(record.work_order_id)) {
      workOrders.set(record.work_order_id, record);
    }
  }

  return Array.from(workOrders.values());
}

export function calculateKpis(records: DashboardRecord[]): KpiMetrics {
  const workOrders = uniqueWorkOrders(records);
  const totalWorkOrders = workOrders.length;
  const grossWorkOrderValue = workOrders.reduce((sum, record) => sum + numberValue(record.total_amount), 0);
  const platformRevenue = workOrders.reduce((sum, record) => sum + numberValue(record.platform_fee), 0);
  const providerPayout = workOrders.reduce((sum, record) => sum + numberValue(record.provider_payout), 0);
  const successfulOrders = workOrders.filter((record) => SUCCESS_STATUSES.has(getStatus(record))).length;
  const cancelledOrders = workOrders.filter((record) => getStatus(record) === "cancelled").length;
  const delays = records
    .map((record) => getPaymentDelayDays(record))
    .filter((delay): delay is number => delay !== null);

  return {
    totalWorkOrders,
    grossWorkOrderValue,
    platformRevenue,
    providerPayout,
    takeRate: grossWorkOrderValue ? (platformRevenue / grossWorkOrderValue) * 100 : 0,
    successRate: totalWorkOrders ? (successfulOrders / totalWorkOrders) * 100 : 0,
    cancellationRate: totalWorkOrders ? (cancelledOrders / totalWorkOrders) * 100 : 0,
    averagePaymentDelay: delays.length ? delays.reduce((sum, delay) => sum + delay, 0) / delays.length : null,
  };
}

export function buildMonthlyRevenue(records: DashboardRecord[]): MonthlyRevenuePoint[] {
  const months = new Map<string, MonthlyRevenuePoint>();

  for (const record of uniqueWorkOrders(records)) {
    const createdAt = parseDate(record.created_at);

    if (!createdAt) {
      continue;
    }

    const month = createdAt.toLocaleDateString("en-US", {
      month: "short",
      year: "2-digit",
    });

    const current = months.get(month) ?? {
      month,
      grossWorkOrderValue: 0,
      platformRevenue: 0,
      providerPayout: 0,
    };

    current.grossWorkOrderValue += numberValue(record.total_amount);
    current.platformRevenue += numberValue(record.platform_fee);
    current.providerPayout += numberValue(record.provider_payout);
    months.set(month, current);
  }

  return Array.from(months.values()).sort((left, right) => {
    const leftDate = new Date(`01 ${left.month}`);
    const rightDate = new Date(`01 ${right.month}`);
    return leftDate.getTime() - rightDate.getTime();
  });
}

export function buildStatusBreakdown(records: DashboardRecord[]): StatusBreakdownPoint[] {
  const statuses = new Map<string, number>();

  for (const record of uniqueWorkOrders(records)) {
    const status = getStatus(record);
    statuses.set(status, (statuses.get(status) ?? 0) + 1);
  }

  return Array.from(statuses.entries())
    .map(([status, totalWorkOrders]) => ({ status, totalWorkOrders }))
    .sort((left, right) => right.totalWorkOrders - left.totalWorkOrders);
}

export function buildCategoryRevenue(records: DashboardRecord[]): CategoryRevenuePoint[] {
  const categories = new Map<string, number>();

  for (const record of uniqueWorkOrders(records)) {
    const category = getServiceCategory(record);
    categories.set(category, (categories.get(category) ?? 0) + numberValue(record.platform_fee));
  }

  return Array.from(categories.entries())
    .map(([category, platformRevenue]) => ({ category, platformRevenue }))
    .sort((left, right) => right.platformRevenue - left.platformRevenue);
}

export function buildTopBuyers(records: DashboardRecord[], limit = 10): BuyerRevenuePoint[] {
  const buyers = new Map<string, BuyerRevenuePoint>();

  for (const record of uniqueWorkOrders(records)) {
    const companyName = getBuyerName(record);
    const current = buyers.get(companyName) ?? {
      companyName,
      buyerIndustry: record.buyer_industry || "Unknown",
      platformRevenue: 0,
    };

    current.platformRevenue += numberValue(record.platform_fee);
    buyers.set(companyName, current);
  }

  return Array.from(buyers.values())
    .sort((left, right) => right.platformRevenue - left.platformRevenue)
    .slice(0, limit);
}

export function buildPaymentDelayRisk(records: DashboardRecord[], limit = 10): PaymentDelayRiskPoint[] {
  const buyers = new Map<
    string,
    {
      companyName: string;
      delayTotal: number;
      latePayments: number;
      paymentCount: number;
    }
  >();

  for (const record of records) {
    const delay = getPaymentDelayDays(record);

    if (!record.payment_id || delay === null) {
      continue;
    }

    const companyName = getBuyerName(record);
    const current = buyers.get(companyName) ?? {
      companyName,
      delayTotal: 0,
      latePayments: 0,
      paymentCount: 0,
    };

    current.delayTotal += delay;
    current.latePayments += delay > 0 ? 1 : 0;
    current.paymentCount += 1;
    buyers.set(companyName, current);
  }

  return Array.from(buyers.values())
    .filter((buyer) => buyer.paymentCount > 0)
    .map((buyer) => ({
      companyName: buyer.companyName,
      averagePaymentDelay: buyer.delayTotal / buyer.paymentCount,
      latePaymentRate: (buyer.latePayments / buyer.paymentCount) * 100,
      paymentCount: buyer.paymentCount,
    }))
    .sort((left, right) => right.averagePaymentDelay - left.averagePaymentDelay)
    .slice(0, limit);
}

export function formatCurrency(value: number): string {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 0,
  }).format(value);
}

export function formatCompactCurrency(value: number): string {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    notation: "compact",
    maximumFractionDigits: 1,
  }).format(value);
}

export function formatNumber(value: number): string {
  return new Intl.NumberFormat("en-US").format(value);
}

export function formatPercent(value: number): string {
  return `${value.toFixed(1)}%`;
}

export function formatDays(value: number | null): string {
  return value === null ? "N/A" : `${value.toFixed(1)} days`;
}

export function formatDate(value: string | null | undefined): string {
  const date = parseDate(value);

  if (!date) {
    return "N/A";
  }

  return date.toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
  });
}

export function titleCase(value: string): string {
  return value.replace(/_/g, " ").replace(/\b\w/g, (character) => character.toUpperCase());
}
