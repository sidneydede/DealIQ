import { useEffect, useRef, useState } from "react";
import * as api from "../api";
import { scoreColor } from "../constants";
import Proposals from "./Proposals";

export default function DealDetail({ dealId, notes, onBack }) {
  const [deal, setDeal] = useState(null);
  const [proposals, setProposals] = useState([]);
  const [dealNotes, setDealNotes] = useState([]);
  const [history, setHistory] = useState([]);
  const [guided, setGuided] = useState([]);
  const [status, setStatus] = useState(null);
  const [error, setError] = useState(null);
  const [message, setMessage] = useState(null);
  const [busy, setBusy] = useState(false);
  const [text, setText] = useState("");
  const [noteText, setNoteText] = useState("");
  const fileRef = useRef(null);

  async function reload() {
    setError(null);
    try {
      const [d, p, n, h, g, s] = await Promise.all([
        api.getDeal(dealId), api.listProposals(dealId), api.listNotes(dealId),
        api.getHistory(dealId), api.guidedQuestions(dealId), api.enrichStatus(dealId),
      ]);
      setDeal(d); setProposals(p); setDealNotes(n);
      setHistory(h); setGuided(g); setStatus(s);
    } catch (err) {
      setError(err.message);
    }
  }
  useEffect(() => { reload(); }, [dealId]);

  async function run(fn, okMsg) {
    setBusy(true); setError(null); setMessage(null);
    try {
      const res = await fn();
      if (res?.message) setMessage(res.message);
      else if (okMsg) setMessage(okMsg);
      await reload();
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  }

  if (!deal) return <div className="card">{error ? <div className="error">{error}</div> : "Chargement…"}</div>;

  return (
    <div>
      <button className="btn secondary small" onClick={onBack}>← Retour</button>

      {/* En-tête */}
      <div className="card" style={{ marginTop: 12 }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
          <div>
            <h2 style={{ marginBottom: 4 }}>{deal.name}</h2>
            <div className="muted">{deal.sector} · {deal.stage} · {deal.country}</div>
          </div>
          <div style={{ textAlign: "right", minWidth: 160 }}>
            <div className="score-pill" style={{ color: scoreColor(deal.completeness_score) }}>
              {deal.completeness_score}<span className="muted" style={{ fontSize: 13 }}>/100</span>
            </div>
            <div className="score-bar">
              <div style={{ width: `${deal.completeness_score}%`, background: scoreColor(deal.completeness_score) }} />
            </div>
            <div className="muted" style={{ marginTop: 4 }}>{deal.score_band}</div>
          </div>
        </div>

        {deal.activity && (
          <div className={`activity ${deal.activity.stale ? "stale" : ""}`} style={{ marginTop: 10 }}>
            Dernière activité publique : {deal.activity.network} —{" "}
            {new Date(deal.activity.last_activity_at).toLocaleDateString("fr-FR")}
            {deal.activity.stale && " (inactif > 90 j)"}
          </div>
        )}
        {deal.data_zero_mode && <div className="note warn" style={{ marginTop: 10 }}>{deal.data_zero_hint}</div>}
        {deal.description && <p style={{ marginTop: 12 }}>{deal.description}</p>}
        {deal.founders && <p className="muted">Fondateur(s) : {deal.founders}</p>}
      </div>

      {/* Enrichissement Agent A */}
      <div className="card">
        <h2>Enrichissement (Agent A)</h2>
        {notes?.enrich && <div className="note">💡 {notes.enrich}</div>}
        <div className="muted" style={{ marginBottom: 8 }}>
          {status?.prerequisite_met
            ? status.can_run
              ? "Prêt à enrichir."
              : `Prochain enrichissement dans ${status.minutes_until_next} min.`
            : "Prérequis non rempli : ajoute au moins un @Twitter ou une URL."}
        </div>
        <button className="btn" disabled={busy || !status?.can_run}
          onClick={() => run(() => api.enrich(dealId))}>
          Enrichir automatiquement
        </button>

        {message && <div className="note warn" style={{ marginTop: 10 }}>{message}</div>}
        {error && <div className="error">{error}</div>}

        <Proposals proposals={proposals} onChanged={reload} onError={setError} />
      </div>

      {/* Import IA */}
      <div className="card">
        <h2>Import de contenu</h2>
        <h3>Coller un post / tweet / message</h3>
        <textarea rows={3} maxLength={2000} value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Colle ici un tweet, un post LinkedIn ou un message WhatsApp…" />
        <div className="actions">
          <button className="btn small" disabled={busy || !text.trim()}
            onClick={() => run(() => api.extractText(dealId, text), null)}>
            Extraire les infos
          </button>
        </div>

        <h3>Deck PDF</h3>
        <input type="file" accept="application/pdf" ref={fileRef} />
        <div className="actions">
          <button className="btn small" disabled={busy}
            onClick={() => {
              const file = fileRef.current?.files?.[0];
              if (file) run(() => api.uploadDeck(dealId, file), null);
            }}>
            Importer le deck
          </button>
        </div>
      </div>

      {/* Questions guidées */}
      {guided.length > 0 && (
        <div className="card">
          <h2>Enrichissement manuel guidé</h2>
          {guided.map((q) => (
            <div key={q.field} className="note">❓ {q.question}</div>
          ))}
        </div>
      )}

      {/* Notes */}
      <div className="card">
        <h2>Journal de deal</h2>
        <textarea rows={2} maxLength={1000} value={noteText}
          onChange={(e) => setNoteText(e.target.value)} placeholder="Ajouter une note…" />
        <div className="actions">
          <button className="btn small" disabled={busy || !noteText.trim()}
            onClick={() => run(async () => { await api.addNote(dealId, noteText); setNoteText(""); }, null)}>
            Ajouter la note
          </button>
        </div>
        {dealNotes.map((n) => (
          <div key={n.id} className="hist-row">
            <span className="muted">{new Date(n.created_at).toLocaleString("fr-FR")}</span> — {n.content}
          </div>
        ))}
      </div>

      {/* Historique */}
      <div className="card">
        <h2>Historique des modifications ({history.length})</h2>
        {history.length === 0 && <p className="muted">Aucune modification.</p>}
        {history.map((h) => (
          <div key={h.id} className="hist-row">
            <code>{h.field}</code> : {h.old_value ?? "∅"} → <strong>{h.new_value ?? "∅"}</strong>{" "}
            <span className="muted">({new Date(h.changed_at).toLocaleString("fr-FR")})</span>
          </div>
        ))}
      </div>
    </div>
  );
}
