import { useEffect, useState, type FormEvent } from "react";
import { useTranslation } from "react-i18next";

import { users as usersApi } from "../api/dealiq";
import { ApiError } from "../api/client";
import type { AdminUser } from "../api/types";
import { useAuth } from "../auth/AuthContext";

const ROLES = [
  "entrepreneur",
  "investisseur",
  "analyste",
  "senior",
  "conformite",
  "sponsor",
  "admin",
];

export default function Users() {
  const { t } = useTranslation();
  const { user: me } = useAuth();
  const [list, setList] = useState<AdminUser[]>([]);
  const [email, setEmail] = useState("");
  const [fullName, setFullName] = useState("");
  const [role, setRole] = useState("entrepreneur");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [tempPassword, setTempPassword] = useState<{ email: string; pwd: string } | null>(null);

  async function reload() {
    setList(await usersApi.list());
  }
  useEffect(() => {
    void reload();
  }, []);

  function fail(e: unknown) {
    setError(e instanceof ApiError ? e.message : t("users.error"));
  }

  async function onCreate(e: FormEvent) {
    e.preventDefault();
    setError(null);
    setTempPassword(null);
    try {
      const created = await usersApi.create({
        email,
        full_name: fullName || undefined,
        role,
        password: password || undefined,
      });
      if (created.temporary_password) {
        setTempPassword({ email: created.email, pwd: created.temporary_password });
      }
      setEmail("");
      setFullName("");
      setPassword("");
      setRole("entrepreneur");
      await reload();
    } catch (err) {
      fail(err);
    }
  }

  async function onChangeRole(u: AdminUser, newRole: string) {
    setError(null);
    try {
      await usersApi.changeRole(u.id, newRole);
      await reload();
    } catch (err) {
      fail(err);
    }
  }

  async function onToggleActive(u: AdminUser) {
    setError(null);
    try {
      await usersApi.setActive(u.id, !u.is_active);
      await reload();
    } catch (err) {
      fail(err);
    }
  }

  return (
    <>
      <h1>{t("users.title")}</h1>

      <form className="card" onSubmit={onCreate} style={{ maxWidth: 560 }}>
        <h3 style={{ marginTop: 0 }}>{t("users.add")}</h3>
        <div className="field">
          <label>{t("users.email")}</label>
          <input
            type="email"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>
        <div className="field">
          <label>{t("users.fullName")}</label>
          <input value={fullName} onChange={(e) => setFullName(e.target.value)} />
        </div>
        <div className="field">
          <label>{t("users.role")}</label>
          <select
            value={role}
            onChange={(e) => setRole(e.target.value)}
            style={{ padding: 10, borderRadius: 8, border: "1px solid var(--c-border)" }}
          >
            {ROLES.map((r) => (
              <option key={r} value={r}>
                {t(`users.roles.${r}`)}
              </option>
            ))}
          </select>
        </div>
        <div className="field">
          <label>{t("users.passwordOptional")}</label>
          <input
            type="text"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder={t("users.passwordPlaceholder")}
          />
        </div>
        <button className="btn" type="submit">
          {t("users.create")}
        </button>
      </form>

      {error && (
        <div className="card" role="alert" style={{ borderColor: "var(--c-danger, #c0392b)" }}>
          <span className="badge badge--warning">{error}</span>
        </div>
      )}

      {tempPassword && (
        <div className="card" role="status">
          <strong>{t("users.tempPasswordTitle")}</strong>
          <p className="muted" style={{ margin: "6px 0" }}>
            {t("users.tempPasswordHint", { email: tempPassword.email })}
          </p>
          <code style={{ fontSize: 16, fontWeight: 700 }}>{tempPassword.pwd}</code>
        </div>
      )}

      <div className="card" style={{ overflowX: "auto" }}>
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr style={{ textAlign: "left", borderBottom: "1px solid var(--c-border)" }}>
              <th style={{ padding: 8 }}>{t("users.email")}</th>
              <th style={{ padding: 8 }}>{t("users.fullName")}</th>
              <th style={{ padding: 8 }}>{t("users.role")}</th>
              <th style={{ padding: 8 }}>{t("users.status")}</th>
              <th style={{ padding: 8 }}>{t("users.actions")}</th>
            </tr>
          </thead>
          <tbody>
            {list.map((u) => {
              const self = me?.id === u.id;
              return (
                <tr key={u.id} style={{ borderBottom: "1px solid var(--c-border)" }}>
                  <td style={{ padding: 8 }}>
                    {u.email} {self && <span className="badge badge--info">{t("users.you")}</span>}
                  </td>
                  <td style={{ padding: 8 }}>{u.full_name ?? "—"}</td>
                  <td style={{ padding: 8 }}>
                    <select
                      value={u.role}
                      disabled={self}
                      onChange={(e) => onChangeRole(u, e.target.value)}
                      style={{ padding: 6, borderRadius: 8, border: "1px solid var(--c-border)" }}
                    >
                      {ROLES.map((r) => (
                        <option key={r} value={r}>
                          {t(`users.roles.${r}`)}
                        </option>
                      ))}
                    </select>
                  </td>
                  <td style={{ padding: 8 }}>
                    {u.is_active ? (
                      <span className="badge badge--success">{t("users.active")}</span>
                    ) : (
                      <span className="badge badge--warning">{t("users.inactive")}</span>
                    )}
                  </td>
                  <td style={{ padding: 8 }}>
                    <button
                      className="btn btn--ghost"
                      disabled={self}
                      onClick={() => onToggleActive(u)}
                    >
                      {u.is_active ? t("users.deactivate") : t("users.reactivate")}
                    </button>
                  </td>
                </tr>
              );
            })}
            {list.length === 0 && (
              <tr>
                <td colSpan={5} className="muted" style={{ padding: 8 }}>
                  {t("users.empty")}
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </>
  );
}
