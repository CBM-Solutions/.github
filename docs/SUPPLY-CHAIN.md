# Supply Chain & Identity Controls

## Stato attuale

- Workflow e action critiche sono pinnate a SHA.
- `zizmor` esegue scan statico dei workflow.
- `template-validation` esegue actionlint e parse YAML/JSON.
- `AI SDLC Governance` valida inventario, eval, CODEOWNERS e control matrix.
- `.github/ai-sdlc/ai-bom.json` è l'inventario AI-BOM/agent BOM della flotta.

## Identità e secret

| Secret | Uso | Stato | Migrazione |
|---|---|---|---|
| `CLAUDE_CODE_OAUTH_TOKEN` | auth `claude-code-action` | repo secret persistente | `anthropic_federation_rule_id` / WIF se disponibile per il piano |
| `MASTER_BOARD_TOKEN` | Project v2, chaining opzionale | PAT fine-grained | GitHub App token short-lived o PAT con scadenza breve |

Il reusable espone `anthropic_federation_rule_id`: i caller possono passarlo
quando l'org abilita federation senza cambiare ogni step Claude.

## Provenance

Per una repo `.github` di template non esiste build artifact classico. La
provenance utile è di tipo source/control:

- commit SHA dei caller verso il reusable;
- `skills_ref` pinnato quando una skill deve essere caricata da un ref specifico;
- CODEOWNERS per modifiche a control plane;
- AI-BOM aggiornato;
- required checks su governance/template/zizmor.

## Roadmap corta

1. Rendere required check: `AI SDLC Governance`, `Template Validation`,
   `Zizmor Workflow Scan`.
2. Abilitare OpenSSF Scorecard a livello org/repo quando disponibile con token
   e SARIF policy.
3. Passare `harden-runner` da `audit` a `block` su read-only agents dopo due
   settimane di endpoint osservati.
4. Sostituire `MASTER_BOARD_TOKEN` con GitHub App token short-lived.
5. Validare WIF Claude su sandbox e rimuovere progressivamente token OAuth.
