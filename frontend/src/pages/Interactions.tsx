import { useCallback, useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

import { deals, interactions as api } from "../api/dealiq";
import { ApiError } from "../api/client";
import { useConfirm } from "../components/Confirm";
import { useToast } from "../components/Toast";
import type { Interaction } from "../api/types";
import QAThread from "../components/QAThread";
import { formatDateTime, formatRelative } from "../utils/format";

const NEXT: Record<string, string[]> = {
  interesse: ["nda_envoye", "ecarte"],
  nda_envoye: ["nda_signe", "ecarte"],
  nda_signe: [],
  ecarte: [],
};

export default function Interactions() {
  const { t, i18n } = useTranslation();
  const toast = useToast();
  const confirm = useConfirm();
  const [list, setList] = useState<Interaction[]>([]);
  const [open, setOpen] = useState<string | null>(null);
  const [fb, setFb] = useState<Record<string, { feedback: string; next_step: string }>>({});

  const reload = useCallback(() => {
    void api.list().then(setList);
  }, []);
  useEffect(() => reload(), [reload]);

  function field(id: string, key: "feedback" | "next_step", value: string) {
    setFb((m) => {
      const cur = m[id] ?? { feedback: "", next_step: "" };
      return { ...m, [id]: { ...cur, [key]: value } };
    });
  }

  async function advance(id: string, status: string) {
    // Écarter un investisseur est sensible : on confirme.
    if (
      status === "ecarte" &&
      !(await confirm({ message: t("interactions.discardConfirm"), danger: true }))
    ) {
      return;
    }
    try {
      const extra = fb[id]
        ? { feedback: fb[id].feedback || undefined, next_step: fb[id].next_step || undefined }
        : undefined;
      await api.setStatus(id, status, extra);
      reload();
      toast.success(t("interactions.statusOk"));
    } catch (err) {
      toast.error(err instanceof ApiError ? err.message : t("security.error"));
    }
  }

  async function track(id: string) {
    try {
      await deals.createFromInteraction(id);
      toast.success(t("interactions.trackedOk"));
    } catch (err) {
      toast.error(err instanceof ApiError ? err.message : t("security.error"));
    }
  }

  return (
    <>
      <h1>{t("interactions.title")}</h1>
      <div className="card" style={{ background: "var(--c-bg)" }}>
        <p className="muted" style={{ margin: 0 }}>
          {t("interactions.sequence")}
        </p>
      </div>

      {list.length === 0 && <p className="muted">{t("interactions.empty")}</p>}

      {list.map((it) => (
        <div className="card" key={it.id}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <div>
              <span className="muted" title={formatDateTime(it.created_at, i18n.language)}>
                {formatRelative(it.created_at, i18n.language)}
              </span>
              <div>
                {t("interactions.status")} :{" "}
                <span className="badge badge--info">{it.status}</span>
              </div>
            </div>
            <div style={{ display: "flex", gap: 8 }}>
              {(NEXT[it.status] ?? []).map((s) => (
                <button key={s} className="btn btn--ghost" onClick={() => advance(it.id, s)}>
                  {s}
                </button>
              ))}
            </div>
          </div>
          {it.note && <p className="muted">{it.note}</p>}
          {(it.feedback || it.next_step) && (
            <div className="card" style={{ background: "var(--c-bg)", margin: "8px 0" }}>
              {it.feedback && (
                <div>
                  <strong>{t("interactions.feedback")} :</strong> {it.feedback}
                </div>
              )}
              {it.next_step && (
                <div>
                  <strong>{t("interactions.nextStep")} :</strong> {it.next_step}
                </div>
              )}
            </div>
          )}
          {/* Saisie feedback / prochaine étape (transmis au prochain changement de statut). */}
          {(NEXT[it.status] ?? []).length > 0 && (
            <div style={{ display: "flex", gap: 8, flexWrap: "wrap", margin: "6px 0" }}>
              <input
                value={fb[it.id]?.feedback ?? ""}
                onChange={(e) => field(it.id, "feedback", e.target.value)}
                placeholder={t("interactions.feedbackPlaceholder")}
                style={{ flex: 1, minWidth: 200, padding: 8, borderRadius: 8, border: "1px solid var(--c-border)" }}
              />
              <input
                value={fb[it.id]?.next_step ?? ""}
                onChange={(e) => field(it.id, "next_step", e.target.value)}
                placeholder={t("interactions.nextStepPlaceholder")}
                style={{ flex: 1, minWidth: 200, padding: 8, borderRadius: 8, border: "1px solid var(--c-border)" }}
              />
            </div>
          )}
          <button
            className="btn btn--ghost"
            style={{ marginTop: 8 }}
            onClick={() => setOpen(open === it.id ? null : it.id)}
          >
            {t("qa.thread")}
          </button>{" "}
          <button
            className="btn btn--ghost"
            style={{ marginTop: 8 }}
            onClick={() => track(it.id)}
          >
            {t("dealPipeline.track")}
          </button>
          {open === it.id && <QAThread interactionId={it.id} canAnswer={true} />}
        </div>
      ))}
    </>
  );
}
