import pandas as pd

PROCESSED_DATA_PATH = "data/processed/"

def load_processed_data():
    """Carica i file processati."""
    movies = pd.read_csv(PROCESSED_DATA_PATH + "movies_processed.csv")
    ratings = pd.read_csv(PROCESSED_DATA_PATH + "ratings_processed.csv")
    return movies, ratings

def recommend_movies(user_id, ratings, movies, top_k=5):
    """
    Raccomanda film basati sui generi valutati dall'utente.
    
    Args:
        user_id (int): ID dell'utente.
        ratings (DataFrame): DataFrame dei rating.
        movies (DataFrame): DataFrame dei film.
        top_k (int): Numero di raccomandazioni da restituire.
    
    Returns:
        DataFrame: Film raccomandati.
    """
    # Filtra i rating dell'utente
    user_ratings = ratings[ratings["userId"] == user_id]

    # Pondera i generi in base ai rating
    genre_weights = {}
    for _, row in user_ratings.iterrows():
        movie_id = row["movieId"]
        rating = row["rating"]
        genres = movies[movies["movieId"] == movie_id]["genres"].values[0]
        for genre in genres:
            genre_weights[genre] = genre_weights.get(genre, 0) + rating

    # Ordina i generi per importanza
    sorted_genres = sorted(genre_weights.items(), key=lambda x: x[1], reverse=True)

    # Raccomanda film con generi simili, esclusi quelli già valutati
    rated_movie_ids = set(user_ratings["movieId"])
    recommendations = movies[~movies["movieId"].isin(rated_movie_ids)]
    recommendations = recommendations[recommendations["genres"].apply(
        lambda x: any(genre in x for genre, _ in sorted_genres)
    )]

    # Ordina le raccomandazioni e restituisci i primi K
    return recommendations.head(top_k)

if __name__ == "__main__":
    movies, ratings = load_processed_data()
    user_id = 1  # Esempio: utente 1
    recommendations = recommend_movies(user_id, ratings, movies)
    print("Raccomandazioni per l'utente:")
    print(recommendations[["title", "genres"]])
