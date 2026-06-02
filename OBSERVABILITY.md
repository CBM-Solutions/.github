# 📊 Fleet Dashboard — agenti Claude (ultimi 30 giorni)

_Aggiornato: 2026-06-02 10:17 UTC · org `CBM-Solutions`_

## Riepilogo

| Metrica | Valore |
|---|---|
| Run totali (escl. skipped) | 4 |
| ✅ Success | 2 |
| 🔴 Failure | 2 |
| Success rate | 50% |
| ⏭️ Skipped (label non-match) | 36 |
| 💸 Stima costo-equivalente | $0.50 _(proxy, non fatturato su Max)_ |

## Per agente

| Agente | Run | Success | Failure | Durata media (s) | Stima costo |
|---|---|---|---|---|---|
| Agent Fix | 1 | 1 | 0 | 64 | $0.10 |
| Agent IaC | 2 | 1 | 1 | 139 | $0.20 |
| Agent Test | 1 | 0 | 1 | 23 | $0.20 |

## Per repository

| Repo | Run | Success | Failure |
|---|---|---|---|
| agent-sandbox | 4 | 2 | 2 |

---
_Nota: il costo per-run (`total_cost_usd`) non è incluso in v1 perché
richiede il download dei log di ogni run. Da valutare come enhancement._
