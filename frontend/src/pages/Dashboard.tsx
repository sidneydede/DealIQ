import { useTranslation } from "react-i18next";

import { useAuth } from "../auth/AuthContext";

const ROLE_LABEL: Record<string, string> = {
  entrepreneur: "Entrepreneur",
  investisseur: "Investisseur",
  analyste: "Analyste",
  senior: "Consultant senior",
  conformite: "Conformité",
  admin: "Administrateur",
};

export default function Dashboard() {
  const { t } = useTranslation();
  const { user } = useAuth();

  return (
    <>
      <h1>{t("nav.dashboard")}</h1>
      <div className="card">
        <p>
          Bienvenue <strong>{user?.full_name ?? user?.email}</strong>.{" "}
          <span className="badge badge--info">{ROLE_LABEL[user?.role ?? ""]}</span>
        </p>
        <p className="muted">
          Socle Lot 0 en place : authentification, rôles (RBAC) et journal d'audit. Les modules
          métier (type de deal, onboarding, readiness, mini-rapport) arrivent aux lots suivants.
        </p>
      </div>
      <p className="disclaimer">{t("disclaimer")}</p>
    </>
  );
}
