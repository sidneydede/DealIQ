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
