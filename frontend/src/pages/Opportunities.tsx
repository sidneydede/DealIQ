import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

import { ApiError } from "../api/client";
import { teasers } from "../api/dealiq";
import type { TeaserPublic } from "../api/types";

const INSTRUMENTS = ["", "equity", "dette", "quasi_equity", "hybride"];

export default function Opportunities() {
  const { t } = useTranslation();
  const [list, setList] = useState<TeaserPublic[]>([]);
  const [instrument, setInstrument] = useState("");
  const [sentId, setSentId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    teasers.catalog(instrument ? { instrument } : {}).then(setList);
  }, [instrument]);

  async function express(id: string) {
    setError(null);
    try {
      await teasers.interest(id);
      setSentId(id);
    } catch (e) {
      setError(e instanceof ApiError ? e.message : "Erreur");
    }
  }

  return (
    <>
      <h1>{t("opportunities.title")}</h1>
      <p className="muted">{t("opportunities.intro")}</p>

      <div className="card" style={{ display: "flex", gap: 12, alignItems: "center" }}>
        <label>
          {t("opportunities.filterInstrument")} :{" "}
          <select
            value={instrument}
            onChange={(e) => setInstrument(e.target.value)}
            style={{ padding: 8, borderRadius: 8, border: "1px solid var(--c-border)" }}
          >
            {INSTRUMENTS.map((i) => (
              <option key={i} value={i}>
                {i || t("opportunities.all")}
              </option>
            ))}
          </select>
        </label>
      </div>

      {error && <p className="error">{error}</p>}
      {list.length === 0 && <p className="muted">{t("opportunities.empty")}</p>}

      {list.map((o) => (
        <div className="card" key={o.id}>
          <h3 style={{ marginTop: 0 }}>{o.title}</h3>
          <p>
            <span className="badge badge--info">{o.instrument}</span>{" "}
            <span className="badge badge--info">{o.zone}</span>{" "}
            <span className="muted">{o.sector}</span>
          </p>
          <p className="muted">
            {t("opportunities.revenue")} : {o.revenue_band} ·{" "}
            {t("opportunities.amount")} : {o.amount_band}
          </p>
          {o.strengths.length > 0 && (
            <p>
              <strong>{t("opportunities.strengths")} :</strong> {o.strengths.join(" · ")}
            </p>
          )}
          {sentId === o.id ? (
            <div className="card" style={{ borderColor: "var(--c-success)", margin: 0 }}>
              <span className="badge badge--success">✓</span> {t("opportunities.interestSent")}
            </div>
          ) : (
            <button className="btn btn--gold" onClick={() => express(o.id)}>
              {t("opportunities.interest")}
            </button>
          )}
          <p className="disclaimer" style={{ marginTop: 10 }}>
            {t("opportunities.ndaNote")}
          </p>
        </div>
      ))}
      <p className="disclaimer">{t("disclaimer")}</p>
    </>
  );
}
