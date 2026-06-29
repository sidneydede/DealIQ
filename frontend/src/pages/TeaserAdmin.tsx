import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

import { ApiError } from "../api/client";
import { cockpit, teasers } from "../api/dealiq";
import { useConfirm } from "../components/Confirm";
import { useToast } from "../components/Toast";
import type { CockpitItem, Teaser } from "../api/types";

export default function TeaserAdmin() {
  const { t } = useTranslation();
  const toast = useToast();
  const confirm = useConfirm();
  const [companies, setCompanies] = useState<CockpitItem[]>([]);
  const [companyId, setCompanyId] = useState("");
  const [teaser, setTeaser] = useState<Teaser | null>(null);

  useEffect(() => {
    void cockpit.companies({ only: "investor_ready", limit: 200 }).then((p) => {
      setCompanies(p.items);
      if (p.items[0]) setCompanyId(p.items[0].company_id);
    });
  }, []);

  useEffect(() => {
    if (!companyId) return;
    teasers
      .forCompany(companyId)
      .then(setTeaser)
      .catch((e) => {
        if (e instanceof ApiError) setTeaser(null);
        else throw e;
      });
  }, [companyId]);

  async function generate() {
    try {
      setTeaser(await teasers.generate(companyId));
      toast.success(t("teaserAdmin.generatedOk"));
    } catch (err) {
      toast.error(err instanceof ApiError ? err.message : t("security.error"));
    }
  }
  async function publish() {
    if (!teaser) return;
    // Publier expose le teaser aux investisseurs : on confirme.
    if (!(await confirm({ message: t("teaserAdmin.publishConfirm") }))) return;
    try {
      setTeaser(await teasers.publish(teaser.id));
      toast.success(t("teaserAdmin.publishedOk"));
    } catch (err) {
      toast.error(err instanceof ApiError ? err.message : t("security.error"));
    }
  }

  return (
    <>
      <h1>{t("teaserAdmin.title")}</h1>

      {companies.length === 0 ? (
        <div className="card">
          <p className="muted">{t("teaserAdmin.none")}</p>
        </div>
      ) : (
        <>
          <div className="card">
            <label>
              {t("teaserAdmin.pick")} :{" "}
              <select
                value={companyId}
                onChange={(e) => setCompanyId(e.target.value)}
                style={{ padding: 8, borderRadius: 8, border: "1px solid var(--c-border)" }}
              >
                {companies.map((c) => (
                  <option key={c.company_id} value={c.company_id}>
                    {c.name}
                  </option>
                ))}
              </select>
            </label>{" "}
            <button className="btn" onClick={generate}>
              {teaser ? t("teaserAdmin.regenerate") : t("teaserAdmin.generate")}
            </button>
          </div>

          {teaser && (
            <div className="card">
              <p className="muted">{t("teaserAdmin.anonNote")}</p>
              <h3 style={{ marginTop: 0 }}>{teaser.title}</h3>
              <p>
                <span className="badge badge--info">{teaser.instrument}</span>{" "}
                <span className="badge badge--info">{teaser.zone}</span>{" "}
                {teaser.status === "publie" ? (
                  <span className="badge badge--success">{t("teaserAdmin.published")}</span>
                ) : (
                  <span className="badge badge--warning">{t("teaserAdmin.draft")}</span>
                )}
              </p>
              <p className="muted">
                CA : {teaser.revenue_band} · Montant : {teaser.amount_band}
              </p>
              <p>{teaser.strengths.join(" · ")}</p>
              {teaser.status !== "publie" && (
                <button className="btn btn--gold" onClick={publish}>
                  {t("teaserAdmin.publish")}
                </button>
              )}
            </div>
          )}
        </>
      )}
    </>
  );
}
