---
name: agent-summary
description: Produce un TL;DR mobile-friendly dell'oggetto etichettato, read-only.
disable-model-invocation: true
---

# agent:summary — TL;DR mobile-friendly

Il messaggio fornisce REPO, evento e riferimenti a issue/PR etichettata.

Produci un TL;DR mobile-friendly (3-5 bullet, max ~80 caratteri per bullet) dell'oggetto etichettato, pensato per essere letto al volo da telefono prima di decidere come procedere manualmente. Includi:
- di cosa si tratta in una frase
- punti chiave / decisioni richieste
- eventuali rischi o blocchi evidenti

Output: un singolo commento sull'oggetto etichettato. Nessuna PR, nessuna modifica al codice, nessuna analisi profonda.
