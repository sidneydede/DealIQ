import { useEffect, useState } from "react";
import * as api from "../api";
import { scoreColor, STAGES } from "../constants";

const BANDS = [
  { key: "0-30", min: 0, max: 30, label: "Très incomplet (0-30)" },
  { key: "31-60", min: 31, max: 60, label: "Partiel (31-60)" },
  { key: "61-85", min: 61, max: 85, label: "Correct (61-85)" },
  { key: "86-100", min: 86, max: 100, label: "Complet (86-100)" },
];

function Bar({ label, count, total, color }) {
  const pct = total ? Math.round((count / total) * 100) : 0;
  return (
    <div className="bar-row">
      <span className="bar-lbl">{label}</span>
      <span className="bar-track">
        <span className="bar-fill" style={{ width: `${pct}%`, background: color || "var(--primary)" }} />
      </span>
      <span className="bar-val">{count}</span>
    </div>
  );
}

export default function Cockpit({ onOpen, onNavigate }) {
  const [deals, setDeals] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    api.listDeals().then(setDeals).catch((e) => setError(e.message));
  }, []);

  const total = deals.length;
  const avg = total ? Math.round(deals.reduce((s, d) => s + d.completeness_score, 0) / total) : 0;
  const ready = deals.filter((d) => d.completeness_score >= 61).length;
  const todo = total - ready;

  const byBand = BANDS.map((b) => ({
    ...b,
    count: deals.filter((d) => d.completeness_score >= b.min && d.completeness_score <= b.max).length,
  }));
  const byStage = STAGES.map((s) => ({
    ...s,
    count: deals.filter((d) => d.stage === s.value).length,
  }));
  const recent = [...deals]
    .sort((a, b) => new Date(b.updated_at) - new Date(a.updated_at))
    .slice(0, 5);

  if (error) return <div className="card"><div className="error">{error}</div></div>;

  return (
    <div>
      <h2 style={{ marginTop: 0 }}>Cockpit</h2>

      {total === 0 ? (
        <div className="card">
          <p className="muted">Aucun deal pour l'instant.</p>
          <button className="btn" onClick={() => onNavigate("sourcing")}>Créer un premier deal</button>
        </div>
      ) : (
        <>
          <div className="stat-grid">
            <div className="stat-card"><div className="lbl">Deals</div><div className="big">{total}</div></div>
            <div className="stat-card"><div className="lbl">Score moyen</div>
              <div className="big" style={{ color: scoreColor(avg) }}>{avg}</div></div>
            <div className="stat-card"><div className="lbl">Prêts à enrichir</div>
              <div className="big" style={{ color: "var(--ok)" }}>{ready}</div></div>
            <div className="stat-card"><div className="lbl">À compléter</div>
              <div className="big" style={{ color: "#e67e22" }}>{todo}</div></div>
          </div>

          <div className="two-col">
            <div className="card">
              <h3>Complétude des fiches</h3>
              {byBand.map((b) => (
                <Bar key={b.key} label={b.label} count={b.count} total={total} color={scoreColor(b.max)} />
              ))}
            </div>
            <div className="card">
              <h3>Répartition par stade</h3>
              {byStage.map((s) => (
                <Bar key={s.value} label={s.label} count={s.count} total={total} />
              ))}
            </div>
          </div>

          <div className="card">
            <h3>Activité récente</h3>
            {recent.map((d) => (
              <div className="deal-item" key={d.id} style={{ cursor: "pointer" }} onClick={() => onOpen(d.id)}>
                <div>
                  <div className="name">{d.name}</div>
                  <div className="muted">{d.sector} · {d.stage} · maj {new Date(d.updated_at).toLocaleDateString("fr-FR")}</div>
                </div>
                <div className="score-pill" style={{ color: scoreColor(d.completeness_score), fontSize: 16 }}>
                  {d.completeness_score}<span className="muted" style={{ fontSize: 12 }}>/100</span>
                </div>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
}
