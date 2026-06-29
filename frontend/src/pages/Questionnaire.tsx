import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { Link } from "react-router-dom";

import { meta, onboarding } from "../api/dealiq";
import type { GatingResult, Question } from "../api/types";
import { useMyCompany } from "../hooks/useMyCompany";

export default function Questionnaire() {
  const { t } = useTranslation();
  const { company, loading } = useMyCompany();
  const [questions, setQuestions] = useState<Question[]>([]);
  const [answers, setAnswers] = useState<Record<string, unknown>>({});
  const [step, setStep] = useState(0);
  const [consent, setConsent] = useState(false);
  const [result, setResult] = useState<GatingResult | null>(null);

  const dealType = company?.financing_need?.deal_type_primary ?? null;

  useEffect(() => {
    if (!dealType) return;
    void meta.questionnaire(dealType).then(setQuestions);
  }, [dealType]);

  useEffect(() => {
    if (!company) return;
    void onboarding.get(company.id).then((s) => {
      setAnswers(s.answers ?? {});
      setStep(s.current_step ?? 0);
      setConsent(s.consent_given);
    });
  }, [company]);

  if (loading) return <p className="muted">Chargement…</p>;
  if (!company || !dealType)
    return (
      <>
        <h1>{t("questionnaire.title")}</h1>
        <div className="card">
          <p className="muted">{t("questionnaire.needCompanyType")}</p>
          <Link className="btn btn--ghost" to="/deal-type">
            {t("nav.dealType")}
          </Link>
        </div>
      </>
    );

  const total = questions.length;
  const onConsentStep = step >= total;

  async function persist(nextStep: number, nextAnswers = answers) {
    if (!company) return;
    setStep(nextStep);
    await onboarding.save(company.id, { answers: nextAnswers, current_step: nextStep });
  }

  function setAnswer(id: string, value: unknown) {
    setAnswers((a) => ({ ...a, [id]: value }));
  }

  async function submit() {
    if (!company) return;
    if (consent) await onboarding.consent(company.id, t("questionnaire.consentText"));
    setResult(await onboarding.submit(company.id));
  }

  if (result) {
    return (
      <>
        <h1>{t("questionnaire.resultTitle")}</h1>
        <div className="card">
          <span
            className={`badge badge--${result.eligible ? "success" : "warning"}`}
          >
            {result.route}
          </span>
          <p>{t(`questionnaire.route.${result.route}`)}</p>
          {result.reasons.map((r, i) => (
            <p key={i} className="muted">
              • {r}
            </p>
          ))}
        </div>
        <p className="disclaimer">{t("disclaimer")}</p>
      </>
    );
  }

  const q = questions[step];

  return (
    <>
      <h1>{t("questionnaire.title")}</h1>
      <p className="muted">
        {t("questionnaire.step")} {Math.min(step + 1, total + 1)}/{total + 1} —{" "}
        {t("questionnaire.intro")}
      </p>

      <div className="card" style={{ maxWidth: 560 }}>
        {!onConsentStep && q && (
          <>
            <h2 style={{ marginTop: 0 }}>{q.label}</h2>
            {q.type === "single_choice" ? (
              <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
                {q.options.map((opt) => (
                  <button
                    key={opt}
                    type="button"
                    className="btn btn--ghost"
                    style={{
                      textAlign: "left",
                      borderColor:
                        answers[q.id] === opt ? "var(--c-gold)" : "var(--c-border)",
                    }}
                    onClick={() => setAnswer(q.id, opt)}
                  >
                    {opt}
                  </button>
                ))}
              </div>
            ) : (
              <input
                type={q.type === "number" ? "number" : "text"}
                value={(answers[q.id] as string) ?? ""}
                onChange={(e) =>
                  setAnswer(
                    q.id,
                    q.type === "number" ? Number(e.target.value) : e.target.value,
                  )
                }
              />
            )}
          </>
        )}

        {onConsentStep && (
          <>
            <h2 style={{ marginTop: 0 }}>{t("questionnaire.consentTitle")}</h2>
            <p className="muted">{t("questionnaire.consentText")}</p>
            <label style={{ display: "flex", gap: 8, alignItems: "center" }}>
              <input
                type="checkbox"
                checked={consent}
                onChange={(e) => setConsent(e.target.checked)}
              />
              {t("questionnaire.consentCheck")}
            </label>
          </>
        )}

        <div style={{ display: "flex", gap: 10, marginTop: 18 }}>
          {step > 0 && (
            <button className="btn btn--ghost" onClick={() => persist(step - 1)}>
              {t("questionnaire.back")}
            </button>
          )}
          {!onConsentStep ? (
            <button className="btn" onClick={() => persist(step + 1)}>
              {t("questionnaire.next")}
            </button>
          ) : (
            <button className="btn btn--gold" disabled={!consent} onClick={submit}>
              {t("questionnaire.submit")}
            </button>
          )}
        </div>
      </div>
      <p className="disclaimer">{t("disclaimer")}</p>
    </>
  );
}
