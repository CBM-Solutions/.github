---
name: agent-refactor
description: Refactoring mirato che preserva il comportamento, con PR e sezione Prima/Dopo.
disable-model-invocation: true
---

# agent:refactor — Refactoring mirato

Il messaggio fornisce REPO, numero/titolo della issue e il suo body.

Esegui un refactoring mirato preservando il comportamento osservabile:

1. Limita lo scope a quanto descritto nella issue.
2. Mantieni i test esistenti verdi; aggiungine solo se servono a fissare il comportamento prima della modifica.
3. Crea un branch dedicato `agent/refactor-<numero issue>`.
4. Nella descrizione della PR includi una sezione "Prima / Dopo" con i pattern principali toccati e `Closes #<numero issue>`.
5. Apri una PR "refactor:" e commenta la issue con il link.

Non introdurre nuove dipendenze o feature.

Per azioni difficili da invertire o distruttive (force-push, reset --hard, rm -rf) non procedere: segnala nella PR e lascia decidere all'umano. Non aggirare i check con `--no-verify`.
