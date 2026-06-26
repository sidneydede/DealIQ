import { useEffect, useState } from "react";

export default function App() {
  const [health, setHealth] = useState("…");

  useEffect(() => {
    fetch("/api/health")
      .then((r) => r.json())
      .then((d) => setHealth(d.status))
      .catch(() => setHealth("indisponible"));
  }, []);

  return (
    <main style={{ fontFamily: "system-ui", padding: 32, maxWidth: 640 }}>
      <h1>DealIQ</h1>
      <p>Sourcing manuel + enrichissement assisté de deals VC — CI/UEMOA.</p>
      <p>
        API : <strong>{health}</strong>
      </p>
      <p style={{ color: "#666" }}>Phase 0 — fondations. Module 1 à venir.</p>
    </main>
  );
}
