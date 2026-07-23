# Roadmap: <Product name>

> Template dell'artefatto **Roadmap**. Fasi **piccole** — ognuna implementabile in una
> sessione focalizzata. Tutti gli item `[x]` rendono una fase delivered; la prima fase non deferred
> con almeno un item `[ ]` e' current, anche se parziale; le successive sono planned. L'opzionale
> `**Status:** deferred` esclude una fase dalla selezione, ma richiede una decisione umana esplicita.
> Se non resta una fase eleggibile, l'assenza del marker top-level
> `**Lifecycle:** complete` e' exhaustion accidentale e richiede re-cadence. Il marker e' valido
> solo quando tutte le fasi non deferred sono delivered: la readiness passa ma la pianificazione
> resta bloccata fino a una riapertura umana atomica che lo rimuove e aggiunge una nuova fase
> eleggibile. Gli item descrivono
> capability/outcome, non task tecnici. Al closeout un outcome approvato parzialmente consegnato
> puo' diventare un `[x]` delivered e un `[ ]` remaining solo se conserva scope e intento approvati;
> la riga `[x]` porta evidenza concisa.

---

## Phase 1: <nome>

**Goal:** <cosa consegna questa fase.>

- [ ] <capability osservabile per l'utente o il sistema>
- [ ] <capability osservabile successiva>

Esempio di closeout parziale, senza inventare scope:

- [x] <outcome approvato consegnato> — evidence: `changes/YYYY-MM-DD-<change>.md`, review PROMOTE.
- [ ] <porzione gia' approvata e ancora necessaria>

---

## Phase 2: <nome>

**Goal:** <...>

- [ ] <item>

---

## Phase 3: <nome di una fase intenzionalmente rinviata>

**Status:** deferred
**Goal:** <outcome ancora ispezionabile, rinviato per decisione umana>

- [ ] <capability rinviata>
