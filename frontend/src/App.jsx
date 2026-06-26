import { useEffect, useState } from "react";
import * as api from "./api";
import Cockpit from "./ui/Cockpit";
import DealDetail from "./ui/DealDetail";
import Home from "./ui/Home";
import Login from "./ui/Login";
import Sidebar from "./ui/Sidebar";
import Sourcing from "./ui/Sourcing";

export default function App() {
  const [user, setUser] = useState(null);
  const [ready, setReady] = useState(false);
  const [notes, setNotes] = useState(null);
  const [view, setView] = useState("home");
  const [openId, setOpenId] = useState(null);

  useEffect(() => {
    async function boot() {
      if (api.getToken()) {
        try { setUser(await api.me()); } catch { api.clearToken(); }
      }
      try { setNotes(await api.pedagogicalNotes()); } catch { /* public */ }
      setReady(true);
    }
    boot();
  }, []);

  function navigate(v) {
    setOpenId(null);
    setView(v);
  }
  function openDeal(id) {
    setOpenId(id);
  }
  function logout() {
    api.clearToken();
    setUser(null);
    setOpenId(null);
    setView("home");
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
            <span style={{ color: "#9fb3c8", marginRight: 12, fontSize: 13 }}>{user.email}</span>
            <button className="btn secondary small" onClick={logout}>Déconnexion</button>
          </div>
        )}
      </div>

      {!user ? (
        <div className="container">
          <Login onLogged={(u) => { setUser(u); setView("home"); }} />
        </div>
      ) : (
        <div className="layout">
          <Sidebar current={openId ? "sourcing" : view} onNavigate={navigate} />
          <main className="content">
            {openId ? (
              <DealDetail dealId={openId} notes={notes} onBack={() => setOpenId(null)} />
            ) : view === "home" ? (
              <Home user={user} onNavigate={navigate} />
            ) : view === "cockpit" ? (
              <Cockpit onOpen={openDeal} onNavigate={navigate} />
            ) : (
              <Sourcing notes={notes} onOpen={openDeal} />
            )}
          </main>
        </div>
      )}
    </>
  );
}
