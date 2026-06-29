import { useCallback, useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

import { interactions as api } from "../api/dealiq";
import type { Interaction } from "../api/types";
import QAThread from "../components/QAThread";

const NEXT: Record<string, string[]> = {
  interesse: ["nda_envoye", "ecarte"],
  nda_envoye: ["nda_signe", "ecarte"],
  nda_signe: [],
  ecarte: [],
};

export default function Interactions() {
  const { t } = useTranslation();
  const [list, setList] = useState<Interaction[]>([]);
  const [open, setOpen] = useState<string | null>(null);

  const reload = useCallback(() => {
    void api.list().then(setList);
  }, []);
  useEffect(() => reload(), [reload]);

  async function advance(id: string, status: string) {
    await api.setStatus(id, status);
    reload();
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
              <span className="muted">{new Date(it.created_at).toLocaleString("fr")}</span>
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
          <button
            className="btn btn--ghost"
            style={{ marginTop: 8 }}
            onClick={() => setOpen(open === it.id ? null : it.id)}
          >
            {t("qa.thread")}
          </button>
          {open === it.id && <QAThread interactionId={it.id} canAnswer={true} />}
        </div>
      ))}
    </>
  );
}
