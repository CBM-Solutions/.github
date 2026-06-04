# Onboarding — Sistema agenti Claude CBM-Solutions

Benvenuto. Questo documento ti porta da zero a operativo in **circa 15 minuti**. È una checklist d'azione — la spiegazione completa di come funziona il sistema sta in [`docs/AGENTI.md`](docs/AGENTI.md), leggila dopo aver completato il setup.

> **Cos'è in due righe:** ogni repo della org può attivare 10 agenti Claude (`fix`, `review`, `docs`, `test`, `refactor`, `summary`, `security`, `cicd`, `iac`, `maintain`) applicando un'etichetta `agent:*` a una issue o PR. L'esecuzione gira su runner GitHub, autenticata sull'abbonamento Claude Max, e si integra con il **Master Board** (Project v2 #4) e con notifiche Telegram.

> **Architettura (Fase 7):** ogni agente è un *thin caller* che richiama un unico reusable workflow centralizzato (`CBM-Solutions/.github/.github/workflows/agent-runner.yml`) — logica comune, pin SHA e sicurezza in un solo punto. Ogni agente legge `CLAUDE.md` dalla root del repo per grounding (convenzioni + regole di sicurezza).

---

## ✅ Checklist personale (10 minuti)

### 1. App GitHub mobile

Senza questa non riceverai push per workflow falliti o review request — diventerai un collo di bottiglia per il team.

- Installa l'**app GitHub** (iOS/Android), accedi col tuo account.
- Apri `Settings → Notifications → Actions` → abilita **"Failed workflows"**.
- In `Settings → Notifications → Review requests` → abilita push.

Test: chiedi a un altro membro di taggarti su una qualsiasi issue. Devi ricevere la notifica entro pochi secondi.

### 2. Telegram — gruppo notifiche

Il sistema invia su Telegram quando un workflow agente fallisce, così non si perde nulla anche se non hai il PC aperto.

- Apri Telegram, scrivi a **@matte** (admin del bot) chiedendo l'invito al gruppo `CBM Agents Alerts`.
- Conferma l'iscrizione, scrivi un messaggio di test nel gruppo.

> Il gruppo riceve solo `failure` — niente spam su run riusciti.

### 3. Verifica accessi GitHub

- Devi essere **owner** o **admin** dell'organizzazione `CBM-Solutions`. Verifica su https://github.com/orgs/CBM-Solutions/people — il tuo ruolo deve essere `Owner`.
- Devi avere accesso al **Master Board**: https://github.com/orgs/CBM-Solutions/projects/4. Se non lo vedi, chiedi a chi ti ha invitato di darti il permesso.
- Sei automaticamente nel pool reviewer round-robin (`montafra`, `K0enjy`, `Belletz-28`). Le PR aperte dagli agenti ti verranno assegnate a turno.

### 4. Token personale Claude (solo se vuoi triggerare agenti dai tuoi repo)

Se gestisci tuoi repo nella org e vuoi che gli agenti girino su quelli, ti serve un OAuth token Claude Max generato dal tuo abbonamento.

```bash
# Una volta sola, in locale:
claude update            # assicurati di avere v1.0.44+
claude setup-token       # produce sk-ant-oat01-...
```

Quel token va caricato come **repo secret** `CLAUDE_CODE_OAUTH_TOKEN` su ciascun repo che vuoi attivare. Non condividerlo: è legato al tuo abbonamento personale.

> **Limite GitHub Free:** non possiamo usare org secrets, quindi ogni repo ha il suo token. È accettabile per il volume attuale.

---

## 🚀 Prima esecuzione

Per verificare che tutto funzioni dalla tua postazione:

1. Vai sul repo di test [`CBM-Solutions/agent-sandbox`](https://github.com/CBM-Solutions/agent-sandbox).
2. **Issues → New issue → "Task per agente Claude"** — compila il form scegliendo agente `summary` e priorità `Medio`.
3. Crea la issue. **Applicale a mano l'etichetta `agent:summary`**.
4. Aspetta ~1 minuto: dovresti vedere il commento di `claude[bot]` con un TL;DR.
5. Apri https://github.com/orgs/CBM-Solutions/projects/4 — la tua issue è apparsa sul Master Board.

Se uno dei passi sopra non funziona, vai alla sezione [Troubleshooting](#-troubleshooting-rapido).

---

## 🛠 Spedire una funzionalità con un agente — flusso end-to-end

Tutto **da remoto** (app GitHub mobile o browser, niente CLI). Esempio: aggiungere una nuova funzionalità.

1. **Apri una issue dettagliata.** Sul repo target → **Issues → New issue → "Task per agente Claude"**. Compila:
   - **Contesto e obiettivo**: cosa va aggiunto, in quale area/file, vincoli noti.
   - **Criteri di accettazione**: come si riconosce che è completo (comportamento osservabile, file toccati, eventuali test).
   - Più sei specifico, migliore è il diff. **Una issue = un obiettivo.**
2. **Applica la label dell'agente.** Per implementare → `agent:fix` (l'agente generico issue→PR; nonostante il nome, è il risolutore che crea la PR a partire dalla issue). La label è il **trigger** e richiede write access (è anche il gate di sicurezza).
   > Il form **non** applica la label da solo: la metti tu dopo aver creato la issue.
3. **L'agente parte da solo** (workflow). Indaga il codice, implementa il minimo necessario, apre una **PR** con `Closes #N` e corpo *cosa / perché / come testare*.
4. **Automatico**: la PR viene **aggiunta al Master Board**, messa in **Status = Test**, e ti assegna un **reviewer** round-robin (mai l'autore della issue).
5. **Notifiche**: push GitHub mobile sulla review request; Telegram **solo se il run fallisce**.
6. **Revisione umana** (consigliata per le feature): apri la PR; opzionalmente applica `agent:review` (e/o `agent:security`) **alla PR** per un'analisi strutturata prima di decidere.
7. **Merge**: approvi e mergi (branch protection: ≥1 approval, niente auto-merge). Sposti l'item su **Done** sulla board.

**Note pratiche**
- Per una **feature grande**, spezzala in più issue/PR: gli agenti rendono meglio sul diff piccolo (è anche una regola del `CLAUDE.md`).
- L'agente **propone**, l'umano è il **merge-gate**. Verifica sempre la PR.
- Se i test del repo falliscono, l'agente è istruito a **non** presentare la PR come pronta ma a segnalarlo nel corpo.
- Oggi non c'è un `agent:feature` dedicato: `agent:fix` è il generalista issue→PR e copre bene le nuove funzionalità con una issue ben scritta.

---

## 📋 Reference rapida agenti

| Quando vuoi… | Usa | Trigger |
|---|---|---|
| Una PR che fixa un bug descritto in issue | `agent:fix` | label su issue |
| Una code review automatica della PR aperta | `agent:review` | label su PR |
| Aggiornare README/docs in base a una issue | `agent:docs` | label su issue |
| Aggiungere unit/integration test | `agent:test` | label su issue |
| Refactoring mirato senza cambi di comportamento | `agent:refactor` | label su issue |
| Solo capire al volo cosa dice un'issue/PR (mobile-friendly) | `agent:summary` | label su issue o PR |
| Security review diff-aware di una PR | `agent:security` | label su PR |
| Scrivere/sistemare CI/CD, Dockerfile, deploy | `agent:cicd` | label su issue |
| Review di Terraform/K8s/config cloud | `agent:iac` | label su PR |
| Ridurre debito tecnico / manutenibilità | `agent:maintain` | label su issue |

**Regola d'oro**: applica una sola label `agent:*` alla volta. Se vuoi più passaggi (fix → review), prima esegui uno, poi rietichetta per il secondo. Le etichette parallele creano PR concorrenti che vanno in conflitto.

Dettaglio completo prompt/permessi per ciascun agente in [`docs/AGENTI.md`](docs/AGENTI.md).

---

## 🗂 Master Board — cosa significano gli stati

| Stato | Quando | Cosa devi fare |
|---|---|---|
| **Todo** | Issue creata, nessun agente attivato | Decidere se va in scope, applicare etichetta agente |
| **In Progress** | Issue presa in carico da un agente (manuale) | Aspettare il completamento |
| **Test** | L'agente ha aperto PR — pronta per review umana | **Ti tocca se sei il reviewer assegnato** |
| **Merge** | Review fatta, pronta per merge | Mergiare quando CI verde |
| **Done** | Merged | Niente |

Lo stato `Test` viene impostato automaticamente quando un agente apre una PR. Gli altri li sposti tu a mano, sul board.

---

## 👥 Cosa fare quando ricevi una review request

Se ti arriva su mobile/desktop "X requested your review on PR #N":

1. **Leggi il commento `agent:review`** (se c'è già) — l'agente ha già fatto il primo passaggio identificando bloccanti.
2. **Conferma le correzioni indicate** o aggiungi commenti tuoi.
3. **Approva o richiedi modifiche.**
4. Sul Master Board sposta lo stato da `Test` → `Merge` (o riportalo a `In Progress` se servono modifiche grosse).

Se non riesci a gestirla entro 24h, riassegna manualmente a un altro reviewer (`gh pr edit <N> --add-reviewer <user>`) o lascia un commento `@<user> puoi farti carico?`. Niente PR orfane.

---

## 🆘 Troubleshooting rapido

| Sintomo | Causa probabile | Fix |
|---|---|---|
| Applico la label e non parte niente | Non hai write permission sul repo | Verifica ruolo nella org |
| Il workflow gira ma non viene postato alcun commento | Manca `CLAUDE_CODE_OAUTH_TOKEN` o è scaduto | Rigenera con `claude setup-token`, ricarica come repo secret |
| La PR si apre ma non finisce sul Master Board | Manca `MASTER_BOARD_TOKEN` o non ha scope `Projects: write` | Rigenera il PAT con il permesso giusto |
| Non ricevo notifica Telegram sui failure | Manca `TELEGRAM_BOT_TOKEN` / `TELEGRAM_CHAT_ID` sul repo | Carica entrambi come repo secret |
| Reviewer non assegnato | Il tuo username non è nel pool | Imposta la variabile repo/org `AGENT_REVIEWERS` (es. `montafra,K0enjy,Belletz-28`) in Settings → Secrets and variables → Actions → Variables |
| Workflow `failure` su step Claude | Quasi sempre quota Claude esaurita o token revocato | Controlla console.anthropic.com / rigenera token |

Per problemi non in tabella, log completo:
```bash
gh run list --repo CBM-Solutions/<repo> --limit 5
gh run view <id> --repo CBM-Solutions/<repo> --log
```

---

## 📚 Approfondimenti

- [`docs/AGENTI.md`](docs/AGENTI.md) — guida completa per ciascun agente, esempi di prompt efficaci, casi d'uso
- [`docs/SETUP-NUOVO-REPO.md`](docs/SETUP-NUOVO-REPO.md) — checklist per attivare gli agenti su un repo nuovo
- [`docs/COSTI.md`](docs/COSTI.md) — andamento consumi e raccomandazioni di scelta modello per agente
- [`profile/README.md`](profile/README.md) — pagina pubblica della org

Domande? Apri una issue con etichetta `question` sul repo `.github` oppure scrivi nel gruppo Telegram.
