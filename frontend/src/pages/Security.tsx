import { useState, type FormEvent } from "react";
import { useTranslation } from "react-i18next";

import { security } from "../api/dealiq";
import { ApiError } from "../api/client";
import { useAuth } from "../auth/AuthContext";

export default function Security() {
  const { t } = useTranslation();
  const { user, refreshUser } = useAuth();
  const [setup, setSetup] = useState<{ secret: string; otpauth_uri: string } | null>(null);
  const [code, setCode] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  const enabled = user?.mfa_enabled;

  function fail(e: unknown) {
    setError(e instanceof ApiError ? e.message : t("security.error"));
  }

  async function startSetup() {
    setError(null);
    try {
      setSetup(await security.mfaSetup());
    } catch (e) {
      fail(e);
    }
  }

  async function onEnable(e: FormEvent) {
    e.preventDefault();
    setError(null);
    setBusy(true);
    try {
      await security.mfaEnable(code);
      setSetup(null);
      setCode("");
      await refreshUser();
    } catch (err) {
      fail(err);
    } finally {
      setBusy(false);
    }
  }

  async function onDisable(e: FormEvent) {
    e.preventDefault();
    setError(null);
    setBusy(true);
    try {
      await security.mfaDisable(code);
      setCode("");
      await refreshUser();
    } catch (err) {
      fail(err);
    } finally {
      setBusy(false);
    }
  }

  return (
    <>
      <h1>{t("security.title")}</h1>

      <div className="card" style={{ maxWidth: 640 }}>
        <h3 style={{ marginTop: 0 }}>{t("security.mfaTitle")}</h3>
        <p>
          {t("security.status")} :{" "}
          {enabled ? (
            <span className="badge badge--success">{t("security.on")}</span>
          ) : (
            <span className="badge badge--warning">{t("security.off")}</span>
          )}
        </p>
        <p className="muted">{t("security.mfaIntro")}</p>

        {error && <p className="error">{error}</p>}

        {!enabled && !setup && (
          <button className="btn" onClick={() => void startSetup()}>
            {t("security.enable")}
          </button>
        )}

        {!enabled && setup && (
          <form onSubmit={onEnable}>
            <p>{t("security.scanHint")}</p>
            <div
              className="card"
              style={{ background: "var(--c-bg-soft, #f6f6f6)", wordBreak: "break-all" }}
            >
              <div className="muted" style={{ fontSize: 12 }}>
                {t("security.secret")}
              </div>
              <code style={{ fontSize: 16, fontWeight: 700 }}>{setup.secret}</code>
              <div className="muted" style={{ fontSize: 11, marginTop: 8 }}>
                {setup.otpauth_uri}
              </div>
            </div>
            <div className="field" style={{ marginTop: 12 }}>
              <label>{t("security.code")}</label>
              <input
                inputMode="numeric"
                autoComplete="one-time-code"
                required
                value={code}
                onChange={(e) => setCode(e.target.value)}
                placeholder="123456"
              />
            </div>
            <button className="btn" type="submit" disabled={busy}>
              {t("security.confirm")}
            </button>
          </form>
        )}

        {enabled && (
          <form onSubmit={onDisable}>
            <p className="muted">{t("security.disableHint")}</p>
            <div className="field">
              <label>{t("security.code")}</label>
              <input
                inputMode="numeric"
                autoComplete="one-time-code"
                required
                value={code}
                onChange={(e) => setCode(e.target.value)}
                placeholder="123456"
              />
            </div>
            <button className="btn btn--ghost" type="submit" disabled={busy}>
              {t("security.disable")}
            </button>
          </form>
        )}
      </div>
    </>
  );
}
