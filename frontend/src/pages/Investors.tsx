import { useCallback, useEffect, useState, type FormEvent } from "react";
import { useTranslation } from "react-i18next";

import { investors } from "../api/dealiq";
import { ApiError } from "../api/client";
import Pager from "../components/Pager";
import type { Investor } from "../api/types";

const LIMIT = 25;

const TYPES = [
  "equity_pe_vc",
  "dette_mezzanine",
  "dfi",
  "family_office",
  "corporate",
  "banque",
];

function InviteRow({ inv, onDone }: { inv: Investor; onDone: () => void }) {
  const { t } = useTranslation();
  const [email, setEmail] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [temp, setTemp] = useState<string | null>(null);
  const [done, setDone] = useState(false);

  async function onInvite(e: FormEvent) {
    e.preventDefault();
    setError(null);
    setTemp(null);
    try {
      const res = await investors.invite(inv.id, email || undefined);
      setDone(true);
      if (res.temporary_password) setTemp(res.temporary_password);
      onDone();
    } catch (err) {
      setError(err instanceof ApiError ? err.message : t("investors.inviteError"));
    }
  }

  return (
    <form onSubmit={onInvite} style={{ marginTop: 8, display: "flex", gap: 8, flexWrap: "wrap" }}>
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder={t("investors.inviteEmail")}
        // Optionnel si un compte est déjà rattaché (ré-invitation).
        required={!inv.user_id}
        style={{ padding: 8, borderRadius: 8, border: "1px solid var(--c-border)", minWidth: 220 }}
      />
      <button className="btn btn--ghost" type="submit">
        {inv.user_id ? t("investors.reinvite") : t("investors.invite")}
      </button>
      {done && !temp && <span className="badge badge--success">{t("investors.inviteSent")}</span>}
      {error && <span className="badge badge--warning">{error}</span>}
      {temp && (
        <span className="muted" style={{ width: "100%" }}>
          {t("investors.tempPassword")} : <code style={{ fontWeight: 700 }}>{temp}</code>
        </span>
      )}
    </form>
  );
}

export default function Investors() {
  const { t } = useTranslation();
  const [list, setList] = useState<Investor[]>([]);
  const [total, setTotal] = useState(0);
  const [offset, setOffset] = useState(0);
  const [name, setName] = useState("");
  const [type, setType] = useState(TYPES[0]);
  const [email, setEmail] = useState("");
  const [query, setQuery] = useState("");
  const [search, setSearch] = useState("");
  const [typeFilter, setTypeFilter] = useState("");
  const [qualifFilter, setQualifFilter] = useState("");

  const filterParams = {
    q: search || undefined,
    type_filter: typeFilter || undefined,
    qualif_status: qualifFilter || undefined,
  };

  const reload = useCallback(async () => {
    const p = await investors.list({ ...filterParams, limit: LIMIT, offset });
    setList(p.items);
    setTotal(p.total);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [search, typeFilter, qualifFilter, offset]);

  useEffect(() => {
    const id = setTimeout(() => setSearch(query.trim()), 300);
    return () => clearTimeout(id);
  }, [query]);

  useEffect(() => {
    setOffset(0);
  }, [search, typeFilter, qualifFilter]);

  useEffect(() => {
    void reload();
  }, [reload]);

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

      <div
        style={{
          display: "flex",
          gap: 8,
          alignItems: "center",
          flexWrap: "wrap",
          margin: "8px 0 4px",
        }}
      >
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder={t("investors.searchPlaceholder")}
          aria-label={t("investors.searchPlaceholder")}
          style={{
            flex: 1,
            minWidth: 200,
            maxWidth: 360,
            padding: "8px 10px",
            borderRadius: 8,
            border: "1px solid var(--c-border)",
          }}
        />
        <select
          value={typeFilter}
          onChange={(e) => setTypeFilter(e.target.value)}
          aria-label={t("investors.type")}
          style={{ padding: 8, borderRadius: 8, border: "1px solid var(--c-border)" }}
        >
          <option value="">{t("investors.allTypes")}</option>
          {TYPES.map((ty) => (
            <option key={ty} value={ty}>
              {ty}
            </option>
          ))}
        </select>
        <select
          value={qualifFilter}
          onChange={(e) => setQualifFilter(e.target.value)}
          aria-label={t("investors.qualifStatus")}
          style={{ padding: 8, borderRadius: 8, border: "1px solid var(--c-border)" }}
        >
          <option value="">{t("investors.allStatuses")}</option>
          {["prospect", "qualifie", "actif", "inactif"].map((s) => (
            <option key={s} value={s}>
              {s}
            </option>
          ))}
        </select>
        <button className="btn btn--ghost" onClick={() => void investors.exportCsv(filterParams)}>
          {t("investors.exportCsv")}
        </button>
      </div>

      {list.map((inv) => (
        <div className="card" key={inv.id}>
          <strong>{inv.name}</strong>{" "}
          <span className="badge badge--info">{inv.type}</span>{" "}
          <span className="badge badge--info">{inv.qualif_status}</span>{" "}
          {inv.user_id ? (
            <span className="badge badge--success">{t("investors.linked")}</span>
          ) : (
            <span className="badge badge--warning">{t("investors.notLinked")}</span>
          )}{" "}
          {inv.criteria ? (
            <span className="badge badge--success">{t("investors.criteriaSet")}</span>
          ) : (
            <span className="badge badge--warning">{t("investors.noCriteria")}</span>
          )}
          <InviteRow inv={inv} onDone={() => void reload()} />
        </div>
      ))}

      <Pager total={total} limit={LIMIT} offset={offset} onChange={setOffset} />
    </>
  );
}
