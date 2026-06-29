import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

import { ApiError } from "../api/client";
import { companies as companiesApi, dd } from "../api/dealiq";
import type { Company, DdAnalysis } from "../api/types";

const SAMPLE = `701000;Ventes;1000000
601000;Achats;400000
681000;Dotations;100000
164000;Emprunts;300000
521000;Banque;50000
311000;Stocks;200000
411000;Clients;150000
401000;Fournisseurs;120000`;

function parseLines(text: string) {
  return text
    .split("\n")
    .map((l) => l.trim())
    .filter(Boolean)
    .map((l) => {
      const parts = l.split(";").map((p) => p.trim());
      if (parts.length >= 3)
        return { account: parts[0], label: parts[1], amount: Number(parts[2]) || 0 };
      return { account: parts[0], amount: Number(parts[1]) || 0 };
    });
}

export default function Dd() {
  const { t } = useTranslation();
  const [companies, setCompanies] = useState<Company[]>([]);
  const [companyId, setCompanyId] = useState("");
  const [text, setText] = useState(SAMPLE);
  const [analysis, setAnalysis] = useState<DdAnalysis | null>(null);
  const [msg, setMsg] = useState<string | null>(null);

  useEffect(() => {
    void companiesApi.list().then((l) => {
      setCompanies(l);
      if (l[0]) setCompanyId(l[0].id);
    });
  }, []);

  async function importBalance() {
    setMsg(null);
    const r = (await dd.importBalance(companyId, parseLines(text))) as { version: number };
    setMsg(`${t("dd.imported")} ${r.version})`);
  }
  async function compute() {
    setMsg(null);
    try {
      setAnalysis(await dd.compute(companyId));
    } catch (e) {
      setMsg(e instanceof ApiError ? e.message : "Erreur");
    }
  }

  return (
    <>
      <h1>{t("dd.title")}</h1>

      <div className="card">
        <select
          value={companyId}
          onChange={(e) => setCompanyId(e.target.value)}
          style={{ padding: 8, borderRadius: 8, border: "1px solid var(--c-border)" }}
        >
          {companies.map((c) => (
            <option key={c.id} value={c.id}>
              {c.name}
            </option>
          ))}
        </select>
      </div>

      <div className="card">
        <label className="muted">{t("dd.balanceLabel")}</label>
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          rows={9}
          style={{
            width: "100%", fontFamily: "monospace", fontSize: 13, padding: 10,
            borderRadius: 8, border: "1px solid var(--c-border)", marginTop: 6,
          }}
        />
        <div style={{ display: "flex", gap: 8, marginTop: 8 }}>
          <button className="btn btn--ghost" onClick={importBalance}>
            {t("dd.import")}
          </button>
          <button className="btn" onClick={compute}>
            {t("dd.compute")}
          </button>
        </div>
        {msg && <p className="muted">{msg}</p>}
      </div>

      {analysis && (
        <>
          <div className="card">
            <h3 style={{ marginTop: 0 }}>{t("dd.synthesis")}</h3>
            <p>{analysis.synthesis}</p>
            <p className="muted" style={{ fontSize: 12 }}>
              {analysis.grid_version} · {analysis.deal_type}
            </p>
          </div>

          <div className="card">
            <h3 style={{ marginTop: 0 }}>{t("dd.retraitements")}</h3>
            {Object.entries(analysis.retraitements).map(([key, r]) => (
              <div key={key} style={{ marginBottom: 8 }}>
                <strong>{t(`dd.labels.${key}`)}</strong> :{" "}
                <span className="num">{r.value.toLocaleString("fr")}</span>
                <div className="muted" style={{ fontSize: 12 }}>
                  {t("dd.rule")} : {r.rule} · {t("dd.sources")} : {r.sources.join(", ")}
                </div>
              </div>
            ))}
          </div>

          <div className="card">
            <h3 style={{ marginTop: 0 }}>{t("dd.focus")}</h3>
            <ul>
              {analysis.focus.map((f, i) => (
                <li key={i}>{f}</li>
              ))}
            </ul>
          </div>
        </>
      )}
    </>
  );
}
