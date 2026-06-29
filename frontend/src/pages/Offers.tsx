import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

import { offers as offersApi } from "../api/dealiq";
import { ApiError } from "../api/client";
import Loading from "../components/Loading";
import { useToast } from "../components/Toast";
import type { OffersResponse } from "../api/types";
import { useMyCompany } from "../hooks/useMyCompany";

export default function Offers() {
  const { t } = useTranslation();
  const toast = useToast();
  const { company } = useMyCompany();
  const [data, setData] = useState<OffersResponse | null>(null);
  const [openKey, setOpenKey] = useState<string | null>(null);
  const [phone, setPhone] = useState("");
  const [message, setMessage] = useState("");
  const [sent, setSent] = useState(false);

  useEffect(() => {
    offersApi.list().then(setData);
  }, []);

  async function submit(offerKey: string) {
    if (!company) return;
    try {
      await offersApi.requestQuote(company.id, {
        offer_key: offerKey,
        contact_phone: phone || undefined,
        message: message || undefined,
      });
      setSent(true);
      setOpenKey(null);
      toast.success(t("offers.quoteSent"));
    } catch (err) {
      toast.error(err instanceof ApiError ? err.message : t("security.error"));
    }
  }

  if (!data) return <Loading />;

  return (
    <>
      <h1>{t("offers.title")}</h1>
      <p className="muted">{t("offers.intro")}</p>

      {sent && <div className="card" style={{ borderColor: "var(--c-success)" }}>
        <span className="badge badge--success">✓</span> {t("offers.quoteSent")}
      </div>}

      {data.offers.map((o) => (
        <div className="card" key={o.key}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <strong>{o.label}</strong>
            {/* Aucun prix affiché — uniquement la logique tarifaire (RG-M7-01/05) */}
            <span className="badge badge--info">{t(`offers.pricing.${o.pricing}`)}</span>
          </div>
          <p className="muted" style={{ marginBottom: 6 }}>
            {t("offers.deliverables")} :
          </p>
          <ul className="muted" style={{ marginTop: 0 }}>
            {o.deliverables.map((d, i) => (
              <li key={i}>{d}</li>
            ))}
          </ul>

          {company && o.pricing !== "gratuit" && (
            openKey === o.key ? (
              <div style={{ marginTop: 10 }}>
                <div className="field">
                  <label>{t("offers.phone")}</label>
                  <input value={phone} onChange={(e) => setPhone(e.target.value)} />
                </div>
                <div className="field">
                  <label>{t("offers.message")}</label>
                  <input value={message} onChange={(e) => setMessage(e.target.value)} />
                </div>
                <button className="btn btn--gold" onClick={() => submit(o.key)}>
                  {t("offers.send")}
                </button>
              </div>
            ) : (
              <button className="btn" onClick={() => { setOpenKey(o.key); setSent(false); }}>
                {t("offers.requestQuote")}
              </button>
            )
          )}
        </div>
      ))}

      <div className="card" style={{ background: "var(--c-bg)" }}>
        <p className="muted" style={{ margin: 0 }}>
          {data.anti_pay_to_play}
        </p>
      </div>
      <p className="disclaimer">{t("disclaimer")}</p>
    </>
  );
}
