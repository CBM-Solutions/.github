# Costi e consumi — sistema agenti

## Cost model

**Zero fatturazione API a token.** L'autenticazione via `CLAUDE_CODE_OAUTH_TOKEN` (generato con `claude setup-token`) imputa ogni run alla quota dell'**abbonamento Claude Max** del proprietario del token. Concretamente: il limite condiviso è quello del piano (~quota mensile + limiti orari/giornalieri di rate), non un costo dollari incrementale.

Esecuzione invece avviene sui **runner GitHub Actions effimeri**:
- Repo pubblici: gratis illimitato
- Repo privati: quota minuti inclusa nel piano GitHub. Per task agente brevi (1-5 min) non la sfiori.

**Server, RAM, infra dedicata: 0€.** Tutto vive su risorse già pagate.

---

## Cost reference per agente (Sonnet 4.6, default)

Dati misurati sul repo `agent-sandbox` durante validazione iniziale.

| Agente | Durata tipica | Turn LLM | Costo equivalente* |
|---|---|---|---|
| `summary` (read-only) | 30-45s | 4 | ~$0.06 |
| `review` (PR media) | 60-90s | 5-8 | ~$0.05-0.10 |
| `fix` (1-2 file) | 60-120s | 4-8 | ~$0.05-0.15 |
| `docs` | 60-180s | 5-10 | ~$0.05-0.10 |
| `refactor` | 60-180s | 5-12 | ~$0.08-0.20 |
| `test` (con run suite) | 120-300s | 6-15 | ~$0.10-0.30 |

\* "Costo equivalente" = quanto sarebbe costato in pricing API a token. Sul tuo piano Max **non lo paghi**, è solo per ordini di grandezza e per stimare quando potresti sfiorare i rate limit.

---

## Quando vale la pena cambiare modello

Default action: **Claude Sonnet 4.6**.

Override in `claude_args` del workflow:
```yaml
claude_args: |
  --model claude-haiku-4-5     # 8-10× più economico, latenza minore
```

| Modello | Quando preferirlo |
|---|---|
| `claude-haiku-4-5` | `summary`, `review` su PR piccole, task ripetitivi a basso valore |
| `claude-sonnet-4-6` (default) | `fix`, `docs`, `test`, `refactor` — best balance |
| `claude-opus-4-7` | Cambi architetturali, debug complessi, una tantum |

**Raccomandazione attuale:** lasciare tutto su Sonnet 4.6 fino a quando i run non superano 50/mese. Sotto quella soglia il margine sui rate limit del Max è ampio.

---

## Cosa monitorare

Su **Anthropic Console** (https://console.anthropic.com): consumo del piano Max in % della quota. Se vedi avvicinarti al 70% pensa a:
- Spostare `summary`/`review` su Haiku
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
