import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

import { cockpit, matching } from "../api/dealiq";
import type { CockpitItem, MatchResult } from "../api/types";

export default function Matching() {
  const { t } = useTranslation();
  const [companies, setCompanies] = useState<CockpitItem[]>([]);
  const [companyId, setCompanyId] = useState<string>("");
  const [showAll, setShowAll] = useState(false);
  const [matches, setMatches] = useState<MatchResult[]>([]);

  useEffect(() => {
    void cockpit.companies({ only: "investor_ready", limit: 200 }).then((p) => {
      setCompanies(p.items);
      if (p.items[0]) setCompanyId(p.items[0].company_id);
    });
  }, []);

  useEffect(() => {
    if (!companyId) return;
    void matching.forCompany(companyId, showAll).then(setMatches);
  }, [companyId, showAll]);

  return (
    <>
      <h1>{t("matching.title")}</h1>

      {companies.length === 0 ? (
        <div className="card">
          <p className="muted">{t("matching.none")}</p>
        </div>
      ) : (
        <>
          <div className="card" style={{ display: "flex", gap: 16, alignItems: "center" }}>
            <label>
              {t("matching.pickCompany")} :{" "}
              <select
                value={companyId}
                onChange={(e) => setCompanyId(e.target.value)}
                style={{ padding: 8, borderRadius: 8, border: "1px solid var(--c-border)" }}
              >
                {companies.map((c) => (
                  <option key={c.company_id} value={c.company_id}>
                    {c.name}
                  </option>
                ))}
              </select>
            </label>
            <label style={{ display: "flex", gap: 6, alignItems: "center" }}>
              <input
                type="checkbox"
                checked={showAll}
                onChange={(e) => setShowAll(e.target.checked)}
              />
              {t("matching.showAll")}
            </label>
          </div>

          <div className="card" style={{ background: "var(--c-bg)" }}>
            <p className="muted" style={{ margin: 0 }}>
              ⚠︎ {t("matching.humanValidation")}
            </p>
          </div>

          {matches.length === 0 && <p className="muted">{t("matching.noMatch")}</p>}
          {matches.map((m) => (
            <div className="card" key={m.investor_id}>
              <div style={{ display: "flex", justifyContent: "space-between" }}>
                <div>
                  <strong>{m.investor_name}</strong>{" "}
                  <span className="badge badge--info">{m.investor_type}</span>{" "}
                  {m.passes_hard_filters ? (
                    <span className="badge badge--success">{t("matching.compatible")}</span>
                  ) : (
                    <span className="badge badge--warning">{t("matching.incompatible")}</span>
                  )}
                </div>
                <div className="num" style={{ fontWeight: 700 }}>
                  {t("matching.fit")} : {Math.round(m.fit_score * 100)}%
                </div>
              </div>
              {m.reasons.length > 0 && (
                <p className="muted" style={{ marginBottom: 0 }}>
                  {t("matching.reasons")} : {m.reasons.join(" · ")}
                </p>
              )}
            </div>
          ))}
        </>
      )}
      <p className="disclaimer">{t("disclaimer")}</p>
    </>
  );
}
