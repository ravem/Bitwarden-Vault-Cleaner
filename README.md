# Bitwarden Login Merge Tool

![Python](https://img.shields.io/badge/python-3.7+-blue.svg) ![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

Uno **script Python** per analizzare ed elaborare un export JSON di Bitwarden, concentrandosi sui **Login (`type=1`)**. Gestisce duplicati basati su username, password e URI, unisce gli URI condivisi e mantiene un log dettagliato.

---

## Tipi di item Bitwarden

| Tipo | Valore `type` | Descrizione |
|------|---------------|------------|
| Login | 1 | Credenziali di accesso (username, password, URI) |
| Secure Note | 2 | Note sicure testuali |
| Card | 3 | Dati di carte di pagamento |
| Identity | 4 | Informazioni personali (nome, indirizzo, ecc.) |

> Lo script **analizza solo i Login (`type=1`)**. Tutti gli altri tipi vengono ignorati.

---

## Funzionalità principali

- ✅ Analizza solo Login, ignorando gli altri tipi  
- ✅ Mantiene account senza URI  
- ✅ Identifica duplicati su **username + password + URI condivisi**  
- ✅ Merge automatico degli URI tra account duplicati  
- ✅ Salvataggio incrementale e log dettagliato  
- ✅ Possibilità di scegliere **file di input/output** all’avvio  

---

## Flusso di merge (diagramma semplificato)

```text
Input JSON -> [Item type=1?] -> NO -> Skipped
                               -> YES
                               -> [Username+Password già presenti?]
                                     -> NO -> Aggiungi ai duplicati
                                     -> YES -> Merge URI e rimuovi duplicato
