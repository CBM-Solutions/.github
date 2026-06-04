# 📊 Fleet Dashboard — trend agenti Claude

_Generato: 2026-06-04 21:35 UTC (~18:00 Europe/Rome) · org `CBM-Solutions` · finestra 180 giorni_

## Riepilogo finestra (180 giorni)

| Metrica | Valore |
|---|---|
| Run totali (escl. skipped) | 26 |
| ✅ Success | 14 |
| 🔴 Failure | 11 |
| Success rate | 53% |
| ⏭️ Skipped (label non-match) | 216 |
| 💸 Stima costo-equivalente (proxy) | $3.05 _(non fatturato su Max)_ |
| 💵 Costo REALE (campione 2 run) | $0.1296 tot · $0.0648/run |

## ✅ Qualità: esito PR agenti (override-rate)

Quanto l'umano accetta il lavoro degli agenti PR-creator (autore `app/claude`):

| Metrica | Valore |
|---|---|
| 🟢 PR merge (accettate) | 0 |
| 🔴 PR chiuse senza merge (override umano) | 2 |
| 🟡 PR ancora aperte | 6 |
| 📉 Override-rate | 100% _(rifiutate / decise)_ |

## 📅 Trend per giorno (ultimi 14)

| Giorno | Run | ✅ | 🔴 | Rate | Durata media (s) |
|---|---|---|---|---|---|
| 2026-05-30 | 16 | 6 | 10 | 37% | 60 |
| 2026-06-02 | 10 | 8 | 1 | 80% | 71 |

## 🗓️ Trend per settimana (ultime 12, ISO)

| Settimana | Run | ✅ | 🔴 | Rate | Durata media (s) |
|---|---|---|---|---|---|
| 2026-W22 | 16 | 6 | 10 | 37% | 60 |
| 2026-W23 | 10 | 8 | 1 | 80% | 71 |

## 📆 Trend per mese (ultimi 6)

| Mese | Run | ✅ | 🔴 | Rate | Durata media (s) |
|---|---|---|---|---|---|
| 2026-05 | 16 | 6 | 10 | 37% | 60 |
| 2026-06 | 10 | 8 | 1 | 80% | 71 |

## Per agente (finestra)

| Agente | Run | Success | Failure | Durata media (s) | Stima costo |
|---|---|---|---|---|---|
| Agent CICD | 3 | 1 | 2 | 29 | $0.42 |
| Agent Fix | 3 | 3 | 0 | 64 | $0.30 |
| Agent IaC | 5 | 2 | 3 | 71 | $0.50 |
| Agent Maintain | 3 | 1 | 2 | 60 | $0.51 |
| Agent Security | 5 | 2 | 3 | 122 | $1.00 |
| Agent Summary | 6 | 5 | 0 | 39 | $0.12 |
| Agent Test | 1 | 0 | 1 | 23 | $0.20 |

## Per repository (finestra)

| Repo | Run | Success | Failure |
|---|---|---|---|
| agent-sandbox | 26 | 14 | 11 |

---
_I trend usano `createdAt` delle run; la settimana è ISO-8601 (lun-dom)._
_Costo REALE: campione delle ultime 20 run riuscite (`total_cost_usd` dai log, soggetto a retention) per calibrare la stima proxy. Override-rate calcolato sulle PR `app/claude` decise (merge o chiuse) nella finestra._
