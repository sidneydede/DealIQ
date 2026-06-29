import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

import { admin } from "../api/dealiq";
import Pager from "../components/Pager";
import type { AuditLogEntry } from "../api/types";

const LIMIT = 50;

export default function Audit() {
  const { t } = useTranslation();
  const [logs, setLogs] = useState<AuditLogEntry[]>([]);
  const [total, setTotal] = useState(0);
  const [offset, setOffset] = useState(0);

  useEffect(() => {
    void admin.audit({ limit: LIMIT, offset }).then((p) => {
      setLogs(p.items);
      setTotal(p.total);
    });
  }, [offset]);

  return (
    <>
      <h1>{t("audit.title")}</h1>
      <div className="card" style={{ padding: 0, overflowX: "auto" }}>
        <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 13 }}>
          <thead>
            <tr style={{ textAlign: "left", color: "var(--c-slate-2)" }}>
              <th style={{ padding: 10 }}>{t("audit.when")}</th>
              <th style={{ padding: 10 }}>{t("audit.actor")}</th>
              <th style={{ padding: 10 }}>{t("audit.action")}</th>
              <th style={{ padding: 10 }}>{t("audit.object")}</th>
            </tr>
          </thead>
          <tbody>
            {logs.length === 0 && (
              <tr>
                <td colSpan={4} style={{ padding: 14 }} className="muted">
                  {t("audit.empty")}
                </td>
              </tr>
            )}
            {logs.map((l) => (
              <tr key={l.id} style={{ borderTop: "1px solid var(--c-border)" }}>
                <td style={{ padding: 10 }} className="muted">
                  {new Date(l.created_at).toLocaleString("fr")}
                </td>
                <td style={{ padding: 10 }}>{l.actor_email ?? l.actor_id ?? "—"}</td>
                <td style={{ padding: 10 }}>
                  <span className="badge badge--info">{l.action}</span>
                </td>
                <td style={{ padding: 10 }} className="muted">
                  {l.object_type ?? ""} {l.object_id ? l.object_id.slice(0, 8) : ""}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <Pager total={total} limit={LIMIT} offset={offset} onChange={setOffset} />
    </>
  );
}
