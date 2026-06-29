import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

import { ApiError } from "../api/client";
import { meta, teasers } from "../api/dealiq";
import type { TeaserPublic } from "../api/types";

const INSTRUMENTS = ["", "equity", "dette", "quasi_equity", "hybride"];

export default function Opportunities() {
  const { t } = useTranslation();
  const [list, setList] = useState<TeaserPublic[]>([]);
  const [instrument, setInstrument] = useState("");
  const [dealType, setDealType] = useState("");
  const [dealTypeLabels, setDealTypeLabels] = useState<Record<string, string>>({});
  const [sentId, setSentId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    void meta.dealTypes().then((d) =>
      setDealTypeLabels(Object.fromEntries(d.map((x) => [x.code, x.label]))),
    );
  }, []);

  useEffect(() => {
    const params: { instrument?: string; deal_type?: string } = {};
    if (instrument) params.instrument = instrument;
    if (dealType) params.deal_type = dealType;
    teasers.catalog(params).then(setList);
  }, [instrument, dealType]);

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

      <div
        style={{ display: "flex", gap: 12, alignItems: "center", flexWrap: "wrap" }}
        className="card"
      >
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
        <label>
          {t("opportunities.filterDealType")} :{" "}
          <select
            value={dealType}
            onChange={(e) => setDealType(e.target.value)}
            style={{ padding: 8, borderRadius: 8, border: "1px solid var(--c-border)" }}
          >
            <option value="">{t("opportunities.all")}</option>
            {Object.entries(dealTypeLabels).map(([code, label]) => (
              <option key={code} value={code}>
                {label}
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
