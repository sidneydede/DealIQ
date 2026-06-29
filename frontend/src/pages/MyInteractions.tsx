import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

import { interactions as api } from "../api/dealiq";
import type { Interaction } from "../api/types";
import QAThread from "../components/QAThread";

export default function MyInteractions() {
  const { t } = useTranslation();
  const [list, setList] = useState<Interaction[]>([]);

  useEffect(() => {
    void api.list().then(setList);
  }, []);

  return (
    <>
      <h1>{t("qa.title")}</h1>
      {list.length === 0 && <p className="muted">{t("qa.empty")}</p>}

      {list.map((it) => (
        <div className="card" key={it.id}>
          <div>
            <span className="badge badge--info">{it.status}</span>{" "}
            <span className="muted" style={{ fontSize: 12 }}>
              {new Date(it.created_at).toLocaleString("fr")}
            </span>
          </div>
          <QAThread interactionId={it.id} canAnswer={false} />
        </div>
      ))}
      <p className="disclaimer">{t("disclaimer")}</p>
    </>
  );
}
