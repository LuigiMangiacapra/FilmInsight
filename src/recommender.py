import pandas as pd

PROCESSED_DATA_PATH = "data/processed/"

def load_processed_data():
    """Carica i file processati."""
    movies = pd.read_csv(PROCESSED_DATA_PATH + "movies_processed.csv")
    ratings = pd.read_csv(PROCESSED_DATA_PATH + "ratings_processed.csv")
    return movies, ratings

def recommend_movies(user_id, ratings, movies, top_k=5):
    """Raccomanda film basati sui generi valutati dall'utente."""
    # Filtra i rating dell'utente
    user_ratings = ratings[ratings["userId"] == user_id]
    # Trova i generi preferiti
    favorite_genres = []
    for movie_id in user_ratings["movieId"]:
        genres = movies[movies["movieId"] == movie_id]["genres"].values[0]
        favorite_genres.extend(genres)
    # Raccomanda film con generi simili
    recommendations = movies[movies["genres"].apply(lambda x: any(g in x for g in favorite_genres))]
    return recommendations.head(top_k)

if __name__ == "__main__":
    movies, ratings = load_processed_data()
    user_id = 1  # Esempio: utente 1
    recommendations = recommend_movies(user_id, ratings, movies)
    print("Raccomandazioni per l'utente:", recommendations)
