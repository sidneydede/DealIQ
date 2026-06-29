import { useCallback, useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

import { ApiError } from "../api/client";
import {
  cockpit,
  dataroom,
  documents as docsApi,
  investors as investorsApi,
} from "../api/dealiq";
import type {
  CockpitItem,
  DataRoom,
  DataRoomAccess,
  DataRoomDocument,
  DataRoomLog,
  DocumentOut,
  Investor,
} from "../api/types";

export default function DataRoomAdmin() {
  const { t } = useTranslation();
  const [companies, setCompanies] = useState<CockpitItem[]>([]);
  const [companyId, setCompanyId] = useState("");
  const [room, setRoom] = useState<DataRoom | null>(null);
  const [companyDocs, setCompanyDocs] = useState<DocumentOut[]>([]);
  const [roomDocs, setRoomDocs] = useState<DataRoomDocument[]>([]);
  const [investors, setInvestors] = useState<Investor[]>([]);
  const [investorId, setInvestorId] = useState("");
  const [access, setAccess] = useState<DataRoomAccess[]>([]);
  const [logs, setLogs] = useState<DataRoomLog[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    void cockpit.companies({ only: "investor_ready", limit: 200 }).then((p) => {
      setCompanies(p.items);
      if (p.items[0]) setCompanyId(p.items[0].company_id);
    });
    void investorsApi.list({ limit: 200 }).then((p) => setInvestors(p.items));
  }, []);

  const refreshRoom = useCallback(async (r: DataRoom) => {
    setRoomDocs(await dataroom.documents(r.id));
    setAccess(await dataroom.access(r.id));
    setLogs(await dataroom.logs(r.id));
  }, []);

  async function openRoom() {
    setError(null);
    const r = await dataroom.open(companyId);
    setRoom(r);
    setCompanyDocs(await docsApi.list(companyId));
    await refreshRoom(r);
  }

  async function publish(docId: string) {
    if (!room) return;
    await dataroom.addDocument(room.id, docId);
    await refreshRoom(room);
  }

  async function grant() {
    if (!room || !investorId) return;
    setError(null);
    try {
      await dataroom.grant(room.id, investorId);
      await refreshRoom(room);
    } catch (e) {
      setError(e instanceof ApiError ? e.message : "Erreur");
    }
  }

  async function revoke(accessId: string) {
    if (!room) return;
    await dataroom.revoke(accessId);
    await refreshRoom(room);
  }

  const inRoom = new Set(roomDocs.map((d) => d.document_id));

  return (
    <>
      <h1>{t("dataroom.title")}</h1>

      {companies.length === 0 ? (
        <div className="card">
          <p className="muted">{t("dataroom.none")}</p>
        </div>
      ) : (
        <div className="card">
          <select
            value={companyId}
            onChange={(e) => setCompanyId(e.target.value)}
            style={{ padding: 8, borderRadius: 8, border: "1px solid var(--c-border)" }}
          >
            {companies.map((c) => (
              <option key={c.company_id} value={c.company_id}>
                {c.name}
              </option>
            ))}
          </select>{" "}
          <button className="btn" onClick={openRoom}>
            {t("dataroom.open")}
          </button>
          <p className="muted" style={{ fontSize: 12 }}>
            {t("dataroom.provider")}
          </p>
        </div>
      )}

      {room && (
        <>
          <div className="card">
            <h3 style={{ marginTop: 0 }}>{t("dataroom.companyDocs")}</h3>
            {companyDocs.map((d) => (
              <div key={d.id} style={{ display: "flex", justifyContent: "space-between" }}>
                <span>
                  {d.filename} <span className="muted">({d.doc_type})</span>
                </span>
                {inRoom.has(d.id) ? (
                  <span className="badge badge--success">✓</span>
                ) : (
                  <button className="btn btn--ghost" onClick={() => publish(d.id)}>
                    {t("dataroom.addToRoom")}
                  </button>
                )}
              </div>
            ))}
          </div>

          <div className="card">
            <h3 style={{ marginTop: 0 }}>{t("dataroom.grantTitle")}</h3>
            <p className="muted" style={{ fontSize: 12 }}>
              {t("dataroom.gateNote")}
            </p>
            <select
              value={investorId}
              onChange={(e) => setInvestorId(e.target.value)}
              style={{ padding: 8, borderRadius: 8, border: "1px solid var(--c-border)" }}
            >
              <option value="">—</option>
              {investors.map((i) => (
                <option key={i.id} value={i.id}>
                  {i.name}
                </option>
              ))}
            </select>{" "}
            <button className="btn" onClick={grant}>
              {t("dataroom.grant")}
            </button>
            {error && <p className="error">{error}</p>}

            <h4>{t("dataroom.accessList")}</h4>
            {access.map((a) => (
              <div key={a.id} style={{ display: "flex", justifyContent: "space-between" }}>
                <span>
                  {a.investor_name}{" "}
                  {a.revoked && <span className="badge badge--warning">{t("dataroom.revoked")}</span>}
                </span>
                {!a.revoked && (
                  <button className="btn btn--ghost" onClick={() => revoke(a.id)}>
                    {t("dataroom.revoke")}
                  </button>
                )}
              </div>
            ))}
          </div>

          <div className="card">
            <h3 style={{ marginTop: 0 }}>{t("dataroom.logs")}</h3>
            {logs.length === 0 && <p className="muted">{t("dataroom.noLogs")}</p>}
            {logs.map((l) => (
              <p key={l.id} className="muted" style={{ margin: "4px 0", fontSize: 13 }}>
                {new Date(l.created_at).toLocaleString("fr")} · {l.action} · doc{" "}
                {l.document_id?.slice(0, 8)}
              </p>
            ))}
          </div>
        </>
      )}
    </>
  );
}
