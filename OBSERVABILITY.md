# 📊 Fleet Dashboard — trend agenti Claude

_Generato: 2026-06-04 23:54 CEST (UTC 21:54) · org `CBM-Solutions` · finestra 180 giorni_

## Riepilogo finestra (180 giorni)

| Metrica | Valore |
|---|---|
| Run totali (escl. skipped) | 25 |
| ✅ Success | 17 |
| 🔴 Failure | 7 |
| Success rate | 68% |
| ⏭️ Skipped (label non-match) | 213 |
| 💸 Stima costo-equivalente (proxy) | $2.74 _(non fatturato su Max)_ |
| 💵 Costo REALE (campione 2 run) | $0.2383 tot · $0.1192/run |

## ✅ Qualità: esito PR agenti (override-rate)

Quanto l'umano accetta il lavoro degli agenti PR-creator (autore `app/claude`):

| Metrica | Valore |
|---|---|
| 🟢 PR merge (accettate) | 0 |
| 🔴 PR chiuse senza merge (override umano) | 5 |
| 🟡 PR ancora aperte | 6 |
| 📉 Override-rate | 100% _(rifiutate / decise)_ |

## 📅 Trend per giorno (ultimi 14)

| Giorno | Run | ✅ | 🔴 | Rate | Durata media (s) |
|---|---|---|---|---|---|
| 2026-05-30 | 12 | 6 | 6 | 50% | 77 |
| 2026-06-02 | 10 | 8 | 1 | 80% | 71 |
| 2026-06-04 | 3 | 3 | 0 | 100% | 77 |

## 🗓️ Trend per settimana (ultime 12, ISO)

| Settimana | Run | ✅ | 🔴 | Rate | Durata media (s) |
|---|---|---|---|---|---|
| 2026-W22 | 12 | 6 | 6 | 50% | 77 |
| 2026-W23 | 13 | 11 | 1 | 84% | 72 |

## 📆 Trend per mese (ultimi 6)

| Mese | Run | ✅ | 🔴 | Rate | Durata media (s) |
|---|---|---|---|---|---|
| 2026-05 | 12 | 6 | 6 | 50% | 77 |
| 2026-06 | 13 | 11 | 1 | 84% | 72 |

## Per agente (finestra)

| Agente | Run | Success | Failure | Durata media (s) | Stima costo |
|---|---|---|---|---|---|
| Agent CICD | 2 | 1 | 1 | 41 | $0.28 |
| Agent Fix | 6 | 6 | 0 | 70 | $0.60 |
| Agent IaC | 4 | 2 | 2 | 87 | $0.40 |
| Agent Maintain | 2 | 1 | 1 | 87 | $0.34 |
| Agent Security | 4 | 2 | 2 | 145 | $0.80 |
| Agent Summary | 6 | 5 | 0 | 39 | $0.12 |
| Agent Test | 1 | 0 | 1 | 23 | $0.20 |

## Per repository (finestra)

| Repo | Run | Success | Failure |
|---|---|---|---|
| agent-sandbox | 25 | 17 | 7 |

---
_I trend usano `createdAt` delle run; la settimana è ISO-8601 (lun-dom)._
_Costo REALE: campione delle ultime 20 run riuscite (`total_cost_usd` dai log, soggetto a retention) per calibrare la stima proxy. Override-rate calcolato sulle PR `app/claude` decise (merge o chiuse) nella finestra._
