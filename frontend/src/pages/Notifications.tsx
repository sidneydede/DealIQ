import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { useNavigate } from "react-router-dom";

import { notifications as notifApi } from "../api/dealiq";
import type { NotificationItem } from "../api/types";

export default function Notifications() {
  const { t, i18n } = useTranslation();
  const navigate = useNavigate();
  const [list, setList] = useState<NotificationItem[]>([]);

  async function reload() {
    setList(await notifApi.list());
  }
  useEffect(() => {
    void reload();
  }, []);

  async function onOpen(n: NotificationItem) {
    if (!n.read_at) {
      await notifApi.markRead(n.id);
    }
    if (n.link) {
      navigate(n.link);
    } else {
      await reload();
    }
  }

  async function onReadAll() {
    await notifApi.markAllRead();
    await reload();
  }

  const fmt = (iso: string) => new Date(iso).toLocaleString(i18n.language);

  return (
    <>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <h1>{t("notifications.title")}</h1>
        <button className="btn btn--ghost" onClick={onReadAll}>
          {t("notifications.markAllRead")}
        </button>
      </div>

      {list.length === 0 && (
        <div className="card">
          <p className="muted">{t("notifications.empty")}</p>
        </div>
      )}

      {list.map((n) => (
        <button
          key={n.id}
          className="card"
          onClick={() => onOpen(n)}
          style={{
            display: "block",
            width: "100%",
            textAlign: "left",
            cursor: "pointer",
            border: n.read_at ? "1px solid var(--c-border)" : "1px solid var(--c-primary, #2d6cdf)",
            background: n.read_at ? undefined : "var(--c-primary-soft, #eef3fe)",
          }}
        >
          <div style={{ display: "flex", justifyContent: "space-between", gap: 8 }}>
            <strong>{n.title}</strong>
            {!n.read_at && <span className="badge badge--info">{t("notifications.new")}</span>}
          </div>
          <p style={{ margin: "4px 0" }}>{n.body}</p>
          <span className="muted" style={{ fontSize: 12 }}>
            {fmt(n.created_at)}
          </span>
        </button>
      ))}
    </>
  );
}
