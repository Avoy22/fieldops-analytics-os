import type { DashboardFilters, DashboardRecord, FilterOptions } from "../types/dashboard";
import { getServiceCategory, getStatus } from "./metrics";

const EMPTY_FILTERS: DashboardFilters = {
  startDate: "",
  endDate: "",
  categories: [],
  statuses: [],
  industries: [],
  countries: [],
};

function uniqueSorted(values: Array<string | null | undefined>): string[] {
  return Array.from(new Set(values.filter((value): value is string => Boolean(value)))).sort((left, right) =>
    left.localeCompare(right),
  );
}

function toDateInputValue(value: string | null): string {
  if (!value) {
    return "";
  }

  return value.slice(0, 10);
}

export function getFilterOptions(records: DashboardRecord[]): FilterOptions {
  const dates = records
    .map((record) => toDateInputValue(record.created_at))
    .filter((value): value is string => Boolean(value))
    .sort();

  return {
    categories: uniqueSorted(records.map((record) => getServiceCategory(record))),
    statuses: uniqueSorted(records.map((record) => getStatus(record))),
    industries: uniqueSorted(records.map((record) => record.buyer_industry)),
    countries: uniqueSorted(records.map((record) => record.country)),
    minDate: dates[0] ?? "",
    maxDate: dates.at(-1) ?? "",
  };
}

export function createDefaultFilters(records: DashboardRecord[]): DashboardFilters {
  const options = getFilterOptions(records);

  if (!records.length) {
    return EMPTY_FILTERS;
  }

  return {
    startDate: options.minDate,
    endDate: options.maxDate,
    categories: options.categories,
    statuses: options.statuses,
    industries: options.industries,
    countries: options.countries,
  };
}

function includesSelected(selectedValues: string[], value: string | null | undefined): boolean {
  return selectedValues.length === 0 || selectedValues.includes(value || "");
}

export function filterRecords(records: DashboardRecord[], filters: DashboardFilters): DashboardRecord[] {
  return records.filter((record) => {
    const createdDate = toDateInputValue(record.created_at);
    const isAfterStart = !filters.startDate || !createdDate || createdDate >= filters.startDate;
    const isBeforeEnd = !filters.endDate || !createdDate || createdDate <= filters.endDate;

    return (
      isAfterStart &&
      isBeforeEnd &&
      includesSelected(filters.categories, getServiceCategory(record)) &&
      includesSelected(filters.statuses, getStatus(record)) &&
      includesSelected(filters.industries, record.buyer_industry) &&
      includesSelected(filters.countries, record.country)
    );
  });
}
