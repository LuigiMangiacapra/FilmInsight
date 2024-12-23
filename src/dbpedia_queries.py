import os
import time
import json
import requests
import logging
import pandas as pd
from dotenv import load_dotenv
from SPARQLWrapper import SPARQLWrapper, JSON
from concurrent.futures import ThreadPoolExecutor
import random  # Per il ritardo casuale in caso di errore 429

# Configurazione del logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Carica variabili d'ambiente
load_dotenv()

# Configurazione variabili
DBPEDIA_ENDPOINT = os.getenv("DBPEDIA_ENDPOINT", "http://dbpedia.org/sparql")
CACHE_PATH = os.getenv("CACHE_PATH", "data/dbpedia/query_results.json")
BATCH_SIZE = 10  # Limite di titoli per batch ridotto per evitare URI troppo lunghi
MAX_THREADS = 5  # Numero massimo di thread per le query parallele

def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        logger.info(f"Creata la directory: {directory}")

def escape_title(title):
    title = title.replace('"', '\\"')  # Escape delle virgolette
    title = title.replace("'", "\\'")  # Escape degli apostrofi
    title = title.replace("\n", "")    # Rimuovere eventuali nuove righe
    return title

def chunk_list(lst, chunk_size):
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]

def query_dbpedia_batch(movie_titles):
    sparql = SPARQLWrapper(DBPEDIA_ENDPOINT)
    
    if len(movie_titles) == 0:
        logger.warning("Nessun titolo nel batch. Saltando la query.")
        return []
    
    titles_filter = " ".join([f'FILTER (rdfs:label = "{escape_title(title)}"@en)' for title in movie_titles])
    
    query = f"""
    SELECT ?title ?abstract ?director ?starring ?genre WHERE {{
        ?film a dbo:Film ;
              rdfs:label ?title ;
              dbo:abstract ?abstract ;
              dbo:director ?director ;
              dbo:starring ?starring ;
              dbo:genre ?genre .
        FILTER (lang(?abstract) = 'en') 
        {titles_filter}
    }}
    """
    
    sparql.setMethod('POST')
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    
    retries = 0
    while retries < 5:  # Prova fino a 5 volte
        try:
            logger.info(f"Eseguendo query batch per {len(movie_titles)} film...")
            results = sparql.query().convert()
            return results.get("results", {}).get("bindings", [])
        except requests.exceptions.RequestException as e:
            if e.response and e.response.status_code == 429:  # Too Many Requests
                retry_time = random.randint(2, 5)  # Attendi un tempo casuale tra 2 e 5 secondi
                logger.warning(f"Troppi tentativi, ritento tra {retry_time} secondi...")
                time.sleep(retry_time)
                retries += 1
            else:
                logger.error(f"Errore durante la query batch: {e}")
                return []
        except Exception as e:
            logger.error(f"Errore generale durante la query batch: {e}")
            return []

    logger.error("Troppi tentativi, la query non è riuscita dopo 5 tentativi.")
    return []

def load_cache():
    if os.path.exists(CACHE_PATH):
        try:
            with open(CACHE_PATH, "r") as f:
                content = f.read().strip()
                if not content:
                    logger.warning(f"Il file di cache '{CACHE_PATH}' è vuoto.")
                    return {}
                cache = json.loads(content)
                logger.info(f"Cache caricata: {len(cache)} voci")
                return cache
        except json.JSONDecodeError as e:
            logger.error(f"Errore nel caricamento della cache: {e}. Il file potrebbe essere danneggiato.")
            return {}
        except Exception as e:
            logger.error(f"Errore sconosciuto nel caricamento della cache: {e}")
            return {}
    logger.info("Cache non trovata. Creazione di una nuova.")
    return {}

def save_cache(cache):
    ensure_directory_exists(os.path.dirname(CACHE_PATH))
    try:
        with open(CACHE_PATH, "w") as f:
            json.dump(cache, f, indent=4)
        logger.info("Cache salvata con successo.")
    except IOError as e:
        logger.error(f"Errore nel salvataggio della cache: {e}")

def enrich_movies(movies):
    cache = load_cache()
    enriched_data = []

    movie_titles = movies["title"].tolist()
    
    all_results = []
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        futures = [executor.submit(query_dbpedia_batch, batch) for batch in chunk_list(movie_titles, BATCH_SIZE)]
        for future in futures:
            all_results.extend(future.result())

    results_map = {result['title']['value']: {
                    "abstract": result.get("abstract", {}).get("value"),
                    "director": result.get("director", {}).get("value"),
                    "starring": result.get("starring", {}).get("value"),
                    "genre": result.get("genre", {}).get("value"),
                    } for result in all_results}

    for title in movie_titles:
        if title in cache:
            logger.info(f"Cache trovata per '{title}'.")
            enriched_data.append(cache[title])
        elif title in results_map:
            enriched_data.append(results_map[title])
            cache[title] = results_map[title]
        else:
            enriched_data.append({"abstract": None, "director": None, "starring": None, "genre": None})
    
    save_cache(cache)

    movies["abstract"] = [d["abstract"] for d in enriched_data]
    movies["director"] = [d["director"] for d in enriched_data]
    movies["starring"] = [d["starring"] for d in enriched_data]
    movies["genre"] = [d["genre"] for d in enriched_data]

    return movies

if __name__ == "__main__":
    try:
        logger.info("Caricamento dei dati da 'movies.csv'...")
        movies_csv_path = os.getenv("MOVIES_CSV_PATH", "data/raw/movies.csv")
        movies = pd.read_csv(movies_csv_path)

        links_csv_path = os.getenv("MOVIES_CSV_PATH", "data/raw/links.csv")
        links = pd.read_csv(links_csv_path)
        movies = pd.merge(movies, links, on='movieId', how='left')

        movies["genre"] = movies["genres"].apply(lambda x: x.split('|') if isinstance(x, str) else [])
        movies["formatted_title"] = movies["title"].apply(escape_title)

        logger.info("Arricchimento dei dati con DBpedia...")
        enriched_movies = enrich_movies(movies)

        output_path = "data/processed/movies_enriched.csv"
        enriched_movies.to_csv(output_path, index=False)
        logger.info(f"Dati arricchiti salvati in '{output_path}'.")
    except Exception as e:
        logger.error(f"Errore nel processo di arricchimento: {e}")
