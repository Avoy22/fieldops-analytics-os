import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { formatCompactCurrency, formatCurrency } from "../lib/metrics";
import type { CategoryRevenuePoint } from "../types/dashboard";

type CategoryRevenueChartProps = {
  data: CategoryRevenuePoint[];
};

function CategoryRevenueChart({ data }: CategoryRevenueChartProps) {
  return (
    <section className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
      <div className="mb-4">
        <h2 className="text-base font-semibold text-slate-950">Platform Revenue By Category</h2>
        <p className="text-sm text-slate-500">Which services contribute the most fee revenue.</p>
      </div>
      <div className="h-72">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data} margin={{ top: 10, right: 20, left: 0, bottom: 10 }}>
            <CartesianGrid stroke="#e2e8f0" strokeDasharray="3 3" vertical={false} />
            <XAxis
              dataKey="category"
              tickLine={false}
              axisLine={false}
              tick={{ fill: "#64748b", fontSize: 12 }}
              interval={0}
              angle={-20}
              textAnchor="end"
              height={60}
            />
            <YAxis
              tickLine={false}
              axisLine={false}
              tick={{ fill: "#64748b", fontSize: 12 }}
              tickFormatter={(value) => formatCompactCurrency(Number(value))}
            />
            <Tooltip formatter={(value) => formatCurrency(Number(value))} />
            <Bar dataKey="platformRevenue" name="Platform revenue" fill="#0284c7" radius={[6, 6, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </section>
  );
}

export default CategoryRevenueChart;
