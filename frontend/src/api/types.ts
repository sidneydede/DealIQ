export interface DealTypeMeta {
  code: string;
  label: string;
  description: string | null;
  instruments: string[];
  target_financiers: string | null;
}

export interface CountryMeta {
  code: string;
  label: string;
  zone: string;
  currency: string;
}

export interface FinancingNeed {
  amount: number | null;
  currency: string;
  use_of_funds: string | null;
  horizon: string | null;
  deal_type_primary: string | null;
  deal_type_secondary: string | null;
}

export interface Company {
  id: string;
  name: string;
  country: string;
  sector: string;
  rccm: string | null;
  stage: string | null;
  status: string;
  revenue_min: number | null;
  revenue_max: number | null;
  currency: string;
  financials_reliability: string;
  owner_id: string | null;
  financing_need: FinancingNeed | null;
}

export interface DuplicateMatch {
  id: string;
  name: string;
  rccm: string | null;
  reason: string;
}

export interface CompanyCreateResult {
  company: Company;
  duplicate_warnings: DuplicateMatch[];
}

export interface Question {
  id: string;
  label: string;
  type: "single_choice" | "number" | "text";
  options: string[];
  required: boolean;
}

export interface OnboardingSession {
  company_id: string;
  answers: Record<string, unknown>;
  current_step: number;
  completed: boolean;
  consent_given: boolean;
  consent_at: string | null;
  gating_route: string | null;
}

export interface GatingResult {
  eligible: boolean;
  route: "pipeline" | "nurturing" | "orientation_cabinet";
  reasons: string[];
}

export interface DocumentOut {
  id: string;
  company_id: string;
  doc_type: string;
  filename: string;
  content_type: string | null;
  size_bytes: number | null;
  sha256: string | null;
  version: number;
  status: "recu" | "verifie" | "rejete";
  created_at: string;
}

export interface ChecklistItem {
  doc_type: string;
  required: boolean;
  received: boolean;
  verified: boolean;
  documents: DocumentOut[];
}

export interface ReadinessScore {
  category: string | null;
  confidence: number | null;
  gaps: string[];
  provisional?: boolean;
}

export interface Report {
  company_name: string;
  category: string | null;
  category_label: string;
  confidence: number | null;
  deal_type: string | null;
  recommended_instrument: string;
  blockers: string[];
  path_to_bankable: string[];
  alternative_suggestion: string | null;
  recommended_services: string[];
  disclaimers: string[];
}

export interface Offer {
  key: string;
  label: string;
  pricing: "gratuit" | "ticket_engagement" | "sur_devis";
  deliverables: string[];
}

export interface OffersResponse {
  offers: Offer[];
  anti_pay_to_play: string;
}

export interface QuoteRequest {
  id: string;
  company_id: string;
  offer_key: string | null;
  deal_type: string | null;
  message: string | null;
  contact_phone: string | null;
  status: string;
  created_at: string;
}

export interface DealTypeHistoryEntry {
  id: string;
  old_primary: string | null;
  new_primary: string | null;
  old_secondary: string | null;
  new_secondary: string | null;
  source: "entrepreneur" | "cabinet";
  actor_id: string | null;
  motif: string | null;
  created_at: string;
}
