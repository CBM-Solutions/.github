# 📊 Fleet Dashboard — trend agenti Claude

_Generato: 2026-07-12 18:49 CEST (UTC 16:49) · org `CBM-Solutions` · finestra 180 giorni_

## Riepilogo finestra (180 giorni)

| Metrica | Valore |
|---|---|
| Run totali (escl. skipped) | 24 |
| ✅ Success | 20 |
| 🔴 Failure | 3 |
| Success rate | 83% |
| ⏭️ Skipped (label non-match) | 213 |
| 💸 Stima costo-equivalente (proxy) | $2.50 _(non fatturato su Max)_ |
| 💵 Costo REALE (campione 2 run) | $0.2468 tot · $0.1234/run |

## ✅ Qualità: esito PR agenti (override-rate)

Quanto l'umano accetta il lavoro degli agenti PR-creator (autore `app/claude`):

| Metrica | Valore |
|---|---|
| 🟢 PR merge (accettate) | 1 |
| 🔴 PR chiuse senza merge (override umano) | 5 |
| 🟡 PR ancora aperte | 8 |
| 📉 Override-rate | 83% _(rifiutate / decise)_ |

## 📅 Trend per giorno (ultimi 14)

| Giorno | Run | ✅ | 🔴 | Rate | Durata media (s) |
|---|---|---|---|---|---|
| 2026-05-30 | 8 | 6 | 2 | 75% | 109 |
| 2026-06-02 | 10 | 8 | 1 | 80% | 71 |
| 2026-06-04 | 3 | 3 | 0 | 100% | 77 |
| 2026-06-05 | 3 | 3 | 0 | 100% | 86 |

## 🗓️ Trend per settimana (ultime 12, ISO)

| Settimana | Run | ✅ | 🔴 | Rate | Durata media (s) |
|---|---|---|---|---|---|
| 2026-W22 | 8 | 6 | 2 | 75% | 109 |
| 2026-W23 | 16 | 14 | 1 | 87% | 75 |

## 📆 Trend per mese (ultimi 6)

| Mese | Run | ✅ | 🔴 | Rate | Durata media (s) |
|---|---|---|---|---|---|
| 2026-05 | 8 | 6 | 2 | 75% | 109 |
| 2026-06 | 16 | 14 | 1 | 87% | 75 |

## Per agente (finestra)

| Agente | Run | Success | Failure | Durata media (s) | Stima costo |
|---|---|---|---|---|---|
| Agent CICD | 1 | 1 | 0 | 77 | $0.14 |
| Agent Docs | 1 | 1 | 0 | 66 | $0.07 |
| Agent Feature | 1 | 1 | 0 | 114 | $0.10 |
| Agent Fix | 6 | 6 | 0 | 70 | $0.60 |
| Agent IaC | 3 | 2 | 1 | 115 | $0.30 |
| Agent Maintain | 1 | 1 | 0 | 168 | $0.17 |
| Agent Security | 3 | 2 | 1 | 183 | $0.60 |
| Agent Summary | 6 | 5 | 0 | 39 | $0.12 |
| Agent Test | 2 | 1 | 1 | 51 | $0.40 |

## Per repository (finestra)

| Repo | Run | Success | Failure |
|---|---|---|---|
| agent-sandbox | 24 | 20 | 3 |

---
_I trend usano `createdAt` delle run; la settimana è ISO-8601 (lun-dom)._
_Costo REALE: campione delle ultime 20 run riuscite (`total_cost_usd` dai log, soggetto a retention) per calibrare la stima proxy. Override-rate calcolato sulle PR `app/claude` decise (merge o chiuse) nella finestra._
