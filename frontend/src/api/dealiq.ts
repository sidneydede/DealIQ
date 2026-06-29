import { api } from "./client";
import type {
  AdminUser,
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
  DdAnalysis,
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
  InviteResult,
  KycCheck,
  Mandate,
  MatchResult,
  MissionDetail,
  NotificationItem,
  OffersResponse,
  Page,
  Program,
  ProgramMember,
  ProgramReport,
  OnboardingSession,
  QAItem,
  Question,
  QuoteRequest,
  ReadinessScore,
  Report,
  ScoringConfig,
  SimulateResult,
  Teaser,
  TeaserPublic,
  UserCreated,
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

export const scoringAdmin = {
  getConfig: () => api.get<ScoringConfig>("/admin/scoring/config"),
  updateConfig: (body: Partial<ScoringConfig>) =>
    api.put<ScoringConfig>("/admin/scoring/config", body),
  simulate: (body: Record<string, unknown>) =>
    api.post<SimulateResult>("/admin/scoring/simulate", body),
};

export const report = {
  get: (id: string) => api.get<Report>(`/companies/${id}/report`),
  downloadPdf: (id: string) =>
    api.download(`/companies/${id}/report.pdf`, `rapport-readiness-${id.slice(0, 8)}.pdf`),
};

export const offers = {
  list: () => api.get<OffersResponse>("/meta/offers"),
  requestQuote: (
    id: string,
    body: { offer_key?: string | null; message?: string; contact_phone?: string },
  ) => api.post<QuoteRequest>(`/companies/${id}/quote-request`, body),
};

export const cockpit = {
  companies: (
    params: {
      deal_type?: string;
      status_filter?: string;
      only?: string;
      q?: string;
      limit?: number;
      offset?: number;
    } = {},
  ) => {
    const clean = Object.fromEntries(
      Object.entries(params).filter(([, v]) => v !== undefined && v !== ""),
    ) as Record<string, string>;
    const qs = new URLSearchParams(clean).toString();
    return api.get<Page<CockpitItem>>(`/cockpit/companies${qs ? `?${qs}` : ""}`);
  },
  exportCsv: (
    params: { deal_type?: string; status_filter?: string; only?: string; q?: string } = {},
  ) => {
    const clean = Object.fromEntries(
      Object.entries(params).filter(([, v]) => v !== undefined && v !== ""),
    ) as Record<string, string>;
    const qs = new URLSearchParams(clean).toString();
    return api.download(`/cockpit/companies.csv${qs ? `?${qs}` : ""}`, "dealflow.csv");
  },
  pipeline: () => api.get<Record<string, number>>("/cockpit/pipeline"),
  setQuoteStatus: (quoteId: string, statusValue: string) =>
    api.patch<QuoteRequest>(`/quote-requests/${quoteId}/status`, { status: statusValue }),
};

export const reporting = {
  dashboard: () => api.get<DashboardData>("/reporting/dashboard"),
};

export const admin = {
  audit: (
    params: { action?: string; object_id?: string; limit?: number; offset?: number } = {},
  ) => {
    const clean = Object.fromEntries(
      Object.entries(params).filter(([, v]) => v !== undefined && v !== ""),
    ) as Record<string, string>;
    const qs = new URLSearchParams(clean).toString();
    return api.get<Page<AuditLogEntry>>(`/audit${qs ? `?${qs}` : ""}`);
  },
};

export const security = {
  mfaSetup: () => api.post<{ secret: string; otpauth_uri: string }>("/auth/mfa/setup"),
  mfaEnable: (code: string) => api.post<{ mfa_enabled: boolean }>("/auth/mfa/enable", { code }),
  mfaDisable: (code: string) => api.post<{ mfa_enabled: boolean }>("/auth/mfa/disable", { code }),
};

export const notifications = {
  list: (params: { unread?: boolean; limit?: number; offset?: number } = {}) => {
    const clean: Record<string, string> = {};
    if (params.unread) clean.unread = "true";
    if (params.limit !== undefined) clean.limit = String(params.limit);
    if (params.offset !== undefined) clean.offset = String(params.offset);
    const qs = new URLSearchParams(clean).toString();
    return api.get<Page<NotificationItem>>(`/notifications${qs ? `?${qs}` : ""}`);
  },
  unreadCount: () => api.get<{ count: number }>("/notifications/unread-count"),
  markRead: (id: string) => api.post<NotificationItem>(`/notifications/${id}/read`),
  markAllRead: () => api.post<{ count: number }>("/notifications/read-all"),
};

export const users = {
  list: () => api.get<AdminUser[]>("/users"),
  create: (body: { email: string; full_name?: string; role: string; password?: string }) =>
    api.post<UserCreated>("/users", body),
  changeRole: (id: string, role: string) => api.patch<AdminUser>(`/users/${id}/role`, { role }),
  setActive: (id: string, is_active: boolean) =>
    api.patch<AdminUser>(`/users/${id}/active`, { is_active }),
};

export const investors = {
  list: (params: { q?: string; limit?: number; offset?: number } = {}) => {
    const clean = Object.fromEntries(
      Object.entries(params).filter(([, v]) => v !== undefined && v !== ""),
    ) as Record<string, string>;
    const qs = new URLSearchParams(clean).toString();
    return api.get<Page<Investor>>(`/investors${qs ? `?${qs}` : ""}`);
  },
  me: () => api.get<Investor>("/investors/me"),
  exportCsv: (q?: string) =>
    api.download(
      `/investors/export.csv${q ? `?q=${encodeURIComponent(q)}` : ""}`,
      "investisseurs.csv",
    ),
  create: (body: { name: string; type: string; user_email?: string }) =>
    api.post<Investor>("/investors", body),
  invite: (id: string, email?: string) =>
    api.post<InviteResult>(`/investors/${id}/invite`, { email: email || null }),
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

export const programs = {
  list: () => api.get<Program[]>("/programs"),
  create: (body: { name: string; sponsor_name: string; sponsor_email?: string }) =>
    api.post<Program>("/programs", body),
  addMember: (programId: string, company_id: string) =>
    api.post<ProgramMember>(`/programs/${programId}/members`, { company_id }),
  members: (programId: string) => api.get<ProgramMember[]>(`/programs/${programId}/members`),
  report: (programId: string) => api.get<ProgramReport>(`/programs/${programId}/report`),
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

export const dd = {
  importBalance: (
    companyId: string,
    lines: { account: string; label?: string; amount: number }[],
    fiscal_year?: string,
  ) => api.post(`/companies/${companyId}/syscohada`, { lines, fiscal_year }),
  compute: (companyId: string) => api.post<DdAnalysis>(`/companies/${companyId}/dd/compute`),
  get: (companyId: string) => api.get<DdAnalysis>(`/companies/${companyId}/dd`),
};

export const deals = {
  list: (params: { stage?: string; deal_type?: string; limit?: number; offset?: number } = {}) => {
    const clean = Object.fromEntries(
      Object.entries(params).filter(([, v]) => v !== undefined && v !== ""),
    ) as Record<string, string>;
    const qs = new URLSearchParams(clean).toString();
    return api.get<Page<Deal>>(`/deals${qs ? `?${qs}` : ""}`);
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
