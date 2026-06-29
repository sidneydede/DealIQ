import { useTranslation } from "react-i18next";

/** État de chargement cohérent dans toute l'application. */
export default function Loading() {
  const { t } = useTranslation();
  return (
    <p className="muted" role="status" aria-live="polite">
      {t("common.loading")}
    </p>
  );
}
