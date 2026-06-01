import {
  formatCurrency,
  formatDate,
  getBuyerName,
  getServiceCategory,
  getStatus,
  parseDate,
  titleCase,
} from "../lib/metrics";
import type { DashboardRecord } from "../types/dashboard";

type DataTableProps = {
  records: DashboardRecord[];
};

const STATUS_CLASSES: Record<string, string> = {
  approved: "bg-emerald-50 text-emerald-700 ring-emerald-600/20",
  completed: "bg-sky-50 text-sky-700 ring-sky-600/20",
  assigned: "bg-amber-50 text-amber-700 ring-amber-600/20",
  pending: "bg-slate-100 text-slate-700 ring-slate-500/20",
  cancelled: "bg-rose-50 text-rose-700 ring-rose-600/20",
};

function DataTable({ records }: DataTableProps) {
  const rows = [...records]
    .sort((left, right) => {
      const leftTime = parseDate(left.created_at)?.getTime() ?? 0;
      const rightTime = parseDate(right.created_at)?.getTime() ?? 0;
      return rightTime - leftTime;
    })
    .slice(0, 100);

  return (
    <section className="rounded-lg border border-slate-200 bg-white shadow-sm">
      <div className="border-b border-slate-200 p-5">
        <h2 className="text-base font-semibold text-slate-950">Filtered Work Orders</h2>
        <p className="text-sm text-slate-500">Showing {rows.length} rows from the current filtered result.</p>
      </div>
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-slate-200 text-left text-sm">
          <thead className="bg-slate-50 text-xs font-semibold uppercase tracking-wide text-slate-500">
            <tr>
              <th className="px-5 py-3">Work order</th>
              <th className="px-5 py-3">Created</th>
              <th className="px-5 py-3">Buyer</th>
              <th className="px-5 py-3">Category</th>
              <th className="px-5 py-3">Country</th>
              <th className="px-5 py-3">Status</th>
              <th className="px-5 py-3 text-right">Gross value</th>
              <th className="px-5 py-3 text-right">Platform revenue</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 bg-white">
            {rows.map((record) => {
              const status = getStatus(record);

              return (
                <tr key={`${record.work_order_id}-${record.payment_id ?? "no-payment"}`} className="hover:bg-slate-50">
                  <td className="whitespace-nowrap px-5 py-4 font-medium text-slate-950">{record.work_order_id}</td>
                  <td className="whitespace-nowrap px-5 py-4 text-slate-600">{formatDate(record.created_at)}</td>
                  <td className="min-w-44 px-5 py-4 text-slate-700">{getBuyerName(record)}</td>
                  <td className="whitespace-nowrap px-5 py-4 text-slate-600">{getServiceCategory(record)}</td>
                  <td className="whitespace-nowrap px-5 py-4 text-slate-600">{record.country || "N/A"}</td>
                  <td className="whitespace-nowrap px-5 py-4">
                    <span
                      className={`inline-flex rounded-full px-2 py-1 text-xs font-semibold ring-1 ring-inset ${
                        STATUS_CLASSES[status] ?? "bg-slate-100 text-slate-700 ring-slate-500/20"
                      }`}
                    >
                      {titleCase(status)}
                    </span>
                  </td>
                  <td className="whitespace-nowrap px-5 py-4 text-right text-slate-700">
                    {formatCurrency(record.total_amount ?? 0)}
                  </td>
                  <td className="whitespace-nowrap px-5 py-4 text-right font-medium text-slate-950">
                    {formatCurrency(record.platform_fee ?? 0)}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </section>
  );
}

export default DataTable;
