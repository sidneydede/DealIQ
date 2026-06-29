import { useEffect, useState } from "react";
import { NavLink, useLocation } from "react-router-dom";
import { useTranslation } from "react-i18next";

import { account, notifications as notifApi } from "../api/dealiq";
import { ApiError } from "../api/client";
import { useAuth, type Role } from "../auth/AuthContext";
import { useToast } from "./Toast";
import { setLanguage } from "../i18n";

function VerifyEmailBanner() {
  const { t } = useTranslation();
  const { user, refreshUser } = useAuth();
  const toast = useToast();
  const [code, setCode] = useState("");

  if (!user || user.email_verified) return null;

  async function verify() {
    try {
      await account.verifyEmail(user!.email, code);
      await refreshUser();
      toast.success(t("verify.ok"));
    } catch (e) {
      toast.error(e instanceof ApiError ? e.message : t("verify.error"));
    }
  }
  async function resend() {
    try {
      await account.resendVerification(user!.email);
      toast.success(t("verify.resent"));
    } catch {
      toast.error(t("verify.error"));
    }
  }

  return (
    <div
      role="alert"
      style={{
        background: "#fff4e0",
        borderBottom: "1px solid #f0c674",
        padding: "8px 16px",
        display: "flex",
        gap: 8,
        alignItems: "center",
        flexWrap: "wrap",
        fontSize: 14,
      }}
    >
      <span>{t("verify.prompt")}</span>
      <input
        value={code}
        onChange={(e) => setCode(e.target.value)}
        inputMode="numeric"
        placeholder="123456"
        style={{ padding: "4px 8px", borderRadius: 6, border: "1px solid var(--c-border)", width: 110 }}
      />
      <button className="btn" style={{ padding: "4px 10px" }} onClick={() => void verify()}>
        {t("verify.verify")}
      </button>
      <button
        className="btn btn--ghost"
        style={{ padding: "4px 10px" }}
        onClick={() => void resend()}
      >
        {t("verify.resend")}
      </button>
    </div>
  );
}

function NotificationBell() {
  const { t } = useTranslation();
  const location = useLocation();
  const [count, setCount] = useState(0);

  async function refresh() {
    try {
      setCount((await notifApi.unreadCount()).count);
    } catch {
      /* hors-ligne : on garde la dernière valeur connue */
    }
  }
  useEffect(() => {
    void refresh();
    const id = setInterval(() => void refresh(), 30000);
    return () => clearInterval(id);
  }, []);
  // Rafraîchir au changement de page (ex. après avoir marqué comme lu).
  useEffect(() => {
    void refresh();
  }, [location.pathname]);

  return (
    <NavLink
      to="/notifications"
      aria-label={t("nav.notifications")}
      style={{ position: "relative", padding: "4px 8px", fontSize: 18, textDecoration: "none" }}
    >
      <span aria-hidden>🔔</span>
      {count > 0 && (
        <span
          aria-label={t("notifications.unreadCount", { count })}
          style={{
            position: "absolute",
            top: -2,
            right: -2,
            background: "var(--c-danger, #c0392b)",
            color: "#fff",
            borderRadius: 10,
            fontSize: 11,
            fontWeight: 700,
            minWidth: 16,
            height: 16,
            lineHeight: "16px",
            textAlign: "center",
            padding: "0 4px",
          }}
        >
          {count > 99 ? "99+" : count}
        </span>
      )}
    </NavLink>
  );
}

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
    roles: ["entrepreneur", "investisseur", "analyste", "senior", "admin", "sponsor"],
  },
  { to: "/company", key: "nav.company", roles: ["entrepreneur"] },
  { to: "/my-mission", key: "nav.myMission", roles: ["entrepreneur"] },
  { to: "/my-criteria", key: "nav.myCriteria", roles: ["investisseur"] },
  { to: "/opportunities", key: "nav.opportunities", roles: ["investisseur"] },
  { to: "/my-interactions", key: "nav.myInteractions", roles: ["investisseur"] },
  { to: "/my-datarooms", key: "nav.myDatarooms", roles: ["investisseur"] },
  { to: "/diagnostic", key: "nav.diagnostic", roles: ["entrepreneur"] },
  { to: "/deal-type", key: "nav.dealType", roles: ["entrepreneur"] },
  { to: "/documents", key: "nav.documents", roles: ["entrepreneur"] },
  { to: "/readiness", key: "nav.readiness", roles: ["entrepreneur"] },
  { to: "/offers", key: "nav.offers", roles: ["entrepreneur"] },
  { to: "/cockpit", key: "nav.cockpit", roles: ["analyste", "senior"] },
  { to: "/tasks", key: "nav.tasks", roles: ["analyste", "senior", "admin"] },
  { to: "/missions", key: "nav.missions", roles: ["analyste", "senior"] },
  { to: "/investors", key: "nav.investors", roles: ["analyste", "senior", "admin"] },
  { to: "/matching", key: "nav.matching", roles: ["analyste", "senior"] },
  { to: "/teasers", key: "nav.teasers", roles: ["analyste", "senior"] },
  { to: "/interactions", key: "nav.interactions", roles: ["analyste", "senior"] },
  { to: "/datarooms", key: "nav.datarooms", roles: ["analyste", "senior"] },
  { to: "/pipeline", key: "nav.dealPipeline", roles: ["analyste", "senior"] },
  { to: "/mandates", key: "nav.mandates", roles: ["senior", "admin"] },
  { to: "/esg", key: "nav.esg", roles: ["analyste", "senior"] },
  { to: "/dd", key: "nav.dd", roles: ["analyste", "senior"] },
  { to: "/programs", key: "nav.programs", roles: ["senior", "admin", "sponsor"] },
  { to: "/conflicts", key: "nav.conflicts", roles: ["conformite", "senior", "admin"] },
  { to: "/reporting", key: "nav.reporting", roles: ["analyste", "senior", "admin"] },
  { to: "/kyc", key: "nav.kyc", roles: ["conformite", "admin"] },
  { to: "/scoring", key: "nav.scoring", roles: ["admin"] },
  { to: "/users", key: "nav.users", roles: ["admin"] },
  { to: "/audit", key: "nav.audit", roles: ["admin", "conformite"] },
  {
    to: "/notifications",
    key: "nav.notifications",
    roles: ["entrepreneur", "investisseur", "analyste", "senior", "admin", "sponsor", "conformite"],
  },
  {
    to: "/security",
    key: "nav.security",
    roles: ["entrepreneur", "investisseur", "analyste", "senior", "admin", "sponsor", "conformite"],
  },
];

export default function Layout({ children }: { children: React.ReactNode }) {
  const { t, i18n } = useTranslation();
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
        <VerifyEmailBanner />
        <header className="topbar">
          <span className="muted">{user?.email}</span>
          <div style={{ display: "flex", gap: 10, alignItems: "center" }}>
            <NotificationBell />
            <div role="group" aria-label="Langue" style={{ fontSize: 13 }}>
              <button
                className="btn btn--ghost"
                style={{ padding: "4px 8px", fontWeight: i18n.language === "fr" ? 700 : 400 }}
                onClick={() => setLanguage("fr")}
              >
                FR
              </button>
              <button
                className="btn btn--ghost"
                style={{ padding: "4px 8px", fontWeight: i18n.language === "en" ? 700 : 400 }}
                onClick={() => setLanguage("en")}
              >
                EN
              </button>
            </div>
            <button className="btn btn--ghost" onClick={logout} aria-label={t("nav.logout")}>
              {t("nav.logout")}
            </button>
          </div>
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
