"""
FilmInsight: Knowledge-based Recommender System
Autore: [Il tuo nome]
"""

import logging
import os
from dotenv import load_dotenv  # Per gestire variabili d'ambiente

# Configurazione base del logging
logging.basicConfig(level=logging.INFO)  # Puoi cambiare a DEBUG, WARNING, ecc. secondo necessità
logger = logging.getLogger(__name__)

# Carica variabili d'ambiente da un file .env (se presente)
load_dotenv()

# Importa moduli di alto livello
try:
    from .data_processing import process_data, load_data
    from .dbpedia_queries import query_dbpedia
    from .recommender import recommend_movies
except ImportError as e:
    logger.error(f"Errore durante l'importazione dei moduli: {e}")
    raise

# Percorsi configurabili tramite variabili d'ambiente o valori di default
DATA_PATH = os.getenv("DATA_PATH", "data/")  # Puoi impostarlo in un file .env
RAW_DATA_PATH = os.getenv("RAW_DATA_PATH", os.path.join(DATA_PATH, "raw/"))
PROCESSED_DATA_PATH = os.getenv("PROCESSED_DATA_PATH", os.path.join(DATA_PATH, "processed/"))
CACHE_PATH = os.getenv("CACHE_PATH", os.path.join(DATA_PATH, "dbpedia/query_results.json"))

logger.info("Configurazione del sistema completata.")
