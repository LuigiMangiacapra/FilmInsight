from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd
import os
import json

DBPEDIA_ENDPOINT = "http://dbpedia.org/sparql"
CACHE_PATH = "data/dbpedia/query_results.json"

def query_dbpedia(movie_title):
    """
    Esegue una query SPARQL per ottenere informazioni sul film da DBpedia.
    
    Args:
        movie_title (str): Titolo del film.
    
    Returns:
        dict: Risultati della query in formato JSON.
    """
    sparql = SPARQLWrapper(DBPEDIA_ENDPOINT)
    sparql.setQuery(f"""
    SELECT ?abstract ?director ?starring WHERE {{
        ?film a dbo:Film ;
              rdfs:label "{movie_title}"@en ;
              dbo:abstract ?abstract ;
              dbo:director ?director ;
              dbo:starring ?starring .
        FILTER (lang(?abstract) = 'en')
    }}
    LIMIT 1
    """)
    sparql.setReturnFormat(JSON)
    try:
        results = sparql.query().convert()
        if results["results"]["bindings"]:
            return results["results"]["bindings"][0]
        else:
            return None
    except Exception as e:
        print(f"Errore durante la query per '{movie_title}': {e}")
        return None

def load_cache():
    """Carica i risultati delle query salvati nel file di cache."""
    if os.path.exists(CACHE_PATH):
        with open(CACHE_PATH, "r") as f:
            return json.load(f)
    return {}

def save_cache(cache):
    """Salva i risultati delle query nel file di cache."""
    os.makedirs(os.path.dirname(CACHE_PATH), exist_ok=True)
    with open(CACHE_PATH, "w") as f:
        json.dump(cache, f, indent=4)

def enrich_movies(movies):
    """
    Arricchisce il dataset dei film con informazioni da DBpedia.
    
    Args:
        movies (DataFrame): DataFrame dei film.
    
    Returns:
        DataFrame: DataFrame arricchito.
    """
    # Carica la cache esistente
    cache = load_cache()
    enriched_data = []

    for _, row in movies.iterrows():
        title = row["title"]
        if title in cache:
            print(f"Cache trovata per '{title}'")
            enriched_data.append(cache[title])
            continue

        print(f"Eseguendo query per '{title}'...")
        data = query_dbpedia(title)
        if data:
            cache[title] = data
        else:
            cache[title] = {"abstract": None, "director": None, "starring": None}
        enriched_data.append(cache[title])

    # Salva la cache aggiornata
    save_cache(cache)

    # Aggiunge le informazioni arricchite al DataFrame
    movies["abstract"] = [d.get("abstract", {}).get("value", None) for d in enriched_data]
    movies["director"] = [d.get("director", {}).get("value", None) for d in enriched_data]
    movies["starring"] = [d.get("starring", {}).get("value", None) for d in enriched_data]

    return movies

if __name__ == "__main__":
    # Carica i film processati
    print("Caricamento dei dati processati...")
    movies = pd.read_csv("data/processed/movies_processed.csv")

    # Arricchisci i dati con DBpedia
    print("Arricchimento dei dati con DBpedia...")
    enriched_movies = enrich_movies(movies)

    # Salva i dati arricchiti
    enriched_movies.to_csv("data/processed/movies_enriched.csv", index=False)
    print("Dati arricchiti salvati in 'movies_enriched.csv'.")
