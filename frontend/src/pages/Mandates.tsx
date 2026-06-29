import { useCallback, useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

import { companies as companiesApi, mandates } from "../api/dealiq";
import { ApiError } from "../api/client";
import { useConfirm } from "../components/Confirm";
import { useToast } from "../components/Toast";
import type { Company, Fee, Mandate } from "../api/types";

const PARTIES = ["entreprise", "investisseur", "les_deux"];
const TYPES = ["levee", "cession", "sourcing", "arrangement_dette", "conseil", "autre"];

export default function MandatesPage() {
  const { t } = useTranslation();
  const toast = useToast();
  const confirm = useConfirm();
  const [companies, setCompanies] = useState<Company[]>([]);
  const [companyId, setCompanyId] = useState("");
  const [list, setList] = useState<Mandate[]>([]);
  const [party, setParty] = useState("entreprise");
  const [type, setType] = useState("levee");
  const [exclusive, setExclusive] = useState(false);
  const [fees, setFees] = useState<Record<string, Fee[]>>({});

  useEffect(() => {
    void companiesApi.list().then((l) => {
      setCompanies(l);
      if (l[0]) setCompanyId(l[0].id);
    });
  }, []);

  const reload = useCallback(async () => {
    if (!companyId) return;
    setList(await mandates.forCompany(companyId));
  }, [companyId]);
  useEffect(() => void reload(), [reload]);

  async function create() {
    try {
      await mandates.create(companyId, {
        represented_party: party,
        mandate_type: type,
        exclusive,
      });
      await reload();
      toast.success(t("mandates.createdOk"));
    } catch (err) {
      toast.error(err instanceof ApiError ? err.message : t("security.error"));
    }
  }
  async function sign(id: string) {
    if (!(await confirm({ message: t("mandates.signConfirm") }))) return;
    try {
      await mandates.update(id, { status: "actif", signed: true });
      await reload();
      toast.success(t("mandates.signedOk"));
    } catch (err) {
      toast.error(err instanceof ApiError ? err.message : t("security.error"));
    }
  }
  async function loadFees(id: string) {
    setFees({ ...fees, [id]: await mandates.fees(id) });
  }
  async function addFee(id: string) {
    await mandates.addFee(id, { fee_type: "success_fee" });
    await loadFees(id);
  }
  async function pay(id: string, feeId: string) {
    await mandates.updateFee(feeId, "paye");
    await loadFees(id);
  }

  return (
    <>
      <h1>{t("mandates.title")}</h1>
      <p className="muted" style={{ fontSize: 12 }}>
        {t("mandates.muraille")}
      </p>

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
        <h3 style={{ marginTop: 0 }}>{t("mandates.add")}</h3>
        <div style={{ display: "flex", gap: 10, flexWrap: "wrap", alignItems: "center" }}>
          <label>
            {t("mandates.represented")}{" "}
            <select value={party} onChange={(e) => setParty(e.target.value)}>
              {PARTIES.map((p) => (
                <option key={p} value={p}>
                  {t(`mandates.parties.${p}`)}
                </option>
              ))}
            </select>
          </label>
          <label>
            {t("mandates.type")}{" "}
            <select value={type} onChange={(e) => setType(e.target.value)}>
              {TYPES.map((ty) => (
                <option key={ty} value={ty}>
                  {ty}
                </option>
              ))}
            </select>
          </label>
          <label style={{ display: "flex", gap: 6, alignItems: "center" }}>
            <input
              type="checkbox"
              checked={exclusive}
              onChange={(e) => setExclusive(e.target.checked)}
            />
            {t("mandates.exclusive")}
          </label>
          <button className="btn" onClick={create}>
            {t("mandates.create")}
          </button>
        </div>
      </div>

      {list.map((m) => (
        <div className="card" key={m.id}>
          <div style={{ display: "flex", justifyContent: "space-between" }}>
            <div>
              <strong>{t(`mandates.parties.${m.represented_party}`)}</strong>{" "}
              <span className="badge badge--info">{m.mandate_type}</span>{" "}
              {m.exclusive && <span className="badge badge--info">excl.</span>}{" "}
              {m.signed ? (
                <span className="badge badge--success">{t("mandates.signed")}</span>
              ) : (
                <span className="badge badge--warning">{t("mandates.draft")}</span>
              )}
            </div>
            <div style={{ display: "flex", gap: 8 }}>
              {!m.signed && (
                <button className="btn btn--ghost" onClick={() => sign(m.id)}>
                  {t("mandates.sign")}
                </button>
              )}
              <button className="btn btn--ghost" onClick={() => loadFees(m.id)}>
                {t("mandates.fees")}
              </button>
            </div>
          </div>

          {fees[m.id] && (
            <div style={{ marginTop: 8 }}>
              {fees[m.id].map((f) => (
                <div key={f.id} style={{ display: "flex", justifyContent: "space-between" }}>
                  <span className="num">
                    {t(`mandates.feeTypes.${f.fee_type}`)} · {f.amount ?? "—"} {f.currency} ·{" "}
                    <span className="badge badge--info">{f.status}</span>
                  </span>
                  {f.status !== "paye" && (
                    <button className="btn btn--ghost" onClick={() => pay(m.id, f.id)}>
                      {t("mandates.markPaid")}
                    </button>
                  )}
                </div>
              ))}
              <button className="btn btn--ghost" onClick={() => addFee(m.id)}>
                {t("mandates.addFee")}
              </button>
            </div>
          )}
        </div>
      ))}
    </>
  );
}
