---
name: agent-test
description: Genera o sistema i test per l'area indicata e apre una PR test.
disable-model-invocation: true
---

# agent:test — Generazione test

Il messaggio fornisce REPO, numero/titolo della issue e il suo body.

Genera o sistema i test per l'area indicata nella issue:

1. Identifica il framework di test del repo (package.json, pyproject, ecc.).
2. Aggiungi/aggiorna i test mantenendo lo stile esistente.
3. Esegui la suite di test e includi l'esito nel corpo della PR. Se i test falliscono, NON presentare la PR come pronta: segnala il problema.
4. Crea un branch dedicato `agent/test-<numero issue>`.
5. Apri una PR "test:" con descrizione che include `Closes #<numero issue>` e commenta la issue.

Non modificare il codice di produzione se non strettamente necessario per rendere i test eseguibili.
