import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

import { scoringAdmin } from "../api/dealiq";
import { ApiError } from "../api/client";
import { useToast } from "../components/Toast";
import type { ScoringConfig, SimulateResult } from "../api/types";

const DIMENSIONS = [
  "traction",
  "profitabilite_cashflow",
  "qualite_info_financiere",
  "clarte_besoin",
  "gouvernance",
  "qualite_documentaire",
  "scalabilite_marche",
  "esg",
];
const THRESHOLD_KEYS = ["investor_ready_min", "early_precoce_max", "precoce_floor"] as const;
const STAGES = ["", "idee", "amorcage", "early", "croissance", "mature"];

export default function ScoringCalibration() {
  const { t } = useTranslation();
  const toast = useToast();
  const [config, setConfig] = useState<ScoringConfig | null>(null);
  const [thresholds, setThresholds] = useState<Record<string, number>>({});
  const [version, setVersion] = useState("");
  const [saved, setSaved] = useState(false);

  const [signals, setSignals] = useState<Record<string, number>>(
    Object.fromEntries(DIMENSIONS.map((d) => [d, 0.5])),
  );
  const [verified, setVerified] = useState(false);
  const [stage, setStage] = useState("");
  const [result, setResult] = useState<SimulateResult | null>(null);

  useEffect(() => {
    void scoringAdmin.getConfig().then((c) => {
      setConfig(c);
      setThresholds(c.thresholds);
      setVersion(c.version);
    });
  }, []);

  async function save() {
    try {
      const c = await scoringAdmin.updateConfig({ thresholds, version });
      setConfig(c);
      setSaved(true);
      toast.success(t("scoring.saved"));
    } catch (err) {
      toast.error(err instanceof ApiError ? err.message : t("security.error"));
    }
  }

  async function simulate() {
    setResult(
      await scoringAdmin.simulate({
        signals,
        has_verified_financials: verified,
        stage: stage || undefined,
        config_override: { thresholds },
      }),
    );
  }

  if (!config) return <p className="muted">Chargement…</p>;

  return (
    <>
      <h1>{t("scoring.title")}</h1>
      <p className="muted">{t("scoring.intro")}</p>

      <div className="card" style={{ maxWidth: 520 }}>
        <h3 style={{ marginTop: 0 }}>{t("scoring.thresholds")}</h3>
        {THRESHOLD_KEYS.map((k) => (
          <div className="field" key={k}>
            <label>{t(`scoring.${k}`)}</label>
            <input
              type="number"
              value={thresholds[k] ?? 0}
              onChange={(e) => setThresholds({ ...thresholds, [k]: Number(e.target.value) })}
            />
          </div>
        ))}
        <div className="field">
          <label>{t("scoring.version")}</label>
          <input value={version} onChange={(e) => setVersion(e.target.value)} />
        </div>
        <button className="btn" onClick={save}>
          {t("scoring.save")}
        </button>
        {saved && <span className="badge badge--success" style={{ marginLeft: 8 }}>✓</span>}
      </div>

      <div className="card">
        <h3 style={{ marginTop: 0 }}>{t("scoring.dealTypeWeights")}</h3>
        {Object.entries(config.deal_type_weights).map(([dt, w]) => (
          <p key={dt} className="muted" style={{ fontSize: 12, margin: "4px 0" }}>
            <strong>{dt}</strong> : {JSON.stringify(w)}
          </p>
        ))}
      </div>

      <div className="card">
        <h3 style={{ marginTop: 0 }}>{t("scoring.simulator")}</h3>
        <p className="muted" style={{ fontSize: 12 }}>
          {t("scoring.withDraft")}
        </p>
        {DIMENSIONS.map((d) => (
          <div key={d} style={{ display: "flex", alignItems: "center", gap: 10 }}>
            <label style={{ flex: 1, fontSize: 13 }}>{d}</label>
            <input
              type="range"
              min={0}
              max={1}
              step={0.1}
              value={signals[d]}
              onChange={(e) => setSignals({ ...signals, [d]: Number(e.target.value) })}
            />
            <span className="num" style={{ width: 32 }}>
              {signals[d].toFixed(1)}
            </span>
          </div>
        ))}
        <div style={{ display: "flex", gap: 16, alignItems: "center", marginTop: 10 }}>
          <label style={{ display: "flex", gap: 6, alignItems: "center" }}>
            <input type="checkbox" checked={verified} onChange={(e) => setVerified(e.target.checked)} />
            {t("scoring.verified")}
          </label>
          <label>
            {t("scoring.stage")}{" "}
            <select value={stage} onChange={(e) => setStage(e.target.value)}>
              {STAGES.map((s) => (
                <option key={s} value={s}>
                  {s || "—"}
                </option>
              ))}
            </select>
          </label>
          <button className="btn btn--gold" onClick={simulate}>
            {t("scoring.run")}
          </button>
        </div>

        {result && (
          <div className="card" style={{ background: "var(--c-bg)", marginTop: 12 }}>
            <p>
              {t("scoring.category")} :{" "}
              <strong>{result.category}</strong> · {t("scoring.total")}{" "}
              <span className="num">{result.total}</span> · {t("scoring.confidence")}{" "}
              <span className="num">{Math.round(result.confidence * 100)}%</span>
            </p>
            {result.gaps.length > 0 && (
              <ul className="muted" style={{ marginBottom: 0 }}>
                {result.gaps.map((g, i) => (
                  <li key={i}>{g}</li>
                ))}
              </ul>
            )}
          </div>
        )}
      </div>
    </>
  );
}
