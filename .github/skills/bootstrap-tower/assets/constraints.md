# Constraints: <Product name>

> Template dell'artefatto **Constraints** (Manifesto tenet 4: input di prima classe).
> Vincoli tecnici / funzionali / non-funzionali che gateano ogni slice.
> I `hard` bloccano la slice; i `soft` sono trade-off dichiarati.

## THIN: leggi trasversali, non catalogo di feature

In inception THIN, i constraint di prodotto sono le poche leggi, boundary e invarianti che restano
validi **attraverso** le slice. Non sono un catalogo completo di requisiti di prodotto: endpoint,
flussi, status code, casi di test e comportamento di una capability entrano nella roadmap e poi
negli EARS della slice selezionata. In genere 3–6 constraint di prodotto attivi danno un inizio
proporzionato, oltre alla baseline ereditata del metodo; il numero non è un gate e il reviewer
giudica la proporzione nel contesto.

Se manca una decisione tecnica, registra una domanda aperta o una capability di roadmap. Non
cristallizzare un'architettura non scelta nella constitution.

## Categorie

| Categoria | Cosa cattura | Esempi |
|---|---|---|
| **technical** | stack, versioni, boundary architetturali, integrazioni obbligate | "runtime Python 3.11", "storage X", "no dip. GPL" |
| **functional** | regole di dominio, invarianti, comportamenti obbligatori | "ogni importo ha valuta", "idempotenza per chiave X" |
| **non_functional (NFR)** | qualità operative misurabili | latenza p95, throughput, costo/token, sicurezza, privacy |

## Proprietà, non meccanismo

Un vincolo dichiara una **proprietà osservabile e verificabile** che il sistema deve avere — **non**
il *meccanismo* con cui la ottieni.

- ✅ **Proprietà** (vincolo): *"lo stato sopravvive ai riavvii ed è coerente tra repliche"*; *"i
  codici non sono indovinabili in sequenza"*.
- ❌ **Meccanismo** (NON in un vincolo): *"lo stato è in `<prodotto X>`"*; *"i codici sono generati
  con `<algoritmo Y>`"*.

Congelare un meccanismo in un vincolo **hard** è una **trappola di auto-conferma**: il design
"soddisfa" il vincolo perché il vincolo *è* il design — e il gate `architecture-review` non ha più
nulla da sfidare (critica **C16**, imparata col dogfooding e ri-osservata sul campo). Il meccanismo
specifico è una **decisione di design** → va in un **ADR / architecture-review**, dove le alternative
si pesano, non blindato nella costituzione.

**Regola del pollice:** se un reviewer ostile potesse chiedere *"perché questo e non X?"*, è un
meccanismo → spostalo in una decisione, e tieni la **proprietà** come vincolo.

## Provenienza e verifica

I campi a collezione usano **JSON inline** (che è YAML valido), così i gate restano stdlib-only:

- `source` è un array non vuoto. `["stakeholder"]` è elicitato; la presenza di `regulation`,
  `normative_spec` o `architecture_decision` rende il vincolo ereditato e richiede un anchor in
  `reference`.
- Ogni anchor è `{source,id,version,path,sha256}`: `path` è repo-relative e tracciato; `sha256`
  rende la risoluzione locale riproducibile. **Non** prova autenticità o sufficienza normativa.
- Un hard dichiara almeno una `projection` (path a un gate Python tracciato) o un `residual`
  instradato a `review`. La projection può provare solo la parte deterministica della proprietà.

## Baseline Control Tower ereditata (obbligatoria)

Questi sei vincoli sono leggi del metodo installato, non vincoli di prodotto. Mantieni gli ID e i
blocchi completi: i riferimenti puntano a superfici locali copiate dal kit. I primi quattro sono la
baseline universale di ogni Change Record; `FUN-ARCHREVIEW-01` e `FUN-AUTONOMY-01` sono sempre
disponibili ma si attivano come proof obligation solo quando una slice introduce rispettivamente una
decisione load-bearing o una modifica strategica a Mission/Constraints.

```yaml
constraint:
  id: FUN-CHANGE-01
  category: functional
  statement: "Every governed change has exactly one confirmed dated Change Record before implementation, with explicit outcome, Roadmap anchor, activated obligations, evidence, corrections, closeout, and the actual independent final verdict."
  rationale: "The installed Change Record kernel requires this exact locally resolvable obligation."
  source: ["normative_spec"]
  reference: [{"source":"normative_spec","id":"Control-Tower-Change-Record-Contract","version":"kernel-2026-07-23","path":"framework/contracts/change-record.md","sha256":"69da6b2d235080ffcfaab8ca7057b9ed97ec31562128dabde08cc4a38c500f2b"}]
  applies_to: [planning, design, coding]
  verification: "framework/scripts/check_change_record.py validates the one-record branch contract; independent review judges obligation completeness and genuine confirmation"
  projection: ["framework/scripts/check_change_record.py"]
  residual: [{"id":"FUN-CHANGE-01::obligation-completeness-and-confirmation","statement":"Review and the human confirm that no material obligation was omitted and the initial confirmation was genuine.","route":"review"}]
  severity: hard
  status: active
```

```yaml
constraint:
  id: FUN-ROADMAP-01
  category: functional
  statement: "The Roadmap uses canonical Phase sections: fully checked phases are delivered, the first non-deferred phase with an unchecked item is current, later eligible phases are planned, and explicit deferred status is skipped. Optional top-level **Lifecycle:** complete is valid only when every non-deferred phase is delivered and means no currently approved work; without it, exhaustion blocks for human re-cadence. Human reopening removes the marker and atomically adds at least one new eligible unchecked phase; contradictory states block."
  rationale: "Readiness, planning, and lifecycle transitions must consume one canonical analyzer without speculative backlog."
  source: ["normative_spec"]
  reference: [{"source":"normative_spec","id":"Control-Tower-Operating-Model","version":"kernel-2026-07-23","path":"framework/doctrine/operating-model.md","sha256":"64b65e4bb117179a1f7afd11e9a4f9d8ca687526036f50ef2b36b118ad6c4152"}]
  applies_to: [planning, design, coding]
  verification: ".github/skills/bootstrap-tower/scripts/scaffold_constitution.py --readiness/--current-phase and framework/scripts/check_change_record.py validate canonical Roadmap state and transitions"
  projection: [".github/skills/bootstrap-tower/scripts/scaffold_constitution.py","framework/scripts/check_change_record.py"]
  residual: [{"id":"FUN-ROADMAP-01::lifecycle-intent","statement":"Review confirms deferral, completion, and reopening are human-authorized and still appropriate; syntax and attestation prove neither identity nor strategic wisdom.","route":"review"}]
  severity: hard
  status: active
```

```yaml
constraint:
  id: NFR-DOCS-01
  category: non_functional
  statement: "Tracked Markdown is UTF-8 without BOM, uses CRLF line endings, and has balanced code fences."
  rationale: "The installed documentation workflow requires reproducible Markdown bytes."
  source: ["normative_spec"]
  reference: [{"source":"normative_spec","id":"Control-Tower-Documentation-Gate","version":"kernel-2026-07-23","path":"framework/scripts/check_docs.py","sha256":"45f74482f6cf295f1d1fabef137d08815244d85a1f9aa5462b6d00764631870f"}]
  applies_to: [coding]
  verification: "framework/scripts/check_docs.py checks every tracked Markdown file"
  projection: ["framework/scripts/check_docs.py"]
  residual: []
  metric: "BOM=0, LoneLF=0, balanced_fences=true"
  severity: hard
  status: active
```

```yaml
constraint:
  id: FUN-MERGE-01
  category: functional
  statement: "Every PR records the actual verdict from an independent final no-edit review on a frozen pushed target, satisfies merge readiness, and stops for human merge authorization."
  rationale: "The installed merge kernel preserves producer-judge separation and the human merge boundary."
  source: ["normative_spec"]
  reference: [{"source":"normative_spec","id":"Control-Tower-Merge-Ready-Gate","version":"kernel-2026-07-23","path":"framework/scripts/check_merge_ready.py","sha256":"588759968c5493d5a79e374fccfd373e187781103d9bd1e0519c9719b3548925"}]
  applies_to: [design, coding]
  verification: "framework/scripts/check_merge_ready.py requires reviewed state, latest STABLE/PROMOTE, complete evidence and closeout, and residual dispositions"
  projection: ["framework/scripts/check_merge_ready.py"]
  residual: [{"id":"FUN-MERGE-01::review-genuineness","statement":"Review and the human confirm single-producer ownership, target stability, independent judgment, and faithful recording of the returned verdict.","route":"review"}]
  severity: hard
  status: active
```

```yaml
constraint:
  id: FUN-ARCHREVIEW-01
  category: functional
  statement: "When a change introduces a load-bearing design decision, an independent blindfolded architecture challenge returns SOUND before coding; ordinary changes do not activate this obligation."
  rationale: "A future architecture-triggered Change Record must resolve the exact constraint required by the installed conditional gate."
  source: ["normative_spec"]
  reference: [{"source":"normative_spec","id":"Control-Tower-Architecture-Review-Skill","version":"kernel-2026-07-23","path":".github/skills/architecture-review/SKILL.md","sha256":"bdc295bc8014172fed1ca9f7ecb6f9c9bb4cf27d626fab34a3881a85176f3005"}]
  applies_to: [design]
  verification: ".github/skills/architecture-review/scripts/check_architecture.py validates challengeable form; independent review judges the trigger and design"
  projection: [".github/skills/architecture-review/scripts/check_architecture.py"]
  residual: [{"id":"FUN-ARCHREVIEW-01::semantic-challenge","statement":"Review confirms the trigger is genuinely load-bearing and the blindfolded challenge is independent and substantive.","route":"review"}]
  severity: hard
  status: active
```

```yaml
constraint:
  id: FUN-AUTONOMY-01
  category: functional
  statement: "A change to constitution/mission.md or constitution/constraints.md requires a recorded human-authorized ADR under constitution/decisions; Roadmap lifecycle movement does not activate this obligation."
  rationale: "The first governed strategy correction must resolve the exact constraint required by the installed autonomy and Change Record gates."
  source: ["normative_spec"]
  reference: [{"source":"normative_spec","id":"Control-Tower-Autonomy-Gate","version":"kernel-2026-07-23","path":"framework/scripts/check_autonomy.py","sha256":"e577e4b7b5f623c3106920ce4593eca5df6a9a0bf8dbf20423786aff375f25b7"}]
  applies_to: [design]
  verification: "framework/scripts/check_autonomy.py requires a new ADR for Mission or Constraints changes; independent review judges genuine human authorization"
  projection: ["framework/scripts/check_autonomy.py"]
  residual: [{"id":"FUN-AUTONOMY-01::human-authorization","statement":"Review confirms the strategic decision recorded by the ADR was genuinely authorized by the human.","route":"review"}]
  severity: hard
  status: active
```

## Vincoli di prodotto (elicitati)

I vincoli di prodotto si aggiungono alla baseline sopra; non la sostituiscono. In genere 3–6 leggi
trasversali sono sufficienti per iniziare, ma il numero non è un gate.

```yaml
constraint:
  id: NFR-LAT-01 | FUN-INV-03 | TEC-STK-02
  category: technical | functional | non_functional
  statement: "descrizione verificabile del vincolo"
  rationale: "perché esiste"
  source: ["stakeholder"]
  reference: []
  applies_to: [requirements, design, planning, coding]
  verification: "come si verifica (test, eval, misura, review)"
  projection: []
  residual: [{"id":"<CONSTRAINT-ID>::<residual-id>","statement":"parte non deterministica da giudicare","route":"review"}]
  metric?: "p95_latency_ms < 300"        # solo NFR misurabili
  severity: hard | soft
  status: active | superseded | waived
  waiver?: "chi ha autorizzato la deroga e perché"
```

<Aggiungi un blocco per ogni vincolo di prodotto. Gli `hard` attivati diventano proof obligation nel Change Record.>
