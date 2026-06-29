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
