import { useCallback, useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

import { deals } from "../api/dealiq";
import Pager from "../components/Pager";
import type { Deal, DealDetail } from "../api/types";

const STAGES = [
  "interesse",
  "nda",
  "data_room",
  "due_diligence",
  "term_sheet",
  "closing",
  "abandonne",
];
const LIMIT = 25;

export default function Pipeline() {
  const { t } = useTranslation();
  const [list, setList] = useState<Deal[]>([]);
  const [total, setTotal] = useState(0);
  const [offset, setOffset] = useState(0);
  const [openId, setOpenId] = useState<string | null>(null);
  const [detail, setDetail] = useState<DealDetail | null>(null);
  const [note, setNote] = useState("");

  const reload = useCallback(() => {
    void deals.list({ limit: LIMIT, offset }).then((p) => {
      setList(p.items);
      setTotal(p.total);
    });
  }, [offset]);
  useEffect(() => reload(), [reload]);

  async function openDeal(id: string) {
    if (openId === id) {
      setOpenId(null);
      return;
    }
    setOpenId(id);
    setDetail(await deals.get(id));
  }

  async function advance(stage: string) {
    if (!detail) return;
    await deals.advance(detail.id, stage, note || undefined);
    setNote("");
    setDetail(await deals.get(detail.id));
    reload();
  }

  async function toggle(milestoneId: string, done: boolean) {
    if (!detail) return;
    await deals.toggleMilestone(milestoneId, done);
    setDetail(await deals.get(detail.id));
  }

  return (
    <>
      <h1>{t("dealPipeline.title")}</h1>
      {list.length === 0 && <p className="muted">{t("dealPipeline.empty")}</p>}

      {list.map((d) => (
        <div className="card" key={d.id}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <div>
              <strong>{d.company_name}</strong> ↔ {d.investor_name}{" "}
              <span className="badge badge--info">{t(`dealPipeline.stages.${d.stage}`)}</span>{" "}
              <span className="muted">{d.deal_type}</span>
            </div>
            <button className="btn btn--ghost" onClick={() => openDeal(d.id)}>
              {openId === d.id ? "—" : "+"}
            </button>
          </div>

          {openId === d.id && detail && (
            <div style={{ marginTop: 12 }}>
              {/* Avancement d'étape */}
              <div style={{ display: "flex", gap: 6, flexWrap: "wrap", marginBottom: 8 }}>
                {STAGES.map((s) => (
                  <button
                    key={s}
                    className={`btn ${s === detail.stage ? "" : "btn--ghost"}`}
                    onClick={() => advance(s)}
                    disabled={s === detail.stage}
                  >
                    {t(`dealPipeline.stages.${s}`)}
                  </button>
                ))}
              </div>
              <input
                placeholder={t("dealPipeline.note")}
                value={note}
                onChange={(e) => setNote(e.target.value)}
                style={{ width: "100%", padding: 8, borderRadius: 8, border: "1px solid var(--c-border)" }}
              />

              {/* Jalons de closing (selon le type de deal) */}
              <h4>{t("dealPipeline.milestones")}</h4>
              {detail.milestones.map((m) => (
                <label key={m.id} style={{ display: "flex", gap: 8, alignItems: "center" }}>
                  <input
                    type="checkbox"
                    checked={m.done}
                    onChange={(e) => toggle(m.id, e.target.checked)}
                  />
                  <span style={{ textDecoration: m.done ? "line-through" : "none" }}>
                    {m.label}
                  </span>
                </label>
              ))}

              {/* Historique */}
              <h4>{t("dealPipeline.history")}</h4>
              {detail.history.map((h) => (
                <p key={h.id} className="muted" style={{ margin: "4px 0", fontSize: 13 }}>
                  {new Date(h.created_at).toLocaleString("fr")} ·{" "}
                  {h.old_stage ? `${t(`dealPipeline.stages.${h.old_stage}`)} → ` : ""}
                  {t(`dealPipeline.stages.${h.new_stage}`)}
                  {h.note ? ` · ${h.note}` : ""}
                </p>
              ))}
            </div>
          )}
        </div>
      ))}

      <Pager total={total} limit={LIMIT} offset={offset} onChange={setOffset} />
    </>
  );
}
