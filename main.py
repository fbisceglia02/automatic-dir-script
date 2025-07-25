import os
import re

# Nome del file che contiene la struttura ad albero
tree_file = "tree.txt"

# Mappatura delle estensioni ai relativi stili di commento
COMMENT_STYLES = {
    ".tf": "#",
    ".tfvars": "#",
}

# Espressioni regolari per identificare le voci dell'albero:
# - Prefissi standard: '├──', '└──'
# - Nuovi prefissi: '+---' e '?   +---'
ENTRY_PATTERN = re.compile(
    r'^(?P<indent>\s*)'
    r'(?:(?:\+---|\?\s*\+---|├──|└──))'
    r'\s*(?P<name>.+)$'
)

def parse_tree(lines):
    """
    Analizza le righe di un file ad albero e restituisce:
      - root: nome della directory radice (senza slash), o None se non definito
      - entries: lista di tuple (level, name) per ogni voce trovata

    Il formato accettato per i nodi è:
      - root: '/nome_root/'
      - voci con indentazione a multipli di 4 spazi seguite da uno dei prefissi:
        '├──', '└──', '+---', '?   +---'
    """
    root = None
    entries = []
    for line in lines:
        text = line.rstrip()
        if not text:
            continue

        # Se la root non è ancora trovata e inizia e finisce con slash, la definiamo
        if root is None and text.startswith("/") and text.endswith("/"):
            root = text.strip().strip("/")
            continue

        # Match delle voci con il pattern esteso
        m = ENTRY_PATTERN.match(text)
        if not m:
            continue

        indent = len(m.group("indent"))
        # Ogni livello è dato da 4 spazi di indentazione
        level = indent // 4 + 1
        name = m.group("name")
        entries.append((level, name))

    return root, entries


def create_structure(tree_file_path):
    """
    Crea file e directory a partire dalla struttura ad albero descritta in tree_file_path.
    Se non viene trovata una directory root, le voci vengono generate nella directory corrente.
    """
    with open(tree_file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    root, entries = parse_tree(lines)
    # Se non esiste root, usiamo la dir corrente
    if not root:
        root = "."

    # Stack per tracciare il percorso corrente: parte da root
    stack = [root]

    for level, name in entries:
        # Riporta lo stack alla lunghezza corretta per il livello
        while len(stack) > level + 1:
            stack.pop()
        # Mantiene i primi 'level' elementi e aggiunge il nome corrente
        stack = stack[:level]
        stack.append(name.rstrip("/"))

        path = os.path.join(*stack)
        if name.endswith("/"):
            # Crea la directory
            os.makedirs(path, exist_ok=True)
        else:
            # Assicura che la cartella padre esista
            os.makedirs(os.path.dirname(path), exist_ok=True)
            # Scrive il file con commento iniziale
            _, ext = os.path.splitext(path)
            comment = COMMENT_STYLES.get(ext, "#")
            with open(path, "w", encoding="utf-8") as wf:
                wf.write(f"{comment} {os.path.basename(path)}\n")


if __name__ == "__main__":
    create_structure(tree_file)
