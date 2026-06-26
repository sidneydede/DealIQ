"""Jeu de données de référence CI/UEMOA (issu du cahier des charges)."""

# Pays — UEMOA (8) + autres marchés d'Afrique de l'Ouest fréquents
COUNTRIES = [
    # (iso2, nom, is_uemoa)
    ("CI", "Côte d'Ivoire", True),
    ("SN", "Sénégal", True),
    ("BJ", "Bénin", True),
    ("BF", "Burkina Faso", True),
    ("ML", "Mali", True),
    ("NE", "Niger", True),
    ("TG", "Togo", True),
    ("GW", "Guinée-Bissau", True),
    ("GH", "Ghana", False),
    ("NG", "Nigeria", False),
    ("GN", "Guinée", False),
]

# Secteurs / verticales courants de l'écosystème early stage CI/UEMOA
SECTORS = [
    "Fintech",
    "Agritech",
    "E-commerce",
    "Edtech",
    "Healthtech",
    "Logistique / Mobilité",
    "Energie / Cleantech",
    "SaaS B2B",
    "Marketplace",
    "Médias / Divertissement",
    "Insurtech",
    "Autre",
]

# Fonds VC actifs sur la zone (référence pédagogique — cf. CDC)
FUNDS = [
    ("Partech Africa", "Sénégal"),
    ("Adiwale Fund", "Côte d'Ivoire"),
    ("Orange Ventures CI", "Côte d'Ivoire"),
    ("Tiim Group", "Côte d'Ivoire"),
    ("AFDB Ventures", "Côte d'Ivoire"),
    ("Cauris Finance", "Togo"),
]

# Accélérateurs / incubateurs (cf. CDC)
ACCELERATORS = [
    ("CTIC Dakar", "Sénégal"),
    ("Orange Corners", "Côte d'Ivoire"),
    ("Seedstars West Africa", "Côte d'Ivoire"),
    ("AFRIC'INNOV", "Côte d'Ivoire"),
    ("HUB Abidjan", "Côte d'Ivoire"),
]

# Canaux de sourcing (Module 1 — champ "Source du deal")
DEAL_SOURCE_TYPES = [
    ("event", "Événement"),
    ("whatsapp", "WhatsApp pro"),
    ("recommendation", "Recommandation directe"),
    ("cold_inbound", "Cold inbound"),
    ("other", "Autre"),
]
