# Constraints: <Product name>

> Template dell'artefatto **Constraints** (Manifesto tenet 4: input di prima classe).
> Vincoli tecnici / funzionali / non-funzionali che gateano ogni slice.
> I `hard` bloccano la slice; i `soft` sono trade-off dichiarati.

## THIN: leggi trasversali, non catalogo di feature

In inception THIN, i constraints sono le poche leggi, boundary e invarianti che restano validi
**attraverso** le slice. Non sono un catalogo completo di requisiti di prodotto: endpoint, flussi,
status code, casi di test e comportamento di una capability entrano nella roadmap e poi negli EARS
della slice selezionata. In genere 3–6 constraint attivi danno un inizio proporzionato, ma il numero
non è un gate: il reviewer giudica la proporzione nel contesto.

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

## Vincoli

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

<Aggiungi un blocco per ogni vincolo. Gli `hard` attivati diventano proof obligation nel Change Record.>
