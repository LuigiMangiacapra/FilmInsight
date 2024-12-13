import unittest
from src.recommender import recommend_movies

class TestRecommender(unittest.TestCase):
    def test_recommend_movies(self):
        # Simula dati di esempio
        movies = ...
        ratings = ...
        result = recommend_movies(1, ratings, movies)
        self.assertGreater(len(result), 0)

if __name__ == "__main__":
    unittest.main()
