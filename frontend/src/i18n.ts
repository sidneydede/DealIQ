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
    company: {
      title: "Mon entreprise",
      none: "Aucune fiche entreprise pour l'instant. Créez-la pour démarrer.",
      create: "Créer ma fiche entreprise",
      name: "Nom de l'entreprise",
      country: "Pays",
      sector: "Secteur d'activité",
      rccm: "RCCM (optionnel)",
      status: "Statut du dossier",
      currency: "Devise",
      reliability: "Fiabilité des données financières",
      declared: "Déclaré / non audité",
      duplicateWarning:
        "Une fiche similaire existe déjà dans la base — à vérifier avec votre conseiller.",
      saved: "Fiche enregistrée.",
    },
    dealType: {
      title: "Mon type de deal",
      question: "Quel type d'opération envisagez-vous ?",
      help: "Ce choix personnalise votre parcours ; il pourra être ajusté avec un expert.",
      current: "Type retenu",
      none: "Aucun type de deal sélectionné pour l'instant.",
      confirm: "Confirmer ce type d'opération",
      needCompany: "Créez d'abord votre fiche entreprise pour choisir un type de deal.",
      history: "Historique des changements",
      bySource: { entrepreneur: "Vous", cabinet: "Cabinet (requalification)" },
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
