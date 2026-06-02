---
name: agent-fix
description: Risolve una issue applicando modifiche minime e aprendo una PR con Closes #N.
disable-model-invocation: true
---

# agent:fix — Risolutore di bug

Il messaggio fornisce REPO, numero/titolo della issue e il suo body. Risolvi la issue in autonomia:

1. Crea un branch dedicato `agent/fix-<numero issue>`.
2. Applica le modifiche minime necessarie a risolvere il problema.
3. Apri una Pull Request verso il branch di default con descrizione chiara che include `Closes #<numero issue>`.
4. Commenta la issue con il link alla PR.

Mantieni lo scope ristretto: niente refactor non richiesti.

Per azioni difficili da invertire o distruttive (force-push, reset --hard, rm -rf, modifiche a infra condivisa) non procedere: segnala nella PR e lascia decidere all'umano. Non aggirare i check con `--no-verify`.
