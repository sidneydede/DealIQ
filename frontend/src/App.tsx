import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";

import Layout from "./components/Layout";
import { useAuth } from "./auth/AuthContext";
import Dashboard from "./pages/Dashboard";
import DealTypeSelect from "./pages/DealTypeSelect";
import Documents from "./pages/Documents";
import Login from "./pages/Login";
import MyCompany from "./pages/MyCompany";
import Questionnaire from "./pages/Questionnaire";

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
          <Route path="/company" element={<MyCompany />} />
          <Route path="/diagnostic" element={<Questionnaire />} />
          <Route path="/deal-type" element={<DealTypeSelect />} />
          <Route path="/documents" element={<Documents />} />
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
