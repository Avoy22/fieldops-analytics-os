import { RotateCcw } from "lucide-react";
import type { DashboardFilters, FilterOptions } from "../types/dashboard";

type FilterArrayKey = "categories" | "statuses" | "industries" | "countries";

type SidebarFiltersProps = {
  filters: DashboardFilters;
  options: FilterOptions;
  onChange: (filters: DashboardFilters) => void;
  onReset: () => void;
};

type CheckboxGroupProps = {
  title: string;
  values: string[];
  selectedValues: string[];
  onToggle: (value: string) => void;
  onSelectAll: () => void;
  onClear: () => void;
};

function CheckboxGroup({ title, values, selectedValues, onToggle, onSelectAll, onClear }: CheckboxGroupProps) {
  return (
    <section className="border-t border-slate-200 pt-5">
      <div className="mb-3 flex items-center justify-between gap-3">
        <h3 className="text-sm font-semibold text-slate-900">{title}</h3>
        <div className="flex gap-2 text-xs font-medium">
          <button type="button" className="text-sky-700 hover:text-sky-900" onClick={onSelectAll}>
            All
          </button>
          <button type="button" className="text-slate-500 hover:text-slate-800" onClick={onClear}>
            Any
          </button>
        </div>
      </div>
      <div className="max-h-40 space-y-2 overflow-auto pr-1">
        {values.map((value) => (
          <label key={value} className="flex items-center gap-2 text-sm text-slate-600">
            <input
              type="checkbox"
              className="h-4 w-4 rounded border-slate-300 text-sky-700 focus:ring-sky-700"
              checked={selectedValues.includes(value)}
              onChange={() => onToggle(value)}
            />
            <span>{value}</span>
          </label>
        ))}
      </div>
    </section>
  );
}

function SidebarFilters({ filters, options, onChange, onReset }: SidebarFiltersProps) {
  function updateDate(key: "startDate" | "endDate", value: string) {
    onChange({ ...filters, [key]: value });
  }

  function toggleValue(key: FilterArrayKey, value: string) {
    const currentValues = filters[key];
    const nextValues = currentValues.includes(value)
      ? currentValues.filter((selectedValue) => selectedValue !== value)
      : [...currentValues, value];

    onChange({ ...filters, [key]: nextValues });
  }

  function setValues(key: FilterArrayKey, values: string[]) {
    onChange({ ...filters, [key]: values });
  }

  return (
    <aside className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm lg:sticky lg:top-6">
      <div className="mb-5 flex items-start justify-between gap-3">
        <div>
          <h2 className="text-base font-semibold text-slate-950">Filters</h2>
          <p className="mt-1 text-sm text-slate-500">Slice the static dashboard extract.</p>
        </div>
        <button
          type="button"
          className="inline-flex items-center gap-1 rounded-md border border-slate-200 px-2 py-1 text-xs font-medium text-slate-600 hover:bg-slate-50"
          onClick={onReset}
        >
          <RotateCcw className="h-3.5 w-3.5" />
          Reset
        </button>
      </div>

      <section className="grid gap-3 sm:grid-cols-2 lg:grid-cols-1">
        <label className="text-sm font-medium text-slate-700">
          Start date
          <input
            type="date"
            className="mt-2 w-full rounded-md border border-slate-200 bg-white px-3 py-2 text-sm text-slate-900 outline-none focus:border-sky-600 focus:ring-2 focus:ring-sky-100"
            min={options.minDate}
            max={options.maxDate}
            value={filters.startDate}
            onChange={(event) => updateDate("startDate", event.target.value)}
          />
        </label>
        <label className="text-sm font-medium text-slate-700">
          End date
          <input
            type="date"
            className="mt-2 w-full rounded-md border border-slate-200 bg-white px-3 py-2 text-sm text-slate-900 outline-none focus:border-sky-600 focus:ring-2 focus:ring-sky-100"
            min={options.minDate}
            max={options.maxDate}
            value={filters.endDate}
            onChange={(event) => updateDate("endDate", event.target.value)}
          />
        </label>
      </section>

      <div className="mt-5 space-y-5">
        <CheckboxGroup
          title="Service category"
          values={options.categories}
          selectedValues={filters.categories}
          onToggle={(value) => toggleValue("categories", value)}
          onSelectAll={() => setValues("categories", options.categories)}
          onClear={() => setValues("categories", [])}
        />
        <CheckboxGroup
          title="Work order status"
          values={options.statuses}
          selectedValues={filters.statuses}
          onToggle={(value) => toggleValue("statuses", value)}
          onSelectAll={() => setValues("statuses", options.statuses)}
          onClear={() => setValues("statuses", [])}
        />
        <CheckboxGroup
          title="Buyer industry"
          values={options.industries}
          selectedValues={filters.industries}
          onToggle={(value) => toggleValue("industries", value)}
          onSelectAll={() => setValues("industries", options.industries)}
          onClear={() => setValues("industries", [])}
        />
        <CheckboxGroup
          title="Country"
          values={options.countries}
          selectedValues={filters.countries}
          onToggle={(value) => toggleValue("countries", value)}
          onSelectAll={() => setValues("countries", options.countries)}
          onClear={() => setValues("countries", [])}
        />
      </div>
    </aside>
  );
}

export default SidebarFilters;
