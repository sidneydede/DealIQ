import DealList from "./DealList";

const STEPS = [
  { n: 1, h: "Saisir manuellement", p: "Tu crées la fiche à partir de ce que tu sais. Le Mode Données Zéro s'active si tu n'as aucune source." },
  { n: 2, h: "Enrichir avec l'IA", p: "Agent A complète depuis X, LinkedIn, le site, Crunchbase… en mode assisté, jamais proactif." },
  { n: 3, h: "Valider champ par champ", p: "Tu acceptes, modifies ou rejettes chaque proposition. Rien n'est écrit sans toi." },
];

export default function Sourcing({ notes, onOpen }) {
  return (
    <div>
      <h2 style={{ marginTop: 0 }}>Sourcing manuel</h2>
      <div className="steps">
        {STEPS.map((s) => (
          <div className="step" key={s.n}>
            <div className="num">{s.n}</div>
            <h4>{s.h}</h4>
            <p>{s.p}</p>
          </div>
        ))}
      </div>
      <DealList notes={notes} onOpen={onOpen} />
    </div>
  );
}
