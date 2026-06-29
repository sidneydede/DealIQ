import { useCallback, useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

import { companies as companiesApi, investors as investorsApi, kyc } from "../api/dealiq";
import { ApiError } from "../api/client";
import { useConfirm } from "../components/Confirm";
import { useToast } from "../components/Toast";
import type { KycCheck } from "../api/types";

const CHECK_TYPES = ["kyb", "aml_screening", "manuelle"];

export default function Kyc() {
  const { t } = useTranslation();
  const toast = useToast();
  const confirm = useConfirm();
  const [checks, setChecks] = useState<KycCheck[]>([]);
  const [subjectType, setSubjectType] = useState<"company" | "investor">("company");
  const [subjects, setSubjects] = useState<{ id: string; name: string }[]>([]);
  const [subjectId, setSubjectId] = useState("");
  const [checkType, setCheckType] = useState("kyb");
  const [notes, setNotes] = useState<Record<string, string>>({});

  const reload = useCallback(() => {
    void kyc.list().then(setChecks);
  }, []);
  useEffect(() => reload(), [reload]);

  useEffect(() => {
    const loader =
      subjectType === "company"
        ? companiesApi.list().then((l) => l.map((c) => ({ id: c.id, name: c.name })))
        : investorsApi
            .list({ limit: 200 })
            .then((p) => p.items.map((i) => ({ id: i.id, name: i.name })));
    void loader.then((list) => {
      setSubjects(list);
      setSubjectId(list[0]?.id ?? "");
    });
  }, [subjectType]);

  async function run() {
    if (!subjectId) return;
    try {
      await kyc.run(subjectType, subjectId, checkType);
      reload();
      toast.success(t("kyc.checkRunOk"));
    } catch (err) {
      toast.error(err instanceof ApiError ? err.message : t("security.error"));
    }
  }
  async function update(id: string, status: string) {
    // Rejeter un contrôle est une décision de conformité sensible : on confirme.
    if (
      status === "rejete" &&
      !(await confirm({ message: t("kyc.rejectConfirm"), danger: true }))
    ) {
      return;
    }
    try {
      await kyc.update(id, status, notes[id]);
      reload();
      toast.success(t("kyc.statusOk"));
    } catch (err) {
      toast.error(err instanceof ApiError ? err.message : t("security.error"));
    }
  }

  return (
    <>
      <h1>{t("kyc.title")}</h1>

      <div className="card">
        <h3 style={{ marginTop: 0 }}>{t("kyc.run")}</h3>
        <p className="muted" style={{ fontSize: 12 }}>
          {t("kyc.mockNote")}
        </p>
        <div style={{ display: "flex", gap: 10, flexWrap: "wrap", alignItems: "center" }}>
          <select
            value={subjectType}
            onChange={(e) => setSubjectType(e.target.value as "company" | "investor")}
            style={{ padding: 8, borderRadius: 8, border: "1px solid var(--c-border)" }}
          >
            <option value="company">{t("kyc.company")}</option>
            <option value="investor">{t("kyc.investor")}</option>
          </select>
          <select
            value={subjectId}
            onChange={(e) => setSubjectId(e.target.value)}
            style={{ padding: 8, borderRadius: 8, border: "1px solid var(--c-border)" }}
          >
            {subjects.map((s) => (
              <option key={s.id} value={s.id}>
                {s.name}
              </option>
            ))}
          </select>
          <select
            value={checkType}
            onChange={(e) => setCheckType(e.target.value)}
            style={{ padding: 8, borderRadius: 8, border: "1px solid var(--c-border)" }}
          >
            {CHECK_TYPES.map((ct) => (
              <option key={ct} value={ct}>
                {t(`kyc.types.${ct}`)}
              </option>
            ))}
          </select>
          <button className="btn" onClick={run}>
            {t("kyc.launch")}
          </button>
        </div>
      </div>

      <h3>{t("kyc.checks")}</h3>
      {checks.length === 0 && <p className="muted">{t("kyc.empty")}</p>}

      {checks.map((c) => {
        const isHit = c.status === "hit" || c.status === "rejete";
        return (
          <div
            className="card"
            key={c.id}
            style={{ borderColor: isHit ? "var(--c-risk)" : "var(--c-border)" }}
          >
            <div style={{ display: "flex", justifyContent: "space-between" }}>
              <div>
                <strong>{c.subject_label ?? c.subject_id}</strong>{" "}
                <span className="badge badge--info">{t(`kyc.types.${c.check_type}`)}</span>{" "}
                <span
                  className={`badge badge--${
                    c.status === "valide" ? "success" : isHit ? "warning" : "info"
                  }`}
                >
                  {c.status}
                </span>
              </div>
              <span className="muted" style={{ fontSize: 12 }}>
                {new Date(c.created_at).toLocaleString("fr")}
              </span>
            </div>
            {isHit && c.status === "hit" && <p className="error">{t("kyc.hitAlert")}</p>}
            <p className="muted" style={{ fontSize: 13 }}>
              {JSON.stringify(c.result)}
            </p>
            {(c.status === "en_attente" || c.check_type === "manuelle") &&
              c.status !== "valide" && (
                <div style={{ display: "flex", gap: 8 }}>
                  <input
                    placeholder={t("kyc.notesPlaceholder")}
                    value={notes[c.id] ?? ""}
                    onChange={(e) => setNotes({ ...notes, [c.id]: e.target.value })}
                    style={{
                      flex: 1, padding: 8, borderRadius: 8, border: "1px solid var(--c-border)",
                    }}
                  />
                  <button className="btn btn--ghost" onClick={() => update(c.id, "valide")}>
                    {t("kyc.validate")}
                  </button>
                  <button className="btn btn--ghost" onClick={() => update(c.id, "rejete")}>
                    {t("kyc.reject")}
                  </button>
                </div>
              )}
          </div>
        );
      })}
    </>
  );
}
