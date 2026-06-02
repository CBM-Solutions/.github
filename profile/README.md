<p align="center">
  <img src="https://github.com/user-attachments/assets/22dba926-5ea5-4ffa-ba1d-32697d713c10" alt="CBM_Logo" width="300" />
</p>

# 🚀 CBM-Solutions
**Benvenuti nella nostra centrale operativa**

---

## ⚡ Core Projects

### 🧠 Caudex (Work in Progress)
*Progetto di punta della suite AI di CBM-Solutions.*
Un sistema avanzato di orchestrazione agentica progettato per l'automazione del ciclo di vita del software. 
- **Stato:** 🤐 [STEALTH MODE] - In fase di test interno.

### 🌐 Web & E-commerce Ecosystem
Progettazione e sviluppo di infrastrutture web scalabili. 
- **Stato:** Sviluppo attivo. I link ai progetti verranno pubblicati post-deploy.

---

## 🧪 R&D & Continuous Evolution

Siamo profondamente convinti che il software non sia mai un prodotto statico. Il nostro laboratorio è in costante fermento:

- **Tech Exploration:** Siamo costantemente alla ricerca di nuove tecnologie, framework e linguaggi. Non ci limitiamo a ciò che conosciamo, ma integriamo ciò che accelera l'innovazione.
- **Experimental Area:** Ottimizzazione flussi e concurrency con **Go**, sviluppo di utility verticali e applicazioni sperimentali in ambito Mobile & Web.
- **AI-First Approach:** Ogni nostro processo interno è in continua evoluzione per integrare le ultime frontiere dell'intelligenza artificiale agentica.

---
## 👥 Il Team
Un mix di competenze trasversali per coprire ogni aspetto dello sviluppo:

* **Process & DB Architect:** Enterprise workflows & SQL architecture.
* **Security Specialist:** System integrity & Cybersecurity.
* **Solution Architect & Marketing:** Product strategy & Market vision.

---

## 🛠 Tech Stack
`Python` • `Go` • `TypeScript` • `SQL` • `AI-Driven Development`

---

## 🤖 Agenti Claude (via etichette)

Ogni repo della org può adottare i workflow template di questa centrale per attivare agenti Claude Code applicando un'etichetta a issue/PR. Esecuzione su runner GitHub effimeri, autenticazione tramite abbonamento Claude Max.

| Etichetta | Cosa fa |
|---|---|
| `agent:fix` | Apre una PR che risolve la issue |
| `agent:review` | Code review strutturata su PR o issue |
| `agent:docs` | Aggiorna README e documentazione |
| `agent:test` | Genera o sistema i test |
| `agent:refactor` | Refactoring mirato preservando il comportamento |
| `agent:summary` | TL;DR mobile-friendly (read-only) |
| `agent:security` | Security review diff-aware (read-only) |
| `agent:cicd` | CI/CD, Dockerfile, script di deploy |
| `agent:iac` | Review Infra-as-Code: Terraform, K8s, cloud (read-only) |
| `agent:maintain` | Riduzione debito tecnico / manutenibilità |

### 🔌 Setup su un nuovo repo

Dal picker **Actions → New workflow** del repo target adottare:
1. `Bootstrap Agent Labels` → eseguire una volta via `workflow_dispatch` per creare le 10 etichette `agent:*`.
2. Tutti gli starter workflow `Agent *` che si vogliono attivare (uno per agente). Ognuno è un *thin caller* che richiama il reusable centralizzato `CBM-Solutions/.github/.github/workflows/agent-runner.yml`.
3. `Notify Agent Failure (Telegram)` per ricevere alert sui run falliti.
4. Copiare `CLAUDE.md` nella root del repo (grounding: convenzioni + regole di sicurezza lette da ogni agente).

Poi caricare i secret a livello **repo** (Settings → Secrets → Actions):

| Secret | Per cosa | Chi |
|---|---|---|
| `CLAUDE_CODE_OAUTH_TOKEN` | Autentica l'agente Claude sul tuo abbonamento Max | Generato con `claude setup-token` |
| `MASTER_BOARD_TOKEN` | Permette ai workflow di scrivere sul Master Board (Project v2 #4) | PAT fine-grained con `Projects: Read and write` sulla org |
| `TELEGRAM_BOT_TOKEN` | Invio messaggi via Bot API | Bot creato via `@BotFather` |
| `TELEGRAM_CHAT_ID` | Chat/gruppo destinazione delle notifiche | `getUpdates` dopo aver scritto al bot |

### 📱 Onboarding membro team

Per ricevere notifiche e operare sul flusso agenti:
- Installare l'**app GitHub mobile** → Settings → Notifications → **Actions** → "Failed workflows" ON
- Confermare di essere uno dei tre admin della org (`montafra`, `K0enjy`, `Belletz-28`) per entrare nel pool round-robin dei reviewer
- Aggiungere il proprio Telegram al gruppo configurato nel `TELEGRAM_CHAT_ID`
- Iscriversi alla notifica del **Master Board** (Project #4) per ricevere alert sui cambi di Status

---

### 📌 Contatti & Link
- 📧 [Contatto](CBM-Solutions@proton.me)
