import { useCallback, useEffect, useState } from "react";

import { companies } from "../api/dealiq";
import type { Company } from "../api/types";

/** Charge la première fiche entreprise accessible à l'utilisateur (la sienne pour l'entrepreneur). */
export function useMyCompany() {
  const [company, setCompany] = useState<Company | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const reload = useCallback(async () => {
    setLoading(true);
    try {
      const list = await companies.list();
      setCompany(list[0] ?? null);
      setError(null);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Erreur de chargement");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void reload();
  }, [reload]);

  return { company, setCompany, loading, error, reload };
}
