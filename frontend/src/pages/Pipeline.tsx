import { useCallback, useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

import { deals, meta } from "../api/dealiq";
import Pager from "../components/Pager";
import { SortSelect, useSort } from "../components/SortHeader";
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
  const [stageFilter, setStageFilter] = useState("");
  const [dealTypeFilter, setDealTypeFilter] = useState("");
  const [dealTypeLabels, setDealTypeLabels] = useState<Record<string, string>>({});
  const { sort, order, toggle: toggleSort, state: sortState } = useSort("created_at", "desc");

  useEffect(() => {
    void meta.dealTypes().then((d) =>
      setDealTypeLabels(Object.fromEntries(d.map((x) => [x.code, x.label]))),
    );
  }, []);

  const reload = useCallback(() => {
    void deals
      .list({
        stage: stageFilter || undefined,
        deal_type: dealTypeFilter || undefined,
        sort,
        order,
        limit: LIMIT,
        offset,
      })
      .then((p) => {
        setList(p.items);
        setTotal(p.total);
      });
  }, [stageFilter, dealTypeFilter, sort, order, offset]);
  useEffect(() => reload(), [reload]);

  // Retour page 1 au changement de filtre / tri.
  useEffect(() => {
    setOffset(0);
  }, [stageFilter, dealTypeFilter, sort, order]);

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
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          gap: 8,
          flexWrap: "wrap",
        }}
      >
        <h1>{t("dealPipeline.title")}</h1>
        <div style={{ display: "flex", gap: 8, alignItems: "center", flexWrap: "wrap" }}>
          <select
            value={stageFilter}
            onChange={(e) => setStageFilter(e.target.value)}
            aria-label={t("dealPipeline.stage")}
            style={{ padding: 8, borderRadius: 8, border: "1px solid var(--c-border)" }}
          >
            <option value="">{t("dealPipeline.allStages")}</option>
            {STAGES.map((s) => (
              <option key={s} value={s}>
                {t(`dealPipeline.stages.${s}`)}
              </option>
            ))}
          </select>
          <select
            value={dealTypeFilter}
            onChange={(e) => setDealTypeFilter(e.target.value)}
            aria-label={t("cockpit.cols.dealType")}
            style={{ padding: 8, borderRadius: 8, border: "1px solid var(--c-border)" }}
          >
            <option value="">{t("cockpit.allDealTypes")}</option>
            {Object.entries(dealTypeLabels).map(([code, label]) => (
              <option key={code} value={code}>
                {label}
              </option>
            ))}
          </select>
          <SortSelect
            byLabel={t("sort.by")}
            state={sortState}
            onSort={toggleSort}
            options={[
              { field: "created_at", label: t("sort.date") },
              { field: "stage", label: t("dealPipeline.stage") },
              { field: "deal_type", label: t("cockpit.cols.dealType") },
            ]}
          />
          <button
            className="btn btn--ghost"
            onClick={() =>
              void deals.exportCsv({
                stage: stageFilter || undefined,
                deal_type: dealTypeFilter || undefined,
                sort,
                order,
              })
            }
          >
            {t("dealPipeline.exportCsv")}
          </button>
        </div>
      </div>
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
