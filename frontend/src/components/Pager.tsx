import { useTranslation } from "react-i18next";

interface PagerProps {
  total: number;
  limit: number;
  offset: number;
  onChange: (offset: number) => void;
}

/** Pagination réutilisable : « X–Y sur N » + Précédent / Suivant. */
export default function Pager({ total, limit, offset, onChange }: PagerProps) {
  const { t } = useTranslation();
  if (total <= limit && offset === 0) return null;

  const from = total === 0 ? 0 : offset + 1;
  const to = Math.min(offset + limit, total);
  const canPrev = offset > 0;
  const canNext = offset + limit < total;

  return (
    <div
      style={{
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        gap: 12,
        marginTop: 12,
      }}
    >
      <span className="muted" style={{ fontSize: 13 }}>
        {t("pager.range", { from, to, total })}
      </span>
      <div style={{ display: "flex", gap: 8 }}>
        <button
          className="btn btn--ghost"
          disabled={!canPrev}
          onClick={() => onChange(Math.max(0, offset - limit))}
        >
          {t("pager.prev")}
        </button>
        <button
          className="btn btn--ghost"
          disabled={!canNext}
          onClick={() => onChange(offset + limit)}
        >
          {t("pager.next")}
        </button>
      </div>
    </div>
  );
}
