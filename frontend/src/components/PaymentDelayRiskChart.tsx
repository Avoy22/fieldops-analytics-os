import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { formatDays, formatPercent } from "../lib/metrics";
import type { PaymentDelayRiskPoint } from "../types/dashboard";

type PaymentDelayRiskChartProps = {
  data: PaymentDelayRiskPoint[];
};

function PaymentDelayRiskChart({ data }: PaymentDelayRiskChartProps) {
  const sortedData = [...data].sort((left, right) => left.averagePaymentDelay - right.averagePaymentDelay);

  return (
    <section className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
      <div className="mb-4">
        <h2 className="text-base font-semibold text-slate-950">Payment Delay Risk By Buyer</h2>
        <p className="text-sm text-slate-500">Buyers with the highest average days paid after due date.</p>
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
              tickFormatter={(value) => `${Number(value).toFixed(0)}d`}
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
              formatter={(value, name) =>
                name === "Late payment rate" ? formatPercent(Number(value)) : formatDays(Number(value))
              }
            />
            <Bar dataKey="averagePaymentDelay" name="Average delay" fill="#f59e0b" radius={[0, 6, 6, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </section>
  );
}

export default PaymentDelayRiskChart;
