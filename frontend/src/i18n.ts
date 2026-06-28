import i18n from "i18next";
import { initReactI18next } from "react-i18next";

// FR par défaut (CDC §7.12). EN pour l'investisseur ajouté ultérieurement.
const fr = {
  translation: {
    app: {
      name: "DealIQ",
      tagline: "Préparation au financement et mise en relation privée",
    },
    nav: {
      dashboard: "Tableau de bord",
      diagnostic: "Mon diagnostic",
      dealType: "Mon type de deal",
      company: "Mon entreprise",
      documents: "Documents",
      readiness: "Ma readiness",
      offers: "Accompagnement",
      cockpit: "Cockpit",
      pipeline: "Pipeline entrepreneur",
      users: "Utilisateurs",
      audit: "Journal d'audit",
      logout: "Se déconnecter",
    },
    auth: {
      loginTitle: "Connexion",
      email: "Adresse e-mail",
      password: "Mot de passe",
      login: "Se connecter",
      register: "Créer un compte",
      noAccount: "Pas encore de compte ?",
      haveAccount: "Déjà inscrit ?",
      fullName: "Nom complet",
      invalid: "E-mail ou mot de passe incorrect",
    },
    disclaimer:
      "DealIQ prépare et met en relation de façon privée des sociétés et des investisseurs qualifiés. Aucune garantie de financement. Pas d'offre au public.",
  },
};

i18n.use(initReactI18next).init({
  resources: { fr },
  lng: "fr",
  fallbackLng: "fr",
  interpolation: { escapeValue: false },
});

export default i18n;
