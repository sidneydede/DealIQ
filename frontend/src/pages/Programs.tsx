import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

import { companies as companiesApi, programs } from "../api/dealiq";
import { ApiError } from "../api/client";
import { useToast } from "../components/Toast";
import { useAuth } from "../auth/AuthContext";
import type { Company, Program, ProgramMember, ProgramReport } from "../api/types";

export default function Programs() {
  const { t } = useTranslation();
  const toast = useToast();
  const { user } = useAuth();
  const isCabinet = user && ["analyste", "senior", "admin"].includes(user.role);

  const [list, setList] = useState<Program[]>([]);
  const [selected, setSelected] = useState<Program | null>(null);
  const [members, setMembers] = useState<ProgramMember[]>([]);
  const [report, setReport] = useState<ProgramReport | null>(null);
  const [companies, setCompanies] = useState<Company[]>([]);
  const [name, setName] = useState("");
  const [sponsorName, setSponsorName] = useState("");
  const [sponsorEmail, setSponsorEmail] = useState("");
  const [companyId, setCompanyId] = useState("");

  async function reload() {
    setList(await programs.list());
  }
  useEffect(() => {
    void reload();
    if (isCabinet)
      void companiesApi.list().then((l) => {
        setCompanies(l);
        if (l[0]) setCompanyId(l[0].id);
      });
  }, [isCabinet]);

  async function open(p: Program) {
    setSelected(p);
    setReport(await programs.report(p.id));
    if (isCabinet) setMembers(await programs.members(p.id));
  }

  async function create() {
    try {
      await programs.create({
        name,
        sponsor_name: sponsorName,
        sponsor_email: sponsorEmail || undefined,
      });
      setName("");
      setSponsorName("");
      setSponsorEmail("");
      await reload();
      toast.success(t("programs.createdOk"));
    } catch (err) {
      toast.error(err instanceof ApiError ? err.message : t("security.error"));
    }
  }

  async function addCompany() {
    if (!selected || !companyId) return;
    try {
      await programs.addMember(selected.id, companyId);
      setMembers(await programs.members(selected.id));
      setReport(await programs.report(selected.id));
      toast.success(t("programs.addedOk"));
    } catch (err) {
      toast.error(err instanceof ApiError ? err.message : t("security.error"));
    }
  }

  return (
    <>
      <h1>{t("programs.title")}</h1>

      {isCabinet && (
        <div className="card">
          <h3 style={{ marginTop: 0 }}>{t("programs.create")}</h3>
          <div className="field">
            <label>{t("programs.name")}</label>
            <input value={name} onChange={(e) => setName(e.target.value)} />
          </div>
          <div className="field">
            <label>{t("programs.sponsorName")}</label>
            <input value={sponsorName} onChange={(e) => setSponsorName(e.target.value)} />
          </div>
          <div className="field">
            <label>{t("programs.sponsorEmail")}</label>
            <input value={sponsorEmail} onChange={(e) => setSponsorEmail(e.target.value)} />
          </div>
          <button className="btn" onClick={create}>
            {t("programs.add")}
          </button>
        </div>
      )}

      {list.length === 0 && <p className="muted">{t("programs.empty")}</p>}
      {list.map((p) => (
        <div className="card" key={p.id}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <div>
              <strong>{p.name}</strong> <span className="muted">— {p.sponsor_name}</span>{" "}
              <span className="badge badge--info">{p.status}</span>
            </div>
            <button className="btn btn--ghost" onClick={() => open(p)}>
              {selected?.id === p.id ? "—" : "+"}
            </button>
          </div>

          {selected?.id === p.id && (
            <div style={{ marginTop: 12 }}>
              {isCabinet && (
                <>
                  <h4>{t("programs.members")}</h4>
                  {members.map((m) => (
                    <div key={m.id}>{m.company_name}</div>
                  ))}
                  <div style={{ display: "flex", gap: 8, marginTop: 8 }}>
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
                    </select>
                    <button className="btn btn--ghost" onClick={addCompany}>
                      {t("programs.addCompany")}
                    </button>
                  </div>
                </>
              )}

              {report && (
                <div className="card" style={{ background: "var(--c-bg)", marginTop: 12 }}>
                  <h4 style={{ marginTop: 0 }}>{t("programs.report")}</h4>
                  <p className="muted" style={{ fontSize: 12 }}>
                    {t("programs.anonNote")}
                  </p>
                  <p>
                    {t("programs.cohortSize")} :{" "}
                    <strong className="num">{report.cohort_size}</strong> · {t("programs.deals")}{" "}
                    {report.deals_total} · {t("programs.closings")} {report.closings}
                  </p>
                  <p className="muted">
                    {t("programs.impact")} : {t("programs.jobs")} {report.esg.jobs_total ?? 0} ·{" "}
                    {t("programs.femaleRatio")}{" "}
                    {Math.round((report.esg.female_ratio ?? 0) * 100)}%
                  </p>
                  <p className="muted">
                    {t("programs.byStatus")} : {JSON.stringify(report.by_status)}
                  </p>
                  <p className="muted">
                    {t("programs.byReadiness")} : {JSON.stringify(report.by_readiness_category)}
                  </p>
                </div>
              )}
            </div>
          )}
        </div>
      ))}
    </>
  );
}
