import { Cell, Legend, Pie, PieChart, ResponsiveContainer, Tooltip } from "recharts";
import { formatNumber, titleCase } from "../lib/metrics";
import type { StatusBreakdownPoint } from "../types/dashboard";

type StatusBreakdownChartProps = {
  data: StatusBreakdownPoint[];
};

const COLORS = ["#0284c7", "#22c55e", "#f59e0b", "#ef4444", "#64748b", "#8b5cf6"];

function StatusBreakdownChart({ data }: StatusBreakdownChartProps) {
  return (
    <section className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
      <div className="mb-4">
        <h2 className="text-base font-semibold text-slate-950">Work Order Status</h2>
        <p className="text-sm text-slate-500">Count of filtered work orders by lifecycle state.</p>
      </div>
      <div className="h-72">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={data}
              dataKey="totalWorkOrders"
              nameKey="status"
              innerRadius={62}
              outerRadius={96}
              paddingAngle={2}
            >
              {data.map((entry, index) => (
                <Cell key={entry.status} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip
              formatter={(value) => formatNumber(Number(value))}
              labelFormatter={(label) => titleCase(String(label))}
            />
            <Legend formatter={(value) => titleCase(String(value))} />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </section>
  );
}

export default StatusBreakdownChart;
