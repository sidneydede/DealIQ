import { api } from "./client";
import type {
  Company,
  CompanyCreateResult,
  CountryMeta,
  DealTypeHistoryEntry,
  DealTypeMeta,
  FinancingNeed,
} from "./types";

export const meta = {
  dealTypes: () => api.get<DealTypeMeta[]>("/meta/deal-types"),
  countries: () => api.get<CountryMeta[]>("/meta/countries"),
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
