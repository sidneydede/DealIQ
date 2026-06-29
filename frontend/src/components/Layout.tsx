import { NavLink } from "react-router-dom";
import { useTranslation } from "react-i18next";

import { useAuth, type Role } from "../auth/AuthContext";

interface NavItem {
  to: string;
  key: string;
  roles: Role[];
}

// Sitemap UI (CDC §7.5) — périmètre Lot 0 (placeholders ; modules branchés aux lots suivants).
const NAV: NavItem[] = [
  {
    to: "/",
    key: "nav.dashboard",
    roles: ["entrepreneur", "investisseur", "analyste", "senior", "admin"],
  },
  { to: "/company", key: "nav.company", roles: ["entrepreneur"] },
  { to: "/my-criteria", key: "nav.myCriteria", roles: ["investisseur"] },
  { to: "/opportunities", key: "nav.opportunities", roles: ["investisseur"] },
  { to: "/diagnostic", key: "nav.diagnostic", roles: ["entrepreneur"] },
  { to: "/deal-type", key: "nav.dealType", roles: ["entrepreneur"] },
  { to: "/documents", key: "nav.documents", roles: ["entrepreneur"] },
  { to: "/readiness", key: "nav.readiness", roles: ["entrepreneur"] },
  { to: "/offers", key: "nav.offers", roles: ["entrepreneur"] },
  { to: "/cockpit", key: "nav.cockpit", roles: ["analyste", "senior"] },
  { to: "/investors", key: "nav.investors", roles: ["analyste", "senior", "admin"] },
  { to: "/matching", key: "nav.matching", roles: ["analyste", "senior"] },
  { to: "/teasers", key: "nav.teasers", roles: ["analyste", "senior"] },
  { to: "/interactions", key: "nav.interactions", roles: ["analyste", "senior"] },
  { to: "/reporting", key: "nav.reporting", roles: ["analyste", "senior", "admin"] },
  { to: "/users", key: "nav.users", roles: ["admin"] },
  { to: "/audit", key: "nav.audit", roles: ["admin", "conformite"] },
];

export default function Layout({ children }: { children: React.ReactNode }) {
  const { t } = useTranslation();
  const { user, logout } = useAuth();
  const items = NAV.filter((n) => user && n.roles.includes(user.role));

  // Barre inférieure mobile : on garde les 5 premières entrées (parcours essentiel).
  const mobileItems = items.slice(0, 5);

  return (
    <div className="app-shell">
      <a className="skip-link" href="#main-content">
        Aller au contenu
      </a>
      <aside className="sidebar" aria-label="Navigation principale">
        <div className="brand">{t("app.name")}</div>
        {items.map((n) => (
          <NavLink key={n.to} to={n.to} end={n.to === "/"}>
            {t(n.key)}
          </NavLink>
        ))}
      </aside>
      <div className="main">
        <header className="topbar">
          <span className="muted">{user?.email}</span>
          <button className="btn btn--ghost" onClick={logout} aria-label={t("nav.logout")}>
            {t("nav.logout")}
          </button>
        </header>
        <main className="content" id="main-content">
          {children}
        </main>
      </div>
      <nav className="bottom-nav" aria-label="Navigation mobile">
        {mobileItems.map((n) => (
          <NavLink key={n.to} to={n.to} end={n.to === "/"}>
            {t(n.key)}
          </NavLink>
        ))}
      </nav>
    </div>
  );
}
