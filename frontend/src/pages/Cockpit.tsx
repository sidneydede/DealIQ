import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

import { cockpit, meta } from "../api/dealiq";
import Pager from "../components/Pager";
import type { CockpitItem, CountryMeta } from "../api/types";

const FILTERS = ["all", "a_traiter", "investor_ready", "sla"] as const;
const STATUSES = [
  "brouillon",
  "qualifie",
  "en_preparation",
  "investor_ready",
  "en_deal",
  "clos",
  "archive",
];
const LIMIT = 25;

export default function Cockpit() {
  const { t } = useTranslation();
  const [items, setItems] = useState<CockpitItem[]>([]);
  const [total, setTotal] = useState(0);
  const [offset, setOffset] = useState(0);
  const [labels, setLabels] = useState<Record<string, string>>({});
  const [countries, setCountries] = useState<CountryMeta[]>([]);
  const [filter, setFilter] = useState<(typeof FILTERS)[number]>("all");
  const [country, setCountry] = useState("");
  const [statusFilter, setStatusFilter] = useState("");
  const [dealType, setDealType] = useState("");
  const [query, setQuery] = useState(""); // saisie
  const [search, setSearch] = useState(""); // terme appliqué (debounce)

  useEffect(() => {
    void meta.dealTypes().then((d) =>
      setLabels(Object.fromEntries(d.map((x) => [x.code, x.label]))),
    );
    void meta.countries().then(setCountries);
  }, []);

  // Debounce de la recherche (300 ms) ; tout changement de filtre/recherche revient page 1.
  useEffect(() => {
    const id = setTimeout(() => setSearch(query.trim()), 300);
    return () => clearTimeout(id);
  }, [query]);

  useEffect(() => {
    setOffset(0);
  }, [filter, search, country, statusFilter, dealType]);

  const filterParams = {
    only: filter === "all" ? undefined : filter,
    q: search || undefined,
    country: country || undefined,
    status_filter: statusFilter || undefined,
    deal_type: dealType || undefined,
  };

  useEffect(() => {
    void cockpit
      .companies({ ...filterParams, limit: LIMIT, offset })
      .then((p) => {
        setItems(p.items);
        setTotal(p.total);
      });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [filter, search, country, statusFilter, dealType, offset]);

  return (
    <>
      <h1>{t("cockpit.title")}</h1>

      <div style={{ display: "flex", gap: 8, marginBottom: 16, flexWrap: "wrap" }}>
        {FILTERS.map((f) => (
          <button
            key={f}
            className={`btn ${filter === f ? "" : "btn--ghost"}`}
            onClick={() => setFilter(f)}
          >
            {t(`cockpit.filters.${f}`)}
          </button>
        ))}
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder={t("cockpit.searchPlaceholder")}
          aria-label={t("cockpit.searchPlaceholder")}
          style={{
            marginLeft: "auto",
            minWidth: 220,
            padding: "8px 10px",
            borderRadius: 8,
            border: "1px solid var(--c-border)",
          }}
        />
        <button
          className="btn btn--ghost"
          onClick={() => void cockpit.exportCsv(filterParams)}
        >
          {t("cockpit.exportCsv")}
        </button>
      </div>

      <div style={{ display: "flex", gap: 8, marginBottom: 16, flexWrap: "wrap" }}>
        <select
          value={country}
          onChange={(e) => setCountry(e.target.value)}
          aria-label={t("cockpit.cols.company")}
          style={{ padding: 8, borderRadius: 8, border: "1px solid var(--c-border)" }}
        >
          <option value="">{t("cockpit.allCountries")}</option>
          {countries.map((c) => (
            <option key={c.code} value={c.code}>
              {c.label}
            </option>
          ))}
        </select>
        <select
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}
          aria-label={t("cockpit.cols.status")}
          style={{ padding: 8, borderRadius: 8, border: "1px solid var(--c-border)" }}
        >
          <option value="">{t("cockpit.allStatuses")}</option>
          {STATUSES.map((s) => (
            <option key={s} value={s}>
              {s}
            </option>
          ))}
        </select>
        <select
          value={dealType}
          onChange={(e) => setDealType(e.target.value)}
          aria-label={t("cockpit.cols.dealType")}
          style={{ padding: 8, borderRadius: 8, border: "1px solid var(--c-border)" }}
        >
          <option value="">{t("cockpit.allDealTypes")}</option>
          {Object.entries(labels).map(([code, label]) => (
            <option key={code} value={code}>
              {label}
            </option>
          ))}
        </select>
      </div>

      <div className="card" style={{ padding: 0, overflowX: "auto" }}>
        <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 14 }}>
          <thead>
            <tr style={{ textAlign: "left", color: "var(--c-slate-2)" }}>
              <th style={{ padding: 12 }}>{t("cockpit.cols.company")}</th>
              <th style={{ padding: 12 }}>{t("cockpit.cols.dealType")}</th>
              <th style={{ padding: 12 }}>{t("cockpit.cols.readiness")}</th>
              <th style={{ padding: 12 }}>{t("cockpit.cols.status")}</th>
              <th style={{ padding: 12 }}>{t("cockpit.cols.quotes")}</th>
              <th style={{ padding: 12 }}>{t("cockpit.cols.age")}</th>
            </tr>
          </thead>
          <tbody>
            {items.length === 0 && (
              <tr>
                <td colSpan={6} style={{ padding: 16 }} className="muted">
                  {t("cockpit.empty")}
                </td>
              </tr>
            )}
            {items.map((it) => (
              <tr key={it.company_id} style={{ borderTop: "1px solid var(--c-border)" }}>
                <td style={{ padding: 12 }}>
                  <strong>{it.name}</strong>
                  <div className="muted">
                    {it.sector} · {it.country}
                  </div>
                </td>
                <td style={{ padding: 12 }}>
                  {it.deal_type_primary ? labels[it.deal_type_primary] ?? it.deal_type_primary : "—"}
                </td>
                <td style={{ padding: 12 }}>
                  {it.readiness_category ? (
                    <span className="badge badge--info">
                      {t(`readiness.categories.${it.readiness_category}`)}
                    </span>
                  ) : (
                    "—"
                  )}
                </td>
                <td style={{ padding: 12 }}>
                  <span className="badge badge--info">{it.status}</span>
                </td>
                <td style={{ padding: 12 }} className="num">
                  {it.quote_requests}
                </td>
                <td style={{ padding: 12 }} className="num">
                  <span className={it.sla_breach ? "badge badge--warning" : ""}>
                    {it.days_open} {t("cockpit.days")}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <Pager total={total} limit={LIMIT} offset={offset} onChange={setOffset} />
    </>
  );
}
