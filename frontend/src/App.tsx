import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";

import Layout from "./components/Layout";
import { useAuth } from "./auth/AuthContext";
import Audit from "./pages/Audit";
import Cockpit from "./pages/Cockpit";
import Dashboard from "./pages/Dashboard";
import DealTypeSelect from "./pages/DealTypeSelect";
import Documents from "./pages/Documents";
import Investors from "./pages/Investors";
import Login from "./pages/Login";
import Matching from "./pages/Matching";
import MyCompany from "./pages/MyCompany";
import MyCriteria from "./pages/MyCriteria";
import Offers from "./pages/Offers";
import Questionnaire from "./pages/Questionnaire";
import Readiness from "./pages/Readiness";
import Reporting from "./pages/Reporting";
import ReportView from "./pages/ReportView";

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
          <Route path="/readiness" element={<Readiness />} />
          <Route path="/report" element={<ReportView />} />
          <Route path="/offers" element={<Offers />} />
          <Route path="/cockpit" element={<Cockpit />} />
          <Route path="/reporting" element={<Reporting />} />
          <Route path="/my-criteria" element={<MyCriteria />} />
          <Route path="/investors" element={<Investors />} />
          <Route path="/matching" element={<Matching />} />
          <Route path="/users" element={<Placeholder title="Utilisateurs" />} />
          <Route path="/audit" element={<Audit />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
}
