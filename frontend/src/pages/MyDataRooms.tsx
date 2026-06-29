import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

import { dataroom } from "../api/dealiq";
import type { DataRoom, DataRoomDocument, DocumentView } from "../api/types";

export default function MyDataRooms() {
  const { t } = useTranslation();
  const [rooms, setRooms] = useState<DataRoom[]>([]);
  const [openId, setOpenId] = useState<string | null>(null);
  const [docs, setDocs] = useState<DataRoomDocument[]>([]);
  const [viewed, setViewed] = useState<DocumentView | null>(null);

  useEffect(() => {
    void dataroom.accessible().then(setRooms);
  }, []);

  async function toggle(roomId: string) {
    setViewed(null);
    if (openId === roomId) {
      setOpenId(null);
      return;
    }
    setOpenId(roomId);
    setDocs(await dataroom.documents(roomId));
  }

  async function view(roomId: string, documentId: string, download = false) {
    setViewed(await dataroom.view(roomId, documentId, download));
  }

  return (
    <>
      <h1>{t("dataroom.myTitle")}</h1>
      {rooms.length === 0 && <p className="muted">{t("dataroom.myEmpty")}</p>}

      {rooms.map((r) => (
        <div className="card" key={r.id}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <strong>Data room {r.provider_ref}</strong>
            <button className="btn btn--ghost" onClick={() => toggle(r.id)}>
              {openId === r.id ? "—" : "+"}
            </button>
          </div>

          {openId === r.id && (
            <div style={{ marginTop: 10 }}>
              {docs.map((d) => (
                <div
                  key={d.id}
                  style={{ display: "flex", justifyContent: "space-between", margin: "6px 0" }}
                >
                  <span>
                    {d.filename} <span className="muted">({d.doc_type})</span>
                  </span>
                  <span style={{ display: "flex", gap: 8 }}>
                    <button className="btn btn--ghost" onClick={() => view(r.id, d.document_id)}>
                      {t("dataroom.view")}
                    </button>
                    <button
                      className="btn btn--ghost"
                      onClick={() => view(r.id, d.document_id, true)}
                    >
                      {t("dataroom.download")}
                    </button>
                  </span>
                </div>
              ))}

              {viewed && (
                <div className="card" style={{ background: "var(--c-bg)", marginTop: 10 }}>
                  <strong>{viewed.filename}</strong>
                  <p className="muted" style={{ margin: "6px 0" }}>
                    {t("dataroom.watermark")} : <em>{viewed.watermark}</em>
                  </p>
                  <p className="muted" style={{ fontSize: 12 }}>
                    {viewed.note}
                  </p>
                </div>
              )}
            </div>
          )}
        </div>
      ))}
      <p className="disclaimer">{t("disclaimer")}</p>
    </>
  );
}
