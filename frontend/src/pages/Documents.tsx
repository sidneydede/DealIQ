import { useCallback, useEffect, useRef, useState } from "react";
import { useTranslation } from "react-i18next";

import { documents } from "../api/dealiq";
import type { ChecklistItem } from "../api/types";
import { useMyCompany } from "../hooks/useMyCompany";

export default function Documents() {
  const { t } = useTranslation();
  const { company, loading } = useMyCompany();
  const [items, setItems] = useState<ChecklistItem[]>([]);
  const [busy, setBusy] = useState<string | null>(null);
  const inputs = useRef<Record<string, HTMLInputElement | null>>({});

  const reload = useCallback(async () => {
    if (company) setItems(await documents.checklist(company.id));
  }, [company]);

  useEffect(() => {
    void reload();
  }, [reload]);

  async function onFile(docType: string, file: File | undefined) {
    if (!company || !file) return;
    setBusy(docType);
    try {
      await documents.upload(company.id, docType, file);
      await reload();
    } finally {
      setBusy(null);
    }
  }

  if (loading) return <p className="muted">Chargement…</p>;
  if (!company)
    return (
      <>
        <h1>{t("documents.title")}</h1>
        <div className="card">
          <p className="muted">{t("documents.needCompany")}</p>
        </div>
      </>
    );

  return (
    <>
      <h1>{t("documents.title")}</h1>
      <p className="muted">{t("documents.intro")}</p>

      {items.map((item) => (
        <div className="card" key={item.doc_type}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <div>
              <strong>{item.doc_type}</strong>{" "}
              <span className={`badge badge--${item.required ? "info" : "warning"}`}>
                {item.required ? t("documents.required") : t("documents.optional")}
              </span>{" "}
              {item.verified ? (
                <span className="badge badge--success">{t("documents.verified")}</span>
              ) : item.received ? (
                <span className="badge badge--info">{t("documents.received")}</span>
              ) : (
                <span className="badge badge--warning">{t("documents.missing")}</span>
              )}
            </div>
            <div>
              <input
                ref={(el) => {
                  inputs.current[item.doc_type] = el;
                }}
                type="file"
                style={{ display: "none" }}
                accept=".pdf,.png,.jpg,.jpeg,.xlsx,.xls"
                onChange={(e) => onFile(item.doc_type, e.target.files?.[0])}
              />
              <button
                className="btn btn--ghost"
                disabled={busy === item.doc_type}
                onClick={() => inputs.current[item.doc_type]?.click()}
              >
                {t("documents.add")}
              </button>
            </div>
          </div>
          {item.documents.length > 0 && (
            <ul className="muted" style={{ marginBottom: 0 }}>
              {item.documents.map((d) => (
                <li key={d.id}>
                  {d.filename} ({t("documents.version")}
                  {d.version}) — {d.status}
                </li>
              ))}
            </ul>
          )}
        </div>
      ))}

      <p className="disclaimer">{t("disclaimer")}</p>
    </>
  );
}
