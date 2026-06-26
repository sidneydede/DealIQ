import { useState } from "react";
import * as api from "../api";
import {
  COUNTRIES, DEAL_SOURCES, DECK_STATUSES, NETWORKS, SECTORS, STAGES,
} from "../constants";

const EMPTY = {
  name: "", sector: "", stage: "idee", country: "CI",
  founders: "", description: "", deal_source: "", website_url: "",
  deck_status: "", what_i_know: "",
};

export default function DealForm({ note, onCreated, onCancel }) {
  const [f, setF] = useState(EMPTY);
  const [socials, setSocials] = useState({});
  const [error, setError] = useState(null);
  const [busy, setBusy] = useState(false);

  const set = (k, v) => setF((p) => ({ ...p, [k]: v }));
  const setSocial = (k, v) => setSocials((p) => ({ ...p, [k]: v }));

  // Mode Données Zéro : pas d'URL, deck = non, aucun réseau renseigné
  const noSocials = NETWORKS.every((n) => !(socials[n.key] || "").trim());
  const dataZero = !f.website_url.trim() && f.deck_status === "non" && noSocials;

  async function submit(e) {
    e.preventDefault();
    setError(null);
    setBusy(true);
    try {
      const body = { ...f };
      Object.keys(body).forEach((k) => {
        if (body[k] === "") delete body[k];
      });
      body.socials = NETWORKS.filter((n) => (socials[n.key] || "").trim()).map(
        (n) => ({ network: n.key, value: socials[n.key].trim() })
      );
      const deal = await api.createDeal(body);
      onCreated(deal);
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="card">
      <h2>Nouveau deal</h2>
      {note && <div className="note">💡 {note}</div>}
      {dataZero && (
        <div className="note warn">
          Mode Données Zéro — Cherche au moins le @Twitter ou le LinkedIn du fondateur.
          C'est souvent la seule donnée publique disponible en CI.
        </div>
      )}
      <form onSubmit={submit}>
        <div className="row">
          <div className="field">
            <label>Nom de la startup *</label>
            <input value={f.name} onChange={(e) => set("name", e.target.value)} required />
          </div>
          <div className="field">
            <label>Secteur *</label>
            <select value={f.sector} onChange={(e) => set("sector", e.target.value)} required>
              <option value="">—</option>
              {SECTORS.map((s) => <option key={s} value={s}>{s}</option>)}
            </select>
          </div>
        </div>
        <div className="row">
          <div className="field">
            <label>Stade *</label>
            <select value={f.stage} onChange={(e) => set("stage", e.target.value)}>
              {STAGES.map((s) => <option key={s.value} value={s.value}>{s.label}</option>)}
            </select>
          </div>
          <div className="field">
            <label>Pays *</label>
            <select value={f.country} onChange={(e) => set("country", e.target.value)}>
              {COUNTRIES.map((c) => <option key={c.iso2} value={c.iso2}>{c.name}</option>)}
            </select>
          </div>
        </div>

        {dataZero ? (
          <div className="field">
            <label>Ce que je sais (max 500)</label>
            <textarea
              rows={3} maxLength={500}
              value={f.what_i_know}
              onChange={(e) => set("what_i_know", e.target.value)}
            />
          </div>
        ) : (
          <>
            <div className="row">
              <div className="field">
                <label>Fondateur(s)</label>
                <input value={f.founders} onChange={(e) => set("founders", e.target.value)} />
              </div>
              <div className="field">
                <label>Source du deal</label>
                <select value={f.deal_source} onChange={(e) => set("deal_source", e.target.value)}>
                  {DEAL_SOURCES.map((s) => <option key={s.value} value={s.value}>{s.label}</option>)}
                </select>
              </div>
            </div>
            <div className="field">
              <label>Description courte (max 280)</label>
              <textarea
                rows={2} maxLength={280}
                value={f.description}
                onChange={(e) => set("description", e.target.value)}
              />
            </div>
          </>
        )}

        <div className="row">
          <div className="field">
            <label>URL site web</label>
            <input value={f.website_url} onChange={(e) => set("website_url", e.target.value)} />
          </div>
          <div className="field">
            <label>Deck disponible</label>
            <select value={f.deck_status} onChange={(e) => set("deck_status", e.target.value)}>
              {DECK_STATUSES.map((s) => <option key={s.value} value={s.value}>{s.label}</option>)}
            </select>
          </div>
        </div>

        <h3>Profils réseaux sociaux</h3>
        {NETWORKS.map((n) => (
          <div className="field" key={n.key}>
            <label>{n.label}</label>
            <input
              placeholder={n.placeholder}
              value={socials[n.key] || ""}
              onChange={(e) => setSocial(n.key, e.target.value)}
            />
          </div>
        ))}

        {error && <div className="error">{error}</div>}
        <div className="actions">
          <button className="btn" disabled={busy}>{busy ? "Création…" : "Créer la fiche"}</button>
          <button type="button" className="btn secondary" onClick={onCancel}>Annuler</button>
        </div>
      </form>
    </div>
  );
}
