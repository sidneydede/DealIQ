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

export interface CockpitItem {
  company_id: string;
  name: string;
  country: string;
  sector: string;
  status: string;
  deal_type_primary: string | null;
  readiness_category: string | null;
  score_total: number | null;
  quote_requests: number;
  days_open: number;
  sla_breach: boolean;
}

export interface DashboardData {
  users_total: number;
  companies_total: number;
  onboarding_started: number;
  onboarding_completed: number;
  completion_rate: number;
  quote_requests_total: number;
  conversion_rate: number;
  by_deal_type: Record<string, number>;
  by_readiness_category: Record<string, number>;
  companies_by_status: Record<string, number>;
}

export interface AuditLogEntry {
  id: string;
  actor_id: string | null;
  actor_email: string | null;
  action: string;
  object_type: string | null;
  object_id: string | null;
  meta: Record<string, unknown>;
  ip_address: string | null;
  created_at: string;
}

export interface Criteria {
  countries: string[];
  sectors: string[];
  instruments: string[];
  deal_types: string[];
  stages: string[];
  exclusions: string[];
  ticket_min: number | null;
  ticket_max: number | null;
  ticket_currency: string;
  esg_required: boolean;
}

export interface Investor {
  id: string;
  name: string;
  type: string;
  jurisdiction: string | null;
  team: string | null;
  qualif_status: string;
  user_id: string | null;
  criteria: Criteria | null;
}

export interface MatchResult {
  investor_id: string;
  investor_name: string;
  investor_type: string;
  passes_hard_filters: boolean;
  fit_score: number;
  reasons: string[];
}

export interface TeaserPublic {
  id: string;
  deal_type: string | null;
  title: string;
  sector: string;
  zone: string | null;
  revenue_band: string | null;
  amount_band: string | null;
  instrument: string | null;
  strengths: string[];
  summary: string | null;
}

export interface Teaser extends TeaserPublic {
  company_id: string;
  version: number;
  status: string;
  created_at: string;
}

export interface Interaction {
  id: string;
  teaser_id: string;
  company_id: string;
  investor_id: string;
  status: string;
  note: string | null;
  created_at: string;
}

export interface QAItem {
  id: string;
  interaction_id: string;
  asked_by: string | null;
  question: string;
  answer: string | null;
  answered_by: string | null;
  status: string;
  created_at: string;
  updated_at: string;
}

export interface KycCheck {
  id: string;
  subject_type: string;
  subject_id: string;
  subject_label: string | null;
  check_type: string;
  status: string;
  provider: string | null;
  result: Record<string, unknown>;
  notes: string | null;
  checked_by: string | null;
  created_at: string;
}

export interface DataRoom {
  id: string;
  company_id: string;
  provider_ref: string | null;
  status: string;
  created_at: string;
}

export interface DataRoomDocument {
  id: string;
  document_id: string;
  filename: string;
  doc_type: string;
  status: string;
}

export interface DataRoomAccess {
  id: string;
  investor_id: string;
  investor_name: string | null;
  granted_by: string | null;
  expires_at: string | null;
  revoked: boolean;
  created_at: string;
}

export interface DataRoomLog {
  id: string;
  document_id: string | null;
  investor_id: string | null;
  actor_id: string | null;
  action: string;
  created_at: string;
}

export interface DocumentView {
  document_id: string;
  filename: string;
  watermark: string;
  view_url: string;
  note: string;
}

export interface Deal {
  id: string;
  company_id: string;
  company_name: string | null;
  investor_id: string;
  investor_name: string | null;
  interaction_id: string | null;
  deal_type: string | null;
  stage: string;
  owner_id: string | null;
  created_at: string;
}

export interface DealMilestone {
  id: string;
  label: string;
  position: number;
  done: boolean;
}

export interface DealStageHistory {
  id: string;
  old_stage: string | null;
  new_stage: string;
  actor_id: string | null;
  note: string | null;
  created_at: string;
}

export interface DealDetail extends Deal {
  milestones: DealMilestone[];
  history: DealStageHistory[];
}

export interface Mandate {
  id: string;
  company_id: string;
  deal_id: string | null;
  represented_party: string;
  mandate_type: string;
  exclusive: boolean;
  duration_months: number | null;
  scope: string | null;
  status: string;
  signed: boolean;
  created_at: string;
}

export interface Fee {
  id: string;
  mandate_id: string;
  fee_type: string;
  amount: number | null;
  currency: string;
  due_date: string | null;
  status: string;
  note: string | null;
}

export interface ConflictItem {
  company_id: string;
  company_name: string | null;
  represented_parties: string[];
  has_conflict: boolean;
  disclosure: string | null;
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
