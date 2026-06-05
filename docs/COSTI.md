# Costi e consumi — sistema agenti

## Cost model

**Zero fatturazione API a token.** L'autenticazione via `CLAUDE_CODE_OAUTH_TOKEN` (generato con `claude setup-token`) imputa ogni run alla quota dell'**abbonamento Claude Max** del proprietario del token. Concretamente: il limite condiviso è quello del piano (~quota mensile + limiti orari/giornalieri di rate), non un costo dollari incrementale.

Esecuzione invece avviene sui **runner GitHub Actions effimeri**:
- Repo pubblici: gratis illimitato
- Repo privati: quota minuti inclusa nel piano GitHub. Per task agente brevi (1-5 min) non la sfiori.

**Server, RAM, infra dedicata: 0€.** Tutto vive su risorse già pagate.

---

## Controllo costi real-time (FinOps serverless)

### GitHub Budgets — guardrail sui minuti Actions
GitHub Budgets dà controllo di spesa **real-time senza alcun server**:
- alert automatici a **75% / 90% / 100%** del budget;
- alert sulle quote incluse a 90% / 100%;
- **hard-stop "prevent usage"** sui prodotti metered (Actions): una volta raggiunta la soglia, i workflow non partono più.

Setup (una volta, a livello org): **Settings → Billing → Budgets and alerts → New budget** → prodotto **Actions** → soglia + abilita "prevent usage" per i repo privati. È il guardrail contro l'esaurimento minuti già sperimentato sul sandbox.

> Repo **pubblici** = minuti standard-runner **gratis e illimitati** (esclusi anche dal platform charge $0.002/min di gen-2026). Dove possibile, tenere gli agenti su repo pubblici azzera il problema minuti.

### Fleet Dashboard — report costi/run
Il workflow `fleet-dashboard.yml` (vedi `OBSERVABILITY.md`) aggrega run, success-rate e durate degli agenti e posta un riepilogo su Telegram. È il "report FinOps" del sistema. Dalla **Fase 8C** riporta due metriche aggiuntive:
- **Costo REALE campionato**: estrae `total_cost_usd` dai log delle ultime `COST_SAMPLE` (default 20) run riuscite e ne calcola totale e media/run. Serve a **calibrare la stima proxy** con numeri reali (soggetto alla retention dei log GitHub: campiona le run più recenti).
- **Override-rate**: % di PR `app/claude` **decise** (merge vs chiuse-senza-merge) che l'umano ha **rifiutato**. È il segnale di **qualità** reale degli agenti PR-creator (equivalente al *break-glass rate* dei team del settore): se sale, conviene rivedere prompt/skill dell'agente.

### ⚠️ Gap: visibilità quota Claude Max
**Non esiste (verificato, 2026) un meccanismo pubblico di telemetria real-time sul consumo della quota/rate-limit dell'abbonamento Max via token OAuth.** A differenza dell'API-key (fatturata a token, tracciabile), il consumo Max non è ispezionabile programmaticamente. Conseguenza: il monitoraggio dei costi-agente combina il **costo reale campionato** (`total_cost_usd` dai log, vedi sopra) con la **stima proxy** (numero run × costo modellato per agente) — non c'è telemetria diretta della quota Max.

Se in futuro servisse precisione sui costi (alto volume), l'opzione è un agente dedicato su **API-key** (a token, tracciabile) per quei task specifici, accettando il costo marginale.

---

## Cost reference per agente (Sonnet 4.6, default)

Dati misurati sul repo `agent-sandbox` durante validazione iniziale.

| Agente | Durata tipica | Turn LLM | Costo equivalente* |
|---|---|---|---|
| `summary` (read-only) | 30-45s | 4 | ~$0.06 |
| `review` (PR media) | 60-90s | 5-8 | ~$0.05-0.10 |
| `fix` (1-2 file) | 60-120s | 4-8 | ~$0.05-0.15 |
| `feature` (Opus, piano + core) | 120-300s | molti | ~$0.20-0.50 |
| `docs` | 60-180s | 5-10 | ~$0.05-0.10 |
| `refactor` | 60-180s | 5-12 | ~$0.08-0.20 |
| `test` (con run suite) | 120-300s | 6-15 | ~$0.10-0.30 |

\* "Costo equivalente" = quanto sarebbe costato in pricing API a token. Sul tuo piano Max **non lo paghi**, è solo per ordini di grandezza e per stimare quando potresti sfiorare i rate limit.

---

## Quando vale la pena cambiare modello

Default action: **Claude Sonnet 4.6**.

Dalla Fase 7 il modello si imposta con l'input `model:` del caller (il reusable `agent-runner.yml` lo passa a `--model` solo se valorizzato):
```yaml
# in workflow-templates/agent-<nome>.yml
with:
  model: claude-haiku-4-5     # 8-10× più economico, latenza minore
```

| Modello | Quando preferirlo |
|---|---|
| `claude-haiku-4-5` | `summary`, `review` su PR piccole, task ripetitivi a basso valore |
| `claude-sonnet-4-6` (default) | `fix`, `docs`, `test`, `refactor` — best balance |
| `claude-opus-4-8` | `review`, `security`, cambi architetturali, debug complessi, una tantum |

**Raccomandazione attuale:** lasciare i PR-creator su Sonnet 4.6, `summary` su Haiku e `review`/`security` su Opus fino a quando i run non superano 50/mese. Sotto quella soglia il margine sui rate limit del Max è ampio.

---

## Cosa monitorare

Su **Anthropic Console** (https://console.anthropic.com): consumo del piano Max in % della quota. Se vedi avvicinarti al 70% pensa a:
- Spostare altri task read-only a basso rischio su Haiku
- Distribuire token su membri diversi (uno per cluster di repo)

Su **GitHub Actions usage** (https://github.com/organizations/CBM-Solutions/settings/billing): minuti consumati sui runner. Soglia di attenzione: 80% del piano.

---

## Stima volume sostenibile

Con un solo abbonamento Max condiviso, il sistema regge comodamente:
- **~30-50 esecuzioni agente al giorno** distribuite su 3-4 ore
- **~1000 esecuzioni/mese**

Sopra queste soglie iniziano a comparire rate limit. Mitigation:
1. Modello più piccolo per gli agenti read-only
2. Più token in rotazione (uno per dev del team, allocato ai propri repo)
3. Account org Anthropic dedicato se diventa business-critical
