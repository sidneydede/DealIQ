import { useEffect, useState } from "react";
import * as api from "../api";

export default function Home({ user, onNavigate }) {
  const [meta, setMeta] = useState(null);

  useEffect(() => {
    api.getMeta().then(setMeta).catch(() => {});
  }, []);

  return (
    <div>
      <div className="hero">
        <h1>Bienvenue sur DealIQ</h1>
        <p>
          Le copilote de sourcing pour l'analyste VC junior en Côte d'Ivoire / UEMOA.
          Tu trouves les deals, l'IA t'aide à les enrichir — toujours sous ton contrôle.
        </p>
        <div className="cta">
          <button className="btn" onClick={() => onNavigate("sourcing")}>
            Démarrer le sourcing
          </button>
          <button className="btn secondary" onClick={() => onNavigate("cockpit")}>
            Voir le cockpit
          </button>
        </div>
      </div>

      <div className="two-col">
        <div className="card">
          <h2>2 modules, rien de plus</h2>
          <p className="muted">
            <strong>1. Sourcing manuel</strong> — tu saisis chaque deal, quelle que soit
            la qualité de l'information disponible. Un score de complétude te guide.
          </p>
          <p className="muted">
            <strong>2. Enrichissement assisté</strong> — l'Agent A complète la fiche depuis
            les sources publiques (X, LinkedIn, site, Crunchbase…), et tu valides champ par champ.
          </p>
        </div>

        <div className="card">
          <h2>Périmètre</h2>
          {meta ? (
            <div className="two-col" style={{ gap: 10 }}>
              <ul className="scope-list">
                {meta.scope.in_scope.map((s) => <li key={s}>{s}</li>)}
              </ul>
              <ul className="scope-list out">
                {meta.scope.out_of_scope.map((s) => <li key={s}>{s}</li>)}
              </ul>
            </div>
          ) : <p className="muted">Chargement…</p>}
        </div>
      </div>

      {meta && (
        <div className="card">
          <h3>Objectif</h3>
          <p>🎯 {meta.mvp_success_criterion}</p>
        </div>
      )}

      <p className="muted">Connecté en tant que {user.email}.</p>
    </div>
  );
}
