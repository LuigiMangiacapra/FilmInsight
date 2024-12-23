import pandas as pd
from dbpedia_queries import query_dbpedia_batch
from concurrent.futures import ThreadPoolExecutor
import re
import time
from mab import EpsilonGreedyMAB  # Importa la classe EpsilonGreedyMAB

PROCESSED_DATA_PATH = "data/processed/"

def load_raw_data():
    """Carica i dati raw e gestisce i generi."""
    print("Caricamento dei dati raw...")
    movies = pd.read_csv(PROCESSED_DATA_PATH + "movies_enriched.csv")  # Carica il file raw
    ratings = pd.read_csv(PROCESSED_DATA_PATH + "ratings_processed.csv")
    
    # Converte la colonna dei generi da stringa a lista
    movies["genres"] = movies["genres"].apply(lambda x: x.split('|') if isinstance(x, str) else [])
    
    print("Dati caricati con successo.")
    return movies, ratings

def clean_title(title):
    """Rimuove l'anno tra parentesi nel titolo, se presente."""
    return re.sub(r"\(\d{4}\)$", "", title).strip()

def query_dbpedia_with_fallback(title):
    """Prova prima con il titolo completo, poi con il titolo pulito senza anno."""
    print(f"Provo a cercare DBpedia per il titolo: {title}")
    
    # Prima prova con il titolo completo (con anno)
    dbpedia_info = query_dbpedia_batch(title)
    
    if not dbpedia_info:
        print(f"Nessun risultato per il titolo completo: {title}. Provo senza l'anno...")
        cleaned_title = clean_title(title)
        dbpedia_info = query_dbpedia_batch(cleaned_title)
        
        if not dbpedia_info:
            print(f"Nessun risultato trovato per il titolo pulito: {cleaned_title}")
    
    return dbpedia_info

def fetch_dbpedia_info_for_movie(movie_title, dbpedia_cache):
    """Esegui la query DBpedia per un film e gestisci la cache."""
    if movie_title not in dbpedia_cache:
        print(f"Titolo '{movie_title}' non trovato nella cache. Eseguo query DBpedia...")
        dbpedia_info = query_dbpedia_with_fallback(movie_title)
        dbpedia_cache[movie_title] = dbpedia_info
        print(f"Cache aggiornata con il titolo '{movie_title}'")
        time.sleep(1)  # Pausa di 1 secondo tra le richieste per evitare errori HTTP 429
    else:
        dbpedia_info = dbpedia_cache[movie_title]
        print(f"Titolo '{movie_title}' trovato nella cache.")
    return dbpedia_info

def recommend_movies(user_id, ratings, movies, top_k=5):
    """
    Raccomanda film basati sui generi e altre informazioni (regista, attori) valutati dall'utente.
    
    Args:
        user_id (int): ID dell'utente.
        ratings (DataFrame): DataFrame dei rating.
        movies (DataFrame): DataFrame dei film.
        top_k (int): Numero di raccomandazioni da restituire.
    
    Returns:
        DataFrame: Film raccomandati.
    """
    print(f"\nAvvio del processo di raccomandazione per l'utente {user_id}...")

    # Filtra i rating dell'utente e uniscili con i film per ottenere i titoli
    user_ratings = ratings[ratings["userId"] == user_id]
    user_ratings = user_ratings.merge(movies[['movieId', 'title', 'genres']], on='movieId', how='left')
    print(f"Numero di film valutati dall'utente {user_id}: {len(user_ratings)}")
    
    # Debug: verifica i generi valutati dall'utente
    print("Generi dei film valutati dall'utente:")
    print(user_ratings[['title', 'genres']].head())

    # Pondera i generi in base ai rating
    genre_weights = {}
    for _, row in user_ratings.iterrows():
        if isinstance(row["genres"], list):  # Assicurati che "genres" sia una lista
            for genre in row["genres"]:
                genre_weights[genre] = genre_weights.get(genre, 0) + row["rating"]
    
    print(f"Pesi dei generi calcolati: {genre_weights}")

    # Cache dei risultati DBpedia per evitare chiamate ripetute
    dbpedia_cache = {}

    # Assicurati che le colonne 'directors' e 'actors' siano inizializzate
    if "directors" not in movies.columns:
        movies["directors"] = [[] for _ in range(len(movies))]
        print("Colonna 'directors' non trovata. Aggiunta colonna vuota.")
    if "actors" not in movies.columns:
        movies["actors"] = [[] for _ in range(len(movies))]
        print("Colonna 'actors' non trovata. Aggiunta colonna vuota.")

    # Filtra i film già valutati
    rated_movie_ids = set(user_ratings["movieId"])
    recommendations = movies[~movies["movieId"].isin(rated_movie_ids)]
    print(f"Numero di film candidati per la raccomandazione: {len(recommendations)}")

    # Filtra i film in base ai generi preferiti
    if genre_weights:
        recommendations = recommendations[recommendations["genres"].apply(
            lambda x: any(genre in x for genre in genre_weights.keys())
            if isinstance(x, list) else False
        )]
        print(f"Numero di film dopo il filtro per i generi: {len(recommendations)}")
    else:
        print("I pesi dei generi sono vuoti. Impossibile procedere con il filtro per i generi.")
        return pd.DataFrame()  # Restituisci un DataFrame vuoto

    # Calcola un punteggio complessivo basato sui generi
    recommendations["score"] = recommendations["genres"].apply(
        lambda x: sum([genre_weights.get(genre, 0) for genre in x]) if isinstance(x, list) else 0
    )

    # Inizializza l'algoritmo Epsilon-Greedy MAB
    mab = EpsilonGreedyMAB(epsilon=0.1, decay=True)

    # Seleziona i film da raccomandare utilizzando l'algoritmo Epsilon-Greedy
    recommended_titles = []
    for _, movie in recommendations.iterrows():
        # Utilizza il punteggio del film come ricompensa per l'algoritmo
        reward = movie['score']
        mab.update(movie['title'], reward)
        recommended_titles.append(movie['title'])

    # Seleziona i top K film in base ai valori dell'algoritmo Epsilon-Greedy
    selected_movies = mab.get_action_values()
    top_movies = sorted(selected_movies.items(), key=lambda x: x[1], reverse=True)[:top_k]

    print(f"Top {top_k} film consigliati per l'utente {user_id}:")
    for movie, score in top_movies:
        print(f"Film: {movie}, Punteggio: {score:.2f}")
    
    return pd.DataFrame(top_movies, columns=["title", "score"])

if __name__ == "__main__":
    movies, ratings = load_raw_data()  # Usa i dati raw
    user_id = 1  # ID dell'utente per il quale fare la raccomandazione
    recommendations = recommend_movies(user_id, ratings, movies)
    
    if recommendations.empty:
        print("Nessuna raccomandazione trovata.")
    else:
        print("Raccomandazioni per l'utente:")
        print(recommendations[["title", "score"]])
