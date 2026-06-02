# Observability & controllo della flotta agenti

Come monitoriamo il sistema di agenti Claude. Tre livelli, tutti **serverless** e a **costo ~zero**.

## 1. GitHub-native (zero setup)

GitHub fornisce metriche org-level su Actions (GA marzo 2025, incluse nel piano Free):
- **Usage metrics**: minuti consumati per workflow/repo/runner.
- **Performance metrics**: durata media, queue time, **failure rate** per workflow e job.
- Fino a **1 anno** di storico.

Dove: **Organization → Insights → Actions** (serve ruolo owner/admin). È il primo posto dove guardare per capire quali agenti girano di più, dove falliscono, quanto durano. Limite: viste aggregate (medie/percentuali), non per-run.

## 2. Fleet Dashboard (workflow schedulato)

`/.github/workflows/fleet-dashboard.yml` (nel repo `.github`) gira ogni giorno e:
- interroga l'Actions API su tutti i repo della org;
- aggrega le run dei workflow `Agent *` e `Fleet` per agente e per repo (success/failure/skipped, durata media);
- scrive **[`OBSERVABILITY.md`](../OBSERVABILITY.md)** (committato in radice del repo `.github`);
- posta un riepilogo su Telegram con un bottone URL alla dashboard.

Attivazione: caricare su `.github` i secret `MASTER_BOARD_TOKEN` (PAT scope repo) e i `TELEGRAM_*`. Avvio manuale: **Actions → Fleet Dashboard → Run workflow**.

> v1 traccia conteggi/durate/success-rate dai metadati delle run (economico). Il costo per-run (`total_cost_usd` nei log) non è incluso perché richiederebbe il download dei log di ogni run — enhancement futuro.

## 3. Production observability (app) — ⏸️ IN PAUSA

Monitoraggio di BarWebsite/Caudex/GoNewspaper (error tracking, APM, uptime) e l'agente `agent:observability` che triagia gli alert e apre issue: **sospeso finché non scegliamo lo strumento**.

Candidati in valutazione (PoC su entrambi prima di decidere):
- **Sentry** free — ottimo error-tracking, ma piano free **single-user** (limite per team di 3).
- **Grafana Cloud** free — multi-utente, OTel-native (da validare nel dettaglio).

Trigger previsto per `agent:observability`: **webhook → `repository_dispatch`** (l'alert del backend lancia il workflow via API GitHub, nessun listener nostro).

## Observability degli agenti via OpenTelemetry (opzionale, futuro)

Claude Code esporta nativamente telemetria OpenTelemetry (metrics/log GA, traces beta) seguendo le GenAI semantic conventions — si abilita con `CLAUDE_CODE_ENABLE_TELEMETRY=1` + exporter OTLP (solo env var, nessun server). Permetterebbe per-step/per-token observability in un backend free. Da considerare quando il volume cresce; oggi le metriche GitHub-native + Fleet Dashboard bastano.

## Quando introdurre un servizio dedicato

- **GitHub Actions Data Stream** (roadmap GitHub, preview): telemetria near-real-time org-wide verso S3/Azure → sostituirà il polling dell'Actions API del Fleet Dashboard quando GA.
- **Telegram bidirezionale** (comandi/approvazioni da chat): richiede webhook/poller → serverless function (Cloudflare Workers/Vercel free) prima di un server vero.
