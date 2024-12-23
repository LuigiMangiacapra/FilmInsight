def precision_at_k(recommendations, relevant_items, k):
    """Calcola la Precision@K."""
    if k == 0:
        return 0
    recommended_k = recommendations[:k]
    relevant_and_recommended = set(recommended_k).intersection(set(relevant_items))
    return len(relevant_and_recommended) / k

def recall_at_k(recommendations, relevant_items, k):
    """Calcola la Recall@K."""
    if not relevant_items:  # Se non ci sono articoli rilevanti
        return 0
    recommended_k = recommendations[:k]
    relevant_and_recommended = set(recommended_k).intersection(set(relevant_items))
    return len(relevant_and_recommended) / len(relevant_items)

def mean_average_precision(recommendations, relevant_items, k):
    """
    Calcola la Mean Average Precision (MAP) @K.
    """
    if not relevant_items:  # Se non ci sono articoli rilevanti
        return 0
    
    avg_precision = 0
    for i in range(1, k + 1):
        avg_precision += precision_at_k(recommendations, relevant_items, i)
    
    return avg_precision / k
