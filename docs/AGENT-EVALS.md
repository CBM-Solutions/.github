# Agent Evals

Gli eval attuali sono offline e statici: definiscono il comportamento atteso per
ogni Agent Skill e bloccano drift di copertura in CI. Non chiamano Claude e non
consumano quota.

## Fonte di verità

- Registry: `.github/ai-sdlc/evals.json`
- Validator: `.github/scripts/validate_ai_sdlc.py`
- Gate: `.github/workflows/ai-sdlc-governance.yml`

## Copertura minima

Ogni agente deve avere almeno:

- `baseline`: scenario operativo normale;
- `prompt_injection`: scenario con istruzione malevola o tentativo di bypass;
- `must`: proprietà che l'agente deve produrre;
- `must_not`: comportamenti vietati.

Il validator fallisce se un agente ha skill/template/label ma non ha eval.

## Evoluzione consigliata

Fase successiva, senza cambiare il registry:

1. aggiungere runner opzionale con token dedicato e repo sandbox;
2. eseguire gli agenti su issue/PR fixture controllate;
3. salvare output e scoring in artifact;
4. misurare regressioni per skill change;
5. promuovere gli eval critici a required check.

## Regola per modifiche skill

Se una PR cambia `.claude/skills/**`, deve aggiornare gli eval quando cambia:

- output atteso;
- tool/permessi usati;
- strategia di rifiuto;
- comportamento PR/commento;
- modello o chaining.
