import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

import { mandates } from "../api/dealiq";
import type { ConflictItem } from "../api/types";

export default function Conflicts() {
  const { t } = useTranslation();
  const [list, setList] = useState<ConflictItem[]>([]);

  useEffect(() => {
    void mandates.conflicts().then(setList);
  }, []);

  return (
    <>
      <h1>{t("conflicts.title")}</h1>
      {list.length === 0 && <p className="muted">{t("conflicts.empty")}</p>}

      {list.map((c) => (
        <div
          className="card"
          key={c.company_id}
          style={{ borderColor: c.has_conflict ? "var(--c-risk)" : "var(--c-border)" }}
        >
          <div style={{ display: "flex", justifyContent: "space-between" }}>
            <strong>{c.company_name}</strong>
            {c.has_conflict ? (
              <span className="badge badge--warning">{t("conflicts.conflict")}</span>
            ) : (
              <span className="badge badge--success">{t("conflicts.ok")}</span>
            )}
          </div>
          <p className="muted">
            {t("conflicts.parties")} : {c.represented_parties.join(", ")}
          </p>
          {c.disclosure && <p className="error">{c.disclosure}</p>}
        </div>
      ))}
    </>
  );
}
