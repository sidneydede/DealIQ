// Client API DealIQ — wrapper fetch avec gestion du token JWT.

const TOKEN_KEY = "dealiq_token";

export const getToken = () => localStorage.getItem(TOKEN_KEY);
export const setToken = (t) => localStorage.setItem(TOKEN_KEY, t);
export const clearToken = () => localStorage.removeItem(TOKEN_KEY);

async function request(path, { method = "GET", body, form, raw } = {}) {
  const headers = {};
  const token = getToken();
  if (token) headers.Authorization = `Bearer ${token}`;

  let payload;
  if (form) {
    headers["Content-Type"] = "application/x-www-form-urlencoded";
    payload = new URLSearchParams(form).toString();
  } else if (raw) {
    payload = raw; // FormData (upload) — pas de Content-Type manuel
  } else if (body !== undefined) {
    headers["Content-Type"] = "application/json";
    payload = JSON.stringify(body);
  }

  const res = await fetch(`/api${path}`, { method, headers, body: payload });
  if (res.status === 204) return null;

  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    const detail = data.detail;
    const msg = Array.isArray(detail)
      ? detail.map((d) => d.msg).join(", ")
      : detail || `Erreur ${res.status}`;
    throw new Error(msg);
  }
  return data;
}

// ── Auth ────────────────────────────────────────────────────────────────────
export async function login(email, password) {
  const data = await request("/auth/login", {
    method: "POST",
    form: { username: email, password },
  });
  setToken(data.access_token);
  return data;
}
export const me = () => request("/auth/me");

// ── Deals ───────────────────────────────────────────────────────────────────
export const listDeals = () => request("/deals");
export const getDeal = (id) => request(`/deals/${id}`);
export const createDeal = (body) => request("/deals", { method: "POST", body });
export const patchDeal = (id, body) =>
  request(`/deals/${id}`, { method: "PATCH", body });
export const deleteDeal = (id) => request(`/deals/${id}`, { method: "DELETE" });

export const listNotes = (id) => request(`/deals/${id}/notes`);
export const addNote = (id, content) =>
  request(`/deals/${id}/notes`, { method: "POST", body: { content } });
export const getHistory = (id) => request(`/deals/${id}/history`);

// ── Enrichissement ──────────────────────────────────────────────────────────
export const enrichStatus = (id) => request(`/deals/${id}/enrich/status`);
export const enrich = (id) => request(`/deals/${id}/enrich`, { method: "POST" });
export const listProposals = (id) => request(`/deals/${id}/proposals`);
export const acceptProposal = (pid) =>
  request(`/proposals/${pid}/accept`, { method: "POST" });
export const modifyProposal = (pid, value) =>
  request(`/proposals/${pid}/modify`, { method: "POST", body: { value } });
export const rejectProposal = (pid) =>
  request(`/proposals/${pid}/reject`, { method: "POST" });

// ── Import IA ────────────────────────────────────────────────────────────────
export const extractText = (id, text) =>
  request(`/deals/${id}/extract-text`, { method: "POST", body: { text } });
export function uploadDeck(id, file) {
  const fd = new FormData();
  fd.append("file", file);
  return request(`/deals/${id}/deck`, { method: "POST", raw: fd });
}
export const guidedQuestions = (id) => request(`/deals/${id}/guided-questions`);

// ── Meta ─────────────────────────────────────────────────────────────────────
export const pedagogicalNotes = () => request("/meta/pedagogical-notes");
