import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

import { ApiError } from "../api/client";
import { companies as companiesApi, esg } from "../api/dealiq";
import { useToast } from "../components/Toast";
import type { Company, EsgProfile } from "../api/types";

const NUM_FIELDS = ["jobs_total", "jobs_female", "jobs_youth"] as const;
const BOOL_FIELDS = [
  "women_in_leadership",
  "environmental_policy",
  "climate_risk_assessed",
  "governance_formalized",
  "board_independent",
] as const;

type Form = Record<string, number | boolean | string | null>;

export default function Esg() {
  const { t } = useTranslation();
  const toast = useToast();
  const [companies, setCompanies] = useState<Company[]>([]);
  const [companyId, setCompanyId] = useState("");
  const [profile, setProfile] = useState<EsgProfile | null>(null);
  const [form, setForm] = useState<Form>({});
  const [exported, setExported] = useState<Record<string, unknown> | null>(null);

  useEffect(() => {
    void companiesApi.list().then((l) => {
      setCompanies(l);
      if (l[0]) setCompanyId(l[0].id);
    });
  }, []);

  async function load() {
    setExported(null);
    try {
      const p = await esg.get(companyId);
      setProfile(p);
      setForm({ ...p, evidence_note: p.evidence_note ?? "" });
    } catch (e) {
      if (e instanceof ApiError && e.status === 404) {
        setProfile(null);
        setForm({});
      } else throw e;
    }
  }

  async function save() {
    const body: Record<string, unknown> = { evidence_note: form.evidence_note ?? null };
    for (const f of NUM_FIELDS) body[f] = form[f] === "" || form[f] == null ? null : Number(form[f]);
    for (const f of BOOL_FIELDS) body[f] = form[f] === undefined ? null : form[f];
    try {
      const p = await esg.upsert(companyId, body);
      setProfile(p);
      setForm({ ...p, evidence_note: p.evidence_note ?? "" });
      toast.success(t("esg.savedOk"));
    } catch (err) {
      toast.error(err instanceof ApiError ? err.message : t("security.error"));
    }
  }

  async function toggleRequired() {
    if (!profile) return;
    setProfile(await esg.setRequired(companyId, !profile.esg_required));
  }

  async function doExport() {
    setExported(await esg.export(companyId));
  }

  function boolSelect(field: string) {
    const v = form[field];
    const val = v === true ? "true" : v === false ? "false" : "";
    return (
      <select
        value={val}
        onChange={(e) =>
          setForm({ ...form, [field]: e.target.value === "" ? null : e.target.value === "true" })
        }
        style={{ padding: 6, borderRadius: 8, border: "1px solid var(--c-border)" }}
      >
        <option value="">{t("esg.unknown")}</option>
        <option value="true">{t("esg.yes")}</option>
        <option value="false">{t("esg.no")}</option>
      </select>
    );
  }

  return (
    <>
      <h1>{t("esg.title")}</h1>

      <div className="card">
        <select
          value={companyId}
          onChange={(e) => setCompanyId(e.target.value)}
          style={{ padding: 8, borderRadius: 8, border: "1px solid var(--c-border)" }}
        >
          {companies.map((c) => (
            <option key={c.id} value={c.id}>
              {c.name}
            </option>
          ))}
        </select>{" "}
        <button className="btn" onClick={load}>
          {t("esg.load")}
        </button>
      </div>

      <div className="card" style={{ maxWidth: 560 }}>
        {NUM_FIELDS.map((f) => (
          <div className="field" key={f}>
            <label>{t(`esg.fields.${f}`)}</label>
            <input
              type="number"
              value={(form[f] as number | string) ?? ""}
              onChange={(e) => setForm({ ...form, [f]: e.target.value })}
            />
          </div>
        ))}
        {BOOL_FIELDS.map((f) => (
          <div className="field" key={f} style={{ flexDirection: "row", gap: 12, alignItems: "center" }}>
            <label style={{ flex: 1 }}>{t(`esg.fields.${f}`)}</label>
            {boolSelect(f)}
          </div>
        ))}
        <div className="field">
          <label>{t("esg.evidence")}</label>
          <input
            value={(form.evidence_note as string) ?? ""}
            onChange={(e) => setForm({ ...form, evidence_note: e.target.value })}
          />
        </div>
        <button className="btn" onClick={save}>
          {t("esg.save")}
        </button>
      </div>

      {profile && (
        <div className="card">
          <p>
            {t("esg.completeness")} :{" "}
            <strong className="num">{Math.round(profile.completeness * 100)}%</strong>{" "}
            {profile.incomplete_for_dfi && (
              <span className="badge badge--warning">{t("esg.incomplete")}</span>
            )}
          </p>
          <label style={{ display: "flex", gap: 8, alignItems: "center" }}>
            <input
              type="checkbox"
              checked={profile.esg_required}
              onChange={toggleRequired}
            />
            {t("esg.required")}
          </label>
          <button className="btn btn--ghost" onClick={doExport} style={{ marginTop: 10 }}>
            {t("esg.export")}
          </button>
          {exported && (
            <pre
              className="muted"
              style={{ whiteSpace: "pre-wrap", fontSize: 12, marginTop: 10 }}
            >
              {JSON.stringify(exported, null, 2)}
            </pre>
          )}
        </div>
      )}
    </>
  );
}
