# Control Tower — Agents (blueprint di fase)

I **custom agent di fase** della metodologia, **attivi** in questo repo sotto
`.github/agents/`. Realizzano il layer "sub-agente di
esecuzione" del Manifesto (§4) e colmano il gap annotato nel dettaglio §1.1
(*tower = agente generico, non un `*.agent.md` dedicato*).

## Il modello: la Tower produce, gli specialisti entrano solo quando servono

- **Umano** — comanda: Vision, Constraints, Roadmap, approvazioni ai gate.
- **Tower (copilota / producer)** — sceglie la slice, elicita, pianifica, implementa e integra;
  per una delivery LIGHT resta l'unico producer della branch.
- **Agenti di fase** — esecutori specializzati e **sostituibili**:

| Agente | Profilo | Fase | `tools` (bordo) | Produce |
|---|---|---|---|---|
| `requirements-agent` | Full | opzionale: complessità comportamentale/isolamento utile, dopo readiness | read · search · edit | handoff per il Change Record |
| `architect-agent` | LIGHT | architettura / design load-bearing, dentro una delivery selezionata | read · search · edit | nota di architettura + decisioni |
| `planner-agent` | Full | opzionale: coordinamento task/evidenza non semplice | read · search · edit | handoff dettagliato, non un record parallelo |
| `reviewer-agent` | LIGHT | readiness, design challenge e final review | read · search · **execute (no edit)** | verdetto |

Gli **artefatti restano il contratto**: gli agenti li *leggono*
(`mission.md`, `constraints.md`, `roadmap.md`, il Change Record), non li ri-codificano.

L'inception THIN resta al **Tower principale**. Dopo readiness, una delivery LIGHT resta nello
stesso producer: Requirements/Planner sono deleghe opzionali con ragione esplicita; Architect entra
solo per design load-bearing. Reviewer resta sempre fresco, no-edit e indipendente.

## Orchestrazione (prompt-based)

La tower delega ogni step in linguaggio naturale, passando solo il contesto
essenziale (es. il path della slice); ogni agente **legge il proprio `.agent.md`**
per tool e vincoli. I tool dell'orchestratore sono un **tetto** per i sub-agenti.
Niente codice di orchestrazione nella prosa (tenet 3); orchestrazione **iterativa
per-slice, non** una pipeline fissa. L'esistenza di un agente non giustifica la sua invocazione.

## Adozione

In questo repo tutti gli agenti sono in `.github/agents/`, **attivi** e canonici. Il bootstrap
LIGHT copia Reviewer e Architect; `-Profile Full` aggiunge Requirements e Planner. Un consumatore
non deve mantenere definizioni divergenti fuori dal canale di copia.

## Cosa muove — e i caveat onesti

- **C2 (enforcement) ↓↓** — `tools`/`model`/tetto sono bordi **configurati**, non prosa.
- **C5 / C9 ↓** — il `reviewer-agent` (senza `edit`) è indipendente da chi produce →
  **separazione dei compiti imposta dai tool**.
- **C3 ↓** — delega + approvazioni ai gate invece che per-token.

Caveat (vedi **C14** nel registro delle critiche):

- **Illusione prosa-in-config**: le *istruzioni* dell'agente restano prosa; solo
  `tools`/`model`/scope sono hard. La distinzione "scrivo doc, non codice" di
  requirements/architect/planner è imposta dalle *istruzioni*, non dai tool.
- **Agent sprawl**: non oltre ~5-10 step; ogni invocazione costa latenza e contesto.
- **Waterfall-by-handoff (C1)**: non cablare requisiti→arch→plan→code come catena
  rigida; la tower li invoca on-demand e iterativamente.
