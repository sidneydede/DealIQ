import { useCallback, useEffect, useState, type FormEvent } from "react";
import { useTranslation } from "react-i18next";

import { tasks as api } from "../api/dealiq";
import { ApiError } from "../api/client";
import { useAuth } from "../auth/AuthContext";
import { useConfirm } from "../components/Confirm";
import { useToast } from "../components/Toast";
import type { Task } from "../api/types";
import { formatDateTime } from "../utils/format";

const FILTERS = ["all", "a_faire", "overdue", "fait", "mine"] as const;

export default function Tasks() {
  const { t, i18n } = useTranslation();
  const { user } = useAuth();
  const toast = useToast();
  const confirm = useConfirm();
  const [list, setList] = useState<Task[]>([]);
  const [filter, setFilter] = useState<(typeof FILTERS)[number]>("a_faire");
  const [title, setTitle] = useState("");
  const [due, setDue] = useState("");

  const reload = useCallback(() => {
    const params: Record<string, unknown> = {};
    if (filter === "a_faire" || filter === "fait") params.status_filter = filter;
    if (filter === "overdue") params.overdue = true;
    if (filter === "mine") params.mine = true;
    void api.list(params).then(setList);
  }, [filter]);
  useEffect(() => reload(), [reload]);

  function fail(e: unknown) {
    toast.error(e instanceof ApiError ? e.message : t("security.error"));
  }

  async function onCreate(e: FormEvent) {
    e.preventDefault();
    try {
      await api.create({
        title,
        due_date: due ? new Date(due).toISOString() : undefined,
        assignee_id: user?.id, // assignée au créateur (utile pour « Mes tâches »)
      });
      setTitle("");
      setDue("");
      reload();
      toast.success(t("tasks.createdOk"));
    } catch (err) {
      fail(err);
    }
  }

  async function toggle(task: Task) {
    try {
      await api.update(task.id, { status: task.status === "fait" ? "a_faire" : "fait" });
      reload();
    } catch (err) {
      fail(err);
    }
  }

  async function remove(task: Task) {
    if (!(await confirm({ message: t("tasks.deleteConfirm"), danger: true }))) return;
    try {
      await api.remove(task.id);
      reload();
      toast.success(t("tasks.deletedOk"));
    } catch (err) {
      fail(err);
    }
  }

  return (
    <>
      <h1>{t("tasks.title")}</h1>

      <form
        className="card"
        onSubmit={onCreate}
        style={{ display: "flex", gap: 8, alignItems: "flex-end", flexWrap: "wrap" }}
      >
        <div className="field" style={{ flex: 1, minWidth: 220, marginBottom: 0 }}>
          <label>{t("tasks.titleLabel")}</label>
          <input required value={title} onChange={(e) => setTitle(e.target.value)} />
        </div>
        <div className="field" style={{ marginBottom: 0 }}>
          <label>{t("tasks.dueDate")}</label>
          <input type="date" value={due} onChange={(e) => setDue(e.target.value)} />
        </div>
        <button className="btn" type="submit">
          {t("tasks.add")}
        </button>
      </form>

      <div style={{ display: "flex", gap: 8, margin: "16px 0", flexWrap: "wrap" }}>
        {FILTERS.map((f) => (
          <button
            key={f}
            className={`btn ${filter === f ? "" : "btn--ghost"}`}
            onClick={() => setFilter(f)}
          >
            {t(`tasks.filters.${f}`)}
          </button>
        ))}
      </div>

      {list.length === 0 && <p className="muted">{t("tasks.empty")}</p>}

      {list.map((task) => (
        <div className="card" key={task.id}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", gap: 8 }}>
            <label style={{ display: "flex", gap: 8, alignItems: "center", flex: 1 }}>
              <input
                type="checkbox"
                checked={task.status === "fait"}
                onChange={() => toggle(task)}
              />
              <span style={{ textDecoration: task.status === "fait" ? "line-through" : "none" }}>
                {task.title}
              </span>
              {task.overdue && <span className="badge badge--warning">{t("tasks.overdue")}</span>}
            </label>
            <button className="btn btn--ghost" onClick={() => remove(task)}>
              {t("tasks.delete")}
            </button>
          </div>
          <div className="muted" style={{ fontSize: 12, marginTop: 4 }}>
            {task.due_date && <>{t("tasks.dueDate")} : {formatDateTime(task.due_date, i18n.language)} · </>}
            {task.company_name && <>{task.company_name} · </>}
            {task.assignee_email ?? ""}
          </div>
        </div>
      ))}
    </>
  );
}
