import { useEffect, useState } from "react";
import * as api from "../api";
import { scoreColor } from "../constants";
import DealForm from "./DealForm";

export default function DealList({ notes, onOpen }) {
  const [deals, setDeals] = useState([]);
  const [creating, setCreating] = useState(false);
  const [error, setError] = useState(null);

  async function load() {
    setError(null);
    try {
      setDeals(await api.listDeals());
    } catch (err) {
      setError(err.message);
    }
  }
  useEffect(() => { load(); }, []);

  if (creating) {
    return (
      <DealForm
        note={notes?.create_deal}
        onCancel={() => setCreating(false)}
        onCreated={(deal) => onOpen(deal.id)}
      />
    );
  }

  return (
    <div className="card">
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <h2>Deals ({deals.length})</h2>
        <button className="btn" onClick={() => setCreating(true)}>+ Nouveau deal</button>
      </div>
      {notes?.create_deal && <div className="note">💡 {notes.create_deal}</div>}
      {error && <div className="error">{error}</div>}
      {deals.length === 0 && <p className="muted">Aucun deal. Crée ta première fiche.</p>}
      {deals.map((d) => (
        <div className="deal-item" key={d.id} onClick={() => onOpen(d.id)} style={{ cursor: "pointer" }}>
          <div>
            <div className="name">{d.name}</div>
            <div className="muted">{d.sector} · {d.stage} · {d.country}</div>
          </div>
          <div style={{ textAlign: "right" }}>
            <div className="score-pill" style={{ color: scoreColor(d.completeness_score), fontSize: 16 }}>
              {d.completeness_score}<span className="muted" style={{ fontSize: 12 }}>/100</span>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
