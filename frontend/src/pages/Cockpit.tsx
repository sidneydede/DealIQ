import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

import { cockpit, meta } from "../api/dealiq";
import type { CockpitItem } from "../api/types";

const FILTERS = ["all", "a_traiter", "investor_ready", "sla"] as const;

export default function Cockpit() {
  const { t } = useTranslation();
  const [items, setItems] = useState<CockpitItem[]>([]);
  const [labels, setLabels] = useState<Record<string, string>>({});
  const [filter, setFilter] = useState<(typeof FILTERS)[number]>("all");

  useEffect(() => {
    void meta.dealTypes().then((d) =>
      setLabels(Object.fromEntries(d.map((x) => [x.code, x.label]))),
    );
  }, []);

  useEffect(() => {
    const params = filter === "all" ? {} : { only: filter };
    void cockpit.companies(params).then(setItems);
  }, [filter]);

  return (
    <>
      <h1>{t("cockpit.title")}</h1>

      <div style={{ display: "flex", gap: 8, marginBottom: 16 }}>
        {FILTERS.map((f) => (
          <button
            key={f}
            className={`btn ${filter === f ? "" : "btn--ghost"}`}
            onClick={() => setFilter(f)}
          >
            {t(`cockpit.filters.${f}`)}
          </button>
        ))}
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
    </>
  );
}
