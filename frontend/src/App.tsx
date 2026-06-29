import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";

import Layout from "./components/Layout";
import { useAuth } from "./auth/AuthContext";
import Audit from "./pages/Audit";
import Cockpit from "./pages/Cockpit";
import Conflicts from "./pages/Conflicts";
import Dashboard from "./pages/Dashboard";
import DataRoomAdmin from "./pages/DataRoomAdmin";
import DealTypeSelect from "./pages/DealTypeSelect";
import Documents from "./pages/Documents";
import Esg from "./pages/Esg";
import Interactions from "./pages/Interactions";
import Investors from "./pages/Investors";
import Kyc from "./pages/Kyc";
import Login from "./pages/Login";
import MandatesPage from "./pages/Mandates";
import Matching from "./pages/Matching";
import MissionAdmin from "./pages/MissionAdmin";
import MyCompany from "./pages/MyCompany";
import MyCriteria from "./pages/MyCriteria";
import MyDataRooms from "./pages/MyDataRooms";
import MyInteractions from "./pages/MyInteractions";
import MyMission from "./pages/MyMission";
import Offers from "./pages/Offers";
import Opportunities from "./pages/Opportunities";
import Pipeline from "./pages/Pipeline";
import Programs from "./pages/Programs";
import Questionnaire from "./pages/Questionnaire";
import Readiness from "./pages/Readiness";
import Reporting from "./pages/Reporting";
import ReportView from "./pages/ReportView";
import TeaserAdmin from "./pages/TeaserAdmin";

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
          <Route path="/my-mission" element={<MyMission />} />
          <Route path="/missions" element={<MissionAdmin />} />
          <Route path="/diagnostic" element={<Questionnaire />} />
          <Route path="/deal-type" element={<DealTypeSelect />} />
          <Route path="/documents" element={<Documents />} />
          <Route path="/readiness" element={<Readiness />} />
          <Route path="/report" element={<ReportView />} />
          <Route path="/offers" element={<Offers />} />
          <Route path="/cockpit" element={<Cockpit />} />
          <Route path="/reporting" element={<Reporting />} />
          <Route path="/my-criteria" element={<MyCriteria />} />
          <Route path="/opportunities" element={<Opportunities />} />
          <Route path="/my-interactions" element={<MyInteractions />} />
          <Route path="/investors" element={<Investors />} />
          <Route path="/matching" element={<Matching />} />
          <Route path="/teasers" element={<TeaserAdmin />} />
          <Route path="/interactions" element={<Interactions />} />
          <Route path="/datarooms" element={<DataRoomAdmin />} />
          <Route path="/my-datarooms" element={<MyDataRooms />} />
          <Route path="/pipeline" element={<Pipeline />} />
          <Route path="/mandates" element={<MandatesPage />} />
          <Route path="/esg" element={<Esg />} />
          <Route path="/programs" element={<Programs />} />
          <Route path="/conflicts" element={<Conflicts />} />
          <Route path="/kyc" element={<Kyc />} />
          <Route path="/users" element={<Placeholder title="Utilisateurs" />} />
          <Route path="/audit" element={<Audit />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
}
