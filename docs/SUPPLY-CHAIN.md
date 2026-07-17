# Supply Chain & Identity Controls

## Stato attuale

- Workflow e action critiche sono pinnate a SHA.
- **Pin enforcement**: `validate_ai_sdlc.py` fallisce se un `uses:` in
  `.github/workflows/**` o `workflow-templates/**` non è pinnato a SHA a 40 cifre
  (oltre allo scan `unpinned-uses` di `zizmor`).
- **Actions-BOM**: `.github/ai-sdlc/actions-bom.json` inventaria ogni action e
  reusable con SHA + versione; il validator verifica parità bidirezionale con i
  pin reali, quindi l'inventario non può andare in drift.
- **OpenSSF Scorecard**: `.github/workflows/scorecard.yml` produce scoring
  supply-chain settimanale + su push a `main`, pubblicato su code-scanning e
  sull'API OpenSSF (repo pubblico).
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
- AI-BOM e actions-BOM aggiornati e validati in CI;
- score OpenSSF Scorecard pubblicato (badge in README);
- required checks su governance/template/zizmor.

## Roadmap corta

1. Rendere required check: `AI SDLC Governance`, `Template Validation`,
   `Zizmor Workflow Scan`, `Scorecard Supply-Chain Security`.
2. Estendere `harden-runner` `block` (già attivo sui read-only agents) anche ai
   PR-creator dopo aver profilato il loro egress più ampio (AISEC-02).
3. Sostituire `MASTER_BOARD_TOKEN` con GitHub App token short-lived (AIID-01).
4. Validare WIF Claude su sandbox e rimuovere progressivamente token OAuth
   (AIID-01).
5. Valutare SLSA provenance / artifact attestation quando esisterà un artefatto
   buildato da attestare, es. un bundle di skill (AISUP-05).
