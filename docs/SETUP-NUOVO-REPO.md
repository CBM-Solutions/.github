# Setup agenti su un nuovo repo — checklist

Tempo richiesto: **~10 minuti** se hai già i token a portata di mano.

## Prerequisiti

- Repo creato sotto org `CBM-Solutions`
- App GitHub **Claude** già installata sull'org (verifica su https://github.com/organizations/CBM-Solutions/settings/installations — se non c'è installala da https://github.com/apps/claude)
- **Reusable workflow centralizzato**: dalla Fase 7 ogni agente è un *thin caller* che richiama `CBM-Solutions/.github/.github/workflows/agent-runner.yml@<sha>`. Funziona out-of-the-box se il repo è **pubblico** (come `.github`). Se il tuo repo è **privato**, abilita l'accesso ai reusable workflow del repo `.github`: Org/repo → **Settings → Actions → General → Access** → consenti i workflow del repo `.github`.
- Hai i seguenti token pronti:
  - `sk-ant-oat01-...` (genera con `claude setup-token`)
  - PAT GitHub fine-grained con scope **Projects: Read and write** sull'org
  - Bot Telegram token + chat_id del gruppo notifiche

---

## Step 1 — Adottare gli starter workflow

1. Apri il tuo repo → tab **Actions**.
2. Click **"New workflow"** → in alto trovi la categoria **"Workflows created by CBM-Solutions"**.
3. Adotta in quest'ordine, uno alla volta (ogni adozione crea un commit):
   1. **Bootstrap Agent Labels** — crea le 11 label `agent:*`
   2. **Agent Summary** (read-only, il più sicuro per primo test)
   3. **Agent Fix**
   4. **Agent Feature** (planner multi-agent, Opus)
   5. **Agent Review**
   6. **Agent Docs**
   7. **Agent Test**
   8. **Agent Refactor**
   9. **Agent Security**
   10. **Agent CICD**
   11. **Agent IaC**
   12. **Agent Maintain**
   13. **Notify Agent Failure (Telegram)**

Suggerimento: se sai già che non userai mai certi agenti su questo repo, saltali — sempre adottabili in seguito.

---

## Step 2 — Caricare i secret

Vai su **Settings → Secrets and variables → Actions → New repository secret** e crea questi 4 secret:

| Nome | Valore |
|---|---|
| `CLAUDE_CODE_OAUTH_TOKEN` | Il tuo `sk-ant-oat01-...` |
| `MASTER_BOARD_TOKEN` | PAT con permission `Projects: Read and write` |
| `TELEGRAM_BOT_TOKEN` | Token del bot (`123456:ABC...`) |
| `TELEGRAM_CHAT_ID` | ID numerico del gruppo (es. `-100123456789`) |

> Se ne carichi solo alcuni: gli step relativi falliscono con warning ma il workflow agente nel complesso resta funzionante (tutti gli step di integrazione hanno `continue-on-error: true`).

### Variabili (opzionali)

In **Settings → Secrets and variables → Actions → Variables** puoi impostare:

| Variabile | A cosa serve | Default se assente |
|---|---|---|
| `AGENT_REVIEWERS` | reviewer round-robin (comma-separated) | `montafra,K0enjy,Belletz-28` |
| `MASTER_BOARD_PROJECT_URL` | URL del Project v2 | progetto #4 |
| `MASTER_BOARD_PROJECT_ID` | ID GraphQL del progetto | ID del board #4 |
| `MASTER_BOARD_STATUS_FIELD_ID` | ID campo Status | campo Status del #4 |
| `MASTER_BOARD_STATUS_TEST_ID` | ID opzione "Test" | opzione Test del #4 |

> Gli ID del Master Board hanno un fallback hard-coded sul board attuale (#4): le variabili servono solo se in futuro si cambia/duplica il board, e si impostano **una volta a livello org** (non per-repo).

### File `CLAUDE.md` (consigliato)

Copia `CLAUDE.md` nella **root del repo** (sorgente in `workflow-templates/CLAUDE.md` del repo `.github`). Viene letto da ogni agente a inizio sessione e fornisce convenzioni + regole di sicurezza. Personalizza la sezione "Convenzioni di progetto" con i comandi di test/build del repo.

### Agent Skills — nessuna azione richiesta

I prompt degli agenti vivono come **Agent Skills centrali** in `CBM-Solutions/.github/.claude/skills/`. Il reusable `agent-runner.yml` le carica a runtime (`use_skills: true`) e le esclude dal commit: **non** devi copiarle nel tuo repo. Per modificarle vedi `docs/AGENTI.md → Modificare il prompt di un agente`.

### Egress monitoring (Fase 8A) — automatico

Il reusable esegue `step-security/harden-runner` come primo step di ogni run (modalità `audit`): **nessuna azione di setup richiesta**. Su repo **pubblici** il link Insights con i domini contattati è gratuito; su repo **privati** il monitoraggio funziona comunque, ma la dashboard Insights di StepSecurity può richiedere un tier dedicato. In `audit` non blocca nulla: serve a costruire l'allowlist prima di un eventuale passaggio a `block`.

### Chaining fix→review (Fase 8D) — opt-in

Per far partire la code review automaticamente dopo che `agent:fix`/`agent:docs`/ecc. apre una PR, imposta `chain_review: true` nel `with:` del caller (default off). Applica la label `agent:review` alla PR appena creata. Abilitalo solo dove la review automatica vale il costo extra di run. **Richiede `MASTER_BOARD_TOKEN`** (PAT scope repo): il `GITHUB_TOKEN` di default non propaga eventi e non farebbe partire la review.

---

## Step 3 — Eseguire il bootstrap label

1. **Actions → Bootstrap Agent Labels → Run workflow → Run**.
2. Attendi che termini (10-20 secondi).
3. Verifica su **Issues → Labels** che ci siano 10 nuove label colorate `agent:fix`, `agent:review`, ecc.

---

## Step 4 — Smoke test

1. Apri una issue di prova (puoi usare il template **"Task per agente Claude"**).
2. Applicale l'etichetta `agent:summary` (la più sicura — read-only).
3. Aspetta ~60 secondi. Verifica:
   - L'app GitHub **Actions** mostra un run "Agent Summary" in successo
   - La issue ha un nuovo commento da `claude[bot]` con TL;DR
   - La issue è apparsa nel [Master Board](https://github.com/orgs/CBM-Solutions/projects/4)

Se non funziona, vai a [`AGENTI.md#troubleshooting`](AGENTI.md) o controlla i log con `gh run view --log`.

---

## Step 5 — Notifica Telegram (test opzionale)

Per verificare l'alert:

1. **Rimuovi temporaneamente** il secret `CLAUDE_CODE_OAUTH_TOKEN`.
2. Riapplica l'etichetta `agent:summary` a una issue.
3. Il workflow fallisce. Nel gruppo Telegram dovresti vedere:
   > 🔴 *Agent Summary* failed
   > *Repo:* `CBM-Solutions/<repo>`

4. **Ripristina il secret** subito dopo.

---

## Branch protection consigliata

Per i repo dove gli agenti aprono PR, configura su `main`:

- **Settings → Branches → Add rule** per `main`
- ✅ Require a pull request before merging
- ✅ Require approvals: 1 (il reviewer auto-assegnato)
- ✅ Require status checks to pass — **consigliato**: se il repo ha CI/test, rendili obbligatori. È il gate che, insieme al prompt test-aware di `agent:test`, impedisce il merge di PR con test rossi (test-gating Fase 7C).
- ❌ NON serve "Restrict who can push" — l'agente apre PR, non pusha su `main`

Senza branch protection l'agente potrebbe in teoria mergiare da solo se gli concedi i permessi; con la protezione, anche se prova, viene bloccato.

---

## Note operative emerse dai test

- **`agent:cicd` e i file in `.github/workflows/`**: per far sì che l'agente pushi direttamente i workflow serve concedere alla GitHub App di Claude il permesso **Workflows: Read and write** (Organization → Settings → GitHub Apps → claude → Permissions). Senza, l'agente ripiega postando il contenuto del file come commento. Dockerfile/script fuori da `.github/workflows/` funzionano senza permessi extra.
- **Repo privati e minuti Actions**: sul piano Free i minuti sono condivisi a livello org. Se i run iniziano a fallire all'avvio con zero step, è la quota esaurita: rendere il repo pubblico (minuti illimitati) o attendere il reset di fatturazione.
- **Modelli**: `agent:security` e `agent:review` girano su `claude-opus-4-8`; verifica nei log la riga "Claude Code initialized" → `model`.

---

## Disattivazione

Per spegnere temporaneamente un singolo agente:
- **Actions → Agent X → "..." menu → Disable workflow**

Per spegnere tutto:
- **Actions → Disable Actions** (a livello repo) oppure
- Revoca il `CLAUDE_CODE_OAUTH_TOKEN` (effetto immediato senza toccare i file)
