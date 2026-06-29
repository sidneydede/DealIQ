import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

import { reporting } from "../api/dealiq";
import type { DashboardData } from "../api/types";

function Kpi({ label, value, hint }: { label: string; value: string; hint?: string }) {
  return (
    <div className="card" style={{ flex: 1, minWidth: 160 }}>
      <div className="muted">{label}</div>
      <div className="num" style={{ fontSize: 28, fontWeight: 700, color: "var(--c-ink)" }}>
        {value}
      </div>
      {hint && <div className="muted" style={{ fontSize: 12 }}>{hint}</div>}
    </div>
  );
}

function Breakdown({ title, data }: { title: string; data: Record<string, number> }) {
  return (
    <div className="card" style={{ flex: 1, minWidth: 220 }}>
      <h3 style={{ marginTop: 0 }}>{title}</h3>
      {Object.keys(data).length === 0 && <p className="muted">—</p>}
      {Object.entries(data).map(([k, v]) => (
        <div key={k} style={{ display: "flex", justifyContent: "space-between" }}>
          <span className="muted">{k}</span>
          <span className="num">{v}</span>
        </div>
      ))}
    </div>
  );
}

export default function Reporting() {
  const { t } = useTranslation();
  const [d, setD] = useState<DashboardData | null>(null);

  useEffect(() => {
    void reporting.dashboard().then(setD);
  }, []);

  if (!d) return <p className="muted">Chargement…</p>;
  const pct = (x: number) => `${Math.round(x * 100)}%`;

  return (
    <>
      <h1>{t("reporting.title")}</h1>

      <div style={{ display: "flex", gap: 14, flexWrap: "wrap" }}>
        <Kpi label={t("reporting.kpi.users")} value={String(d.users_total)} />
        <Kpi label={t("reporting.kpi.companies")} value={String(d.companies_total)} />
        <Kpi
          label={t("reporting.kpi.completion")}
          value={pct(d.completion_rate)}
          hint={`${t("reporting.target")} ≥ 40%`}
        />
        <Kpi
          label={t("reporting.kpi.conversion")}
          value={pct(d.conversion_rate)}
          hint={`${t("reporting.target")} ≥ 15%`}
        />
        <Kpi label={t("reporting.kpi.quotes")} value={String(d.quote_requests_total)} />
      </div>

      <h2 style={{ marginTop: 24 }}>{t("reporting.investorFunnel")}</h2>
      <div style={{ display: "flex", gap: 14, flexWrap: "wrap" }}>
        <Kpi label={t("reporting.kpi.investors")} value={String(d.investors_total)} />
        <Kpi label={t("reporting.kpi.teasersPublished")} value={String(d.teasers_published)} />
        <Kpi label={t("reporting.kpi.interactions")} value={String(d.interactions_total)} />
        <Kpi label={t("reporting.kpi.deals")} value={String(d.deals_total)} />
        <Kpi label={t("reporting.kpi.closings")} value={String(d.deals_closing)} />
        <Kpi label={t("reporting.kpi.interestToDeal")} value={pct(d.interest_to_deal_rate)} />
      </div>

      <div style={{ display: "flex", gap: 14, flexWrap: "wrap", marginTop: 14 }}>
        <Breakdown title={t("reporting.byDealType")} data={d.by_deal_type} />
        <Breakdown title={t("reporting.byCategory")} data={d.by_readiness_category} />
        <Breakdown title={t("reporting.byStatus")} data={d.companies_by_status} />
        <Breakdown title={t("reporting.byInteractionStatus")} data={d.interactions_by_status} />
        <Breakdown title={t("reporting.byDealStage")} data={d.deals_by_stage} />
      </div>
    </>
  );
}
