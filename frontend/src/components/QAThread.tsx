import { useCallback, useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

import { qa } from "../api/dealiq";
import type { QAItem } from "../api/types";

export default function QAThread({
  interactionId,
  canAnswer,
}: {
  interactionId: string;
  canAnswer: boolean;
}) {
  const { t } = useTranslation();
  const [items, setItems] = useState<QAItem[]>([]);
  const [question, setQuestion] = useState("");
  const [drafts, setDrafts] = useState<Record<string, string>>({});

  const reload = useCallback(() => {
    void qa.thread(interactionId).then(setItems);
  }, [interactionId]);
  useEffect(() => reload(), [reload]);

  async function ask() {
    if (question.trim().length < 3) return;
    await qa.ask(interactionId, question.trim());
    setQuestion("");
    reload();
  }
  async function answer(id: string) {
    const text = (drafts[id] ?? "").trim();
    if (!text) return;
    await qa.answer(id, text);
    setDrafts({ ...drafts, [id]: "" });
    reload();
  }
  async function close(id: string) {
    await qa.close(id);
    reload();
  }

  return (
    <div style={{ marginTop: 10 }}>
      <strong>{t("qa.thread")}</strong>
      <p className="muted" style={{ fontSize: 12 }}>
        {t("qa.traced")}
      </p>

      {items.length === 0 && <p className="muted">{t("qa.noQuestions")}</p>}

      {items.map((it) => (
        <div
          key={it.id}
          style={{ borderLeft: "3px solid var(--c-border)", paddingLeft: 12, margin: "10px 0" }}
        >
          <div>
            <span className="badge badge--info">{it.status}</span>{" "}
            <span className="muted" style={{ fontSize: 12 }}>
              {new Date(it.created_at).toLocaleString("fr")}
            </span>
          </div>
          <p style={{ margin: "4px 0" }}>
            <strong>Q :</strong> {it.question}
          </p>
          {it.answer ? (
            <p style={{ margin: "4px 0", color: "var(--c-success)" }}>
              <strong>R :</strong> {it.answer}
            </p>
          ) : (
            <p className="muted" style={{ fontSize: 13 }}>
              {t("qa.awaiting")}
            </p>
          )}

          {canAnswer && it.status !== "cloturee" && (
            <div style={{ display: "flex", gap: 8, marginTop: 6 }}>
              <input
                placeholder={t("qa.answerPlaceholder")}
                value={drafts[it.id] ?? ""}
                onChange={(e) => setDrafts({ ...drafts, [it.id]: e.target.value })}
                style={{ flex: 1, padding: 8, borderRadius: 8, border: "1px solid var(--c-border)" }}
              />
              <button className="btn btn--ghost" onClick={() => answer(it.id)}>
                {t("qa.answer")}
              </button>
              <button className="btn btn--ghost" onClick={() => close(it.id)}>
                {t("qa.close")}
              </button>
            </div>
          )}
        </div>
      ))}

      <div style={{ display: "flex", gap: 8, marginTop: 10 }}>
        <input
          placeholder={t("qa.askPlaceholder")}
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          style={{ flex: 1, padding: 8, borderRadius: 8, border: "1px solid var(--c-border)" }}
        />
        <button className="btn" onClick={ask}>
          {t("qa.send")}
        </button>
      </div>
    </div>
  );
}
