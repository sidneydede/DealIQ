import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

import { companies, meta } from "../api/dealiq";
import type { DealTypeHistoryEntry, DealTypeMeta } from "../api/types";
import { useMyCompany } from "../hooks/useMyCompany";

export default function DealTypeSelect() {
  const { t } = useTranslation();
  const { company, loading, reload } = useMyCompany();
  const [types, setTypes] = useState<DealTypeMeta[]>([]);
  const [selected, setSelected] = useState<string | null>(null);
  const [history, setHistory] = useState<DealTypeHistoryEntry[]>([]);
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    void meta.dealTypes().then(setTypes);
  }, []);

  useEffect(() => {
    if (company) {
      setSelected(company.financing_need?.deal_type_primary ?? null);
      void companies.dealTypeHistory(company.id).then(setHistory);
    }
  }, [company]);

  async function confirm() {
    if (!company || !selected) return;
    setBusy(true);
    try {
      await companies.setDealType(company.id, { deal_type_primary: selected });
      await reload();
      setHistory(await companies.dealTypeHistory(company.id));
    } finally {
      setBusy(false);
    }
  }

  if (loading) return <p className="muted">Chargement…</p>;
  if (!company)
    return (
      <>
        <h1>{t("dealType.title")}</h1>
        <div className="card">
          <p className="muted">{t("dealType.needCompany")}</p>
        </div>
      </>
    );

  const current = company.financing_need?.deal_type_primary;

  return (
    <>
      <h1>{t("dealType.question")}</h1>
      <p className="muted">{t("dealType.help")}</p>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fill, minmax(240px, 1fr))",
          gap: 14,
          marginBottom: 18,
        }}
      >
        {types.map((dt) => {
          const isSel = selected === dt.code;
          return (
            <button
              key={dt.code}
              type="button"
              onClick={() => setSelected(dt.code)}
              className="card"
              style={{
                textAlign: "left",
                cursor: "pointer",
                borderColor: isSel ? "var(--c-gold)" : "var(--c-border)",
                borderWidth: isSel ? 2 : 1,
                margin: 0,
              }}
            >
              <strong>{dt.label}</strong>
              {dt.code === current && (
                <span className="badge badge--success" style={{ marginLeft: 8 }}>
                  {t("dealType.current")}
                </span>
              )}
              <p className="muted" style={{ marginBottom: 0 }}>
                {dt.description}
              </p>
            </button>
          );
        })}
      </div>

      <button className="btn btn--gold" disabled={!selected || busy} onClick={confirm}>
        {t("dealType.confirm")}
      </button>

      {history.length > 0 && (
        <div className="card" style={{ marginTop: 24 }}>
          <h3 style={{ marginTop: 0 }}>{t("dealType.history")}</h3>
          {history.map((h) => (
            <p key={h.id} className="muted" style={{ margin: "6px 0" }}>
              <span className="badge badge--info">
                {t(`dealType.bySource.${h.source}`)}
              </span>{" "}
              {h.old_primary ?? "—"} → <strong>{h.new_primary}</strong>
              {h.motif ? ` · ${h.motif}` : ""}{" "}
              <span style={{ opacity: 0.7 }}>{new Date(h.created_at).toLocaleString("fr")}</span>
            </p>
          ))}
        </div>
      )}

      <p className="disclaimer">{t("disclaimer")}</p>
    </>
  );
}
