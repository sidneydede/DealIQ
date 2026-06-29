/** Formatage date/heure/montant — centralisé pour un rendu cohérent et localisé. */

/** Horodatage relatif (« il y a 2 j », « 3 min ago »). */
export function formatRelative(iso: string, lang = "fr"): string {
  const then = new Date(iso).getTime();
  if (Number.isNaN(then)) return "";
  const diffSec = Math.round((Date.now() - then) / 1000);
  const rtf = new Intl.RelativeTimeFormat(lang || "fr", { numeric: "auto" });
  const abs = Math.abs(diffSec);
  const steps: [number, Intl.RelativeTimeFormatUnit][] = [
    [60, "second"],
    [3600, "minute"],
    [86400, "hour"],
    [2592000, "day"],
    [31536000, "month"],
    [Infinity, "year"],
  ];
  const divisors: Record<string, number> = {
    second: 1,
    minute: 60,
    hour: 3600,
    day: 86400,
    month: 2592000,
    year: 31536000,
  };
  for (const [limit, unit] of steps) {
    if (abs < limit) return rtf.format(-Math.round(diffSec / divisors[unit]), unit);
  }
  return rtf.format(-Math.round(diffSec / divisors.year), "year");
}

/** Date/heure absolue localisée. */
export function formatDateTime(iso: string, lang = "fr"): string {
  const d = new Date(iso);
  return Number.isNaN(d.getTime()) ? "" : d.toLocaleString(lang || "fr");
}

/** Montant formaté en devise (XOF/XAF/EUR/USD), sans décimales. */
export function formatMoney(
  amount: number | null | undefined,
  currency = "XOF",
  lang = "fr",
): string {
  if (amount == null) return "—";
  try {
    return new Intl.NumberFormat(lang || "fr", {
      style: "currency",
      currency,
      maximumFractionDigits: 0,
    }).format(amount);
  } catch {
    return `${amount.toLocaleString(lang || "fr")} ${currency}`;
  }
}
