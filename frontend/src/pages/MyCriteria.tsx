import { useEffect, useState, type FormEvent } from "react";
import { useTranslation } from "react-i18next";

import { investors } from "../api/dealiq";
import { ApiError } from "../api/client";
import type { Criteria, Investor } from "../api/types";

const EMPTY: Criteria = {
  countries: [], sectors: [], instruments: [], deal_types: [], stages: [], exclusions: [],
  ticket_min: null, ticket_max: null, ticket_currency: "XOF", esg_required: false,
};

const toList = (s: string) => s.split(",").map((x) => x.trim()).filter(Boolean);
const toStr = (l: string[]) => l.join(", ");

export default function MyCriteria() {
  const { t } = useTranslation();
  const [investor, setInvestor] = useState<Investor | null>(null);
  const [loading, setLoading] = useState(true);
  const [c, setC] = useState<Criteria>(EMPTY);
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    investors
      .me()
      .then((inv) => {
        setInvestor(inv);
        if (inv.criteria) setC(inv.criteria);
      })
      .catch((e) => {
        if (!(e instanceof ApiError)) throw e;
      })
      .finally(() => setLoading(false));
  }, []);

  async function onSave(e: FormEvent) {
    e.preventDefault();
    if (!investor) return;
    await investors.setCriteria(investor.id, c);
    setSaved(true);
  }

  if (loading) return <p className="muted">Chargement…</p>;
  if (!investor)
    return (
      <>
        <h1>{t("criteria.title")}</h1>
        <div className="card">
          <p className="muted">{t("criteria.none")}</p>
        </div>
      </>
    );

  const listField = (label: string, key: keyof Criteria) => (
    <div className="field">
      <label>{label}</label>
      <input
        value={toStr((c[key] as string[]) ?? [])}
        onChange={(e) => setC({ ...c, [key]: toList(e.target.value) })}
      />
    </div>
  );

  return (
    <>
      <h1>{t("criteria.title")}</h1>
      <p className="muted">{t("criteria.intro")}</p>
      {saved && (
        <div className="card" style={{ borderColor: "var(--c-success)" }}>
          <span className="badge badge--success">✓</span> {t("criteria.saved")}
        </div>
      )}
      <form className="card" onSubmit={onSave} style={{ maxWidth: 560 }}>
        {listField(t("criteria.countries"), "countries")}
        {listField(t("criteria.sectors"), "sectors")}
        {listField(t("criteria.instruments"), "instruments")}
        {listField(t("criteria.dealTypes"), "deal_types")}
        {listField(t("criteria.stages"), "stages")}
        {listField(t("criteria.exclusions"), "exclusions")}
        <div style={{ display: "flex", gap: 12 }}>
          <div className="field" style={{ flex: 1 }}>
            <label>{t("criteria.ticketMin")}</label>
            <input
              type="number"
              value={c.ticket_min ?? ""}
              onChange={(e) =>
                setC({ ...c, ticket_min: e.target.value ? Number(e.target.value) : null })
              }
            />
          </div>
          <div className="field" style={{ flex: 1 }}>
            <label>{t("criteria.ticketMax")}</label>
            <input
              type="number"
              value={c.ticket_max ?? ""}
              onChange={(e) =>
                setC({ ...c, ticket_max: e.target.value ? Number(e.target.value) : null })
              }
            />
          </div>
        </div>
        <label style={{ display: "flex", gap: 8, alignItems: "center", marginBottom: 14 }}>
          <input
            type="checkbox"
            checked={c.esg_required}
            onChange={(e) => setC({ ...c, esg_required: e.target.checked })}
          />
          {t("criteria.esg")}
        </label>
        <button className="btn" type="submit">
          {t("criteria.save")}
        </button>
      </form>
      <p className="disclaimer">{t("disclaimer")}</p>
    </>
  );
}
