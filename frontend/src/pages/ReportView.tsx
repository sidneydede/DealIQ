import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

import { report as reportApi } from "../api/dealiq";
import Loading from "../components/Loading";
import type { Report } from "../api/types";
import { useMyCompany } from "../hooks/useMyCompany";

export default function ReportView() {
  const { t } = useTranslation();
  const { company, loading } = useMyCompany();
  const [data, setData] = useState<Report | null>(null);

  const hasType = !!company?.financing_need?.deal_type_primary;

  useEffect(() => {
    if (company && hasType) reportApi.get(company.id).then(setData).catch(() => setData(null));
  }, [company, hasType]);

  if (loading) return <Loading />;
  if (!company || !hasType)
    return (
      <>
        <h1>{t("report.title")}</h1>
        <div className="card">
          <p className="muted">{t("report.empty")}</p>
        </div>
      </>
    );
  if (!data) return <Loading />;

  return (
    <>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <h1>{t("report.title")}</h1>
        <div style={{ display: "flex", gap: 8 }}>
          <button className="btn" onClick={() => void reportApi.downloadPdf(company.id)}>
            {t("report.downloadPdf")}
          </button>
          <button className="btn btn--ghost" onClick={() => window.print()}>
            {t("report.print")}
          </button>
        </div>
      </div>

      <div className="card">
        <h2 style={{ marginTop: 0 }}>{data.company_name}</h2>
        <p>
          {t("report.category")} : <strong>{data.category_label}</strong>
        </p>
        <p>
          {t("report.instrument")} : <strong>{data.recommended_instrument}</strong>
        </p>
      </div>

      <div className="card">
        <h3 style={{ marginTop: 0 }}>{t("report.blockers")}</h3>
        <ul>
          {data.blockers.map((b, i) => (
            <li key={i}>{b}</li>
          ))}
        </ul>
      </div>

      {data.alternative_suggestion && (
        <div className="card" style={{ borderColor: "var(--c-warning)" }}>
          <strong>{t("report.alternative")} : </strong>
          {data.alternative_suggestion}
        </div>
      )}

      <p className="disclaimer">
        {data.disclaimers.map((d, i) => (
          <span key={i}>
            {d}
            <br />
          </span>
        ))}
      </p>
    </>
  );
}
