import { useEffect, useState, type FormEvent } from "react";
import { useTranslation } from "react-i18next";

import { investors } from "../api/dealiq";
import type { Investor } from "../api/types";

const TYPES = [
  "equity_pe_vc",
  "dette_mezzanine",
  "dfi",
  "family_office",
  "corporate",
  "banque",
];

export default function Investors() {
  const { t } = useTranslation();
  const [list, setList] = useState<Investor[]>([]);
  const [name, setName] = useState("");
  const [type, setType] = useState(TYPES[0]);
  const [email, setEmail] = useState("");

  async function reload() {
    setList(await investors.list());
  }
  useEffect(() => {
    void reload();
  }, []);

  async function onCreate(e: FormEvent) {
    e.preventDefault();
    await investors.create({ name, type, user_email: email || undefined });
    setName("");
    setEmail("");
    await reload();
  }

  return (
    <>
      <h1>{t("investors.title")}</h1>

      <form className="card" onSubmit={onCreate} style={{ maxWidth: 560 }}>
        <h3 style={{ marginTop: 0 }}>{t("investors.add")}</h3>
        <div className="field">
          <label>{t("investors.name")}</label>
          <input required value={name} onChange={(e) => setName(e.target.value)} />
        </div>
        <div className="field">
          <label>{t("investors.type")}</label>
          <select
            value={type}
            onChange={(e) => setType(e.target.value)}
            style={{ padding: 10, borderRadius: 8, border: "1px solid var(--c-border)" }}
          >
            {TYPES.map((ty) => (
              <option key={ty} value={ty}>
                {ty}
              </option>
            ))}
          </select>
        </div>
        <div className="field">
          <label>{t("investors.linkEmail")}</label>
          <input value={email} onChange={(e) => setEmail(e.target.value)} />
        </div>
        <button className="btn" type="submit">
          {t("investors.create")}
        </button>
      </form>

      {list.map((inv) => (
        <div className="card" key={inv.id}>
          <strong>{inv.name}</strong>{" "}
          <span className="badge badge--info">{inv.type}</span>{" "}
          <span className="badge badge--info">{inv.qualif_status}</span>{" "}
          {inv.criteria ? (
            <span className="badge badge--success">{t("investors.criteriaSet")}</span>
          ) : (
            <span className="badge badge--warning">{t("investors.noCriteria")}</span>
          )}
        </div>
      ))}
    </>
  );
}
