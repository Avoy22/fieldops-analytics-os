const GLOSSARY_ITEMS = [
  {
    term: "Gross Work Order Value",
    definition: "Total work order value before platform fees and provider payouts.",
  },
  {
    term: "Platform Revenue",
    definition: "Fees retained by FieldOps from completed marketplace activity.",
  },
  {
    term: "Provider Payout",
    definition: "Amount paid out to service providers after platform fees.",
  },
  {
    term: "Take Rate",
    definition: "Platform revenue divided by gross work order value.",
  },
  {
    term: "Success Rate",
    definition: "Share of work orders with completed or approved status.",
  },
  {
    term: "Cancellation Rate",
    definition: "Share of work orders with cancelled status.",
  },
  {
    term: "Average Payment Delay",
    definition: "Average days paid after the due date for records with payment timing data.",
  },
];

function MetricGlossary() {
  return (
    <section className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
      <h2 className="text-base font-semibold text-slate-950">Metric Glossary</h2>
      <div className="mt-4 grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        {GLOSSARY_ITEMS.map((item) => (
          <div key={item.term} className="rounded-md bg-slate-50 p-4">
            <h3 className="text-sm font-semibold text-slate-900">{item.term}</h3>
            <p className="mt-2 text-sm leading-6 text-slate-600">{item.definition}</p>
          </div>
        ))}
      </div>
    </section>
  );
}

export default MetricGlossary;
