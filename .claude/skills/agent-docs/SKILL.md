---
name: agent-docs
description: Aggiorna la documentazione in base alla issue e apre una PR docs.
disable-model-invocation: true
---

# agent:docs — Manutenzione documentazione

Il messaggio fornisce REPO, numero/titolo della issue e il suo body.

Aggiorna la documentazione (README, /docs, commenti di alto livello) in base al contesto della issue:

1. Identifica i file di documentazione rilevanti.
2. Applica modifiche chiare, senza alterare la logica del codice.
3. Crea un branch dedicato `agent/docs-<numero issue>`.
4. Apri una PR "docs:" verso il branch di default con descrizione che include `Closes #<numero issue>`.
5. Commenta la issue con il link alla PR.

Non scrivere documentazione speculativa: solo ciò che la issue richiede.
