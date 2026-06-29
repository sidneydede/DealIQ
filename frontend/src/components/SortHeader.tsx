import { useState, type CSSProperties, type ReactNode } from "react";

export type Order = "asc" | "desc";
export interface SortState {
  sort: string;
  order: Order;
}

/** État de tri + bascule (asc↔desc, ou nouvelle colonne en asc). */
export function useSort(defaultField = "", defaultOrder: Order = "asc") {
  const [sort, setSort] = useState(defaultField);
  const [order, setOrder] = useState<Order>(defaultOrder);
  const toggle = (field: string) => {
    if (sort === field) {
      setOrder((o) => (o === "asc" ? "desc" : "asc"));
    } else {
      setSort(field);
      setOrder("asc");
    }
  };
  return { sort, order, toggle, state: { sort, order } as SortState };
}

export interface SortOption {
  field: string;
  label: string;
}

/** Sélecteur de tri pour les listes en cartes (pas d'en-têtes) : « Trier par » + sens. */
export function SortSelect({
  options,
  state,
  onSort,
  byLabel,
}: {
  options: SortOption[];
  state: SortState;
  onSort: (field: string) => void;
  byLabel: string;
}) {
  return (
    <div style={{ display: "flex", gap: 6, alignItems: "center" }}>
      <span className="muted" style={{ fontSize: 13 }}>
        {byLabel}
      </span>
      <select
        value={state.sort}
        onChange={(e) => {
          if (e.target.value !== state.sort) onSort(e.target.value);
        }}
        aria-label={byLabel}
        style={{ padding: 8, borderRadius: 8, border: "1px solid var(--c-border)" }}
      >
        {options.map((o) => (
          <option key={o.field} value={o.field}>
            {o.label}
          </option>
        ))}
      </select>
      <button
        type="button"
        className="btn btn--ghost"
        onClick={() => onSort(state.sort)}
        aria-label={state.order === "asc" ? "ascending" : "descending"}
        title={state.order === "asc" ? "↑" : "↓"}
        style={{ padding: "6px 10px" }}
      >
        {state.order === "asc" ? "▲" : "▼"}
      </button>
    </div>
  );
}

/** En-tête de colonne cliquable (tri serveur). */
export function SortHeader({
  field,
  label,
  state,
  onSort,
  style,
}: {
  field: string;
  label: ReactNode;
  state: SortState;
  onSort: (field: string) => void;
  style?: CSSProperties;
}) {
  const active = state.sort === field;
  return (
    <th
      onClick={() => onSort(field)}
      aria-sort={active ? (state.order === "asc" ? "ascending" : "descending") : "none"}
      style={{ cursor: "pointer", userSelect: "none", whiteSpace: "nowrap", ...style }}
    >
      {label}
      {active ? (state.order === "asc" ? " ▲" : " ▼") : ""}
    </th>
  );
}
