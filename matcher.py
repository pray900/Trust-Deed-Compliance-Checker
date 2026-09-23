# matcher.py
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
 
THRESHOLD_COVERED   = 0.82   # tweak based on testing
THRESHOLD_PARTIAL   = 0.65
 
def check_regulation(reg_text, clauses, clause_embeddings, embedder_fn):
    reg_embedding = embedder_fn(reg_text).reshape(1, -1)
 
    scores = cosine_similarity(reg_embedding,
                               np.array(clause_embeddings))[0]
 
    best_idx   = int(np.argmax(scores))
    best_score = float(scores[best_idx])
 
    if best_score >= THRESHOLD_COVERED:
        status = "Covered"
    elif best_score >= THRESHOLD_PARTIAL:
        status = "Partially Covered"
    else:
        status = "Missing"
 
    return {
        "regulation": reg_text,
        "status": status,
        "score": round(best_score, 4),
        "best_matching_clause": clauses[best_idx]
    }