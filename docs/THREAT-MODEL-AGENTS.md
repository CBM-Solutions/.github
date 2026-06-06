# Threat Model — agenti Claude GitHub Actions

## Sistema

La flotta esegue agenti Claude su runner GitHub Actions effimeri. Il trigger è
una label `agent:*` applicata da utenti con write access. I caller sono sottili e
usano il reusable `.github/workflows/agent-runner.yml`; le metodologie vivono in
`.claude/skills/agent-*/SKILL.md`.

## Asset

- Codice dei repo target e branch aperti dagli agenti.
- Secret `CLAUDE_CODE_OAUTH_TOKEN` e `MASTER_BOARD_TOKEN`.
- Project v2, review request, label e notifiche.
- Agent Skills, `CLAUDE.md`, workflow template e reusable runner.
- Commenti issue/PR prodotti dagli agenti, perché influenzano decisioni umane.

## Trust Boundary

| Boundary | Non fidato | Controllo |
|---|---|---|
| Issue/PR body → prompt | testo utente, diff, commenti | write-access gate, skill guardrail, no interpolazione in `run:` |
| Prompt → tool | richieste generate dal modello | `--allowedTools` per agente + `--disallowedTools` centrale |
| Runner → rete | possibili canali di esfiltrazione | `harden-runner` audit/block-ready |
| Skills/template → agent behavior | supply-chain interna | CODEOWNERS + eval registry + governance CI |
| Token → integrazioni GitHub/Claude | credenziali statiche residue | secret espliciti, no `secrets: inherit`, migration path WIF/App token |

## Rischi e mitigazioni

| Rischio 2026 | Scenario | Mitigazione attuale | Gap residuo |
|---|---|---|---|
| Prompt injection / goal hijack | issue chiede di ignorare policy o stampare token | `CLAUDE.md`, skill guardrail, disallowed tools, eval injection | aggiungere live eval con token dedicato |
| Tool misuse / unexpected code execution | agente usa shell per azioni fuori scope | allowlist per agente, blocklist centrale, review umana | valutare sandbox più stretto per PR-creator |
| Identity/privilege abuse | PAT statico abusato o scope eccessivo | secret espliciti e step scoped | migrare a GitHub App token/WIF |
| Skill supply chain | modifica malevola a `SKILL.md` altera comportamento | CODEOWNERS, eval registry, validator | firma/provenance skill futura |
| Context poisoning | contenuto repo/issue contiene istruzioni malevole | grounding tratta input come non fidato | aggiungere fixture più realistiche da incidenti interni |
| Human trust exploitation | commento agente appare autorevole ma sbagliato | sezioni confidence/severity, review umana obbligatoria | dashboard su override-rate per agente |
| Cascading multi-agent failure | `feature` propone task e specialisti amplificano errore | auto-fan-out disabilitato, chaining opt-in | token short-lived + policy prima di fan-out automatico |
| Egress/exfiltration | output o rete usati per esfiltrare secret | harden-runner audit, disallowed curl/wget/env/cat | passaggio graduale a block allowlist |

## Policy operativa

- Gli agenti read-only non modificano codice: commentano soltanto.
- I PR-creator aprono PR, mai merge diretto.
- Azioni distruttive o infra condivisa richiedono decisione umana.
- Ogni nuovo agente deve avere label, issue option, template, properties, skill,
  AI-BOM entry e almeno due eval (`baseline`, `prompt_injection`).
