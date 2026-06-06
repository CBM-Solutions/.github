# AI SDLC Controls — CBM agent fleet

Questa repo è il control plane AI SDLC della flotta agenti Claude. I controlli
sono volutamente DRY: una matrice machine-readable, un validator CI e pochi
documenti di evidenza invece di checklist duplicate nei singoli agenti.

## Standard di riferimento

- NIST AI RMF 1.0 + NIST AI 600-1 GenAI Profile: govern, map, measure, manage.
- NIST SSDF SP 800-218: secure-by-design, review, provenance, secret handling.
- OWASP LLM Top 10 2025: prompt injection, insecure output/tool handling,
  sensitive information disclosure, supply chain.
- OWASP Agentic Top 10 / Agentic Skills Top 10 2026: goal hijack, tool misuse,
  identity abuse, skill supply chain, unexpected code execution, governance.
- SLSA 1.2 + OpenSSF Scorecard: source integrity, pinned dependencies,
  provenance-oriented evidence.

## Controlli implementati

La fonte di verità è `.github/ai-sdlc/control-matrix.json`.

| Area | Controllo | Evidenza primaria |
|---|---|---|
| Governance | Registro controlli AI SDLC con owner e standard mapping | `.github/ai-sdlc/control-matrix.json` |
| Threat model | Trust boundary, asset, failure mode e mitigazioni agentiche | `docs/THREAT-MODEL-AGENTS.md` |
| Eval | Casi baseline + prompt-injection + refusal per ogni skill | `.github/ai-sdlc/evals.json` |
| Inventory | AI-BOM della flotta agenti, skill, template e secret | `.github/ai-sdlc/ai-bom.json` |
| Provenance | Actions-BOM con SHA + pin enforcement in CI | `.github/ai-sdlc/actions-bom.json` |
| Scorecard | Scoring supply-chain OpenSSF su code-scanning + API | `.github/workflows/scorecard.yml` |
| Policy | CODEOWNERS su workflow, skills, template e governance docs | `.github/CODEOWNERS` |
| CI gate | Validator statico senza dipendenze esterne | `.github/workflows/ai-sdlc-governance.yml` |
| Supply chain | Pin SHA, zizmor, template validation, migration path token | `docs/SUPPLY-CHAIN.md` |

Lo stato di ogni controllo è `implemented`, `partial` (con `roadmap` per il gap
residuo) o `planned`. Il validator richiede evidenza per implemented/partial e
una roadmap per partial/planned, così la matrice non può sovrastimare lo stato.

## Regola di modifica

Ogni modifica a workflow, Agent Skills, `CLAUDE.md`, template o controlli deve:

1. aggiornare l'inventario se cambia la flotta;
2. aggiornare gli eval se cambia comportamento/prompt;
3. mantenere evidenza valida nella control matrix;
4. passare `AI SDLC Governance`, `Template Validation` e `Zizmor Workflow Scan`;
5. ricevere review umana via CODEOWNERS.

## Residual risk accettato

- `harden-runner` resta default `audit` per non rompere build/test eterogenei; il
  reusable è già `block`-ready via input centralizzati.
- Il token Claude OAuth e il token board sono ancora compatibili con l'attuale
  setup Free/org; la migrazione a WIF/GitHub App token è descritta in
  `docs/SUPPLY-CHAIN.md` e supportata dal reusable dove tecnicamente possibile.
