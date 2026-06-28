import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";

import Layout from "./components/Layout";
import { useAuth } from "./auth/AuthContext";
import Dashboard from "./pages/Dashboard";
import Login from "./pages/Login";

function Placeholder({ title }: { title: string }) {
  return (
    <>
      <h1>{title}</h1>
      <div className="card">
        <p className="muted">Module à implémenter dans un prochain lot.</p>
      </div>
    </>
  );
}

export default function App() {
  const { user, loading } = useAuth();

  if (loading) return <div className="center-screen muted">Chargement…</div>;
  if (!user) return <Login />;

  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/diagnostic" element={<Placeholder title="Mon diagnostic" />} />
          <Route path="/deal-type" element={<Placeholder title="Mon type de deal" />} />
          <Route path="/documents" element={<Placeholder title="Documents" />} />
          <Route path="/readiness" element={<Placeholder title="Ma readiness" />} />
          <Route path="/offers" element={<Placeholder title="Accompagnement" />} />
          <Route path="/cockpit" element={<Placeholder title="Cockpit cabinet" />} />
          <Route path="/users" element={<Placeholder title="Utilisateurs" />} />
          <Route path="/audit" element={<Placeholder title="Journal d'audit" />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
}
