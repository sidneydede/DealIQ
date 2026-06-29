import { useEffect, useState, type FormEvent } from "react";
import { useTranslation } from "react-i18next";

import { companies, meta } from "../api/dealiq";
import Loading from "../components/Loading";
import { useToast } from "../components/Toast";
import type { CountryMeta, DuplicateMatch } from "../api/types";
import { useMyCompany } from "../hooks/useMyCompany";

export default function MyCompany() {
  const { t } = useTranslation();
  const toast = useToast();
  const { company, loading, reload } = useMyCompany();
  const [countries, setCountries] = useState<CountryMeta[]>([]);
  const [name, setName] = useState("");
  const [country, setCountry] = useState("CI");
  const [sector, setSector] = useState("");
  const [rccm, setRccm] = useState("");
  const [warnings, setWarnings] = useState<DuplicateMatch[]>([]);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    void meta.countries().then(setCountries);
  }, []);

  async function onCreate(e: FormEvent) {
    e.preventDefault();
    setBusy(true);
    setError(null);
    try {
      const res = await companies.create({ name, country, sector, rccm: rccm || null });
      setWarnings(res.duplicate_warnings);
      await reload();
      toast.success(t("company.saved"));
    } catch (err) {
      const m = err instanceof Error ? err.message : "Erreur";
      setError(m);
      toast.error(m);
    } finally {
      setBusy(false);
    }
  }

  if (loading) return <Loading />;

  if (company) {
    const fn = company.financing_need;
    return (
      <>
        <h1>{t("company.title")}</h1>
        {warnings.length > 0 && (
          <div className="card" style={{ borderColor: "var(--c-warning)" }}>
            <strong className="badge badge--warning">⚠︎</strong> {t("company.duplicateWarning")}
            <ul>
              {warnings.map((w) => (
                <li key={w.id} className="muted">
                  {w.name} {w.rccm ? `(RCCM ${w.rccm})` : ""} — {w.reason}
                </li>
              ))}
            </ul>
          </div>
        )}
        <div className="card">
          <h2 style={{ marginTop: 0 }}>{company.name}</h2>
          <p>
            <span className="badge badge--info">{company.status}</span>{" "}
            <span className="muted">
              {company.sector} · {company.country} · {company.currency}
            </span>
          </p>
          <p className="muted">
            {t("company.reliability")} :{" "}
            <span className="badge badge--warning">{t("company.declared")}</span>
          </p>
          <p className="muted">
            {t("dealType.current")} :{" "}
            <strong>{fn?.deal_type_primary ?? t("dealType.none")}</strong>
          </p>
        </div>
        <p className="disclaimer">{t("disclaimer")}</p>
      </>
    );
  }

  return (
    <>
      <h1>{t("company.title")}</h1>
      <p className="muted">{t("company.none")}</p>
      <form className="card" onSubmit={onCreate} style={{ maxWidth: 480 }}>
        <div className="field">
          <label htmlFor="cname">{t("company.name")}</label>
          <input id="cname" required value={name} onChange={(e) => setName(e.target.value)} />
        </div>
        <div className="field">
          <label htmlFor="ccountry">{t("company.country")}</label>
          <select
            id="ccountry"
            value={country}
            onChange={(e) => setCountry(e.target.value)}
            style={{ padding: 10, borderRadius: 8, border: "1px solid var(--c-border)" }}
          >
            {countries.map((c) => (
              <option key={c.code} value={c.code}>
                {c.label} ({c.zone})
              </option>
            ))}
          </select>
        </div>
        <div className="field">
          <label htmlFor="csector">{t("company.sector")}</label>
          <input id="csector" required value={sector} onChange={(e) => setSector(e.target.value)} />
        </div>
        <div className="field">
          <label htmlFor="crccm">{t("company.rccm")}</label>
          <input id="crccm" value={rccm} onChange={(e) => setRccm(e.target.value)} />
        </div>
        {error && <p className="error">{error}</p>}
        <button className="btn" type="submit" disabled={busy}>
          {t("company.create")}
        </button>
      </form>
      <p className="disclaimer">{t("disclaimer")}</p>
    </>
  );
}
