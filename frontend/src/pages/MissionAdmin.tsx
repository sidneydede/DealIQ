import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

import { ApiError } from "../api/client";
import { companies as companiesApi, missions } from "../api/dealiq";
import { useConfirm } from "../components/Confirm";
import { useToast } from "../components/Toast";
import type { Company, MissionDetail } from "../api/types";

const KINDS = ["business_plan", "modele_financier", "valorisation", "teaser", "data_room_init"];

export default function MissionAdmin() {
  const { t } = useTranslation();
  const toast = useToast();
  const confirm = useConfirm();
  const [companies, setCompanies] = useState<Company[]>([]);
  const [companyId, setCompanyId] = useState("");
  const [mission, setMission] = useState<MissionDetail | null>(null);
  const [kind, setKind] = useState(KINDS[0]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    void companiesApi.list().then((l) => {
      setCompanies(l);
      if (l[0]) setCompanyId(l[0].id);
    });
  }, []);

  async function start() {
    setError(null);
    setMission(await missions.create(companyId));
  }
  async function refresh() {
    if (mission) setMission(await missions.get(mission.company_id));
  }
  async function toggle(taskId: string, done: boolean) {
    await missions.toggleTask(taskId, done);
    await refresh();
  }
  async function addDeliverable() {
    if (mission) await missions.addDeliverable(mission.id, kind);
    await refresh();
  }
  async function validate(deliverableId: string) {
    await missions.updateDeliverable(deliverableId, "valide");
    await refresh();
  }
  async function review() {
    if (!mission) return;
    try {
      await missions.review(mission.id);
      await refresh();
      toast.success(t("mission.reviewedOk"));
    } catch (e) {
      setError(e instanceof ApiError ? e.message : "Erreur");
      toast.error(e instanceof ApiError ? e.message : t("security.error"));
    }
  }
  async function promote() {
    if (!mission) return;
    if (!(await confirm({ message: t("mission.promoteConfirm") }))) return;
    setError(null);
    try {
      await missions.promote(mission.id);
      await refresh();
      toast.success(t("mission.promotedOk"));
    } catch (e) {
      setError(e instanceof ApiError ? e.message : "Erreur");
      toast.error(e instanceof ApiError ? e.message : t("security.error"));
    }
  }

  return (
    <>
      <h1>{t("mission.title")}</h1>

      <div className="card">
        <select
          value={companyId}
          onChange={(e) => setCompanyId(e.target.value)}
          style={{ padding: 8, borderRadius: 8, border: "1px solid var(--c-border)" }}
        >
          {companies.map((c) => (
            <option key={c.id} value={c.id}>
              {c.name} ({c.status})
            </option>
          ))}
        </select>{" "}
        <button className="btn" onClick={start}>
          {t("mission.start")}
        </button>
      </div>

      {error && <p className="error">{error}</p>}

      {mission && (
        <>
          <div className="card">
            <h3 style={{ marginTop: 0 }}>{t("mission.checklist")}</h3>
            {mission.tasks.map((task) => (
              <label key={task.id} style={{ display: "flex", gap: 8, alignItems: "center" }}>
                <input
                  type="checkbox"
                  checked={task.done}
                  onChange={(e) => toggle(task.id, e.target.checked)}
                />
                <span style={{ textDecoration: task.done ? "line-through" : "none" }}>
                  {task.label}
                </span>
              </label>
            ))}
          </div>

          <div className="card">
            <h3 style={{ marginTop: 0 }}>{t("mission.deliverables")}</h3>
            {mission.deliverables.map((d) => (
              <div key={d.id} style={{ display: "flex", justifyContent: "space-between" }}>
                <span>
                  {t(`mission.kinds.${d.kind}`)} v{d.version}{" "}
                  <span className="badge badge--info">{d.status}</span>
                </span>
                {d.status !== "valide" && (
                  <button className="btn btn--ghost" onClick={() => validate(d.id)}>
                    ✓
                  </button>
                )}
              </div>
            ))}
            <div style={{ marginTop: 8 }}>
              <select value={kind} onChange={(e) => setKind(e.target.value)}>
                {KINDS.map((k) => (
                  <option key={k} value={k}>
                    {t(`mission.kinds.${k}`)}
                  </option>
                ))}
              </select>{" "}
              <button className="btn btn--ghost" onClick={addDeliverable}>
                {t("mission.addDeliverable")}
              </button>
            </div>
          </div>

          <div className="card">
            <h3 style={{ marginTop: 0 }}>{t("mission.reviews")}</h3>
            {mission.reviews.map((r) => (
              <p key={r.id} className="muted">
                {t("mission.reviewedBy")} : {r.role}
              </p>
            ))}
            <button className="btn btn--ghost" onClick={review}>
              {t("mission.reviewAnalyste")} / {t("mission.reviewSenior")}
            </button>
          </div>

          <div className="card">
            {mission.blockers.length > 0 && (
              <p className="muted">
                {t("mission.blockers")} : {mission.blockers.join(" · ")}
              </p>
            )}
            <button className="btn btn--gold" disabled={!mission.can_promote} onClick={promote}>
              {t("mission.promote")}
            </button>
          </div>
        </>
      )}
    </>
  );
}
