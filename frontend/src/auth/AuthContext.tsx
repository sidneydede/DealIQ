import { createContext, useContext, useEffect, useState, type ReactNode } from "react";

import { api, tokens } from "../api/client";

export type Role =
  | "entrepreneur"
  | "investisseur"
  | "analyste"
  | "senior"
  | "conformite"
  | "admin";

export interface User {
  id: string;
  email: string;
  full_name: string | null;
  role: Role;
  is_active: boolean;
}

interface TokenPair {
  access_token: string;
  refresh_token: string;
}

interface AuthState {
  user: User | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, fullName: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthState | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

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

  async function login(email: string, password: string) {
    const pair = await api.post<TokenPair>("/auth/login", { email, password }, false);
    tokens.set(pair.access_token, pair.refresh_token);
    setUser(await api.get<User>("/auth/me"));
  }

  async function register(email: string, password: string, fullName: string) {
    await api.post("/auth/register", { email, password, full_name: fullName }, false);
    await login(email, password);
  }

  function logout() {
    tokens.clear();
    setUser(null);
  }

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth(): AuthState {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth doit être utilisé dans <AuthProvider>");
  return ctx;
}
