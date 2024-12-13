import pandas as pd
import os

# Percorsi dei dati
RAW_DATA_PATH = "data/raw/"
PROCESSED_DATA_PATH = "data/processed/"

def load_data():
    """Carica i file CSV dal dataset MovieLens."""
    movies = pd.read_csv(os.path.join(RAW_DATA_PATH, "movies.csv"))
    ratings = pd.read_csv(os.path.join(RAW_DATA_PATH, "ratings.csv"))
    links = pd.read_csv(os.path.join(RAW_DATA_PATH, "links.csv"))
    tags = pd.read_csv(os.path.join(RAW_DATA_PATH, "tags.csv"))
    return movies, ratings, links, tags

def clean_movies(movies):
    """Pulisce e prepara il file movies.csv."""
    # Separazione dei generi in una lista
    movies["genres"] = movies["genres"].apply(lambda x: x.split("|") if isinstance(x, str) else [])
    return movies

def save_processed_data(movies, ratings, links, tags):
    """Salva i file processati."""
    os.makedirs(PROCESSED_DATA_PATH, exist_ok=True)
    movies.to_csv(os.path.join(PROCESSED_DATA_PATH, "movies_processed.csv"), index=False)
    ratings.to_csv(os.path.join(PROCESSED_DATA_PATH, "ratings_processed.csv"), index=False)
    links.to_csv(os.path.join(PROCESSED_DATA_PATH, "links_processed.csv"), index=False)
    tags.to_csv(os.path.join(PROCESSED_DATA_PATH, "tags_processed.csv"), index=False)

def process_data():
    """Pipeline principale per processare i dati."""
    movies, ratings, links, tags = load_data()
    movies = clean_movies(movies)
    save_processed_data(movies, ratings, links, tags)

if __name__ == "__main__":
    process_data()
