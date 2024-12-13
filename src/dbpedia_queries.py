from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd
import os

DBPEDIA_ENDPOINT = "http://dbpedia.org/sparql"
CACHE_PATH = "data/dbpedia/query_results.json"

def query_dbpedia(movie_title):
    """Esegue una query SPARQL per ottenere informazioni sul film."""
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
    results = sparql.query().convert()
    return results

def enrich_movies(movies):
    """Arricchisce i dati dei film con informazioni da DBpedia."""
    enriched_data = []
    for _, row in movies.iterrows():
        title = row["title"]
        try:
            data = query_dbpedia(title)
            enriched_data.append(data)
        except Exception as e:
            print(f"Errore con il film {title}: {e}")
    return enriched_data

if __name__ == "__main__":
    # Carica i film processati
    movies = pd.read_csv("data/processed/movies_processed.csv")
    # Arricchisci i dati
    enriched_data = enrich_movies(movies)
    # Salva i risultati
    os.makedirs(os.path.dirname(CACHE_PATH), exist_ok=True)
    with open(CACHE_PATH, "w") as f:
        f.write(str(enriched_data))
