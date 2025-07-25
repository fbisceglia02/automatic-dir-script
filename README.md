# Strumento di Creazione Struttura da File ad Albero

Questo tool legge un file di testo che descrive una struttura ad albero e genera ricorsivamente directory e file corrispondenti. Ogni file viene creato con un commento nella prima riga contenente il nome del file.

## Caratteristiche principali

* **Parsing flessibile**: riconosce i prefissi standard `├──`/`└──`, i simboli `+---` e `?   +---`.
* **Root opzionale**: se non viene specificata una root (es. `/rootname/`), crea direttamente nella directory corrente.
* **Commenti automatici**: ogni file creato include un commento (es. `# nomefile.tf`) come prima riga.
* **Supporto estensioni**: mappatura estensioni a commenti (attualmente `.tf` e `.tfvars`).

## Requisiti

* Python 3.x
* Sistema operativo con supporto per i caratteri UTF-8 e la creazione di directory.

## Installazione

1. Clona il repository:

   ```bash
   git clone https://tuo-repo.git
   cd tuo-repo
   ```
2. Assicurati di avere Python 3 installato:

   ```bash
   python --version
   ```

## Utilizzo

1. Prepara un file `tree.txt` con la struttura ad albero, ad esempio:

   ```text
   /mio-progetto/
   ├── main.tf
   ├── modules/
   │   └── storage/
   │       ├── main.tf
   │       └── variables.tf
   └── README.md
   ```
2. Esegui lo script per generare la struttura:

   ```bash
   python main.py
   ```
3. La struttura verrà creata in base al `tree.txt`. Se non è presente una root, i file saranno creati nella cartella corrente.

## Formato del file di input (`tree.txt`)

* **Root** (opzionale): `/nome_root/` su una linea propria.
* **Indentazione**: multipli di 4 spazi per i livelli.
* **Prefissi nodo**: `├──`, `└──`, `+---`, `?   +---` seguiti da uno spazio e dal nome.
* **Directory**: nome che termina con `/`.
* **File**: nome senza `/` finale.

### Esempio avanzato

```
/project-example/
├── infra/
│   ├── main.tf
│   ├── variables.tf
│   └── modules/
│       └── network/
│           └── main.tf
└── docs/
    +---README.md
    ?   +---overview.md
```

## Personalizzazione

* Modificare `COMMENT_STYLES` per aggiungere nuovi stili di commento per altre estensioni.
* Estendere `ENTRY_PATTERN` se si desiderano nuovi prefissi o formati.

## Contributi

Pull request e issue sono benvenute!

## Licenza

Questo progetto è rilasciato sotto licenza MIT. Visita il file `LICENSE` per maggiori dettagli.
