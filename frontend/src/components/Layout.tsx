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
  { to: "/", key: "nav.dashboard", roles: ["entrepreneur", "analyste", "senior", "admin"] },
  { to: "/diagnostic", key: "nav.diagnostic", roles: ["entrepreneur"] },
  { to: "/deal-type", key: "nav.dealType", roles: ["entrepreneur"] },
  { to: "/documents", key: "nav.documents", roles: ["entrepreneur"] },
  { to: "/readiness", key: "nav.readiness", roles: ["entrepreneur"] },
  { to: "/offers", key: "nav.offers", roles: ["entrepreneur"] },
  { to: "/cockpit", key: "nav.cockpit", roles: ["analyste", "senior"] },
  { to: "/users", key: "nav.users", roles: ["admin"] },
  { to: "/audit", key: "nav.audit", roles: ["admin", "conformite"] },
];

export default function Layout({ children }: { children: React.ReactNode }) {
  const { t } = useTranslation();
  const { user, logout } = useAuth();
  const items = NAV.filter((n) => user && n.roles.includes(user.role));

  return (
    <div className="app-shell">
      <aside className="sidebar">
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
          <button className="btn btn--ghost" onClick={logout}>
            {t("nav.logout")}
          </button>
        </header>
        <main className="content">{children}</main>
      </div>
    </div>
  );
}
