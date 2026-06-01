import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { formatCompactCurrency, formatCurrency } from "../lib/metrics";
import type { BuyerRevenuePoint } from "../types/dashboard";

type TopBuyersChartProps = {
  data: BuyerRevenuePoint[];
};

function TopBuyersChart({ data }: TopBuyersChartProps) {
  const sortedData = [...data].sort((left, right) => left.platformRevenue - right.platformRevenue);

  return (
    <section className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
      <div className="mb-4">
        <h2 className="text-base font-semibold text-slate-950">Top Buyers By Platform Revenue</h2>
        <p className="text-sm text-slate-500">Largest buyer accounts in the filtered slice.</p>
      </div>
      <div className="h-80">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={sortedData} layout="vertical" margin={{ top: 10, right: 20, left: 70, bottom: 0 }}>
            <CartesianGrid stroke="#e2e8f0" strokeDasharray="3 3" horizontal={false} />
            <XAxis
              type="number"
              tickLine={false}
              axisLine={false}
              tick={{ fill: "#64748b", fontSize: 12 }}
              tickFormatter={(value) => formatCompactCurrency(Number(value))}
            />
            <YAxis
              type="category"
              dataKey="companyName"
              tickLine={false}
              axisLine={false}
              tick={{ fill: "#64748b", fontSize: 12 }}
              width={130}
            />
            <Tooltip
              formatter={(value) => formatCurrency(Number(value))}
              labelFormatter={(label) => `Buyer: ${label}`}
            />
            <Bar dataKey="platformRevenue" name="Platform revenue" fill="#0f172a" radius={[0, 6, 6, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </section>
  );
}

export default TopBuyersChart;
