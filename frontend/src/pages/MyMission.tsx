import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

import { ApiError } from "../api/client";
import { missions } from "../api/dealiq";
import type { MissionDetail } from "../api/types";
import { useMyCompany } from "../hooks/useMyCompany";

export default function MyMission() {
  const { t } = useTranslation();
  const { company, loading } = useMyCompany();
  const [mission, setMission] = useState<MissionDetail | null>(null);
  const [started, setStarted] = useState<boolean | null>(null);

  useEffect(() => {
    if (!company) return;
    missions
      .get(company.id)
      .then((m) => {
        setMission(m);
        setStarted(true);
      })
      .catch((e) => {
        if (e instanceof ApiError && e.status === 404) setStarted(false);
        else throw e;
      });
  }, [company]);

  if (loading) return <p className="muted">Chargement…</p>;

  if (started === false || !mission)
    return (
      <>
        <h1>{t("mission.myTitle")}</h1>
        <div className="card">
          <p className="muted">{t("mission.notStarted")}</p>
        </div>
      </>
    );

  const done = mission.tasks.filter((x) => x.done).length;

  return (
    <>
      <h1>{t("mission.myTitle")}</h1>
      <div className="card">
        <p>
          {t("mission.progress")} :{" "}
          <strong className="num">
            {done}/{mission.tasks.length}
          </strong>{" "}
          <span className="badge badge--info">{mission.status}</span>
        </p>
        {mission.tasks.map((task) => (
          <div key={task.id}>
            {task.done ? "✅" : "⬜"} {task.label}
          </div>
        ))}
      </div>

      {mission.deliverables.length > 0 && (
        <div className="card">
          <h3 style={{ marginTop: 0 }}>{t("mission.deliverables")}</h3>
          {mission.deliverables.map((d) => (
            <div key={d.id}>
              {t(`mission.kinds.${d.kind}`)} v{d.version} —{" "}
              <span className="badge badge--info">{d.status}</span>
            </div>
          ))}
        </div>
      )}
      <p className="disclaimer">{t("disclaimer")}</p>
    </>
  );
}
