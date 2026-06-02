# Guida agenti Claude — reference completa

Documento di riferimento per consultazione quotidiana. Per l'onboarding e la prima esecuzione vedi [`../ONBOARDING.md`](../ONBOARDING.md).

## Indice

- [Architettura in 30 secondi](#architettura-in-30-secondi)
- [I 10 agenti in dettaglio](#i-10-agenti-in-dettaglio)
- [Come scrivere una buona issue per un agente](#come-scrivere-una-buona-issue-per-un-agente)
- [Comportamenti automatici](#comportamenti-automatici)
- [Limiti, costi, performance](#limiti-costi-performance)
- [Sicurezza e governance](#sicurezza-e-governance)

---

## Architettura in 30 secondi

```
Issue/PR + label "agent:X"  →  GitHub Actions (runner effimero)
                                   │
                                   ▼
                          Claude Code (auth Max via OAuth)
                                   │
                ┌──────────────────┼─────────────────────┐
                ▼                  ▼                     ▼
            PR aperta        Commento posted     Master Board update
            (fix/docs/        (review/summary)    (tutti gli agenti)
             test/refactor)         │                     │
                │                   │                     ▼
                ▼                   │              Reviewer auto-assigned
        Reviewer routing            │              (solo PR-creator)
        round-robin                 │
                                    ▼
                          [se failure] → Telegram alert
```

Nessun server. Nessun webhook gateway. Tutto su infrastruttura GitHub + abbonamento Claude Max esistente.

---

## I 10 agenti in dettaglio

### `agent:fix` — Risolutore di bug

**Trigger:** label su una issue.

**Cosa fa:** legge il body della issue, crea un branch `agent/fix-<N>`, applica modifiche minime al codice, apre una PR con `Closes #N`, commenta la issue con il link.

**Quando usarlo:**
- Bug ben definito con riproduzione chiara
- Comportamento atteso vs attuale documentato
- Scope contenuto (1-3 file)

**Quando NON usarlo:**
- Feature nuove (Claude tende a sovrascrivere troppo)
- Bug architetturali profondi
- Issue vaghe ("non funziona", "lento")

**Esempio buono di issue:**
> File `src/auth.js`, funzione `validateToken()`: se il token ha scope vuoto ritorna `true` invece di `false`. Atteso: rifiutare token senza scope. Test esistente in `auth.test.js` linea 42 da estendere.

**Esempio scarso:**
> il login non va

### `agent:review` — Code review automatica

**Trigger:** label su PR (o issue, ma su PR è più utile).

**Cosa fa:** legge il diff completo, analizza con focus su correttezza/sicurezza/edge case, posta un commento strutturato con sezioni **Bloccanti / Da valutare / Note minori**.

**Quando usarlo:**
- Primo passaggio prima della review umana — l'agente screma l'ovvio
- PR di un agente fix/refactor (review di se stessi può sembrare strano ma funziona perché un altro contesto rilegge)
- PR esterne dove vuoi un secondo paio d'occhi automatico

**Limiti:**
- Non beccherà problemi di business logic che richiedono contesto profondo del progetto
- Non sostituisce la review umana sui cambi sensibili (security, payment, data migration)

### `agent:docs` — Manutenzione documentazione

**Trigger:** label su issue.

**Cosa fa:** aggiorna README, file in `/docs`, commenti di alto livello. Apre PR `docs:`. **Non tocca la logica del codice.**

**Quando usarlo:**
- README obsoleto rispetto a una feature appena rilasciata
- Aggiungere sezione Usage/Installation/FAQ
- Tradurre/uniformare il tono della doc

**Esempio buono di issue:**
> Aggiungere sezione "Configurazione" al README di `auth-service` che documenti tutte le env var lette in `src/config.ts`, inclusi i default.

### `agent:test` — Generazione test

**Trigger:** label su issue.

**Cosa fa:** identifica il framework (`package.json`, `pyproject.toml`, ecc.), aggiunge test mantenendo lo stile esistente, verifica che la suite passi prima di aprire PR.

**Quando usarlo:**
- Coverage gap noti su file o funzioni specifiche
- Prima di un refactor risk-y (fissi il comportamento con test, poi refactori)
- Test mancanti dopo un fix umano

**Importante:** se il repo non ha un framework di test configurato, l'agente lo creerà (es. `node --test` per Node senza dipendenze). Verifica che la scelta sia compatibile con il resto del progetto prima di mergiare.

### `agent:refactor` — Refactoring mirato

**Trigger:** label su issue.

**Cosa fa:** applica refactoring scope-limited preservando comportamento osservabile. Include sezione "Prima / Dopo" nella PR.

**Quando usarlo:**
- Estrarre costanti/funzioni quando il pattern si ripete
- Rinominare per chiarezza
- Spostare codice tra moduli

**Quando NON usarlo:**
- Riscritture architetturali (troppo scope per un agente)
- Cambi che richiedono decisioni di design (interfacce, pattern)

**Buona pratica:** lancia prima `agent:test` per fissare il comportamento, poi `agent:refactor`. Così hai una rete di sicurezza.

### `agent:summary` — TL;DR mobile-friendly

**Trigger:** label su issue o PR.

**Cosa fa:** commento di 3-5 bullet (max ~80 caratteri ciascuno) pensato per essere letto al volo da smartphone.

**Quando usarlo:**
- Sei in mobilità e qualcuno ti gira un'issue lunga
- PR di 500 righe e vuoi capire l'idea prima di sederti a fare review seria
- Stand-up: vuoi riassumere lo stato di N issue in 30 secondi

**Read-only:** non modifica nulla, non apre PR. È il più sicuro di tutti — puoi farlo girare a costo bassissimo (~$0.01).

### `agent:security` — Security review diff-aware

**Trigger:** label su PR (o issue).

**Cosa fa:** legge il diff, cerca vulnerabilità (injection, XSS, auth flaw, secret hardcoded, input non validato, deserializzazione insicura, path traversal, SSRF, dipendenze vulnerabili) e posta un commento con sezioni **Critico / Alto / Medio / Basso**, ognuna con confidence e remediation.

**Quando usarlo:**
- Prima di mergiare PR che toccano auth, input utente, query DB, upload file
- Audit periodico di un'area sensibile
- Doppio controllo su codice generato da altri agenti

**Note:** usa il modello Opus (recall massima sui bug) e il pattern "report-everything" — segnala anche i finding incerti, il triage lo fai tu. Read-only, non apre PR.

### `agent:cicd` — DevOps / CI-CD automation

**Trigger:** label su issue.

**Cosa fa:** crea o sistema workflow GitHub Actions, Dockerfile, docker-compose, script di build/release/deploy. Apre PR `cicd:`.

**Quando usarlo:**
- "Aggiungi un workflow CI che fa lint + test su ogni PR"
- "Scrivi un Dockerfile multi-stage per questo servizio Node"
- "Sistema il workflow di release che fallisce sul tag"

**Limiti di sicurezza:** NON esegue deploy reali né comandi distruttivi — prepara solo la PR. Per azioni irreversibili o su infra condivisa, segnala e lascia decidere a te.

> **⚠️ Permesso `workflows` necessario.** Il token della GitHub App di Claude di default **non può creare o modificare file in `.github/workflows/`** (limite di sicurezza GitHub). Se chiedi a `agent:cicd` di scrivere un workflow, senza il permesso aggiuntivo l'agente non riesce a pushare e ripiega postando il contenuto del file + le istruzioni come commento (degrado graceful). Per abilitare la scrittura diretta dei workflow: Organization → Settings → GitHub Apps → claude → Permissions → **Workflows: Read and write**. In alternativa, l'agente può scrivere Dockerfile/script/config fuori da `.github/workflows/` senza alcun permesso extra.

### `agent:iac` — Infra-as-Code review

**Trigger:** label su PR (o issue).

**Cosa fa:** review read-only di Terraform, manifest K8s, docker-compose, config cloud. Cerca misconfigurazioni di sicurezza (security group aperti, bucket pubblici, IAM larghi, container privileged), secret in chiaro, assenza di resource limit, drift, best practice mancanti.

**Quando usarlo:**
- PR che modifica `.tf` o manifest K8s prima del merge
- Audit di sicurezza dell'infrastruttura dichiarativa

### `agent:maintain` — Manutenibilità / tech-debt

**Trigger:** label su issue.

**Cosa fa:** refactor mirato di manutenibilità (naming, dead code, duplicazione, funzioni troppo complesse, struttura moduli) preservando il comportamento. Apre PR `maintain:` con sezione "Prima / Dopo".

**Quando usarlo:**
- "Estrai la logica duplicata tra X e Y"
- "Questo modulo è troppo grande, spezzalo"
- Ripagare debito tecnico noto in modo incrementale

**Differenza da `refactor`:** `refactor` è chirurgico su una richiesta puntuale; `maintain` ragiona sulla salute del codice di un'area e propone il primo passo incrementale. Entrambi anti-overengineering.

---

## Come scrivere una buona issue per un agente

Usa sempre il template **"Task per agente Claude"** (`.github/ISSUE_TEMPLATE/agent_task.yml`). Compilato bene aumenta drasticamente la qualità dell'output.

### Contesto e obiettivo

Includi:
- **File e righe coinvolte** quando le conosci (es. `src/auth.js:42`)
- **Comportamento attuale** in una frase
- **Comportamento atteso** in una frase
- **Vincoli noti** (compatibilità, performance, stile)

### Criteri di accettazione

- Test che devono passare
- File che ti aspetti vengano modificati
- Cosa NON deve cambiare (per evitare scope creep)

### Priorità

Allineata al campo del Master Board:
- 🔴 **Urgente** — blocca produzione o team
- 🟡 **Medio** — default, da fare nello sprint corrente
- 🔵 **Bassa** — quando c'è tempo

---

## Comportamenti automatici

Quando trigghi un agente, il sistema fa automaticamente:

1. **Esecuzione su runner effimero** GitHub (Ubuntu, 7GB RAM, distrutto a fine job)
2. **Commento dell'agente** sulla issue/PR target
3. **PR creata** (per `fix`, `docs`, `test`, `refactor`, `cicd`, `maintain`) sul branch `<tipo>/<descrizione>`
4. **Aggiunta al Master Board** (Project #4)
5. **Status = "Test"** se è stata aperta una PR
6. **Reviewer assegnato round-robin** dal pool `AGENT_REVIEWERS` (default `montafra,K0enjy,Belletz-28`, evitando l'autore della issue)
7. **Notifica Telegram** se il workflow fallisce

I passi 4-6 sono `continue-on-error: true`: se uno dei secret di integrazione manca, il workflow non fallisce — solo logga un warning. Quindi gli agenti funzionano anche in setup parziale, ma perdi visibilità sul board.

Configurazione da tenere allineata nei template:
- Project target: `https://github.com/orgs/CBM-Solutions/projects/4`
- Status automatico: opzione `Test` del campo `Status` nel Project v2
- Reviewer pool: variabile repo `AGENT_REVIEWERS`, fallback `montafra,K0enjy,Belletz-28`

---

## Limiti, costi, performance

### Modello (selezione per agente)

Default dell'action: **`claude-sonnet-4-6`**. Override per agente via `--model` in `claude_args`:
```yaml
claude_args: |
  --model claude-opus-4-8
  --allowedTools "..."
```

Configurazione attuale dei template:

| Modello | Agenti | Razionale |
|---|---|---|
| `claude-haiku-4-5` | `summary` | Task breve read-only, ~10× più economico |
| `claude-sonnet-4-6` | `fix`, `docs`, `test`, `refactor`, `cicd`, `maintain`, `iac` | Best balance qualità/costo per coding |
| `claude-opus-4-8` | `security`, `review` | Migliore recall su bug e vulnerabilità |

> Il parametro `effort` (es. `xhigh` per coding) è a livello API e non è esposto come flag CLI in `claude_args`; lo steering equivalente si ottiene via prompt e scelta del modello. Per i task dove serve più ragionamento, il modello Opus + prompt "ragiona attentamente prima di agire" è la leva.

### Costi misurati sul sandbox (Sonnet 4.6)

| Agente | Run tipico | Costo |
|---|---|---|
| `summary` | 30s, 4 turn | ~$0.06 |
| `fix` (1-2 file) | 1-2min, 4-8 turn | ~$0.05-0.15 |
| `docs` | 1-3min | ~$0.05-0.10 |
| `test` (con esecuzione) | 2-5min | ~$0.10-0.30 |
| `refactor` | 1-3min | ~$0.08-0.20 |
| `review` (PR media, Opus) | 1-2min | ~$0.10-0.25 |
| `security` (PR media, Opus) | 1-3min | ~$0.10-0.30 |
| `iac` | 1-2min | ~$0.05-0.15 |
| `cicd` | 1-3min | ~$0.08-0.20 |
| `maintain` | 1-4min | ~$0.10-0.25 |

Imputati alla quota Claude Max del proprietario del `CLAUDE_CODE_OAUTH_TOKEN` caricato nel repo. **Non c'è fatturazione API a token aggiuntiva.**

### Limiti di rate

L'OAuth token attinge ai limiti del piano Max del suo proprietario. Per il volume attuale (poche esecuzioni al giorno) è irrilevante. Se in futuro si scalasse, opzioni:
- Distribuire token di membri diversi su repo diversi
- Passare a un'org subscription dedicata

---

## Sicurezza e governance

### Chi può triggerare un agente

Solo chi ha **write access** sul repo. È una guardia nativa di GitHub Actions sul trigger `labeled`. Un outside collaborator senza write non può attivare nulla.

### Cosa l'agente può fare

Tutto ciò che il `GITHUB_TOKEN` del runner permette (vedi `permissions:` in ciascun workflow):
- `fix/docs/test/refactor/cicd/maintain`: read+write su `contents`, `pull-requests`, `issues`
- `review/summary/security/iac`: read su `contents`, write su `pull-requests` e `issues` (per commentare)

L'agente NON ha:
- Accesso ai secret oltre quelli esplicitamente passati come env/with
- Possibilità di committare direttamente su `main` (la branch protection del repo si applica)
- Accesso a repo diversi da quello che lo ha triggerato

### Allowed tools

Ogni workflow passa una whitelist precisa di tool consentiti (Edit/Write/Read + alcuni `gh`/`git`/`npm`/...). Se Claude prova un tool fuori lista, viene bloccato. Vedi `claude_args: --allowedTools "..."` in ogni template.

### Revoca rapida

Se vedi comportamento anomalo da un agente:
1. Revoca il `CLAUDE_CODE_OAUTH_TOKEN` dal repo (Settings → Secrets → delete) — l'agente smette di funzionare immediatamente.
2. Disabilita il workflow specifico (Actions → workflow → "Disable workflow").
3. Investiga via `gh run view --log` prima di riattivare.

---

## Dove vivono le cose

```
.github (questo repo, organization-level)
├── ONBOARDING.md                        ← punto d'ingresso team
├── docs/
│   ├── AGENTI.md                        ← questo file
│   ├── SETUP-NUOVO-REPO.md              ← attivare gli agenti su un repo
│   └── COSTI.md                         ← report consumi
├── workflow-templates/                  ← starter per i repo della org
│   ├── agent-fix.yml + .properties.json
│   ├── agent-review.yml
│   ├── agent-docs.yml
│   ├── agent-test.yml
│   ├── agent-refactor.yml
│   ├── agent-summary.yml
│   ├── agent-security.yml
│   ├── agent-cicd.yml
│   ├── agent-iac.yml
│   ├── agent-maintain.yml
│   ├── labels-bootstrap.yml             ← crea le 10 label
│   ├── labels.yml                       ← definizione dichiarativa
│   └── notify-on-failure.yml            ← alert Telegram
├── .github/ISSUE_TEMPLATE/
│   └── agent_task.yml                   ← form ereditato da tutti i repo
└── profile/README.md                    ← pagina pubblica org
```
