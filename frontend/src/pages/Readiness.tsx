import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { Link } from "react-router-dom";

import { readiness } from "../api/dealiq";
import { ApiError } from "../api/client";
import type { ReadinessScore } from "../api/types";
import { useMyCompany } from "../hooks/useMyCompany";

const LADDER = ["trop_precoce", "a_preparer", "plutot_dette_banque", "investor_ready"];

export default function Readiness() {
  const { t } = useTranslation();
  const { company, loading } = useMyCompany();
  const [score, setScore] = useState<ReadinessScore | null>(null);
  const [busy, setBusy] = useState(false);

  const hasType = !!company?.financing_need?.deal_type_primary;

  useEffect(() => {
    if (!company || !hasType) return;
    readiness.get(company.id).then(setScore).catch(() => setScore(null));
  }, [company, hasType]);

  async function compute() {
    if (!company) return;
    setBusy(true);
    try {
      setScore(await readiness.compute(company.id));
    } catch (e) {
      if (!(e instanceof ApiError)) throw e;
    } finally {
      setBusy(false);
    }
  }

  if (loading) return <p className="muted">Chargement…</p>;
  if (!company || !hasType)
    return (
      <>
        <h1>{t("readiness.title")}</h1>
        <div className="card">
          <p className="muted">{t("readiness.needCompanyType")}</p>
          <Link className="btn btn--ghost" to="/deal-type">
            {t("nav.dealType")}
          </Link>
        </div>
      </>
    );

  return (
    <>
      <h1>{t("readiness.title")}</h1>

      {!score ? (
        <div className="card">
          <button className="btn btn--gold" onClick={compute} disabled={busy}>
            {t("readiness.compute")}
          </button>
        </div>
      ) : (
        <>
          <div className="card">
            <p className="muted">{t("readiness.yourFile")} :</p>
            <h2 style={{ marginTop: 0 }}>
              {t(`readiness.categories.${score.category}`)}
            </h2>
            <span className="badge badge--info">{t("readiness.provisional")}</span>

            {/* Échelle de progression (non punitive) — jamais de score chiffré */}
            <div style={{ display: "flex", gap: 6, marginTop: 16 }}>
              {LADDER.map((c) => (
                <div
                  key={c}
                  style={{
                    flex: 1,
                    padding: "8px 6px",
                    borderRadius: 8,
                    textAlign: "center",
                    fontSize: 13,
                    background:
                      c === score.category ? "var(--c-ink)" : "var(--c-bg)",
                    color: c === score.category ? "#fff" : "var(--c-slate-2)",
                    border: "1px solid var(--c-border)",
                  }}
                >
                  {t(`readiness.categories.${c}`)}
                </div>
              ))}
            </div>
          </div>

          {score.gaps.length > 0 && (
            <div className="card">
              <h3 style={{ marginTop: 0 }}>{t("readiness.gaps")}</h3>
              <ul>
                {score.gaps.map((g, i) => (
                  <li key={i}>{g}</li>
                ))}
              </ul>
            </div>
          )}

          <div style={{ display: "flex", gap: 10 }}>
            <Link className="btn" to="/report">
              {t("readiness.seeReport")}
            </Link>
            <Link className="btn btn--ghost" to="/offers">
              {t("readiness.seeOffers")}
            </Link>
          </div>
          <p className="muted" style={{ marginTop: 12 }}>
            {t("readiness.noPunish")}
          </p>
        </>
      )}
      <p className="disclaimer">{t("disclaimer")}</p>
    </>
  );
}
