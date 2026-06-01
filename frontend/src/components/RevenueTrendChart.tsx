import {
  Area,
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { formatCompactCurrency, formatCurrency } from "../lib/metrics";
import type { MonthlyRevenuePoint } from "../types/dashboard";

type RevenueTrendChartProps = {
  data: MonthlyRevenuePoint[];
};

function RevenueTrendChart({ data }: RevenueTrendChartProps) {
  return (
    <section className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
      <div className="mb-4">
        <h2 className="text-base font-semibold text-slate-950">Monthly Revenue Trend</h2>
        <p className="text-sm text-slate-500">Gross value, platform revenue, and provider payout over time.</p>
      </div>
      <div className="h-80">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data} margin={{ top: 10, right: 20, left: 0, bottom: 0 }}>
            <CartesianGrid stroke="#e2e8f0" strokeDasharray="3 3" />
            <XAxis dataKey="month" tickLine={false} axisLine={false} tick={{ fill: "#64748b", fontSize: 12 }} />
            <YAxis
              tickLine={false}
              axisLine={false}
              tick={{ fill: "#64748b", fontSize: 12 }}
              tickFormatter={(value) => formatCompactCurrency(Number(value))}
            />
            <Tooltip formatter={(value) => formatCurrency(Number(value))} />
            <Legend />
            <Area
              type="monotone"
              dataKey="grossWorkOrderValue"
              name="Gross value"
              stroke="#0284c7"
              fill="#bae6fd"
              fillOpacity={0.35}
            />
            <Line
              type="monotone"
              dataKey="platformRevenue"
              name="Platform revenue"
              stroke="#0f172a"
              strokeWidth={3}
              dot={false}
            />
            <Line
              type="monotone"
              dataKey="providerPayout"
              name="Provider payout"
              stroke="#22c55e"
              strokeWidth={2}
              dot={false}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </section>
  );
}

export default RevenueTrendChart;
