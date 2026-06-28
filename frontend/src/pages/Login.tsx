import { useState, type FormEvent } from "react";
import { useTranslation } from "react-i18next";

import { ApiError } from "../api/client";
import { useAuth } from "../auth/AuthContext";

export default function Login() {
  const { t } = useTranslation();
  const { login, register } = useAuth();
  const [mode, setMode] = useState<"login" | "register">("login");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [fullName, setFullName] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);
    setBusy(true);
    try {
      if (mode === "login") await login(email, password);
      else await register(email, password, fullName);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : t("auth.invalid"));
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="center-screen">
      <div className="card auth-card">
        <div className="brand" style={{ color: "var(--c-ink)", fontWeight: 700, fontSize: 22 }}>
          {t("app.name")}
        </div>
        <p className="muted">{t("app.tagline")}</p>
        <h2>{mode === "login" ? t("auth.loginTitle") : t("auth.register")}</h2>

        <form onSubmit={onSubmit}>
          {mode === "register" && (
            <div className="field">
              <label htmlFor="fn">{t("auth.fullName")}</label>
              <input id="fn" value={fullName} onChange={(e) => setFullName(e.target.value)} />
            </div>
          )}
          <div className="field">
            <label htmlFor="em">{t("auth.email")}</label>
            <input
              id="em"
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>
          <div className="field">
            <label htmlFor="pw">{t("auth.password")}</label>
            <input
              id="pw"
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>
          {error && <p className="error">{error}</p>}
          <button className="btn" type="submit" disabled={busy} style={{ width: "100%" }}>
            {mode === "login" ? t("auth.login") : t("auth.register")}
          </button>
        </form>

        <p className="muted" style={{ marginTop: 14 }}>
          {mode === "login" ? t("auth.noAccount") : t("auth.haveAccount")}{" "}
          <a
            href="#"
            onClick={(e) => {
              e.preventDefault();
              setError(null);
              setMode(mode === "login" ? "register" : "login");
            }}
          >
            {mode === "login" ? t("auth.register") : t("auth.login")}
          </a>
        </p>

        <p className="disclaimer">{t("disclaimer")}</p>
      </div>
    </div>
  );
}
