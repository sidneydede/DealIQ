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
