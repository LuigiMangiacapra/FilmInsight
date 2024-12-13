import os
import json

def ensure_directory_exists(directory):
    """Crea una directory se non esiste."""
    if not os.path.exists(directory):
        os.makedirs(directory)

def save_json(data, path):
    """Salva i dati in formato JSON."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def load_json(path):
    """Carica i dati da un file JSON."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def print_separator(title):
    """Stampa un separatore con un titolo."""
    print("\n" + "=" * 50)
    print(f"{title:^50}")
    print("=" * 50 + "\n")
