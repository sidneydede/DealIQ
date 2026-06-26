import { useEffect, useState } from "react";
import * as api from "./api";
import DealDetail from "./ui/DealDetail";
import DealList from "./ui/DealList";
import Login from "./ui/Login";

export default function App() {
  const [user, setUser] = useState(null);
  const [ready, setReady] = useState(false);
  const [notes, setNotes] = useState(null);
  const [openId, setOpenId] = useState(null);

  // Restaure la session si un token est présent
  useEffect(() => {
    async function boot() {
      if (api.getToken()) {
        try { setUser(await api.me()); } catch { api.clearToken(); }
      }
      try { setNotes(await api.pedagogicalNotes()); } catch { /* public, ignore */ }
      setReady(true);
    }
    boot();
  }, []);

  function logout() {
    api.clearToken();
    setUser(null);
    setOpenId(null);
  }

  if (!ready) return null;

  return (
    <>
      <div className="topbar">
        <div>
          <h1>DealIQ</h1>
          <span className="sub">Sourcing manuel + enrichissement assisté — CI/UEMOA</span>
        </div>
        {user && (
          <div>
            <span className="muted" style={{ color: "#9fb3c8", marginRight: 12 }}>{user.email}</span>
            <button className="btn secondary small" onClick={logout}>Déconnexion</button>
          </div>
        )}
      </div>

      <div className="container">
        {!user ? (
          <Login onLogged={setUser} />
        ) : openId ? (
          <DealDetail dealId={openId} notes={notes} onBack={() => setOpenId(null)} />
        ) : (
          <DealList notes={notes} onOpen={setOpenId} />
        )}
      </div>
    </>
  );
}
