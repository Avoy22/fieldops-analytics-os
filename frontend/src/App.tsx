import { useEffect, useMemo, useState } from "react";
import {
  Banknote,
  BriefcaseBusiness,
  CheckCircle2,
  CircleDollarSign,
  Clock3,
  Percent,
  ReceiptText,
  XCircle,
} from "lucide-react";
import CategoryRevenueChart from "./components/CategoryRevenueChart";
import DataTable from "./components/DataTable";
import KpiCard from "./components/KpiCard";
import MetricGlossary from "./components/MetricGlossary";
import PaymentDelayRiskChart from "./components/PaymentDelayRiskChart";
import RevenueTrendChart from "./components/RevenueTrendChart";
import SidebarFilters from "./components/SidebarFilters";
import StatusBreakdownChart from "./components/StatusBreakdownChart";
import TopBuyersChart from "./components/TopBuyersChart";
import { createDefaultFilters, filterRecords, getFilterOptions } from "./lib/filters";
import {
  buildCategoryRevenue,
  buildMonthlyRevenue,
  buildPaymentDelayRisk,
  buildStatusBreakdown,
  buildTopBuyers,
  calculateKpis,
  formatCurrency,
  formatDays,
  formatNumber,
  formatPercent,
} from "./lib/metrics";
import type { DashboardFilters, DashboardRecord } from "./types/dashboard";

function App() {
  const [records, setRecords] = useState<DashboardRecord[]>([]);
  const [filters, setFilters] = useState<DashboardFilters>({
    startDate: "",
    endDate: "",
    categories: [],
    statuses: [],
    industries: [],
    countries: [],
  });
  const [isLoading, setIsLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState("");

  useEffect(() => {
    async function loadDashboardData() {
      try {
        const response = await fetch("/data/dashboard-data.json");

        if (!response.ok) {
          throw new Error(`Could not load dashboard-data.json (${response.status})`);
        }

        const data = (await response.json()) as unknown;

        if (!Array.isArray(data)) {
          throw new Error("dashboard-data.json must contain an array of records");
        }

        const dashboardRecords = data as DashboardRecord[];
        setRecords(dashboardRecords);
        setFilters(createDefaultFilters(dashboardRecords));
      } catch (error) {
        setErrorMessage(error instanceof Error ? error.message : "Unknown dashboard data error");
      } finally {
        setIsLoading(false);
      }
    }

    void loadDashboardData();
  }, []);

  const filterOptions = useMemo(() => getFilterOptions(records), [records]);
  const filteredRecords = useMemo(() => filterRecords(records, filters), [records, filters]);
  const kpis = useMemo(() => calculateKpis(filteredRecords), [filteredRecords]);
  const monthlyRevenue = useMemo(() => buildMonthlyRevenue(filteredRecords), [filteredRecords]);
  const statusBreakdown = useMemo(() => buildStatusBreakdown(filteredRecords), [filteredRecords]);
  const categoryRevenue = useMemo(() => buildCategoryRevenue(filteredRecords), [filteredRecords]);
  const topBuyers = useMemo(() => buildTopBuyers(filteredRecords), [filteredRecords]);
  const paymentDelayRisk = useMemo(() => buildPaymentDelayRisk(filteredRecords), [filteredRecords]);

  const kpiCards = [
    {
      title: "Total Work Orders",
      value: formatNumber(kpis.totalWorkOrders),
      helper: "Filtered work order count",
      icon: <BriefcaseBusiness className="h-5 w-5" />,
    },
    {
      title: "Gross Work Order Value",
      value: formatCurrency(kpis.grossWorkOrderValue),
      helper: "Total marketplace value",
      icon: <CircleDollarSign className="h-5 w-5" />,
    },
    {
      title: "Platform Revenue",
      value: formatCurrency(kpis.platformRevenue),
      helper: "Fees retained by the platform",
      icon: <ReceiptText className="h-5 w-5" />,
    },
    {
      title: "Provider Payout",
      value: formatCurrency(kpis.providerPayout),
      helper: "Value passed to providers",
      icon: <Banknote className="h-5 w-5" />,
    },
    {
      title: "Take Rate",
      value: formatPercent(kpis.takeRate),
      helper: "Platform revenue divided by gross value",
      icon: <Percent className="h-5 w-5" />,
    },
    {
      title: "Success Rate",
      value: formatPercent(kpis.successRate),
      helper: "Completed or approved work orders",
      icon: <CheckCircle2 className="h-5 w-5" />,
    },
    {
      title: "Cancellation Rate",
      value: formatPercent(kpis.cancellationRate),
      helper: "Cancelled work orders",
      icon: <XCircle className="h-5 w-5" />,
    },
    {
      title: "Average Payment Delay",
      value: formatDays(kpis.averagePaymentDelay),
      helper: "Average days paid after due date",
      icon: <Clock3 className="h-5 w-5" />,
    },
  ];

  if (isLoading) {
    return (
      <main className="min-h-screen bg-slate-50 p-6">
        <div className="mx-auto flex min-h-[70vh] max-w-7xl items-center justify-center">
          <div className="rounded-lg border border-slate-200 bg-white p-6 text-center shadow-sm">
            <p className="text-base font-semibold text-slate-950">Loading FieldOps dashboard</p>
            <p className="mt-2 text-sm text-slate-500">Fetching /data/dashboard-data.json</p>
          </div>
        </div>
      </main>
    );
  }

  if (errorMessage) {
    return (
      <main className="min-h-screen bg-slate-50 p-6">
        <div className="mx-auto flex min-h-[70vh] max-w-3xl items-center justify-center">
          <div className="rounded-lg border border-rose-200 bg-white p-6 shadow-sm">
            <p className="text-base font-semibold text-rose-700">Dashboard data could not be loaded</p>
            <p className="mt-2 text-sm text-slate-600">{errorMessage}</p>
            <p className="mt-4 rounded-md bg-slate-50 p-3 text-sm text-slate-600">
              Expected file: <code className="font-semibold">frontend/public/data/dashboard-data.json</code>
            </p>
          </div>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-slate-50">
      <div className="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
        <header className="mb-6 flex flex-col gap-4 border-b border-slate-200 pb-6 lg:flex-row lg:items-end lg:justify-between">
          <div>
            <p className="text-sm font-semibold uppercase tracking-wide text-sky-700">FieldOps Analytics OS</p>
            <h1 className="mt-2 text-3xl font-semibold tracking-tight text-slate-950 sm:text-4xl">
              Marketplace Operations Dashboard
            </h1>
            <p className="mt-3 max-w-3xl text-base leading-7 text-slate-600">
              A React view of work order revenue, fulfillment health, buyer concentration, and payment risk from the
              exported SQLite dataset.
            </p>
          </div>
          <div className="rounded-lg border border-slate-200 bg-white px-4 py-3 text-sm text-slate-600 shadow-sm">
            <span className="font-semibold text-slate-950">{formatNumber(filteredRecords.length)}</span> of{" "}
            {formatNumber(records.length)} records visible
          </div>
        </header>

        <div className="grid gap-6 lg:grid-cols-[300px_minmax(0,1fr)]">
          <SidebarFilters
            filters={filters}
            options={filterOptions}
            onChange={setFilters}
            onReset={() => setFilters(createDefaultFilters(records))}
          />

          <div className="space-y-6">
            <section className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
              {kpiCards.map((card) => (
                <KpiCard key={card.title} title={card.title} value={card.value} helper={card.helper} icon={card.icon} />
              ))}
            </section>

            <RevenueTrendChart data={monthlyRevenue} />

            <section className="grid gap-6 xl:grid-cols-2">
              <StatusBreakdownChart data={statusBreakdown} />
              <CategoryRevenueChart data={categoryRevenue} />
              <TopBuyersChart data={topBuyers} />
              <PaymentDelayRiskChart data={paymentDelayRisk} />
            </section>

            <DataTable records={filteredRecords} />
            <MetricGlossary />
          </div>
        </div>
      </div>
    </main>
  );
}

export default App;
