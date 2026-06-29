import { api } from "./client";
import type {
  AuditLogEntry,
  ChecklistItem,
  CockpitItem,
  Company,
  CompanyCreateResult,
  ConflictItem,
  CountryMeta,
  Criteria,
  DashboardData,
  DataRoom,
  DataRoomAccess,
  DataRoomDocument,
  DataRoomLog,
  Deal,
  DealDetail,
  DealMilestone,
  DocumentView,
  EsgProfile,
  DealTypeHistoryEntry,
  DealTypeMeta,
  DocumentOut,
  FinancingNeed,
  GatingResult,
  Interaction,
  Fee,
  Investor,
  KycCheck,
  Mandate,
  MatchResult,
  MissionDetail,
  OffersResponse,
  OnboardingSession,
  QAItem,
  Question,
  QuoteRequest,
  ReadinessScore,
  Report,
  Teaser,
  TeaserPublic,
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

export const teasers = {
  // Cabinet
  generate: (companyId: string) => api.post<Teaser>(`/companies/${companyId}/teaser`),
  forCompany: (companyId: string) => api.get<Teaser>(`/companies/${companyId}/teaser`),
  publish: (teaserId: string) => api.post<Teaser>(`/teasers/${teaserId}/publish`),
  // Investisseur (anonymisé)
  catalog: (params: { instrument?: string; deal_type?: string; sector?: string } = {}) => {
    const qs = new URLSearchParams(params as Record<string, string>).toString();
    return api.get<TeaserPublic[]>(`/teasers${qs ? `?${qs}` : ""}`);
  },
  interest: (teaserId: string, note?: string) =>
    api.post<Interaction>(`/teasers/${teaserId}/interest`, { note }),
};

export const interactions = {
  list: () => api.get<Interaction[]>("/interactions"),
  setStatus: (id: string, statusValue: string) =>
    api.patch<Interaction>(`/interactions/${id}/status`, { status: statusValue }),
};

export const kyc = {
  list: (params: { status_filter?: string } = {}) => {
    const qs = new URLSearchParams(params as Record<string, string>).toString();
    return api.get<KycCheck[]>(`/kyc/checks${qs ? `?${qs}` : ""}`);
  },
  run: (subject_type: string, subject_id: string, check_type: string) =>
    api.post<KycCheck>("/kyc/checks", { subject_type, subject_id, check_type }),
  update: (id: string, status: string, notes?: string) =>
    api.patch<KycCheck>(`/kyc/checks/${id}`, { status, notes }),
};

export const esg = {
  get: (companyId: string) => api.get<EsgProfile>(`/companies/${companyId}/esg`),
  upsert: (companyId: string, body: Record<string, unknown>) =>
    api.put<EsgProfile>(`/companies/${companyId}/esg`, body),
  setRequired: (companyId: string, esg_required: boolean) =>
    api.patch<EsgProfile>(`/companies/${companyId}/esg/required`, { esg_required }),
  export: (companyId: string) =>
    api.get<Record<string, unknown>>(`/companies/${companyId}/esg/export`),
};

export const missions = {
  create: (companyId: string) => api.post<MissionDetail>(`/companies/${companyId}/mission`),
  get: (companyId: string) => api.get<MissionDetail>(`/companies/${companyId}/mission`),
  toggleTask: (taskId: string, done: boolean) =>
    api.patch(`/mission-tasks/${taskId}`, { done }),
  addDeliverable: (missionId: string, kind: string) =>
    api.post(`/missions/${missionId}/deliverables`, { kind }),
  updateDeliverable: (deliverableId: string, statusValue: string) =>
    api.patch(`/deliverables/${deliverableId}`, { status: statusValue }),
  review: (missionId: string) => api.post(`/missions/${missionId}/review`),
  promote: (missionId: string) => api.post<Company>(`/missions/${missionId}/promote`),
};

export const mandates = {
  forCompany: (companyId: string) => api.get<Mandate[]>(`/companies/${companyId}/mandates`),
  create: (
    companyId: string,
    body: { represented_party: string; mandate_type: string; exclusive: boolean },
  ) => api.post<Mandate>(`/companies/${companyId}/mandates`, body),
  update: (id: string, body: { status?: string; signed?: boolean }) =>
    api.patch<Mandate>(`/mandates/${id}`, body),
  fees: (id: string) => api.get<Fee[]>(`/mandates/${id}/fees`),
  addFee: (id: string, body: { fee_type: string; amount?: number; currency?: string }) =>
    api.post<Fee>(`/mandates/${id}/fees`, body),
  updateFee: (feeId: string, statusValue: string) =>
    api.patch<Fee>(`/fees/${feeId}`, { status: statusValue }),
  conflicts: () => api.get<ConflictItem[]>("/conflicts"),
};

export const deals = {
  list: (params: { stage?: string; deal_type?: string } = {}) => {
    const qs = new URLSearchParams(params as Record<string, string>).toString();
    return api.get<Deal[]>(`/deals${qs ? `?${qs}` : ""}`);
  },
  get: (id: string) => api.get<DealDetail>(`/deals/${id}`),
  createFromInteraction: (interactionId: string) =>
    api.post<Deal>(`/interactions/${interactionId}/deal`),
  advance: (id: string, stage: string, note?: string) =>
    api.patch<Deal>(`/deals/${id}/stage`, { stage, note }),
  toggleMilestone: (milestoneId: string, done: boolean) =>
    api.patch<DealMilestone>(`/deal-milestones/${milestoneId}`, { done }),
};

export const dataroom = {
  open: (companyId: string) => api.post<DataRoom>(`/companies/${companyId}/dataroom`),
  addDocument: (roomId: string, document_id: string) =>
    api.post<DataRoomDocument>(`/dataroom/${roomId}/documents`, { document_id }),
  documents: (roomId: string) => api.get<DataRoomDocument[]>(`/dataroom/${roomId}/documents`),
  grant: (roomId: string, investor_id: string) =>
    api.post<DataRoomAccess>(`/dataroom/${roomId}/access`, { investor_id }),
  access: (roomId: string) => api.get<DataRoomAccess[]>(`/dataroom/${roomId}/access`),
  revoke: (accessId: string) => api.post<{ revoked: boolean }>(`/dataroom/access/${accessId}/revoke`),
  logs: (roomId: string) => api.get<DataRoomLog[]>(`/dataroom/${roomId}/logs`),
  accessible: () => api.get<DataRoom[]>("/dataroom/accessible"),
  view: (roomId: string, documentId: string, download = false) =>
    api.post<DocumentView>(
      `/dataroom/${roomId}/documents/${documentId}/view${download ? "?download=true" : ""}`,
    ),
};

export const qa = {
  thread: (interactionId: string) => api.get<QAItem[]>(`/interactions/${interactionId}/qa`),
  ask: (interactionId: string, question: string) =>
    api.post<QAItem>(`/interactions/${interactionId}/qa`, { question }),
  answer: (itemId: string, answer: string) =>
    api.post<QAItem>(`/qa/${itemId}/answer`, { answer }),
  close: (itemId: string) => api.patch<QAItem>(`/qa/${itemId}/close`),
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
