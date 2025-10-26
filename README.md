# Bitwarden Vault cleanup Tool / Strumento di cleanup di un vault Bitwarden

![Python](https://img.shields.io/badge/python-3.7+-blue.svg) ![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

Uno **script Python** per analizzare ed elaborare un export JSON di Bitwarden, concentrandosi sui **Login (`type=1`)**. Gestisce duplicati basati su username, password e URI, unisce gli URI condivisi e mantiene un log dettagliato.  

A **Python script** to analyze and process a Bitwarden JSON export, focusing on **Login items (`type=1`)**. It handles duplicates based on username, password, and URI, merges shared URIs, and keeps a detailed log.

---

## Tipi di item Bitwarden / Bitwarden Item Types

| Tipo / Type | Valore `type` / Type Value | Descrizione / Description |
|------------|---------------------------|---------------------------|
| Login | 1 | Credenziali di accesso (username, password, URI) / Access credentials |
| Secure Note | 2 | Note sicure testuali / Secure text notes |
| Card | 3 | Dati di carte di pagamento / Payment card details |
| Identity | 4 | Informazioni personali / Personal information |

> Lo script **analizza solo i Login (`type=1`)**. Tutti gli altri tipi vengono ignorati.  
> The script **processes only Login items (`type=1`)**. All other types are ignored.

---

## Funzionalità principali / Features

- ✅ Analizza solo Login, ignorando gli altri tipi / Only analyzes Login items  
- ✅ Mantiene account senza URI / Keeps accounts even without URIs  
- ✅ Identifica duplicati su **username + password + URI condivisi** / Detects duplicates on username + password + shared URIs  
- ✅ Merge automatico degli URI tra account duplicati / Automatically merges URIs of duplicate accounts  
- ✅ Salvataggio incrementale e log dettagliato / Incremental save and detailed logging  
- ✅ Possibilità di scegliere **file di input/output** all’avvio / Allows choosing input/output files at runtime  

---

## Flusso di pulizia / Cleanup Flow (diagramma semplificato / simplified diagram)

```text
Input JSON -> [Item type=1?] -> NO -> Skipped
                               -> YES
                               -> [Username+Password already exists?]
                                     -> NO -> Add to vault
                                     -> YES -> Merge URIs and remove duplicate
```
---
## Requisiti / Requirements

Python 3.7+, moduli / modules: json, re, datetime, os, urllib.parse

---
## Utilizzo / Usage

1. Clona il repository / Clone the repository:
```
git clone <URL_REPO>
cd <REPO_NAME>
```

2. Esporta il vault in formato .json / Export the vault in .json format

3. Esegui lo script / Run the script:
```
python bitwarden_merge.py
```
---
