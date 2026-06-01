export type DashboardRecord = {
  work_order_id: string;
  buyer_id: string;
  company_name: string | null;
  buyer_industry: string | null;
  provider_id: string | null;
  category?: string | null;
  service_category?: string | null;
  status: string | null;
  country: string | null;
  city: string | null;
  created_at: string | null;
  assigned_at: string | null;
  completed_at: string | null;
  approved_at: string | null;
  total_amount: number | null;
  platform_fee: number | null;
  provider_payout: number | null;
  take_rate: number | null;
  payment_id: string | null;
  payment_status: string | null;
  payment_due_date: string | null;
  paid_at: string | null;
  payment_delay_days?: number | null;
  days_to_pay?: number | null;
};

export type DashboardFilters = {
  startDate: string;
  endDate: string;
  categories: string[];
  statuses: string[];
  industries: string[];
  countries: string[];
};

export type FilterOptions = {
  categories: string[];
  statuses: string[];
  industries: string[];
  countries: string[];
  minDate: string;
  maxDate: string;
};

export type KpiMetrics = {
  totalWorkOrders: number;
  grossWorkOrderValue: number;
  platformRevenue: number;
  providerPayout: number;
  takeRate: number;
  successRate: number;
  cancellationRate: number;
  averagePaymentDelay: number | null;
};

export type MonthlyRevenuePoint = {
  month: string;
  grossWorkOrderValue: number;
  platformRevenue: number;
  providerPayout: number;
};

export type StatusBreakdownPoint = {
  status: string;
  totalWorkOrders: number;
};

export type CategoryRevenuePoint = {
  category: string;
  platformRevenue: number;
};

export type BuyerRevenuePoint = {
  companyName: string;
  buyerIndustry: string;
  platformRevenue: number;
};

export type PaymentDelayRiskPoint = {
  companyName: string;
  averagePaymentDelay: number;
  latePaymentRate: number;
  paymentCount: number;
};
