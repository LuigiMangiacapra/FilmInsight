def precision_at_k(recommendations, relevant_items, k):
    """Calcola la Precision@K."""
    recommended_k = recommendations[:k]
    relevant_and_recommended = set(recommended_k).intersection(set(relevant_items))
    return len(relevant_and_recommended) / k
