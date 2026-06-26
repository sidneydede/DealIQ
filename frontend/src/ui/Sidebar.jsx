const ITEMS = [
  { key: "home", ico: "🏠", label: "Accueil" },
  { key: "cockpit", ico: "📊", label: "Cockpit" },
  { key: "sourcing", ico: "📋", label: "Sourcing" },
];

const SOURCING_STEPS = [
  "1 · Saisir un deal",
  "2 · Enrichir (Agent A)",
  "3 · Valider champ par champ",
];

export default function Sidebar({ current, onNavigate }) {
  return (
    <nav className="sidebar">
      {ITEMS.map((it) => (
        <div key={it.key}>
          <button
            className={`nav-item ${current === it.key ? "active" : ""}`}
            onClick={() => onNavigate(it.key)}
          >
            <span className="nav-ico">{it.ico}</span>
            {it.label}
          </button>
          {it.key === "sourcing" && current === "sourcing" && (
            <div>
              {SOURCING_STEPS.map((s) => (
                <div className="nav-step" key={s}>{s}</div>
              ))}
            </div>
          )}
        </div>
      ))}

      <div className="nav-section">Périmètre</div>
      <div className="nav-step">Sourcing manuel</div>
      <div className="nav-step">Enrichissement assisté</div>
      <div className="nav-step" style={{ opacity: .6 }}>Pas de scoring / pipeline / DD</div>
    </nav>
  );
}
