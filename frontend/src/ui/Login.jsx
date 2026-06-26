import { useState } from "react";
import * as api from "../api";

export default function Login({ onLogged }) {
  const [email, setEmail] = useState("analyste@dealiq.ci");
  const [password, setPassword] = useState("changeme");
  const [error, setError] = useState(null);
  const [busy, setBusy] = useState(false);

  async function submit(e) {
    e.preventDefault();
    setError(null);
    setBusy(true);
    try {
      await api.login(email, password);
      const user = await api.me();
      onLogged(user);
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="login-wrap">
      <div className="card">
        <h2>Connexion DealIQ</h2>
        <form onSubmit={submit}>
          <div className="field">
            <label>Email</label>
            <input value={email} onChange={(e) => setEmail(e.target.value)} />
          </div>
          <div className="field">
            <label>Mot de passe</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>
          {error && <div className="error">{error}</div>}
          <button className="btn" disabled={busy}>
            {busy ? "Connexion…" : "Se connecter"}
          </button>
        </form>
        <p className="muted" style={{ marginTop: 12 }}>
          Identifiants de seed par défaut pré-remplis (cf. <code>.env</code>).
        </p>
      </div>
    </div>
  );
}
