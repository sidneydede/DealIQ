// Listes de référence pour les formulaires (alignées sur le backend / seed).

export const STAGES = [
  { value: "idee", label: "Idée" },
  { value: "mvp", label: "MVP" },
  { value: "traction", label: "Traction" },
  { value: "scale", label: "Scale" },
];

export const DECK_STATUSES = [
  { value: "", label: "—" },
  { value: "oui", label: "Oui" },
  { value: "non", label: "Non" },
  { value: "en_attente", label: "En attente" },
];

export const DEAL_SOURCES = [
  { value: "", label: "—" },
  { value: "event", label: "Événement" },
  { value: "whatsapp", label: "WhatsApp pro" },
  { value: "recommendation", label: "Recommandation" },
  { value: "cold_inbound", label: "Cold inbound" },
  { value: "autre", label: "Autre" },
];

export const SECTORS = [
  "Fintech", "Agritech", "E-commerce", "Edtech", "Healthtech",
  "Logistique / Mobilité", "Energie / Cleantech", "SaaS B2B",
  "Marketplace", "Médias / Divertissement", "Insurtech", "Autre",
];

export const COUNTRIES = [
  { iso2: "CI", name: "Côte d'Ivoire" },
  { iso2: "SN", name: "Sénégal" },
  { iso2: "BJ", name: "Bénin" },
  { iso2: "BF", name: "Burkina Faso" },
  { iso2: "ML", name: "Mali" },
  { iso2: "NE", name: "Niger" },
  { iso2: "TG", name: "Togo" },
  { iso2: "GW", name: "Guinée-Bissau" },
  { iso2: "GH", name: "Ghana" },
  { iso2: "NG", name: "Nigeria" },
  { iso2: "GN", name: "Guinée" },
];

export const NETWORKS = [
  { key: "x_twitter", label: "X / Twitter", placeholder: "@handle ou URL" },
  { key: "linkedin_company", label: "LinkedIn entreprise", placeholder: "URL page entreprise" },
  { key: "linkedin_founder", label: "LinkedIn fondateur", placeholder: "URL profil" },
  { key: "facebook", label: "Facebook", placeholder: "URL page publique" },
  { key: "instagram", label: "Instagram", placeholder: "@handle ou URL" },
];

export function scoreColor(score) {
  if (score <= 30) return "#c0392b";
  if (score <= 60) return "#e67e22";
  if (score <= 85) return "#2980b9";
  return "#27ae60";
}
