import type { ReactNode } from "react";

type KpiCardProps = {
  title: string;
  value: string;
  helper: string;
  icon: ReactNode;
};

function KpiCard({ title, value, helper, icon }: KpiCardProps) {
  return (
    <article className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="text-sm font-medium text-slate-500">{title}</p>
          <p className="mt-3 text-2xl font-semibold tracking-tight text-slate-950">{value}</p>
        </div>
        <div className="rounded-lg bg-slate-100 p-2 text-slate-700">{icon}</div>
      </div>
      <p className="mt-3 text-sm text-slate-500">{helper}</p>
    </article>
  );
}

export default KpiCard;
