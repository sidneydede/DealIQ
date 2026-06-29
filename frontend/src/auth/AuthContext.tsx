import { createContext, useContext, useEffect, useState, type ReactNode } from "react";

import { api, tokens } from "../api/client";

export type Role =
  | "entrepreneur"
  | "investisseur"
  | "analyste"
  | "senior"
  | "conformite"
  | "sponsor"
  | "admin";

export interface User {
  id: string;
  email: string;
  full_name: string | null;
  role: Role;
  is_active: boolean;
  mfa_enabled: boolean;
}

interface LoginResponse {
  mfa_required: boolean;
  access_token: string | null;
  refresh_token: string | null;
  mfa_token: string | null;
}

interface AuthState {
  user: User | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<{ mfaRequired: boolean }>;
  verifyMfa: (code: string) => Promise<void>;
  register: (email: string, password: string, fullName: string) => Promise<void>;
  refreshUser: () => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthState | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [mfaToken, setMfaToken] = useState<string | null>(null);

  useEffect(() => {
    if (!tokens.access) {
      setLoading(false);
      return;
    }
    api
      .get<User>("/auth/me")
      .then(setUser)
      .catch(() => tokens.clear())
      .finally(() => setLoading(false));
  }, []);

  async function finishLogin(res: LoginResponse) {
    tokens.set(res.access_token as string, res.refresh_token as string);
    setMfaToken(null);
    setUser(await api.get<User>("/auth/me"));
  }

  async function login(email: string, password: string): Promise<{ mfaRequired: boolean }> {
    const res = await api.post<LoginResponse>("/auth/login", { email, password }, false);
    if (res.mfa_required) {
      setMfaToken(res.mfa_token);
      return { mfaRequired: true };
    }
    await finishLogin(res);
    return { mfaRequired: false };
  }

  async function verifyMfa(code: string) {
    const res = await api.post<LoginResponse>(
      "/auth/mfa/verify",
      { mfa_token: mfaToken, code },
      false,
    );
    await finishLogin(res);
  }

  async function register(email: string, password: string, fullName: string) {
    await api.post("/auth/register", { email, password, full_name: fullName }, false);
    await login(email, password); // un nouveau compte n'a jamais la 2FA active
  }

  async function refreshUser() {
    setUser(await api.get<User>("/auth/me"));
  }

  function logout() {
    tokens.clear();
    setMfaToken(null);
    setUser(null);
  }

  return (
    <AuthContext.Provider
      value={{ user, loading, login, verifyMfa, register, refreshUser, logout }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth(): AuthState {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth doit être utilisé dans <AuthProvider>");
  return ctx;
}
