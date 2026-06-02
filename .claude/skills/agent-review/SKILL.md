---
name: agent-review
description: Code review strutturata (read-only) con report-everything, commento su PR/issue.
disable-model-invocation: true
---

# agent:review — Code review automatica

Il messaggio fornisce REPO, evento e riferimenti a issue/PR etichettata.

Esegui code review focalizzata su:
- bug di correttezza ed edge case
- rischi di sicurezza (injection, auth, secret, input non validato)
- regressioni di performance evidenti
- chiarezza e manutenibilità solo se rilevante

## Reporting
Segnala OGNI problema che trovi, anche incerto o a bassa severità: non auto-filtrare per importanza. Per ciascun finding indica confidence e severità stimata, così un umano può fare il triage a valle. Riporta solo bug reali (comportamento errato, test che fallirebbe, risultato fuorviante); ometti le pure preferenze di stile.

Output: un singolo commento strutturato sull'oggetto etichettato (PR o issue), con sezioni "Bloccanti", "Da valutare", "Note minori". Non aprire PR, non modificare codice.
