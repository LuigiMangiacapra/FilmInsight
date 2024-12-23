import pandas as pd
import os
import logging
from dotenv import load_dotenv

# Configurazione del logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Carica variabili d'ambiente
load_dotenv()

# Percorsi dei dati (configurabili tramite variabili d'ambiente)
DATA_PATH = os.getenv("DATA_PATH", "data/")
RAW_DATA_PATH = os.getenv("RAW_DATA_PATH", os.path.join(DATA_PATH, "raw/"))
PROCESSED_DATA_PATH = os.getenv("PROCESSED_DATA_PATH", os.path.join(DATA_PATH, "processed/"))

def ensure_directory_exists(directory):
    """
    Crea la directory se non esiste.
    
    Args:
        directory (str): Percorso della directory da creare.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
        logger.info(f"Creata la directory: {directory}")

def load_raw_data():
    """
    Carica i file CSV raw dai percorsi specificati.
    
    Returns:
        tuple: Quattro DataFrame (movies, ratings, links, tags).
    """
    try:
        logger.info("Caricamento dei dati raw dai file CSV...")
        movies = pd.read_csv(os.path.join(RAW_DATA_PATH, "movies.csv"))
        ratings = pd.read_csv(os.path.join(RAW_DATA_PATH, "ratings.csv"))
        links = pd.read_csv(os.path.join(RAW_DATA_PATH, "links.csv"))
        tags = pd.read_csv(os.path.join(RAW_DATA_PATH, "tags.csv"))
        logger.info("Dati raw caricati con successo.")
        return movies, ratings, links, tags
    except FileNotFoundError as e:
        logger.error(f"Errore durante il caricamento dei dati raw: {e}")
        raise
    except Exception as e:
        logger.error(f"Errore imprevisto durante il caricamento dei dati raw: {e}")
        raise

def process_movies_data(movies):
    """
    Elabora i dati dei film separando i generi.
    
    Args:
        movies (DataFrame): DataFrame contenente i dati dei film.
    
    Returns:
        DataFrame: DataFrame con i generi separati.
    """
    try:
        logger.info("Elaborazione dei dati dei film...")
        movies['genres'] = movies['genres'].str.split('|')  # Separiamo i generi
        logger.info("Elaborazione completata.")
        return movies
    except KeyError as e:
        logger.error(f"Colonna mancante nei dati dei film: {e}")
        raise
    except Exception as e:
        logger.error(f"Errore imprevisto durante l'elaborazione dei dati dei film: {e}")
        raise

def save_processed_data(movies, ratings, links, tags):
    """
    Salva i dati processati nella cartella 'processed'.
    
    Args:
        movies (DataFrame): DataFrame dei film processati.
        ratings (DataFrame): DataFrame dei ratings.
        links (DataFrame): DataFrame dei links.
        tags (DataFrame): DataFrame dei tags.
    """
    try:
        ensure_directory_exists(PROCESSED_DATA_PATH)
        logger.info("Salvataggio dei dati processati...")
        movies.to_csv(os.path.join(PROCESSED_DATA_PATH, "movies_processed.csv"), index=False)
        ratings.to_csv(os.path.join(PROCESSED_DATA_PATH, "ratings_processed.csv"), index=False)
        links.to_csv(os.path.join(PROCESSED_DATA_PATH, "links_processed.csv"), index=False)
        tags.to_csv(os.path.join(PROCESSED_DATA_PATH, "tags_processed.csv"), index=False)
        logger.info("Dati processati salvati con successo.")
    except Exception as e:
        logger.error(f"Errore durante il salvataggio dei dati processati: {e}")
        raise

def run_data_processing():
    """
    Funzione principale per caricare, processare e salvare i dati.
    """
    try:
        logger.info("Avvio del processo di elaborazione dei dati...")
        movies, ratings, links, tags = load_raw_data()

        movies = process_movies_data(movies)

        save_processed_data(movies, ratings, links, tags)
        logger.info("Processo di elaborazione completato con successo.")
    except Exception as e:
        logger.error(f"Errore durante il processo di elaborazione dei dati: {e}")
        raise

if __name__ == "__main__":
    run_data_processing()
