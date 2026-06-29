import { api } from "./client";
import type {
  AuditLogEntry,
  ChecklistItem,
  CockpitItem,
  Company,
  CompanyCreateResult,
  CountryMeta,
  Criteria,
  DashboardData,
  DealTypeHistoryEntry,
  DealTypeMeta,
  DocumentOut,
  FinancingNeed,
  GatingResult,
  Investor,
  MatchResult,
  OffersResponse,
  OnboardingSession,
  Question,
  QuoteRequest,
  ReadinessScore,
  Report,
} from "./types";

export const meta = {
  dealTypes: () => api.get<DealTypeMeta[]>("/meta/deal-types"),
  countries: () => api.get<CountryMeta[]>("/meta/countries"),
  questionnaire: (dealType: string) =>
    api.get<Question[]>(`/meta/questionnaire/${dealType}`),
};

export const onboarding = {
  get: (id: string) => api.get<OnboardingSession>(`/companies/${id}/questionnaire`),
  save: (id: string, body: { answers: Record<string, unknown>; current_step: number }) =>
    api.put<OnboardingSession>(`/companies/${id}/questionnaire`, body),
  consent: (id: string, consent_text: string) =>
    api.post<OnboardingSession>(`/companies/${id}/questionnaire/consent`, { consent_text }),
  submit: (id: string) => api.post<GatingResult>(`/companies/${id}/questionnaire/submit`),
};

export const documents = {
  list: (id: string) => api.get<DocumentOut[]>(`/companies/${id}/documents`),
  checklist: (id: string) => api.get<ChecklistItem[]>(`/companies/${id}/documents/checklist`),
  upload: (id: string, docType: string, file: File) => {
    const form = new FormData();
    form.append("doc_type", docType);
    form.append("file", file);
    return api.upload<DocumentOut>(`/companies/${id}/documents`, form);
  },
};

export const readiness = {
  compute: (id: string) => api.post<ReadinessScore>(`/companies/${id}/score`),
  get: (id: string) => api.get<ReadinessScore>(`/companies/${id}/score`),
};

export const report = {
  get: (id: string) => api.get<Report>(`/companies/${id}/report`),
};

export const offers = {
  list: () => api.get<OffersResponse>("/meta/offers"),
  requestQuote: (
    id: string,
    body: { offer_key?: string | null; message?: string; contact_phone?: string },
  ) => api.post<QuoteRequest>(`/companies/${id}/quote-request`, body),
};

export const cockpit = {
  companies: (params: { deal_type?: string; status_filter?: string; only?: string } = {}) => {
    const qs = new URLSearchParams(params as Record<string, string>).toString();
    return api.get<CockpitItem[]>(`/cockpit/companies${qs ? `?${qs}` : ""}`);
  },
  pipeline: () => api.get<Record<string, number>>("/cockpit/pipeline"),
  setQuoteStatus: (quoteId: string, statusValue: string) =>
    api.patch<QuoteRequest>(`/quote-requests/${quoteId}/status`, { status: statusValue }),
};

export const reporting = {
  dashboard: () => api.get<DashboardData>("/reporting/dashboard"),
};

export const admin = {
  audit: (params: { action?: string; object_id?: string } = {}) => {
    const qs = new URLSearchParams(params as Record<string, string>).toString();
    return api.get<AuditLogEntry[]>(`/audit${qs ? `?${qs}` : ""}`);
  },
};

export const investors = {
  list: () => api.get<Investor[]>("/investors"),
  me: () => api.get<Investor>("/investors/me"),
  create: (body: { name: string; type: string; user_email?: string }) =>
    api.post<Investor>("/investors", body),
  setCriteria: (id: string, body: Criteria) =>
    api.put<Criteria>(`/investors/${id}/criteria`, body),
};

export const matching = {
  forCompany: (companyId: string, includeNonEligible = false) =>
    api.get<MatchResult[]>(
      `/companies/${companyId}/matches${includeNonEligible ? "?include_non_eligible=true" : ""}`,
    ),
};

export interface CompanyCreateInput {
  name: string;
  country: string;
  sector: string;
  rccm?: string | null;
}

export const companies = {
  list: () => api.get<Company[]>("/companies"),
  get: (id: string) => api.get<Company>(`/companies/${id}`),
  create: (input: CompanyCreateInput) => api.post<CompanyCreateResult>("/companies", input),
  setDealType: (
    id: string,
    body: { deal_type_primary: string; deal_type_secondary?: string | null },
  ) => api.post<FinancingNeed>(`/companies/${id}/deal-type`, body),
  requalify: (
    id: string,
    body: { deal_type_primary: string; deal_type_secondary?: string | null; motif: string },
  ) => api.post<FinancingNeed>(`/companies/${id}/deal-type/requalify`, body),
  dealTypeHistory: (id: string) =>
    api.get<DealTypeHistoryEntry[]>(`/companies/${id}/deal-type/history`),
};
