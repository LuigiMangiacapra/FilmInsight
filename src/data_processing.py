import pandas as pd
import os

# Percorsi dei dati
RAW_DATA_PATH = "data/raw/"
PROCESSED_DATA_PATH = "data/processed/"

def ensure_directory_exists(directory):
    """Crea la directory se non esiste."""
    if not os.path.exists(directory):
        os.makedirs(directory)

def load_raw_data():
    """Carica i file CSV raw."""
    movies = pd.read_csv(os.path.join(RAW_DATA_PATH, "movies.csv"))
    ratings = pd.read_csv(os.path.join(RAW_DATA_PATH, "ratings.csv"))
    links = pd.read_csv(os.path.join(RAW_DATA_PATH, "links.csv"))
    tags = pd.read_csv(os.path.join(RAW_DATA_PATH, "tags.csv"))
    return movies, ratings, links, tags

def process_movies_data(movies):
    """Elabora i dati dei film separando i generi."""
    movies['genres'] = movies['genres'].str.split('|')  # Separiamo i generi
    return movies

def save_processed_data(movies, ratings, links, tags):
    """Salva i dati processati nella cartella 'processed'."""
    ensure_directory_exists(PROCESSED_DATA_PATH)
    movies.to_csv(os.path.join(PROCESSED_DATA_PATH, "movies_processed.csv"), index=False)
    ratings.to_csv(os.path.join(PROCESSED_DATA_PATH, "ratings_processed.csv"), index=False)
    links.to_csv(os.path.join(PROCESSED_DATA_PATH, "links_processed.csv"), index=False)
    tags.to_csv(os.path.join(PROCESSED_DATA_PATH, "tags_processed.csv"), index=False)

def run_data_processing():
    """Funzione principale per caricare, processare e salvare i dati."""
    print("Caricamento dei dati raw...")
    movies, ratings, links, tags = load_raw_data()

    print("Processamento dei dati...")
    movies = process_movies_data(movies)

    print("Salvataggio dei dati processati...")
    save_processed_data(movies, ratings, links, tags)
    print("Dati processati e salvati con successo.")

if __name__ == "__main__":
    run_data_processing()
