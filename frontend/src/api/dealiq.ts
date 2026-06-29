import { api } from "./client";
import type {
  ChecklistItem,
  Company,
  CompanyCreateResult,
  CountryMeta,
  DealTypeHistoryEntry,
  DealTypeMeta,
  DocumentOut,
  FinancingNeed,
  GatingResult,
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
