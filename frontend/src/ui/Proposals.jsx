import { useState } from "react";
import * as api from "../api";

function labelClass(label) {
  if (!label) return "badge";
  if (label.toLowerCase().includes("déclaré")) return "badge declared";
  return "badge ai";
}

function ProposalCard({ p, onChanged, onError }) {
  const [editing, setEditing] = useState(false);
  const [value, setValue] = useState(p.suggested_value || "");
  const [busy, setBusy] = useState(false);
  const resolved = p.status !== "pending";

  async function act(fn) {
    setBusy(true);
    onError(null);
    try {
      await fn();
      await onChanged();
    } catch (err) {
      onError(err.message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className={`proposal ${resolved ? "resolved" : ""}`}>
      <div>
        <span className="field-name">{p.field}</span>{" "}
        <small className="src">via {p.source} · confiance {p.confidence}</small>
      </div>
      {p.label && <span className={labelClass(p.label)}>{p.label}</span>}
      <div className="val">{p.suggested_value}</div>

      {resolved ? (
        <div className="muted">Statut : <strong>{p.status}</strong></div>
      ) : editing ? (
        <div>
          <textarea rows={2} value={value} onChange={(e) => setValue(e.target.value)} />
          <div className="actions">
            <button className="btn ok small" disabled={busy}
              onClick={() => act(() => api.modifyProposal(p.id, value))}>
              Enregistrer la modification
            </button>
            <button className="btn secondary small" onClick={() => setEditing(false)}>Annuler</button>
          </div>
        </div>
      ) : (
        <div className="actions">
          <button className="btn ok small" disabled={busy}
            onClick={() => act(() => api.acceptProposal(p.id))}>Accepter</button>
          <button className="btn secondary small" onClick={() => setEditing(true)}>Modifier</button>
          <button className="btn danger small" disabled={busy}
            onClick={() => act(() => api.rejectProposal(p.id))}>Rejeter</button>
        </div>
      )}
    </div>
  );
}

export default function Proposals({ proposals, onChanged, onError }) {
  const pending = proposals.filter((p) => p.status === "pending");
  const done = proposals.filter((p) => p.status !== "pending");
  if (proposals.length === 0) return null;
  return (
    <div>
      <h3>Propositions à valider ({pending.length})</h3>
      {pending.map((p) => (
        <ProposalCard key={p.id} p={p} onChanged={onChanged} onError={onError} />
      ))}
      {done.length > 0 && <h3>Traitées</h3>}
      {done.map((p) => (
        <ProposalCard key={p.id} p={p} onChanged={onChanged} onError={onError} />
      ))}
    </div>
  );
}
