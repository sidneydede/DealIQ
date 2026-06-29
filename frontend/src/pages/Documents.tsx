import { useCallback, useEffect, useRef, useState } from "react";
import { useTranslation } from "react-i18next";

import { documents } from "../api/dealiq";
import { ApiError } from "../api/client";
import Loading from "../components/Loading";
import { useToast } from "../components/Toast";
import type { ChecklistItem } from "../api/types";
import { useMyCompany } from "../hooks/useMyCompany";

interface Preview {
  url: string;
  type: string;
  name: string;
  id: string;
}

export default function Documents() {
  const { t } = useTranslation();
  const toast = useToast();
  const { company, loading } = useMyCompany();
  const [items, setItems] = useState<ChecklistItem[]>([]);
  const [busy, setBusy] = useState<string | null>(null);
  const [preview, setPreview] = useState<Preview | null>(null);
  const inputs = useRef<Record<string, HTMLInputElement | null>>({});

  async function openPreview(d: { id: string; filename: string }) {
    try {
      const blob = await documents.preview(d.id);
      setPreview({ url: URL.createObjectURL(blob), type: blob.type, name: d.filename, id: d.id });
    } catch (e) {
      toast.error(e instanceof ApiError ? e.message : t("documents.previewError"));
    }
  }
  function closePreview() {
    if (preview) URL.revokeObjectURL(preview.url);
    setPreview(null);
  }

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

  if (loading) return <Loading />;
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
            <ul style={{ marginBottom: 0, listStyle: "none", paddingLeft: 0 }}>
              {item.documents.map((d) => (
                <li
                  key={d.id}
                  style={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                    gap: 8,
                    flexWrap: "wrap",
                    padding: "4px 0",
                  }}
                >
                  <span className="muted">
                    {d.filename} ({t("documents.version")}
                    {d.version}) — {d.status}
                  </span>
                  <span style={{ display: "flex", gap: 6 }}>
                    <button className="btn btn--ghost" style={{ padding: "4px 10px" }} onClick={() => void openPreview(d)}>
                      {t("documents.preview")}
                    </button>
                    <button
                      className="btn btn--ghost"
                      style={{ padding: "4px 10px" }}
                      onClick={() => void documents.download(d.id, d.filename)}
                    >
                      {t("documents.download")}
                    </button>
                  </span>
                </li>
              ))}
            </ul>
          )}
        </div>
      ))}

      {preview && (
        <div
          role="dialog"
          aria-modal="true"
          onClick={closePreview}
          style={{
            position: "fixed",
            inset: 0,
            background: "rgba(0,0,0,.55)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            zIndex: 1100,
            padding: 16,
          }}
        >
          <div
            className="card"
            onClick={(e) => e.stopPropagation()}
            style={{ width: "min(900px, 96vw)", height: "min(85vh, 900px)", display: "flex", flexDirection: "column", margin: 0 }}
          >
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 8 }}>
              <strong>{preview.name}</strong>
              <span style={{ display: "flex", gap: 8 }}>
                <button className="btn btn--ghost" onClick={() => void documents.download(preview.id, preview.name)}>
                  {t("documents.download")}
                </button>
                <button className="btn" onClick={closePreview}>
                  {t("common.cancel")}
                </button>
              </span>
            </div>
            <div style={{ flex: 1, overflow: "auto", background: "#f4f4f4", borderRadius: 6 }}>
              {preview.type.includes("pdf") ? (
                <iframe title={preview.name} src={preview.url} style={{ width: "100%", height: "100%", border: 0 }} />
              ) : preview.type.startsWith("image/") ? (
                <img src={preview.url} alt={preview.name} style={{ maxWidth: "100%", display: "block", margin: "auto" }} />
              ) : (
                <p className="muted" style={{ padding: 16 }}>
                  {t("documents.previewUnsupported")}
                </p>
              )}
            </div>
          </div>
        </div>
      )}

      <p className="disclaimer">{t("disclaimer")}</p>
    </>
  );
}
